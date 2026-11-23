"""Scientific interchange checks; not an authorization/physical validation engine.
Closed-map rules from shipped CDDL subset; explicit relationship checks below.
"""
from pathlib import Path
import math,re,json,statistics
from codec import *
SCHEMAS=Path(__file__).resolve().parents[1]/'schemas'
MAPS={}
for m in re.finditer(r'^([\w-]+) = \{\n(.*?)^\}',(SCHEMAS/'legacy-maps.cddl').read_text(),re.M|re.S):
    fields={}
    for line in m[2].splitlines():
        g=re.fullmatch(r'\s*(\? )?"([^"]+)": (.*?),?\s*',line)
        if g:fields[g[2]]=(not bool(g[1]),g[3].rstrip(','))
        elif line.strip():raise RuntimeError('regra CDDL não reconhecida: '+line)
    MAPS[m[1]]=fields

def fail(path):raise FormatError('estrutura incompatível: '+path)
def shape(x,t,path='$'):
    if t=='value':return
    if ' / ' in t:
        for y in t.split(' / '):
            try:shape(x,y,path);return
            except FormatError:pass
        fail(path)
    if t in MAPS:
        f=MAPS[t];require(type(x) is dict and set(x)<=set(f) and all(k in x for k,(r,_) in f.items() if r),'mapa incompatível '+path)
        for k,v in x.items():shape(v,f[k][1],path+'.'+k)
    elif t.startswith('['):
        g=re.fullmatch(r'\[(\d*)\*(\d*) (.+)\]',t)
        if g:
            require(type(x) is list and int(g[1] or 0)<=len(x)<=int(g[2] or 200000),'lista incompatível '+path)
            for v in x:shape(v,g[3],path+'[]')
        elif t=='[number64, number64]':require(type(x) is list and len(x)==2,'par inválido');[numbercheck(v) for v in x]
        else:raise RuntimeError('regra não implementada '+t)
    elif t=='null':require(x is None,path)
    elif t=='bool':require(type(x) is bool,path)
    elif t=='false':require(x is False,path)
    elif t=='number64':numbercheck(x)
    elif t=='nullable-number':require(x is None or type(x) in (int,float),path)
    elif t=='object-value':require(type(x) is dict,path)
    elif t in ('text-value','identity','nonempty'):require(type(x) is str and (bool(x) or t=='text-value'),path)
    elif t=='hex256':require(type(x) is str and re.fullmatch('[a-f0-9]{64}',x),path)
    elif t=='source-condition':require(x in ('unknown','isolated','unison'),path)
    elif t=='grid-values':require(type(x) is list,path);gridcheck(x)
    elif t.startswith('"'):require(x==json.loads(t),path)
    elif re.fullmatch(r'-?\d+\.\.-?\d+',t):a,b=map(int,t.split('..'));require(type(x) is int and a<=x<=b,path)
    elif t.isdigit():require(type(x) is int and x==int(t),path)
    else:raise RuntimeError('tipo CDDL não implementado '+t)

def ident(s,n=256):require(type(s) is str and 0<len(utf16(s))<=2*n,'identificador inválido')
def text(s,n):require(type(s) is str and len(utf16(s))<=2*n,'texto inválido')
def num(x):return type(x) in (int,float) and math.isfinite(x)
def pos(x):return num(x) and x>0
def unique(a):require(len(a)==len(set(a)),'identificador duplicado')
def rational(n,d):
    require(type(n) is int and type(d) is int and abs(n)<=SAFE and 0<abs(d)<=SAFE,'fração inválida');g=math.gcd(n,d);sign=1 if d>0 else -1;return [sign*n//g,sign*d//g]
def frac(s):
    m=re.fullmatch(r'(-?\d+)(?:/(\d+))?',str(s));require(m,'fração inválida');return rational(int(m[1]),int(m[2] or 1))
def offsets(o):return {k:{'cp':frac(v['cp']),'cs':frac(v['cs'])} for k,v in (o or {}).items()}
def semantic(s):
    l=s['layout'];e=s['edo'];ts=sorted(s['targets'],key=lambda t:(utf16(t['keyId']),t['octave']))
    return {'snapshotSchemaVersion':1,'builder':'afinador-semantic-snapshot-3.0','temperament':s['temperament'],'definition':s['definition'],'recipe':None if e is not None else sorted([{'index':q['index'],'cp':rational(q['acumCpNum'],q['acumCpDen']),'cs':rational(q['acumCsNum'],q['acumCsDen'])} for q in s['quintas']],key=lambda q:q['index']),'closure':None if e is not None else s['compensatoryIndex'],'layout':{'layoutId':'edo-'+str(e['divisionCount']),'keyboardKeys':e.get('keyboardKeys')} if e is not None else {'layoutId':l['layoutId'],'baseLayoutId':l['baseLayoutId'],'extensionFifths':offsets(l.get('extensionFifths')),'extraPitchOffsets':offsets(l.get('extraPitchOffsets'))},'reference':{'degree':e['referenceDegree'],'octave':e['referenceOctave'],'hz':e['referenceHz'],'divisionCount':e['divisionCount'],'fifthGeneratorSteps':e['fifthGeneratorSteps'],'degreeOffsets':offsets(e.get('degreeOffsets'))} if e is not None else {'hz':s['referenceA4Hz']},'targets':[{k:t[k] for k in ('keyId','pitchId','soundId','octave','frequency')} for t in ts]}
def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def snapshot(s):
    shape(s,'snapshot-map');m={}
    for t in s['targets']:
        for k in ('keyId','pitchId','soundId','name','scientific'):ident(t[k])
        require(t['targetId']==compact([t['keyId'],t['octave']]) and t['targetId'] not in m and 0<t['frequency']<=100000,'alvo inválido');m[t['targetId']]=t
    return m

def binding(b,m,h):
    if b['noteBindingStatus']=='confirmed':
        t=m.get(b.get('targetId'));require(t is not None and all(t[k]==b.get(v) for k,v in [('keyId','keyId'),('pitchId','pitchId'),('octave','octave'),('soundId','soundIdAtCapture'),('frequency','frequencyHz')]) and b.get('snapshotHash')==h,'vínculo não corresponde ao snapshot')

def audit_b(s,a):
    if a['B'] is None:return
    B=a['B'];require(a['status']=='consistent_provisional' and a.get('model')=='stiff_string' and s['sourceCondition']=='isolated' and s['acousticContext']['acousticModelId']=='stiff_string' and 0<B<=(.05 if s['instrument']=='Outro' else .02),'B consolidado incompatível');ids=a['includedExecutionIds'];es=a['executions'];require(3<=len(ids)<=64 and len(es)==len(ids),'execuções do B inválidas');unique(ids);unique([e['executionId'] for e in es]);require(set(ids)=={e['executionId'] for e in es},'referência de B inválida');raw={e['executionId']:e for e in s['executions']};funds=[]
    for e in es:
        r=raw[e['executionId']];F=e['FHz'];f=e['modelFundamentalHz'];require(r['eligible'] and r['includedInAggregate'] and r['result'] and pos(F) and pos(f) and abs(1200*math.log2(f/(F*math.sqrt(1+B))))<=.01,'escala de B inválida');funds.append(f);ps=e['partials'];require(4<=len(ps)<=24,'parciais B inválidos');orders=[];errors=[]
        for p in ps:
            n=p['order'];hz=p['measuredHz'];require(type(n) is int and 1<=n<=24 and n not in r.get('excludedPartialOrders',[]) and pos(hz) and pos(p['predictedHz']) and num(p['residualCents']),'parcial B inválido');orders.append(n);require(any(q['partialOrder']==n and q['status']=='accepted' and abs(1200*math.log2(q['measuredHz']/hz))<=.1 for q in r['result']['partials']),'B sem evidência');pred=n*F*math.sqrt(1+B*n*n);res=1200*math.log2(hz/pred);require(abs(1200*math.log2(p['predictedHz']/pred))<=.01 and abs(p['residualCents']-res)<=.01,'resíduo B divergente');errors.append(abs(res))
        unique(orders);require(max(orders)-min(orders)>=3 and statistics.median(errors)<=1.5001 and max(errors)<=6.0001,'resíduo B acima do limite')
    require(abs(1200*math.log2(max(funds)/min(funds)))<=45.0001,'ataques incompatíveis')

def session(s):
    shape(s,'session-map');ident(s['sessionId']);ident(s['createdAt']);fs=s['sampleRateHz'];require(8000<=fs<=192000,'taxa inválida');h=s['snapshotHash'];m=snapshot(s['musicalSnapshot']);require(semantic_hash(s['musicalSnapshot'])==h,'snapshotHash divergente');binding(s['binding'],m,h)
    c=s['acousticContext'];p=c['procedure'];fam=s['instrument'];cond=s['sourceCondition'];models=('automatic','exploratory','harmonic_series','stiff_string','modal_nonharmonic');require(fam in ('Cravo','Piano','Fortepiano','Outro') and c['schemaVersion']==2 and c['family']==fam and c['sourceCondition']==cond and c['physicalValidation']=='pending' and c['curveEligible'] is False,'contexto acústico inválido');require(type(p['exploratory']) is bool,'procedimento inválido');text(p['sourceLabel'],80);text(p['technique'],160);require(cond=='isolated' or p['sourceLabel']=='','fonte incompatível')
    if fam=='Outro':require(not p['exploratory'] and p['requestedModel'] in models and cond==('isolated' if p['requestedModel']=='stiff_string' else 'unknown'),'procedimento Outro inválido');model=p['requestedModel']
    else:require(p['requestedModel'] is None,'procedimento inválido');model='exploratory' if p['exploratory'] else 'stiff_string' if cond=='isolated' else 'harmonic_series'
    require(c['acousticModelId']==model,'modelo acústico inválido');neutral=model in ('exploratory','modal_nonharmonic');require(not neutral or s['binding']['noteBindingStatus']=='unresolved','atribuição incompatível');segments=[g['id'] for g in s['segments']];unique(segments);ids=[e['executionId'] for e in s['executions']];unique(ids)
    for e in s['executions']:
        ident(e['executionId']);require(e['segmentId'] in segments and type(e['ordinal']) is int and e['ordinal']>0 and (not e['includedInAggregate'] or e['eligible']),'execução inválida');binding(e['noteBindingAtCapture'],m,h);require(not neutral or e['noteBindingAtCapture']['noteBindingStatus']=='unresolved','atribuição incompatível');z=e['result']
        if z is None:continue
        require(z['sampleRateHz']==e['sampleRateHz']==fs,'taxa espectral incompatível');require(z['status'] in ('experimental','inconclusive'),'status espectral');b=z.get('inharmonicity');a=z.get('familyAnalysis');an=z.get('analysis20') or {};used=an.get('usedModel',model);require(not an or an.get('requestedModel')==model and (used==model or model in ('automatic','stiff_string','harmonic_series') and used in ('harmonic_series','exploratory')),'reanálise incompatível')
        if used=='stiff_string':require(not a,'modelo incompatível')
        else:require(not b and a and a['acousticModelId']==used and a['B'] is None and a['curveEligible'] is False and a['physicalValidation']=='pending','família incompatível')
        if neutral:require(z.get('fundamentalEstimateHz') is None and not z['partials'],'atribuição indevida')
        for x in z['partials']+z['candidates']:require(0<x['measuredHz']<=fs/2 and abs(x['amplitudeDbRelative'])<=1000,'pico fora da faixa')
        for x in z['spectrum']:require(0<=x[0]<=fs/2 and abs(x[1])<=1000,'bin fora da faixa')
        for x in z['partials']:require(pos(x['idealHarmonicHz']),'parcial inválido')
        if b:require(b.get('curveEligible') is not True and (b['B'] is None or 0<=b['B']<=(.05 if fam=='Outro' else .02)) and b['sourceContext']['instrument']==fam and b['sourceContext']['sourceCondition']==cond,'B individual incompatível')
        require(z.get('analysisSettings15')==s.get('analysisSettings15'),'configuração acústica diverge')
    a=s.get('aggregate')
    if a:
        require(model=='stiff_string' and a['sessionId']==s['sessionId'] and a['snapshotHash']==h and a['curveEligible'] is False,'consolidado incompatível');unique(a['includedExecutionIds']);require(set(a['includedExecutionIds'])<=set(ids),'execução inexistente');require(not a.get('validation') or a['validation']['physicalValidation']=='pending','validação externa não autorizada');audit_b(s,a)
    if 'B' in s:require(s['B']==(a['B'] if a else None),'B exportado divergente')
    for r in s.get('aggregationRevisions',[]):
        for refs in [r['requestedExecutionIds']]+([r['result']['includedExecutionIds']] if r.get('result') else []):unique(refs);require(set(refs)<=set(ids),'revisão sem execução')

def profile(p):
    shape(p,'profile-map');ident(p['profileId']);ident(p['displayName'],120);ident(p['createdAt']);text(p['instrumentSubtype'],120);text(p['notes'],2000);f=p['instrumentFamily'];m=p.get('acousticModelId');require((f in ('Piano','Cravo','Fortepiano') and m=='stiff_string') or (f=='Outro' and m in ('automatic','exploratory','harmonic_series','stiff_string','modal_nonharmonic')),'família do perfil inválida');unique([(t['keyId'],t['octave']) for t in p['instrumentLayout']['keys']])
def record(p,r,s):
    shape(r,'record-header-map');require(r['profileId']==p['profileId'] and p['instrumentFamily']==s['instrument'] and (s['instrument']!='Outro' or p['acousticModelId']==s['acousticContext']['acousticModelId']),'perfil da sessão incompatível');text(r['note'],2000);ident(r['recordedAt']);label=r['stringLabel'];text(label,80);require(label==label.strip() and (not s.get('stringLabel') or s['stringLabel']==label),'label divergente');b=s['binding'];k=next(({x:t[x] for x in ('keyId','pitchId','octave')} for t in p['instrumentLayout']['keys'] if b['noteBindingStatus']=='confirmed' and all(t[x]==b.get(x) for x in ('keyId','pitchId','octave'))),None);cond=s['sourceCondition'];string=compact([k['keyId'],k['octave'],cond,label]) if k and label else None;sh=semantic_hash(s);base=semantic_hash(semantic(s['musicalSnapshot']));a=s.get('aggregate') or {};obs='experimental' if a.get('B') is not None or any(e['eligible'] and ((e.get('result') or {}).get('familyAnalysis') or {}).get('status')=='experimental' or e['eligible'] and ((e.get('result') or {}).get('inharmonicity') or {}).get('status')=='compatible_provisional' for e in s['executions']) else 'inconclusive'
    for field,val in {'sessionHash':sh,'baseSnapshotHash':base,'physicalKey':k,'sourceCondition':cond,'stringId':string,'observationStatus':obs,'recordId':semantic_hash({'sessionHash':sh,'baseSnapshotHash':base,'stringId':string})}.items():require(r[field]==val,'integridade do registro: '+field)
    # Combined semantic tree budget (header + evidence), without concatenating a second CBOR object.
    tree_budget(dict(r,session=s))
def integrity(o):
    require(o['integrity']=={'algorithm':'SHA-256/JCS','sha256':semantic_hash({k:v for k,v in o.items() if k!='integrity'})},'integridade JCS divergente')
def revision(v):
    shape(v,'revision-map');integrity(v);c=v['curve'];require(c['curveId']==v['curveId'] and c['curveVersion']==v['versionNumber'] and (v['reviewStatus']!='approved_experimental' or c['status']=='preview'),'identidade/revisão inválida');snapshot(c['baseSnapshot']);require(c['baseSnapshotHash']==semantic_hash(semantic(c['baseSnapshot'])) and c['instrumentLayoutHash']==semantic_hash(c['physicalLayout']) and c['compatibilityHash']==semantic_hash({k:c[k] for k in ('baseSnapshotHash','instrumentLayoutHash')}),'hash da curva divergente');unique([x['recordId'] for x in v['sourceManifest']]);require(c['curveEligible'] is False and c['physicalValidation']=='pending','curva não autorizada');unique([(x['keyId'],x['octave']) for x in c['corrections']]);
    for x in c['corrections']:require(pos(x['frequencyHz']) and pos(x['proposedFrequencyHz']) and abs(x['deltaCents'])<=30,'correção inválida')
    require(near_tree(v['fundamentalAudit'],curve_audit(c)),'auditoria fundamental divergente')
def relations(vs):
    unique([v['versionId'] for v in vs]);by={v['versionId']:v for v in vs}
    for v in vs:
        if v['parentVersionId'] is None:require(v['parentHash'] is None and v['versionNumber']==1 and v['changeFromParent'] is None,'raiz histórica inválida')
        else:
            p=by.get(v['parentVersionId']);require(p and p['integrity']['sha256']==v['parentHash'] and p['curveId']==v['curveId'] and v['versionNumber']>p['versionNumber'],'ancestral ausente/incompatível')
            if 'curve' in p and 'curve' in v:require(near_tree(v['changeFromParent'],curve_diff(p['curve'],v['curve'])),'diff histórico divergente')

def validate_kind(k,o):
    if k==1:session(o)
    elif k==2:profile(o)
    elif k==3:shape(o,'record-header-map')
    elif k==4:revision(o)
    else:raise FormatError('manifesto precisa de contêiner')

# Port of AfinadorAuditoria4B.validate/fundamental/diff. The numerical comparison
# for recomputed transcendentals uses the original near tolerance instead of
# requiring byte-identical libm results. Actual stored hashes are checked exactly.
def key(t):return (t['keyId'],t['octave'])
def near(a,b):return num(a) and num(b) and abs(a-b)<=1e-7*max(1,abs(b))
def cents(x):return 1200*math.log2(x)
def near_tree(a,b):
    if type(a) is int and type(b) is int:return a==b
    if num(a) and num(b):return near(a,b)
    if type(a)!=type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(near_tree(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(near_tree(x,y) for x,y in zip(a,b))
    return a==b

def curve_audit(c):
    require(c['schema']=='afinador.tuning-curve' and c['schemaVersion']==1 and c['status'] in ('preview','incomplete'),'curva incompatível');m={key(t):t for t in c['baseSnapshot']['targets']};ks=c['physicalLayout']['keys'];ps=c['corrections'];require(0<len(ps)==len(ks)<=256,'mapa de correções inválido');idx={}
    for p,k in zip(ps,ks):
        t=m.get(key(p));require(t and key(k)==key(p) and p['pitchId']==k['pitchId']==t['pitchId'] and p['soundId']==t['soundId'] and key(p) not in idx and p['frequencyHz']==t['frequency'] and near(p['proposedFrequencyHz'],p['frequencyHz']*2**(p['deltaCents']/1200)),'ponto de curva inconsistente');idx[key(p)]=p
        if c['status']=='incomplete' or p['source']=='theoretical_fallback':require(p['deltaCents']==0,'nota sem correção deslocada')
    o=c['objective'];a=idx.get(key(o['anchorPolicy']));require(a and a['deltaCents']==0,'âncora alterada');require(o['priorityMode'] in ('fidelity','acoustic') and o['style'] in ('conservative','balanced','acoustic') and len(o['fundamentalIntervalConstraints'])<=32768 and len(c['intervalAudit']['pairs'])<=40000,'objetivo inválido')
    for r in o['fundamentalIntervalConstraints']:
        a,b=idx.get(key(r['lowerTarget'])),idx.get(key(r['upperTarget']));require(a and b and near(b['deltaCents']-a['deltaCents'],0) and r['satisfied'] is True and near(r['fundamentalIntervalShiftCents'],0),'restrição estrita violada')
    for r in c['intervalAudit']['pairs']:
        a,b=idx.get(key(r['lowerTarget'])),idx.get(key(r['upperTarget']));require(a and b and r['baseSnapshotHash']==c['baseSnapshotHash'] and pos(r['gLower']) and pos(r['gUpper']) and type(r['partialLower']) is int and type(r['partialUpper']) is int and r['partialLower']>0 and r['partialUpper']>0,'relação inválida')
        I=cents(b['frequencyHz']/a['frequencyHz']);t=cents(r['partialLower']/r['partialUpper'])-I;s0=cents(a['frequencyHz']*r['gLower']/(b['frequencyHz']*r['gUpper']));pa=a['proposedFrequencyHz']*r['gLower'];pb=b['proposedFrequencyHz']*r['gUpper'];s=cents(pa/pb);shift=b['deltaCents']-a['deltaCents'];goal=t if o['priorityMode']=='fidelity' else 0
        checks={'temperamentIntervalCents':I,'referencePartialDetuningCents':t,'targetDetuningCents':goal,'s0':s0,'predictedLowerPartialHz':pa,'predictedUpperPartialHz':pb,'predictedPartialDifferenceHz':abs(pa-pb),'predictedPartialDetuningCents':s,'residualCents':s-goal,'fundamentalIntervalShiftCents':shift,'finalFundamentalIntervalCents':I+shift};require(all(near(r.get(k),v) for k,v in checks.items()),'auditoria intervalar inconsistente')
    changed=[]
    for i in range(len(ps)):
        for j in range(i+1,len(ps)):
            a,b=(j,i) if ps[i]['frequencyHz']>ps[j]['frequencyHz'] else (i,j);shift=ps[b]['deltaCents']-ps[a]['deltaCents']
            if abs(shift)<=1e-8:continue
            I=cents(ps[b]['frequencyHz']/ps[a]['frequencyHz']);changed.append([a,b,I,I+shift,shift])
    return {'columns':['lowerIndex','upperIndex','temperamentCents','finalCents','shiftCents'],'totalPairs':len(ps)*(len(ps)-1)//2,'changedCount':len(changed),'changed':changed,'omittedPolicy':'abs(shift)<=1e-8 cents; derive every unchanged pair from corrections'}

def curve_diff(a,b):
    require(all(a[k]==b[k] for k in ('baseSnapshotHash','instrumentLayoutHash','profileId')) and len(a['corrections'])==len(b['corrections']),'base ancestral incompatível');bm={key(p):(i,p) for i,p in enumerate(b['corrections'])};points=[]
    for i,p in enumerate(a['corrections']):
        j,z=bm[key(p)];require(p['pitchId']==z['pitchId'] and p['frequencyHz']==z['frequencyHz'],'identidade ancestral incompatível');points.append(dict(i=i,j=j,label=p['label'],beforeHz=p['proposedFrequencyHz'],afterHz=z['proposedFrequencyHz'],beforeCents=p['deltaCents'],afterCents=z['deltaCents'],changeCents=z['deltaCents']-p['deltaCents']))
    def ak(r):return key(r['lowerTarget']),key(r['upperTarget']),r['partialLower'],r['partialUpper']
    old={ak(r):r for r in a['intervalAudit']['pairs']};added=0;partial=[]
    for r in b['intervalAudit']['pairs']:
        o=old.pop(ak(r),None)
        if o is None:added+=1;continue
        row={k:r[k] for k in ('lowerTarget','upperTarget','lowerLabel','upperLabel','partialLower','partialUpper')}
        for label,k in [('target','targetDetuningCents'),('detuning','predictedPartialDetuningCents'),('residual','residualCents'),('differenceHz','predictedPartialDifferenceHz'),('fundamentalShift','fundamentalIntervalShiftCents')]:row[label+'Before']=o[k];row[label+'After']=r[k]
        partial.append(row)
    changes=[abs(p['changeCents']) for p in points if abs(p['changeCents'])>1e-8];return {'points':points,'changedCount':len(changes),'maxChangeCents':max(changes,default=0),'rmsChangeCents':math.sqrt(sum(p['changeCents']**2 for p in points)/len(points)),'partial':partial,'addedCriteria':added,'removedCriteria':len(old)}


def tree_budget(o):
    count=0
    def walk(v,d):
        nonlocal count
        count+=1;require(count<=MAX_NODES and d<=60,'orçamento da árvore combinada')
        if type(v) is dict:
            require(len(v)<=4096,'mapa excessivo')
            for k,x in v.items():textcheck(k,True);walk(x,d+1)
        elif type(v) is list:
            require(len(v)<=200000,'array excessivo')
            for x in v:walk(x,d+1)
        elif type(v) is str:textcheck(v)
        elif v is not None and type(v) is not bool:numbercheck(v)
    walk(o,0)
