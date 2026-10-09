import itertools, json, datetime as D
from bt import *
SPLIT=int(D.datetime(2026,9,21,tzinfo=UTC).timestamp())
data={nm:load(nm) for nm in INST}
def ev(**kw):
    out={}
    for nm in INST:
        tr=run(data[nm],nm,**kw)
        out[nm]=(stats([t for t in tr if t['t']<SPLIT]),stats([t for t in tr if t['t']>=SPLIT]),stats(tr),tr)
    return out
def row(label,o):
    tot=[o[n][2] for n in INST]
    N=sum(s['n'] for s in tot);R=sum(s['tot'] for s in tot)
    isr=sum(o[n][0]['tot'] for n in INST);isn=sum(o[n][0]['n'] for n in INST)
    osr=sum(o[n][1]['tot'] for n in INST);osn=sum(o[n][1]['n'] for n in INST)
    return (label,N,R,R/N if N else 0,isn,isr/isn if isn else 0,osn,osr/osn if osn else 0,[round(o[n][2]['avg'],2) for n in INST],[o[n][2]['n'] for n in INST])
if __name__=='__main__':
    rows=[]
    kz={'none':None,'ldn':[(420,600)],'ny':[(750,960)],'ldn+ny':[(420,600),(750,960)]}
    for setup in ['reclaim','continuation']:
      for bias in ['auto','any','htf_with','htf_against','auto_htf']:
        for entry in (['market','limit50','limitopen'] if setup=='reclaim' else ['market']):
          for buf,rmax in [(0.75,2.5),(1.0,3.0),(1.5,4.0),(2.0,5.0)]:
            for kzn,kzv in kz.items():
                o=ev(setup=setup,bias=bias,entry=entry,buf=buf,risk_max=rmax,kz=kzv)
                rows.append(row(f'{setup}|{bias}|{entry}|buf{buf}|{kzn}',o))
    json.dump(rows,open('grid_out.json','w'))
    rows.sort(key=lambda r:-r[3])
    print('label N totR avgR | IS n avg | OOS n avg | avg per inst | n per inst')
    for r in rows[:25]: print(r[0],r[1],round(r[2],1),round(r[3],3),'|',r[4],round(r[5],3),'|',r[6],round(r[7],3),'|',r[8],r[9])
    print('... worst')
    for r in rows[-5:]: print(r[0],r[1],round(r[2],1),round(r[3],3))
    print('positive IS & OOS:',[ (r[0],r[1],round(r[5],2),round(r[7],2)) for r in rows if r[5]>0.05 and r[7]>0.05 and r[4]>=15 and r[6]>=8][:15])
