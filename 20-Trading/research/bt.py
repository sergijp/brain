"""Незалежний бектест методу «зняття пулу → реклейм» (M5). Дзеркало логіки індикатора «тестовий мій» + варіанти.
Дані: JSON [[t,o,h,l,c],…] з TradingView (M5). Запуск: див. grid.py"""
import json, datetime as D, math
UTC = D.UTC
INST = {
 'EURUSD': dict(pip=1e-4, sw=0.3, clus=1.0, entry_max_pips=15.0, entry_max_atr=None, min_stop_pips=2.0, asia_min=15.0, asia_min_atr=None, tol_map=20.0, spread=0.6),
 'GBPUSD': dict(pip=1e-4, sw=0.3, clus=1.0, entry_max_pips=15.0, entry_max_atr=None, min_stop_pips=2.0, asia_min=15.0, asia_min_atr=None, tol_map=20.0, spread=0.9),
 'GER40':  dict(pip=1.0,  sw=1.0, clus=3.0, entry_max_pips=None, entry_max_atr=2.7, min_stop_pips=0.0, asia_min=None, asia_min_atr=2.5, tol_map=60.0, spread=1.5),
}
DEF = dict(buf=0.75, risk_min=0.8, risk_max=2.5, rr_min=2.25, body=0.3, bias='auto', sess=(350,1140), entry='market',
           setup='reclaim', day_limit=-3.0, cost=True, pend_bars=6, htf_mode=None, htf_n=3, max_age=3, kz=None)

def ts(t): return D.datetime.fromtimestamp(t, UTC)

class Lv: pass

def run(bars, name, **kw):
    P = dict(DEF); P.update(kw); I = INST[name]; pip = I['pip']
    n = len(bars); T=[b[0] for b in bars];O=[b[1] for b in bars];H=[b[2] for b in bars];L=[b[3] for b in bars];C=[b[4] for b in bars]
    SW=I['sw']*pip; CL=I['clus']*pip
    tr=[0]*n; atr=[None]*n
    for i in range(n): tr[i]=H[i]-L[i] if i==0 else max(H[i]-L[i],abs(H[i]-C[i-1]),abs(L[i]-C[i-1]))
    for i in range(23,n): atr[i]=sum(tr[:24])/24 if i==23 else (atr[i-1]*23+tr[i])/24
    h1={}
    for i in range(n):
        k=T[i]//3600
        if k not in h1: h1[k]=[H[i],L[i]]
        else: h1[k][0]=max(h1[k][0],H[i]); h1[k][1]=min(h1[k][1],L[i])
    ks=sorted(h1); piv_hi={};piv_lo={}
    for j in range(2,len(ks)-2):
        if not all(ks[j+d+1]-ks[j+d]==1 for d in (-2,-1,0,1)): continue
        hh=[h1[ks[j+d]][0] for d in (-2,-1,0,1,2)]; ll=[h1[ks[j+d]][1] for d in (-2,-1,0,1,2)]
        if hh[2]>max(hh[0],hh[1],hh[3],hh[4]): piv_hi.setdefault(ks[j]+3,[]).append(hh[2])
        if ll[2]<min(ll[0],ll[1],ll[3],ll[4]): piv_lo.setdefault(ks[j]+3,[]).append(ll[2])
    # денні закриття для HTF-біасу (UTC-день)
    dclose={};dopen={}
    for i in range(n):
        d=ts(T[i]).date()
        if d not in dopen: dopen[d]=O[i]
        dclose[d]=C[i]
    dkeys=sorted(dclose)
    lv=[]
    def add(price,isH,tag,bi):
        for l in lv:
            if not l.swept and l.isH==isH and abs(l.p-price)<=CL:
                l.n+=1;l.lo=min(l.lo,price);l.hi=max(l.hi,price);l.p=(l.lo+l.hi)/2;return
        l=Lv();l.p=l.lo=l.hi=price;l.isH=isH;l.n=1;l.swept=False;l.done=False;l.born=bi;l.sb=None;l.ext=None;l.tag=tag;l.acc=None;lv.append(l)
        if len(lv)>70: lv.pop(0)
    dayH=dayL=None;asC=None;asH=asL=asHt=asLt=None;biasAuto=0;dayR=0.0
    tOn=False;cur=None;pend=None;trades=[]
    inA=lambda i:(ts(T[i]).hour>=22 or ts(T[i]).hour<6)
    htf=0
    for i in range(n):
        dt=ts(T[i]);mod=dt.hour*60+dt.minute
        newDay = i==0 or ts(T[i-1]).date()!=dt.date()
        inSess=P['sess'][0]<=mod<P['sess'][1]
        if P['kz'] is not None: inSess = inSess and any(a<=mod<b for a,b in P['kz'])
        if newDay or dayH is None:
            if dayH is not None:
                add(dayH,True,'PDH',i); add(dayL,False,'PDL',i)
            dayH,dayL=H[i],L[i]; dayR=0.0
            # HTF: тренд за 3 завершені дні
            d=dt.date(); idx=dkeys.index(d)
            if idx>=P['htf_n']+1:
                htf = 1 if dclose[dkeys[idx-1]]>dclose[dkeys[idx-1-P['htf_n']]] else -1
            else: htf=0
        ia=inA(i);ia1=inA(i-1) if i>0 else False
        if ia and not ia1: asC=[H[i],L[i],T[i],T[i]]
        elif ia and asC:
            if H[i]>asC[0]: asC[0]=H[i];asC[2]=T[i]
            if L[i]<asC[1]: asC[1]=L[i];asC[3]=T[i]
        if (not ia) and ia1 and asC:
            asH,asL,asHt,asLt=asC[0],asC[1],asC[2],asC[3]
            add(asH,True,'ASIA H',i);add(asL,False,'ASIA L',i)
            a=atr[i]
            minR = I['asia_min']*pip if I['asia_min'] else (I['asia_min_atr']*a if a else 1e9)
            tol=I['tol_map']*pip if pip<1 else I['tol_map']
            hiAt=loAt=False
            for l in lv:
                if l.tag not in('ASIA H','ASIA L'):
                    if l.isH and abs(asH-l.p)<=tol: hiAt=True
                    if (not l.isH) and abs(asL-l.p)<=tol: loAt=True
            hiOk=hiAt and asHt>asLt and (asH-asL)>=minR; loOk=loAt and asLt>asHt and (asH-asL)>=minR
            biasAuto=-1 if (hiOk and not loOk) else 1 if (loOk and not hiOk) else 0
        k=T[i]//3600
        if i==0 or T[i-1]//3600!=k:
            for p in piv_hi.get(k,[]): add(p,True,'H1',i)
            for p in piv_lo.get(k,[]): add(p,False,'H1',i)
        a=atr[i]
        bm=P['bias']
        if bm=='auto': bias=biasAuto; known=bias!=0
        elif bm=='any': bias=0; known=True
        elif bm=='htf_with': bias=htf; known=htf!=0
        elif bm=='htf_against': bias=-htf; known=htf!=0
        elif bm=='auto_htf': bias=biasAuto; known=bias!=0 and bias==htf
        elif bm=='auto_vs_htf': bias=biasAuto; known=bias!=0 and bias==-htf
        else: raise ValueError(bm)
        canTrade=(not tOn) and pend is None and inSess and dayR>P['day_limit'] and known and a is not None
        # --- pending fill
        if pend is not None and not tOn:
            p=pend; s=p['side']
            tp_touched = (L[i]<=p['tp']) if s==-1 else (H[i]>=p['tp'])
            fill = (H[i]>=p['entry']) if s==-1 else (L[i]<=p['entry'])
            if i>p['i'] and fill and not tp_touched:
                tOn=True;cur=dict(p);cur['i']=i-1;cur['t']=T[i];pend=None   # i-1: перевірка стопу/цілі вже на барі заповнення (стоп першим)
            elif i>p['i'] and (tp_touched or i>=p['exp'] or not inSess):
                pend=None
        def make_setup(l,side,entry,ext,bar_i):
            buf=max(P['buf']*a,I['min_stop_pips']*pip)
            sl=ext+buf if side==-1 else ext-buf
            bd=1e9;edge=None
            for q in lv:
                if not q.swept and q.isH==(side==-1):
                    if side==-1 and q.lo>entry and q.lo-entry<bd: bd=q.lo-entry;edge=q.hi
                    if side==1 and q.hi<entry and entry-q.hi<bd: bd=entry-q.hi;edge=q.lo
            if edge is not None: sl=max(sl,edge+0.5*pip) if side==-1 else min(sl,edge-0.5*pip)
            risk=abs(sl-entry)
            if not (P['risk_min']*a<=risk<=P['risk_max']*a and risk>=I['min_stop_pips']*pip): return None
            bt=1e9;tp=None
            for q in lv:
                if not q.swept and q.isH==(side==1):
                    px=q.hi if side==-1 else q.lo
                    dist=entry-px if side==-1 else px-entry
                    if dist>0 and dist/risk>=P['rr_min'] and dist<bt: bt=dist;tp=px
            if tp is None: return None
            return dict(side=side,entry=entry,sl=sl,tp=tp,i=bar_i,t=T[bar_i],risk=risk,rr=abs(tp-entry)/risk,tag=l.tag,hour=ts(T[bar_i]).hour,exp=bar_i+P['pend_bars'])
        entered=False
        for l in list(lv):
            if not l.swept:
                if l.isH and H[i]>l.hi+SW: l.swept=True;l.sb=i;l.ext=H[i]
                if (not l.isH) and L[i]<l.lo-SW: l.swept=True;l.sb=i;l.ext=L[i]
            if l.swept and not l.done:
                l.ext=max(l.ext,H[i]) if l.isH else min(l.ext,L[i])
                if P['setup']=='reclaim':
                    cb = (C[i]<l.lo and (i==l.sb or C[i-1]>=l.lo)) if l.isH else (C[i]>l.hi and (i==l.sb or C[i-1]<=l.hi))
                    body = a is not None and ((C[i]<O[i] and (O[i]-C[i])>=P['body']*a) if l.isH else (C[i]>O[i] and (C[i]-O[i])>=P['body']*a))
                    if cb:
                        l.done=True
                        side=-1 if l.isH else 1
                        if body and canTrade and not entered and (i-l.born)>=3 and (bias==0 or bias==side):
                            maxd = I['entry_max_pips']*pip if I['entry_max_pips'] else I['entry_max_atr']*a
                            if abs(C[i]-l.ext)<=maxd:
                                if P['entry']=='market': entry=C[i]
                                elif P['entry']=='limit50': entry=(C[i]+ (H[i] if side==-1 else L[i]))/2 if False else (O[i]+C[i])/2
                                elif P['entry']=='limitopen': entry=O[i]
                                su=make_setup(l,side,entry,l.ext,i)
                                if su:
                                    su['sweepbar']=l.sb
                                    if P['entry']=='market': tOn=True;cur=su
                                    else: pend=su
                                    entered=True
                    elif i-l.sb>=P['max_age']: l.done=True
                else:  # continuation: прийняття за рівнем + ретест
                    # прийняття: закриття за межею рівня у бік зняття
                    if l.acc is None:
                        if (C[i]>l.hi+SW) if l.isH else (C[i]<l.lo-SW): l.acc=i
                        elif i-l.sb>=P['max_age']: l.done=True
                    else:
                        side=1 if l.isH else -1
                        hold = (L[i]<=l.hi+SW and C[i]>l.hi) if l.isH else (H[i]>=l.lo-SW and C[i]<l.lo)
                        body = a is not None and ((C[i]>O[i] and (C[i]-O[i])>=P['body']*a) if l.isH else (C[i]<O[i] and (O[i]-C[i])>=P['body']*a))
                        if i>l.acc and hold and body:
                            l.done=True
                            if canTrade and not entered and (bias==0 or bias==side):
                                ext = L[i] if side==1 else H[i]
                                su=make_setup(l,side,C[i],ext,i)
                                if su: su['sweepbar']=l.sb;tOn=True;cur=su;entered=True
                        elif i-l.acc>=6: l.done=True
        if tOn and i>cur['i']:
            s=cur['side']
            hitSl = H[i]>=cur['sl'] if s==-1 else L[i]<=cur['sl']
            hitTp = L[i]<=cur['tp'] if s==-1 else H[i]>=cur['tp']
            ex=None;why=''
            if hitSl: ex=cur['sl'];why='СТОП'
            elif hitTp: ex=cur['tp'];why='ЦІЛЬ'
            elif mod>=P['sess'][1]-5: ex=C[i];why='ЧАС'
            if ex is not None:
                r=s*(ex-cur['entry'])/cur['risk']
                if P['cost']: r-= I['spread']*pip/cur['risk']
                dayR+=r;cur.update(ex=ex,r=r,why=why,xt=T[i]);trades.append(cur);tOn=False
        if H[i]>dayH: dayH=H[i]; add(dayH,True,'DAY',i)
        if L[i]<dayL: dayL=L[i]; add(dayL,False,'DAY',i)
        lv[:]=[l for l in lv if not (l.tag=='DAY' and l.swept and l.done)]
    return trades

def stats(tr):
    if not tr: return dict(n=0,wr=0,avg=0,tot=0,pf=0,dd=0,tp=0)
    rs=[t['r'] for t in tr]; w=[r for r in rs if r>0]; l=[-r for r in rs if r<=0]
    eq=0;pk=0;dd=0
    for r in rs: eq+=r;pk=max(pk,eq);dd=max(dd,pk-eq)
    return dict(n=len(rs),wr=len(w)/len(rs),avg=sum(rs)/len(rs),tot=sum(rs),pf=(sum(w)/sum(l)) if l and sum(l)>0 else 99,dd=dd,tp=sum(1 for t in tr if t['why']=='ЦІЛЬ'))
def load(name):
    f={'EURUSD':'/tmp/bars_eur_long.json','GBPUSD':'/tmp/bars_OANDA_GBPUSD.json','GER40':'/tmp/bars_FOREXCOM_GER40.json'}[name]
    return json.load(open(f))
