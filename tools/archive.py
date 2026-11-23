"""Seekable ZIP STORE reader, strict AFB manifest and bounded per-entry reads.
No extraction of arbitrary paths. Writer spools prepared blocks to disk.
"""
import os,stat,tempfile,zipfile,struct,hashlib
from pathlib import Path
from codec import *
import semantics as sem
MAX_ZIP=1024*MIB; MAX_RAW_SUM=8192*MIB; MAX_CD=2*MIB; MAX_ENTRIES=4002
EOCD=struct.Struct('<4s4H2IH'); CENTRAL=struct.Struct('<4s6H3I5H2I'); LOCAL=struct.Struct('<4s5H3I2H')

def path_kind(i,k):
    if k==5:return (('profile.afb',2) if i==0 else (f'records/{(i-1)//2:06d}.afb',3) if i%2 else (f'sessions/{(i-1)//2:06d}.afb',1))
    return f'curves/{i:06d}.afb',4

def read_exact(f,n):
    b=f.read(n);require(len(b)==n,'ZIP truncado');return b
class Archive:
    def __init__(self,path):
        self.f=open(path,'rb');self.path=Path(path)
        try:self._open()
        except BaseException:self.f.close();raise
    def close(self):self.f.close()
    def __enter__(self):return self
    def __exit__(self,*a):self.close()
    def _open(self):
        f=self.f;size=os.fstat(f.fileno()).st_size;require(22<=size<=MAX_ZIP,'ZIP tamanho inválido');f.seek(size-22);sig,d,cdisk,nd,nt,cs,co,comment=EOCD.unpack(read_exact(f,22));require(sig==b'PK\x05\x06' and d==cdisk==comment==0 and nd==nt and 1<=nt<=MAX_ENTRIES and 0<cs<=MAX_CD and co+cs==size-22,'EOCD inválido');f.seek(co);cd=read_exact(f,cs);p=0;rows=[];names=set()
        for i in range(nt):
            require(p+46<=cs,'central truncada');sig,made,need,flags,method,tm,dt,crc,csize,usize,nl,xl,cl,disk,ia,ea,off=CENTRAL.unpack_from(cd,p);p+=46
            require(sig==b'PK\x01\x02' and need<=20 and flags in (0,2048) and method==0 and xl==cl==disk==0 and 1<=nl<=64 and p+nl<=cs and 136<csize==usize<=128+PAY,'entrada ZIP inválida');name=cd[p:p+nl].decode('ascii');p+=nl
            require(name not in names and not ea&0x10 and stat.S_IFMT(ea>>16) in (0,stat.S_IFREG),'entrada duplicada/link/diretório');names.add(name);rows.append({'name':name,'need':need,'flags':flags,'time':tm,'date':dt,'crc':crc,'size':usize,'offset':off})
        require(p==cs and rows[0]['name']=='manifest.afb','central/manifesto inválido');end=0
        for row in rows:
            require(row['offset']==end,'lacuna/sobreposição ZIP');f.seek(end);sig,need,flags,method,tm,dt,crc,csize,usize,nl,xl=LOCAL.unpack(read_exact(f,30));require(sig==b'PK\x03\x04' and (need,flags,method,tm,dt,crc,csize,usize,xl)==(row['need'],row['flags'],0,row['time'],row['date'],row['crc'],row['size'],row['size'],0) and nl==len(row['name']),'local/central divergente');require(read_exact(f,nl).decode('ascii')==row['name'],'nome local divergente');row['data']=f.tell();end=row['data']+row['size'];require(end<=co,'entrada ultrapassa central')
        require(end==co,'bytes ocultos no ZIP');self.rows=rows;require(rows[0]['size']<=128+CHUNK+8,'manifesto excessivo');b=self._read(rows[0]);info,m=unpack(b);k=info['kind'];require(k in (5,6),'kind manifesto inválido');keys={'schema','schemaVersion','entries'}|({'profileId'} if k==5 else set());require(type(m) is dict and set(m)==keys and type(m['schemaVersion']) is int and m['schemaVersion']==1 and m['schema']==('afinador.binary-profile-manifest' if k==5 else 'afinador.binary-curve-manifest'),'manifesto inválido');es=m['entries'];require(type(es) is list and len(es)==nt-1 and (k==5 and 1<=len(es)<=4001 and len(es)%2==1 or k==6 and len(es)<=128),'quantidade de entradas inválida');self.manifest=m;self.kind=k;total=info['rawBytes'];ids=set()
        if k==5:sem.ident(m['profileId'])
        for i,(e,row) in enumerate(zip(es,rows[1:])):
            name,kind=path_kind(i,k);require(type(e) is dict and set(e)=={'path','kind','id','bytes','rawBytes','sha256'} and e['path']==row['name']==name and all(type(e[x]) is int for x in ('kind','bytes','rawBytes')) and e['kind']==kind and e['bytes']==row['size'],'manifesto diverge do ZIP');sem.ident(e['id']);sem.shape(e['sha256'],'hex256');f.seek(row['data']);h=inspect_header(read_exact(f,128),row['size']);require(h['kind']==kind and h['rawBytes']==e['rawBytes'],'manifesto diverge do envelope');total+=h['rawBytes'];require(total<=MAX_RAW_SUM,'soma raw excessiva');row.update(h)
            if kind in (2,3,4):require((kind,e['id']) not in ids,'ID duplicado');ids.add((kind,e['id']))
            if kind==2:require(e['id']==m['profileId'],'profileId divergente')
        self.raw_total=total
    def _read(self,row):
        self.f.seek(row['data']);b=read_exact(self.f,row['size']);require(zlib.crc32(b)==row['crc'],'CRC ZIP inválido');return b
    def block(self,i):
        require(type(i) is int and 0<=i<len(self.manifest['entries']),'índice fora de faixa');e=self.manifest['entries'][i];b=self._read(self.rows[i+1]);require(hexsha(b)==e['sha256'],'hash do manifesto inválido');info,o=unpack(b,e['kind']);sem.validate_kind(e['kind'],o);key={1:'sessionId',2:'profileId',3:'recordId',4:'versionId'}[e['kind']];require(o[key]==e['id'],'ID do manifesto divergente');return o
    def profile(self):require(self.kind==5,'não é perfil');return self.block(0)
    def records(self,selected=None):
        p=self.profile();n=(len(self.manifest['entries'])-1)//2;indices=range(n) if selected is None else [selected];seen={}
        for i in indices:
            require(type(i) is int and 0<=i<n,'índice de sessão fora de faixa');r=self.block(1+2*i);s=self.block(2+2*i);sem.record(p,r,s);sid=s['sessionId'];require(sid not in seen or seen[sid]==r['stringId'],'colisão sessionId/stringId');seen[sid]=r['stringId'];yield dict(r,session=s)
    def revisions(self):
        require(self.kind==6,'não é histórico');meta=[]
        for i in range(len(self.manifest['entries'])):
            v=self.block(i);meta.append({**{k:v[k] for k in ('versionId','curveId','versionNumber','parentVersionId','parentHash','integrity')},'changeFromParent':None if v['changeFromParent'] is None else True});yield v
        sem.relations(meta)
        by={v['versionId']:i for i,v in enumerate(meta)}
        for i,v in enumerate(meta):
            if v['parentVersionId'] is not None:
                child=self.block(i);parent=self.block(by[v['parentVersionId']]);require(sem.near_tree(child['changeFromParent'],sem.curve_diff(parent['curve'],child['curve'])),'diff histórico divergente')
    def validate(self):
        n=0
        for _ in self.records() if self.kind==5 else self.revisions():n+=1
        return n

# Use disk spool so no full collection of compressed blocks in RAM.
def write_archive(path,kind,items,profile_id=None,codec=1,typed=False):
    require(kind in (5,6),'kind ZIP inválido');entries=[];total=0;stored_total=0
    with tempfile.TemporaryDirectory(prefix='afb-spool-') as td:
        root=Path(td)
        for i,(k,ident,o) in enumerate(items):
            require(i<(4001 if kind==5 else 128),'entradas excessivas');name,expected=path_kind(i,kind);require(k==expected,'ordem de blocos inválida');sem.validate_kind(k,o);b=pack(o,k,codec,typed);raw=inspect_header(b,len(b))['rawBytes'];total+=raw;stored_total+=len(b)+100+2*len(name);require(total<=MAX_RAW_SUM and stored_total<=MAX_ZIP,'soma raw/ZIP excessiva');(root/str(i)).write_bytes(b);entries.append({'path':name,'kind':k,'id':ident,'bytes':len(b),'rawBytes':raw,'sha256':hexsha(b)})
        m={'schema':'afinador.binary-profile-manifest' if kind==5 else 'afinador.binary-curve-manifest','schemaVersion':1,'entries':entries}
        if kind==5:m['profileId']=profile_id
        manifest=pack(m,kind,0);require(len(manifest)+sum(e['bytes']+100+2*len(e['path']) for e in entries)+200<=MAX_ZIP,'ZIP excede limite')
        with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
            def put(name,b):
                info=zipfile.ZipInfo(name,(2026,1,1,0,0,0));info.create_system=0;info.create_version=20;info.extract_version=20;z.writestr(info,b)
            put('manifest.afb',manifest)
            for i,e in enumerate(entries):
                b=(root/str(i)).read_bytes();require(hexsha(b)==e['sha256'],'spool adulterado');put(e['path'],b)
        with Archive(path) as a:a.validate()
