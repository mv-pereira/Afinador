#!/usr/bin/env python3
import sys,unittest,tempfile,copy,struct,json,zipfile
from pathlib import Path
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'tools'))
from codec import *
from archive import Archive,write_archive
from cli import decode,encode,validation
import semantics as sem
F=P/'fixtures'

def rehash(b):
    b=bytearray(b);b[64:96]=sha(b[128:]);b[96:128]=sha(b[:96]);return bytes(b)
def fake_chunk(z,n,codec):
    pl=struct.pack('>II',n,len(z))+z;h=HEADER.pack(MAGIC,1,0,1,codec,0,n,len(pl),1,0)+sha(b'a'*n)+sha(pl);return h+sha(h)+pl

class CodecTests(unittest.TestCase):
    def test_fixtures(self):
        exp=json.loads((F/'session-expected.json').read_text())
        for codec in CODECS:
            with self.subTest(codec=codec):
                i,o=unpack((F/f'session-{codec}.afs').read_bytes(),1);self.assertTrue(exact(o,exp));sem.session(o)
    def test_transport(self):
        for name in ('transport-edge','transport-multichunk'):
            _,o=unpack((F/(name+'.afb')).read_bytes());self.assertTrue(exact(o,cbor_decode(cbor_encode(o,True))))
        o=unpack((F/'transport-edge.afb').read_bytes())[1];self.assertLess(math.copysign(1,o['zeroNegative']),0);self.assertEqual(o['safeInteger'],SAFE)
    def test_edge_values(self):
        o={'spectrumGrid202':{'version':1,'values':[-1600,-1,0]},'numbers':[SAFE,-SAFE,-4294967297,-0.0,0,5e-324,1e-6,1e-7,1.2345678901234567],'unicode':'\ufeff𝄞♯'}
        for c in (0,1,2):
            for typed in (False,True):self.assertTrue(exact(o,unpack(pack(o,1,c,typed))[1]))
        self.assertEqual(jsnum(1e-6),'0.000001');self.assertEqual(jsnum(1e-7),'1e-7')
    def test_reject_cbor(self):
        bad=['','ff','f7','f90000','fa00000000','fb7ff8000000000000','fb7ff0000000000000','1b0020000000000000','3b0020000000000000','9f01ff','bf616101ff','a2616101616102','a10101','a1695f5f70726f746f5f5f00','a16370636d00','63eda080','62c080','4100','d849420000','810100','9affffffff','ba01000000','d8ff00','7f6161ff','a16161']
        for b in bad:
            with self.subTest(b=b):
                with self.assertRaises((FormatError,UnicodeError)):cbor_decode(bytes.fromhex(b))
    def test_bad_envelope(self):
        b=(F/'session-zstd.afs').read_bytes()
        cases=[b[:i] for i in (0,8,96,127,128,135,len(b)-1)]+[b+b'x']
        for i in (0,8,13,14,28,96,128,len(b)-1):c=bytearray(b);c[i]^=1;cases.append(bytes(c))
        for i in (8,10,12,13,14,16,20,24,28,32,128,132):
            c=bytearray(b);c[i]^=1;cases.append(rehash(c))
        for i,c in enumerate(cases):
            with self.subTest(i=i):
                with self.assertRaises(FormatError):unpack(c)
    def test_multi_chunk_writer(self):
        o={'rows':['abc'*30000+str(i) for i in range(26)]}
        for c in (0,1,2):
            info,q=unpack(pack(o,1,c));self.assertGreater(info['chunks'],1);self.assertTrue(exact(o,q))
    def test_typed_little_endian(self):
        key=b'spectrumGrid202'; raw=b'\xa1'+bytes([0x60+len(key)])+key+b'\xa2\x67version\x01\x66values\xd8\x4d\x44'+struct.pack('<hh',-1600,0)
        self.assertEqual(cbor_decode(raw),{'spectrumGrid202':{'version':1,'values':[-1600,0]}})
    def test_grid_signed_and_invalid(self):
        v={'spectrumGrid202':{'version':1,'values':[-1600,-0.0,0]}}
        self.assertTrue(exact(v,cbor_decode(cbor_encode(v,True))))
        for g in ({'values':[0]},{'version':1,'values':[1]},{'version':2,'values':[0]},{'version':1,'values':[]},{'version':1,'values':[False]}):
            with self.assertRaises(FormatError):cbor_encode({'spectrumGrid202':g},True)
        # Input forged independently: a generic map named spectrumGrid202 lacking version.
        key=b'spectrumGrid202';raw=b'\xa1'+bytes([0x60+len(key)])+key+b'\xa1\x66values\x81\x00'
        with self.assertRaises(FormatError):cbor_decode(raw)
    def test_bombs(self):
        ob=b'a'*100000;z=gzip.compress(ob,mtime=0);g=z[:-4]+struct.pack('<I',1)
        for x in [fake_chunk(g,1,2),fake_chunk(z+z,len(ob),2),fake_chunk(zcomp(ob)+zcomp(ob),len(ob),1),fake_chunk(zcomp(ob),1,1),fake_chunk(b'aa',1,0)]:
            with self.assertRaises(FormatError):unpack_raw(x)
    def test_json(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'x.json'
            for x in ('{"a":1,"a":2}','{"a":1,"\\u0061":2}','{"constructor":0}','{"a":NaN}','{"a":9007199254740992}','{"a":"\\ud800"}','['*62+'0'+']'*62):
                p.write_text(x)
                with self.assertRaises((ValueError,UnicodeError)):json_read(p)
            p.write_text('{"a":-0}');self.assertLess(math.copysign(1,json_read(p)['a']),0)
    def test_semantic_and_hash(self):
        o=json.loads((F/'session-expected.json').read_text());sem.session(o)
        for field,val in [('snapshotHash','0'*64),('curveEligible',True),('sampleRateHz',0),('instrument','Outro')]:
            c=dict(o);c[field]=val
            with self.assertRaises(FormatError):sem.session(c)
    def test_archive_fixtures(self):
        with Archive(F/'profile.afp') as a:
            self.assertEqual(a.validate(),1);r=next(a.records(0));exp=json.loads((F/'profile-expected.json').read_text());self.assertTrue(exact(r['session'],json.loads((F/'session-expected.json').read_text())));self.assertTrue(exact(a.profile(),exp['profile']));self.assertTrue(exact({k:v for k,v in r.items() if k!='session'},exp['recordHeader']))
        for fn,n in [('history-empty.afc',0),('history-incomplete.afc',1)]:
            with Archive(F/fn) as a:self.assertEqual(a.validate(),n)
    def test_archive_conversion(self):
        with tempfile.TemporaryDirectory() as td:
            for fn in ('profile.afp','history-empty.afc','history-incomplete.afc'):
                a=Path(td)/(fn+'.json');b=Path(td)/fn;c=Path(td)/(fn+'.out.json');decode(F/fn,a,None,False);encode(a,b,1,True,False);decode(b,c,None,False);self.assertTrue(exact(json_read(a),json_read(c)))
    def test_selective(self):
        with Archive(F/'profile.afp') as a:
            with self.assertRaises(FormatError):next(a.records(1))
            self.assertEqual(next(a.records(0))['session']['sessionId'],'fixture-session')
    def test_archive_corruption(self):
        b=(F/'profile.afp').read_bytes();i=b.index(b'PK\x01\x02');bad=[b+b'0',b'0'+b,b[:-1]]
        for offset in (6,8,14,i+8,i+10,i+16,i+42,len(b)-2):
            c=bytearray(b);c[offset]^=1;bad.append(c)
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'x.afp'
            for c in bad:
                p.write_bytes(c)
                with self.assertRaises((FormatError,UnicodeError)):
                    with Archive(p) as a:a.validate()
            # payload corruption not covered by fast manifest inspection: full read must reject
            with Archive(F/'profile.afp') as a:off=a.rows[-1]['data']+129
            c=bytearray(b);c[off]^=1;p.write_bytes(c)
            with Archive(p) as a:
                self.assertEqual(len(a.manifest['entries']),3)
                with self.assertRaises(FormatError):a.validate()
    def test_atomic(self):
        with tempfile.TemporaryDirectory() as td:
            src=Path(td)/'bad.afs';dst=Path(td)/'out.json';src.write_bytes(b'AFBLOCK\n');dst.write_text('unchanged')
            with self.assertRaises(FormatError):decode(src,dst,None,True)
            self.assertEqual(dst.read_text(),'unchanged')
    def test_multirecord_profile(self):
        exp=json.loads((F/'profile-expected.json').read_text());p=exp['profile'];s=json.loads((F/'session-expected.json').read_text());rs=[]
        for i in range(104):
            v=dict(s,sessionId=f'synthetic-{i}');h=dict(exp['recordHeader'],sessionHash=semantic_hash(v));h['recordId']=semantic_hash({k:h[k] for k in ('sessionHash','baseSnapshotHash','stringId')});rs.append(dict(h,session=v))
        o={'schema':'afinador.acoustic-profile','schemaVersion':1,'profile':p,'records':rs,'curves':[]};o['integrity']={'algorithm':'SHA-256/JCS','sha256':semantic_hash(o)}
        with tempfile.TemporaryDirectory() as td:
            a=Path(td)/'a.json';b=Path(td)/'a.afp';c=Path(td)/'c.json';a.write_text(json.dumps(o));encode(a,b,1,True,False)
            with Archive(b) as ar:
                self.assertEqual(len(ar.manifest['entries']),209);self.assertEqual(next(ar.records(103))['session']['sessionId'],'synthetic-103');self.assertEqual(ar.validate(),104)
            decode(b,c,None,False);self.assertTrue(exact(o,json_read(c)))
    def test_history_reject(self):
        v=json.loads((F/'curve-expected.json').read_text());v['parentVersionId']='missing';v['parentHash']='0'*64;v['versionNumber']=2;v['curve']['curveVersion']=2;v['integrity']['sha256']=semantic_hash({k:x for k,x in v.items() if k!='integrity'})
        with self.assertRaises(FormatError):sem.relations([v])

if __name__=='__main__':unittest.main(verbosity=2)
