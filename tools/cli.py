"""Command line tools, no GUI or HTML dependency. Outputs committed only on success."""
import argparse,contextlib,os,sys,tempfile,json,hashlib
from pathlib import Path
from codec import *
from archive import Archive,write_archive
import semantics as sem

@contextlib.contextmanager
def atomic(path,source,force=False):
    p=Path(path);require(p.resolve()!=Path(source).resolve(),'não sobrescreva a fonte');require(force or not p.exists(),'saída já existe (use --force)');p.parent.mkdir(parents=True,exist_ok=True);fd,t=tempfile.mkstemp(prefix='.afb-',dir=p.parent);os.close(fd)
    try:
        yield Path(t)
        if force:os.replace(t,p)
        else:os.link(t,p);os.unlink(t)
    finally:
        if os.path.exists(t):os.unlink(t)

def detect(p):
    with open(p,'rb') as f:b=f.read(4096)
    if b[:8]==MAGIC:return 'afb'
    if b.startswith(b'PK\x03\x04'):return 'zip'
    if b.lstrip().startswith(b'{'):return 'json'
    raise FormatError('formato não reconhecido')
def read_block(p,transport=False):
    with open(p,'rb') as f:b=f.read(128+PAY+1)
    require(len(b)<=128+PAY,'bloco excessivo');i,o=unpack(b)
    if not transport:require(i['kind']==1,'arquivo standalone deve ser sessão; utilize --transport-only para diagnóstico');sem.session(o)
    return i,o

def items_profile(o):
    require(set(o)=={'schema','schemaVersion','profile','records','curves','integrity'} and o['schemaVersion']==1 and o['curves']==[] and type(o['records']) is list and len(o['records'])<=2000,'perfil legado inválido');sem.integrity(o);p=o['profile'];sem.profile(p);yield 2,p['profileId'],p
    for r in o['records']:
        s=r['session'];h={k:v for k,v in r.items() if k!='session'};sem.session(s);sem.record(p,h,s);yield 3,h['recordId'],h;yield 1,s['sessionId'],s

def encode(source,target,codec,typed,force):
    o=json_read(source)
    with atomic(target,source,force) as tmp:
        if o.get('format')=='afinador.acquisition-session':
            sem.session(o);tmp.write_bytes(pack(o,1,codec,typed))
        elif o.get('schema')=='afinador.acoustic-profile':write_archive(tmp,5,items_profile(o),o['profile']['profileId'],codec,typed)
        elif o.get('schema')=='afinador.tuning-curve-history':
            sem.shape(o,'history-map');sem.integrity(o);sem.relations(o['versions']);write_archive(tmp,6,((4,v['versionId'],v) for v in o['versions']),codec=codec,typed=typed)
        else:raise FormatError('schema JSON não suportado')

def output_json(tmp,obj):
    with open(tmp,'w',encoding='utf-8') as f:json.dump(obj,f,ensure_ascii=False,allow_nan=False,indent=2);f.write('\n')

def stream_legacy(tmp,a):
    # Emit JSON in canonical key order for hash without materializing all records.
    # Emitted values preserve negative zero via ordinary JSON; hash uses JCS separately.
    fields={'schema':'afinador.acoustic-profile' if a.kind==5 else 'afinador.tuning-curve-history','schemaVersion':1}
    listkey='records' if a.kind==5 else 'versions'
    if a.kind==5:fields.update(profile=a.profile(),curves=[])
    h=hashlib.sha256();h.update(b'{');first=True
    with open(tmp,'w',encoding='utf-8') as f:
        f.write('{\n')
        for k in sorted([*fields,listkey],key=utf16):
            if not first:h.update(b',');f.write(',\n')
            first=False;prefix=jcs(k)+':';h.update(prefix.encode());f.write(prefix)
            if k==listkey:
                h.update(b'[');f.write('[\n');one=True
                for o in a.records() if a.kind==5 else a.revisions():
                    if not one:h.update(b',');f.write(',\n')
                    one=False;h.update(jcs(o).encode());json.dump(o,f,ensure_ascii=False,separators=(',',':'),allow_nan=False)
                h.update(b']');f.write('\n]')
            else:h.update(jcs(fields[k]).encode());json.dump(fields[k],f,ensure_ascii=False,allow_nan=False,separators=(',',':'))
        h.update(b'}');f.write(',\n"integrity":'+json.dumps({'algorithm':'SHA-256/JCS','sha256':h.hexdigest()})+'\n}\n')

def decode(source,target,index,force,transport=False,full_record=False):
    t=detect(source)
    with atomic(target,source,force) as tmp:
        if t=='afb':require(index is None,'índice apenas para perfil/histórico');_,o=read_block(source,transport);output_json(tmp,o)
        elif t=='zip':
            require(not transport,'transport-only apenas em AFB individual')
            with Archive(source) as a:
                if index is None:stream_legacy(tmp,a)
                elif a.kind==5:
                    r=next(a.records(index));output_json(tmp,r if full_record else r['session'])
                else:output_json(tmp,a.block(index))
        else:raise FormatError('entrada não binária')

def inspect(source,deep=False,transport=False):
    t=detect(source)
    if t=='afb':
        i,o=read_block(source,transport);r=dict(i,codec=next(k for k,v in CODECS.items() if v==i['codec']));r.update({k:o.get(k) for k in ('sessionId','instrument','createdAt','B','aggregationStatus') if type(o) is dict and k in o});return r
    if t=='zip':
        with Archive(source) as a:
            r={'kind':a.kind,'raw_bytes_total':a.raw_total,'manifest':a.manifest,'scope':'índice; payloads ainda não verificados'}
            if deep:r.update(validated_count=a.validate(),scope='conteúdo percorrido; sem autorização física')
            return r
    if t=='json':
        o=json_read(source);return {'format':o.get('format',o.get('schema')),'schemaVersion':o.get('schemaVersion'),'sessionId':o.get('sessionId'),'scope':'JSON estrutural'}

def validation(source,transport=False):
    t=detect(source)
    if t=='afb':i,_=read_block(source,transport);return {'ok':True,'kind':i['kind'],'scope':'transporte CBOR/AFB' if transport else 'transporte + estrutura e vínculos implementados','physical_authorization':False}
    if t=='zip':
        with Archive(source) as a:return {'ok':True,'kind':a.kind,'count':a.validate(),'scope':'transporte + estrutura e vínculos implementados','physical_authorization':False}
    o=json_read(source)
    if o.get('format')=='afinador.acquisition-session':sem.session(o)
    elif o.get('schema')=='afinador.acoustic-profile':
        for _ in items_profile(o):pass
    elif o.get('schema')=='afinador.tuning-curve-history':
        sem.shape(o,'history-map');sem.integrity(o);sem.relations(o['versions']);[sem.revision(v) for v in o['versions']]
    else:raise FormatError('schema não suportado')
    return {'ok':True,'scope':'estrutura e vínculos implementados','physical_authorization':False}

def main(command=None,argv=None):
    p=argparse.ArgumentParser(description='Afinador AFB 1.0 — ferramentas científicas experimentais')
    if command is None:p.add_argument('command',choices=['encode','decode','inspect','validate','convert'])
    p.add_argument('source');p.add_argument('-o','--output');p.add_argument('--codec',choices=CODECS,default='zstd');p.add_argument('--typed',action='store_true');p.add_argument('--index',type=int,help='índice zero-based da sessão/revisão');p.add_argument('--record',action='store_true',help='extrair registro completo em vez da sessão');p.add_argument('--force',action='store_true');p.add_argument('--deep',action='store_true');p.add_argument('--transport-only',action='store_true',help='diagnóstico de fixtures AFB, não validador acústico');a=p.parse_args(argv);cmd=command or a.command
    try:
        if cmd=='convert':cmd='encode' if detect(a.source)=='json' else 'decode'
        if cmd in ('encode','decode'):
            require(a.output,'informe --output');require(cmd!='encode' or (a.index is None and not a.transport_only and not a.record),'opções incompatíveis');require(not a.record or a.index is not None,'--record exige --index')
            if cmd=='encode':encode(a.source,a.output,CODECS[a.codec],a.typed,a.force)
            else:decode(a.source,a.output,a.index,a.force,a.transport_only,a.record)
            print(a.output)
        else:print(json.dumps(inspect(a.source,a.deep,a.transport_only) if cmd=='inspect' else validation(a.source,a.transport_only),ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError,KeyError,TypeError,IndexError,OverflowError,RecursionError,struct.error) as e:
        print('AFB: '+str(e),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
