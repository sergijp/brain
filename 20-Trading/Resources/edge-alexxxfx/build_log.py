import json,re,csv,collections

M=json.load(open('edge_msgs.json'))
MONTH={'січня':'01','лютого':'02','березня':'03','квітня':'04','травня':'05','червня':'06',
'липня':'07','серпня':'08','вересня':'09','жовтня':'10','листопада':'11','грудня':'12'}
def iso(dt):
    m=re.match(r'(\d+)\s+([а-яіїєґ]+)\s+(\d{4})',dt or '')
    return f"{m.group(3)}-{MONTH.get(m.group(2),'??')}-{int(m.group(1)):02d}" if m else ''
def hhmm(dt):
    m=re.search(r'(\d{2}:\d{2}):\d{2}',dt or ''); return m.group(1) if m else ''

PAIRS=[('EURUSD',r'(?i)\bEURUSD\b|\bEU\b|\bевро\b|\bEUR\b'),('GBPUSD',r'(?i)\bGBPUSD\b|\bGU\b|фунт|\bGBP\b'),
('XAUUSD',r'(?i)\bXAUUSD\b|\bXAU\b|золот|\bGOLD\b'),('XAGUSD',r'(?i)\bXAGUSD\b|\bXAG\b|серебр'),
('USDJPY',r'(?i)\bUSDJPY\b|\bUJ\b|\bJPY\b|\bиен'),('USOIL',r'(?i)\bUSOIL\b|\bWTI\b|нефт'),
('NZDUSD',r'(?i)\bNZD\b'),('AUDUSD',r'(?i)\bAUD\b'),('USDCAD',r'(?i)\bCAD\b'),('EURGBP',r'(?i)\bEURGBP\b'),
('DXY',r'(?i)\bDXY\b'),('BTCUSD',r'(?i)\bBTC\b|биткоин'),('NQ',r'(?i)\bNQ\b|\bUS100\b|\bNAS100\b'),
('AAPL',r'(?i)\bAAPL\b'),('NVDA',r'(?i)\bNVDA\b')]
MODELS=[('IDM',r'(?i)\bIDM\b|Inducement|Induced RTO'),('VC',r'(?i)\bVC\b|Volume Confirmation'),
('Market',r'(?i)market entry|по рынку'),('FVG',r'(?i)\bFVG\b|\bIMB\b|имбаланс'),('SNR',r'(?i)\bSNR\b'),
('RB',r'(?i)\bRB\b|Rejection Block'),('OB',r'(?i)\bOB\b'),('Breaker',r'(?i)\bBZ\b|Breaker'),
('PosAdding',r'(?i)Position Adding|добор|доливк|перезаход'),('MeanRev',r'(?i)Mean Reversion'),
('Swing',r'(?i)\bswing\b|свинг'),('Shift',r'(?i)\bshift\b|смещени')]
SESS=['LOKZ','NYKZ','LCKZ','NYM','LOM']
TFS=['1M','W1','D1','H12','H4','H1','M15','m15','M5','m5']
R_RE=re.compile(r'([+\-]?\d+(?:[.,]\d+)?)\s*R\b')
PCT_RE=re.compile(r'([+\-]?\d+(?:[.,]\d+)?)\s*%')
CHAIN=re.compile(r'X[+\-]?\d?\s*TF[^\n.]{0,160}')
PERF=re.compile(r'(?i)#statistics|#tradewithedge|закрыва\w* (лучший )?(месяц|квартал|год)|итоги (января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря|месяца|квартала|года)|WR\s*\d+|Winrate|квартальная прибыль|годовой результат|месяц закрыт|закрыт в [+\-]')

def cat_of(t,m):
    if PERF.search(t) and (PCT_RE.search(t) or R_RE.search(t)): return 'PERFORMANCE'
    if re.search(r'(?i)trade analysis|breakdown|разбор позици|детальн\w+ анализ позици',t): return 'TRADE_ANALYSIS'
    if R_RE.search(t) and re.search(r'(?i)позици|\btrade\b|сделк|план отработал|закрыт|following the plan',t): return 'TRADE_RESULT'
    if re.search(r'(?i)trade idea|торгов\w+ иде|идея позици|рассматриваю|планирую открыть',t): return 'TRADE_IDEA'
    if re.search(r'(?i)pre-session|trading plan|торговый план|план &|план на ',t): return 'PLAN'
    if re.search(r'(?i)post-session|weekly review|daily report|monthly review|bias vs price',t): return 'REVIEW'
    if re.search(r'(?i)market note|заметк[аи]|note:',t): return 'NOTE'
    if re.search(r'(?i)analysis|анализ|narrative|нарратив',t) and any(re.search(p,t) for _,p in PAIRS): return 'ANALYSIS'
    if any(re.search(p,t) for _,p in PAIRS) and (m['tv'] or m['photos'] or m['files']): return 'CHART'
    return None

rows=[]
for m in M:
    t=(m['text'] or ''); fn=' '.join(m['files']); blob=t+' '+fn
    c=cat_of(t,m)
    if not c: continue
    fR=re.findall(r'\(([A-Z]{3,6})\s*([+\-]\d+(?:[.,]\d+)?)\)',fn)
    rows.append(dict(
        date=iso(m['dt']), time=hhmm(m['dt']), msg=m['id'], cat=c,
        pairs='|'.join(n for n,p in PAIRS if re.search(p,blob)),
        dir='Long' if re.search(r'(?i)\bлонг|\blong\b|покупк|\bbuy\b',t) else ('Short' if re.search(r'(?i)\bшорт|\bshort\b|продаж|\bsell\b',t) else ''),
        R='|'.join(R_RE.findall(t)) or '|'.join(f'{a}{b}R' for a,b in fR),
        pct='|'.join(PCT_RE.findall(t)) if c=='PERFORMANCE' else '',
        models='|'.join(n for n,p in MODELS if re.search(p,blob)),
        session='|'.join(x for x in SESS if re.search(r'(?i)\b'+x+r'\b',t)),
        tfs='|'.join(dict.fromkeys(x.upper() for x in TFS if re.search(r'\b'+x+r'\b',t))),
        chain=' ;; '.join(x.strip() for x in CHAIN.findall(t)[:3]),
        charts=len(m['tv']), photos=len(m['photos']),
        tv='|'.join(m['tv']), yt='|'.join(m['yt']),
        files='|'.join(f.split('/')[-1] for f in m['files']),
        text=re.sub(r'\s+',' ',t)[:800],
    ))
rows.sort(key=lambda r:(r['date'],r['time']))
with open('edge_trade_log.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print('ROWS',len(rows)); print(collections.Counter(r['cat'] for r in rows))
print('by year',sorted(collections.Counter(r['date'][:4] for r in rows).items()))
print('with R',sum(1 for r in rows if r['R']),'with chain',sum(1 for r in rows if r['chain']))
pc=collections.Counter()
for r in rows:
    for p in filter(None,r['pairs'].split('|')): pc[p]+=1
print('pairs',pc.most_common(10))
mc=collections.Counter()
for r in rows:
    for p in filter(None,r['models'].split('|')): mc[p]+=1
print('models',mc.most_common())
