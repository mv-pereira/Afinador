#!/usr/bin/env python3
"""Interoperability of AFB transport with a TRUSTED local Afinador HTML.
Not browser/IndexedDB validation or authorization of acoustic data.
"""
import argparse,json,re,subprocess,sys,tempfile,zipfile
from pathlib import Path
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'tools'))
from codec import exact,pack,unpack

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('html',type=Path);p.add_argument('--profile',type=Path)
    args=p.parse_args()
    scripts=dict(re.findall(r'<script\b([^>]*)>(.*?)</script>',args.html.read_text(encoding='utf-8'),re.S))
    sec=scripts[' id="fonteSeguranca13"'];codec=scripts[' id="afbCodec214"'];worker=scripts[' id="afbWorker215Source" type="text/plain"']
    worker=worker.split('/* Protocol 2: one in-flight request',1)[0]
    js=r'''const fs=require('fs');const c=AFB21Codec.create();const cases=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
    (async()=>{for(const q of cases){const r=await AFB21Envelope.unpackRaw(fs.readFileSync(q.input),q.kind);const o=c.decode(q.kind,r.raw);fs.writeFileSync(q.output,await AFB21Envelope.packRaw(q.kind,q.codec,c.encode(q.kind,o,{typed:q.typed})));}console.log('JS decode/encode:',cases.length);})().catch(e=>{console.error(e);process.exit(1)});'''
    with tempfile.TemporaryDirectory() as t:
        d=Path(t);cases=[]; expected=[]
        def add(b,codec,typed):
            i,o=unpack(b);n=len(cases);f=d/f'{n}.in';g=d/f'{n}.out';f.write_bytes(b)
            cases.append(dict(input=str(f),output=str(g),kind=i['kind'],codec=codec,typed=typed));expected.append(o)
        fixture=unpack((P/'fixtures/session-store.afs').read_bytes())[1]
        for codec_id in (0,1,2):
            for typed in (False,True):add(pack(fixture,1,codec_id,typed),codec_id,typed)
        for fn in ('profile.afp','history-empty.afc','history-incomplete.afc'):
            with zipfile.ZipFile(P/'fixtures'/fn) as z:
                for n in z.namelist():
                    b=z.read(n);i,_=unpack(b);add(b,0 if i['kind']>=5 else 1,False)
        if args.profile:
            # Archive validates the manifest and bounded block reads before using the provided file.
            from archive import Archive
            with Archive(args.profile) as ar: ar.validate()
            with zipfile.ZipFile(args.profile) as z:
                for n in z.namelist():
                    b=z.read(n);i,_=unpack(b);add(b,0 if i['kind']>=5 else 1,False)
        (d/'run.cjs').write_text(sec+'\n'+codec+'\n'+worker+'\n'+js,encoding='utf-8')
        (d/'cases.json').write_text(json.dumps(cases),encoding='utf-8')
        subprocess.run(['node',str(d/'run.cjs'),str(d/'cases.json')],check=True,timeout=180)
        for q,o in zip(cases,expected):
            i,r=unpack(Path(q['output']).read_bytes());assert i['kind']==q['kind'] and exact(r,o),q['input']
        print(f'Interoperabilidade Python → JS → Python: {len(cases)}/{len(cases)}')
if __name__=='__main__':main()
