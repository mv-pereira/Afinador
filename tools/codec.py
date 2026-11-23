"""AFB 1.0 byte codec. Python >=3.10, stdlib + system libzstd 1.5.7 tested.
No execution of data, bounded DEFLATE/Zstd output. Separate semantic validation.
"""
import ctypes as C
import ctypes.util
import gzip
import hashlib
import json
import math
import re
import struct
import zlib
from functools import lru_cache

MIB=2**20; CHUNK=2*MIB; RAW=32*MIB; PAY=34*MIB; STORED=CHUNK+65536
SAFE=2**53-1; MAX_NODES=2500000; MAX_TOKENS=5000000
FORBIDDEN={'__proto__','constructor','prototype','pcm','wav','rawAudio','audioBlob'}
MAGIC=b'AFBLOCK\n'; HEADER=struct.Struct('>8sHHBBHIIII')
CODECS={'store':0,'zstd':1,'gzip':2}
class FormatError(ValueError): pass

def require(ok,msg):
    if not ok: raise FormatError(msg)
def sha(b): return hashlib.sha256(b).digest()
def hexsha(b): return sha(b).hex()
def utf16(s):
    try: return s.encode('utf-16-be')
    except UnicodeError as e: raise FormatError('Unicode inválido') from e
def textcheck(s,key=False):
    require(type(s) is str,'chave não textual')
    require(len(utf16(s))<=2*(256 if key else 100000),'texto excessivo')
    if key: require(s not in FORBIDDEN,'chave proibida')
def numbercheck(v):
    require(type(v) in (int,float) and math.isfinite(v) and (not float(v).is_integer() or abs(v)<=SAFE),'número fora do domínio seguro')
def grid(path): return path[-2:]==('spectrumGrid202','values')
def gridvalue(x):return type(x) in (int,float) and math.isfinite(x) and float(x).is_integer() and -1600<=x<=0
def gridcheck(v): require(type(v) is list and 0<len(v)<=4096 and all(gridvalue(x) for x in v),'grade Int16 inválida')
def signedzero(x):return type(x) is float and x==0 and math.copysign(1,x)<0

def cbor_encode(obj,typed=False,limit=RAW):
    out=bytearray(); nodes=0; tokens=0; active=set()
    def put(b):
        require(len(out)+len(b)<=limit,'CBOR excede limite');out.extend(b)
    def head(m,n):
        if n<24: put(bytes([m*32+n]));return
        k=next(k for k in (1,2,4,8) if n<1<<(8*k));put(bytes([m*32+{1:24,2:25,4:26,8:27}[k]])+n.to_bytes(k,'big'))
    def string(s,key=False):
        textcheck(s,key);b=s.encode('utf-8');head(3,len(b));put(b)
    def e(v,path,d):
        nonlocal nodes,tokens
        nodes+=1;tokens+=1;require(nodes<=MAX_NODES and tokens<=MAX_TOKENS and d<=60,'orçamento CBOR excedido')
        if path[-1:]==('spectrumGrid202',):require(type(v) is dict and set(v)=={'version','values'},'campos de grade inválidos')
        if path[-2:]==('spectrumGrid202','version'):require(type(v) in (int,float) and v==1,'versão de grade inválida')
        if grid(path):gridcheck(v)
        if v is None: put(b'\xf6')
        elif type(v) is bool: put(b'\xf5' if v else b'\xf4')
        elif type(v) in (int,float):
            numbercheck(v)
            if type(v) is int or (v.is_integer() and not (v==0 and math.copysign(1,v)<0)):
                n=int(v);head(0 if n>=0 else 1,n if n>=0 else -1-n)
            else: put(b'\xfb'+struct.pack('>d',v))
        elif type(v) is str: string(v)
        elif type(v) in (list,dict):
            require(id(v) not in active,'ciclo');active.add(id(v))
            if type(v) is list:
                require(len(v)<=200000,'array excessivo')
                if typed and grid(path) and not any(signedzero(x) for x in v):
                    gridcheck(v);nodes+=len(v);tokens+=1;require(nodes<=MAX_NODES and tokens<=MAX_TOKENS and d<60,'grade excede orçamento');head(6,73);head(2,len(v)*2);put(struct.pack('>'+str(len(v))+'h',*map(int,v)))
                else:
                    head(4,len(v))
                    for x in v:e(x,path+('[]',),d+1)
            else:
                require(len(v)<=4096,'mapa excessivo');head(5,len(v))
                for k,x in v.items():
                    tokens+=1;require(tokens<=MAX_TOKENS,'tokens excessivos');string(k,True);e(x,path+(k,),d+1)
            active.remove(id(v))
        else: raise FormatError('tipo não suportado')
    e(obj,(),0);return bytes(out)

class Reader:
    def __init__(self,b,build):self.b=memoryview(b);self.p=0;self.nodes=0;self.tokens=0;self.build=build
    def take(self,n):
        require(0<=n<=len(self.b)-self.p,'CBOR truncado');p=self.p;self.p+=n;return self.b[p:self.p]
    def head(self):
        self.tokens+=1;require(self.tokens<=MAX_TOKENS,'tokens excessivos');c=self.take(1)[0];m,a=c>>5,c&31
        if a<24:return m,a,a
        require(a in (24,25,26,27),'CBOR indefinite/reservado');return m,int.from_bytes(self.take({24:1,25:2,26:4,27:8}[a]),'big'),a
    def string(self,n,key=False):
        require(n<=400000,'texto excessivo');s=self.take(n).tobytes().decode('utf-8','strict');textcheck(s,key);return s
    def value(self,path=(),d=0):
        self.nodes+=1;require(self.nodes<=MAX_NODES and d<=60,'nós/profundidade excedidos');m,n,a=self.head(); gr=path[-1:]==('spectrumGrid202',);ver=path[-2:]==('spectrumGrid202','version');vals=grid(path)
        require(not gr or m==5 and n==2,'grade inválida');require(not ver or m in (0,1) or m==7 and a==27,'versão grade inválida');require(not vals or m in (4,6),'valores grade inválidos')
        if m in (0,1):v=n if m==0 else -1-n;numbercheck(v);require(not ver or v==1,'versão grade inválida');return v
        if m==3:return self.string(n)
        if m==7:
            if a in (20,21,22):return {20:False,21:True,22:None}[a]
            require(a==27,'simples/float não permitido');v=struct.unpack('>d',n.to_bytes(8,'big'))[0];numbercheck(v);require(not ver or v==1,'versão grade inválida');return v
        if m==4:
            require(n<=200000 and n<=len(self.b)-self.p and self.nodes+n<=MAX_NODES,'array inválido')
            if vals:
                require(0<n<=4096 and d<60,'grade excessiva');v=[self.value(path+('[]',),d+1) for _ in range(n)];gridcheck(v);return v if self.build else None
            if self.build:return [self.value(path+('[]',),d+1) for _ in range(n)]
            for _ in range(n):self.value(path+('[]',),d+1)
            return None
        if m==5:
            require(n<=4096 and 2*n<=len(self.b)-self.p and self.nodes+n<=MAX_NODES,'mapa inválido');seen=set();out={}
            for _ in range(n):
                t,l,_=self.head();require(t==3,'chave não textual');k=self.string(l,True);require(not gr or k in ('version','values'),'campo grade inválido');require(k not in seen,'chave duplicada');seen.add(k);v=self.value(path+(k,),d+1)
                if self.build:out[k]=v
            return out if self.build else None
        if m==6:
            require(n in (73,77) and grid(path),'tag proibida');t,l,_=self.head();require(t==2 and 0<l<=8192 and l%2==0,'grade inválida');self.nodes+=l//2;require(self.nodes<=MAX_NODES and d<60,'grade excede orçamento');v=[x[0] for x in struct.iter_unpack('>h' if n==73 else '<h',self.take(l))];gridcheck(v);return v if self.build else None
        raise FormatError('tipo CBOR proibido')

def cbor_decode(b,limit=RAW):
    require(0<len(b)<=limit,'tamanho CBOR inválido')
    try:
        for build in (False,True):
            r=Reader(b,build);o=r.value();require(r.p==len(b),'sufixo CBOR')
        return o
    except UnicodeError as e:raise FormatError('UTF-8 inválido') from e

@lru_cache(maxsize=1)
def library():
    name=ctypes.util.find_library('zstd');require(name,'libzstd ausente; consulte README')
    l=C.CDLL(name)
    for n,a,r in [('ZSTD_compressBound',[C.c_size_t],C.c_size_t),('ZSTD_compress',[C.c_void_p,C.c_size_t,C.c_void_p,C.c_size_t,C.c_int],C.c_size_t),('ZSTD_decompress',[C.c_void_p,C.c_size_t,C.c_void_p,C.c_size_t],C.c_size_t),('ZSTD_isError',[C.c_size_t],C.c_uint),('ZSTD_versionString',[],C.c_char_p)]:
        f=getattr(l,n);f.argtypes=a;f.restype=r
    return l

def zframe(b,n):
    require(len(b)>=6 and b[:4]==b'\x28\xb5\x2f\xfd','magic Zstd inválido');p=5;d=b[4];f=d>>6;single=bool(d&32);require(not d&27,'dicionário/bits reservados Zstd')
    if not single:
        w=b[p];p+=1;base=1<<(10+(w>>3));win=base+base//8*(w&7)
    k=(1 if single else 0,2,4,8)[f];require(k and p+k<=len(b),'content size Zstd ausente');size=int.from_bytes(b[p:p+k],'little')+(256 if k==2 else 0);p+=k;require(size==n and 0<n<=CHUNK,'content size Zstd divergente');win=size if single else win;require(win<=CHUNK,'janela Zstd excessiva')
    while True:
        require(p+3<=len(b),'bloco Zstd truncado');h=int.from_bytes(b[p:p+3],'little');p+=3;t=(h>>1)&3;l=h>>3;require(t!=3 and l<=min(131072,win),'bloco Zstd inválido');p+=1 if t==1 else l;require(p<=len(b),'bloco Zstd truncado')
        if h&1:break
    require(p+(4 if d&4 else 0)==len(b),'frame Zstd extra/truncado')
def zcomp(b):
    l=library();out=C.create_string_buffer(l.ZSTD_compressBound(len(b)));n=l.ZSTD_compress(out,len(out),b,len(b),3);require(not l.ZSTD_isError(n) and 0<n<=STORED,'compressão Zstd falhou');r=out.raw[:n];zframe(r,len(b));return r
def zun(b,n):
    zframe(b,n);l=library();out=C.create_string_buffer(n);r=l.ZSTD_decompress(out,n,b,len(b));require(not l.ZSTD_isError(r) and r==n,'descompressão Zstd falhou');return out.raw

def gun(b,n):
    require(len(b)>=18 and b[:4]==b'\x1f\x8b\x08\x00','GZIP header inválido');crc,size=struct.unpack('<II',b[-8:]);require(size==n,'ISIZE divergente');d=zlib.decompressobj(-15)
    try:r=d.decompress(b[10:-8],n+1)
    except zlib.error as e:raise FormatError('DEFLATE inválido') from e
    require(len(r)==n and d.eof and not d.unused_data and not d.unconsumed_tail,'GZIP tamanho/fim inválido');require(zlib.crc32(r)==crc,'CRC GZIP inválido');return r

def pack_raw(raw,kind,codec=1):
    require(type(kind) is int and kind in range(1,7) and codec in (0,1,2) and (kind<5 or codec==0),'kind/codec inválido');require(0<len(raw)<=(CHUNK if kind>=5 else RAW),'CBOR bruto excessivo');payload=bytearray();q=0
    for i in range(0,len(raw),CHUNK):
        r=raw[i:i+CHUNK];z=r if codec==0 else zcomp(r) if codec==1 else gzip.compress(r,compresslevel=6,mtime=0);require(0<len(z)<=STORED,'chunk armazenado excessivo');payload.extend(struct.pack('>II',len(r),len(z)));payload.extend(z);q+=1
    require(len(payload)<=PAY,'payload excessivo');h=HEADER.pack(MAGIC,1,0,kind,codec,0,len(raw),len(payload),q,0)+sha(raw)+sha(payload);return h+sha(h)+payload

def inspect_header(b,total):
    require(len(b)>=128,'cabeçalho truncado');magic,ma,mi,k,c,f,n,l,q,r=HEADER.unpack(b[:32]);require((magic,ma,mi,f,r)==(MAGIC,1,0,0,0) and k in range(1,7) and c in (0,1,2) and (k<5 or c==0),'envelope incompatível');require(0<n<=(CHUNK if k>=5 else RAW) and 0<l<=PAY and total==128+l and q==(n+CHUNK-1)//CHUNK,'tamanho/chunks inválidos');require(sha(b[:96])==b[96:128],'hash do cabeçalho inválido');return {'kind':k,'codec':c,'rawBytes':n,'bytes':total,'chunks':q}
def unpack_raw(b,expected=None):
    info=inspect_header(b,len(b));k,c,n,q=(info[x] for x in ('kind','codec','rawBytes','chunks'));require(expected is None or k==expected,'kind divergente');require(sha(memoryview(b)[128:])==b[64:96],'hash payload inválido');p=128;spans=[]
    for i in range(q):
        require(p+8<=len(b),'chunk truncado');a,z=struct.unpack_from('>II',b,p);p+=8;require(a==min(CHUNK,n-i*CHUNK) and 0<z<=STORED and p+z<=len(b),'chunk inválido');require(c!=0 or a==z,'STORE divergente');spans.append((p,z,a));p+=z
    require(p==len(b),'sufixo payload')
    if c==1:
        for p,z,a in spans:zframe(b[p:p+z],a)
    raw=bytearray()
    for p,z,a in spans:
        v=b[p:p+z];r=v if c==0 else zun(v,a) if c==1 else gun(v,a);raw.extend(r)
    require(len(raw)==n and sha(raw)==b[32:64],'hash raw inválido');return info,raw

def pack(obj,kind,codec=1,typed=False):return pack_raw(cbor_encode(obj,typed,CHUNK if kind>=5 else RAW),kind,codec)
def unpack(b,expected=None):
    i,r=unpack_raw(b,expected);return i,cbor_decode(r,CHUNK if i['kind']>=5 else RAW)

def exact(a,b):
    if type(a) in (int,float) and type(b) in (int,float):return a==b and (a!=0 or math.copysign(1,a)==math.copysign(1,b))
    if type(a)!=type(b):return False
    if isinstance(a,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    if isinstance(a,dict):return a.keys()==b.keys() and all(exact(a[k],b[k]) for k in a)
    return a==b

# JSON preflight parser: no unbounded json.loads on untrusted input. Preserve -0.
NUM=re.compile(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?')
WS=re.compile(r'[ \t\r\n]*')
def json_read(path):
    with open(path,'rb') as f:b=f.read(RAW+1)
    require(0<len(b)<=RAW,'JSON legado >32 MiB ou vazio');s=b.decode('utf-8');p=0;nodes=0
    def ws():
        nonlocal p;p=WS.match(s,p).end()
    def string(key=False):
        nonlocal p
        v,p=json.decoder.scanstring(s,p+1,True);textcheck(v,key);return v
    def v(d):
        nonlocal p,nodes
        ws();nodes+=1;require(nodes<=MAX_NODES and d<=60 and p<len(s),'JSON excede limites/truncado');c=s[p]
        if c=='"':return string()
        if c in '[{':
            mp=c=='{';end='}' if mp else ']';out={} if mp else [];p+=1;ws()
            if p<len(s) and s[p]==end:p+=1;return out
            while True:
                require(len(out)<(4096 if mp else 200000),'coleção JSON excessiva');ws()
                if mp:
                    require(p<len(s) and s[p]=='"','chave JSON inválida');k=string(True);require(k not in out,'chave JSON duplicada');ws();require(p<len(s) and s[p]==':','JSON inválido');p+=1;out[k]=v(d+1)
                else:out.append(v(d+1))
                ws();require(p<len(s),'JSON truncado');c=s[p];p+=1
                if c==end:return out
                require(c==',','JSON inválido')
        for lit,x in [('true',True),('false',False),('null',None)]:
            if s.startswith(lit,p):p+=len(lit);return x
        m=NUM.match(s,p);require(m and len(m[0])<=128,'número JSON inválido');t=m[0];p=m.end();x=float(t) if t=='-0' or any(c in t for c in '.eE') else int(t);numbercheck(x);return x
    o=v(0);ws();require(p==len(s),'sufixo JSON');return o

# RFC 8785-style serialization for finite safe JS numbers. Verified against baseline corpus;
# not a claim of exhaustive ECMAScript shortest-decimal equivalence.
def jsnum(x):
    numbercheck(x)
    if x==0:return '0'
    if type(x) is int:return str(x)
    s=repr(x).lower();sign='-' if s.startswith('-') else '';s=s.lstrip('-');a,_,ex=s.partition('e');ex=int(ex or '0');i,_,frac=a.partition('.');digits=(i+frac).lstrip('0');point=len(i)+ex-(len(i+frac)-len((i+frac).lstrip('0')));digits=digits.rstrip('0')
    if 0<point<=21:return sign+(digits+'0'*(point-len(digits)) if point>=len(digits) else digits[:point]+'.'+digits[point:])
    if -6<point<=0:return sign+'0.'+'0'*(-point)+digits
    e=point-1;return sign+digits[0]+('.'+digits[1:] if len(digits)>1 else '')+'e'+('+' if e>=0 else '')+str(e)
def jcs(x):
    if x is None:return 'null'
    if type(x) is bool:return 'true' if x else 'false'
    if type(x) in (int,float):return jsnum(x)
    if type(x) is str:return json.dumps(x,ensure_ascii=False,separators=(',',':'))
    if type(x) is list:return '['+','.join(map(jcs,x))+']'
    require(type(x) is dict,'tipo JCS inválido');return '{'+','.join(jcs(k)+':'+jcs(x[k]) for k in sorted(x,key=utf16))+'}'
def semantic_hash(x):return hexsha(jcs(x).encode('utf-8'))
