import json,re,csv,collections

M=json.load(open('edge_msgs.json'))

MONTH={'січня':'01','лютого':'02','березня':'03','квітня':'04','травня':'05','червня':'06',
'липня':'07','серпня':'08','вересня':'09','жовтня':'10','листопада':'11','грудня':'12'}
def iso(dt):
    if not dt: return ''
    m=re.match(r'(\d+)\s+([а-яіїєґ]+)\s+(\d{4})(?:,\s*(\d{2}:\d{2}))?',dt)
    if not m: return dt
    d,mo,y,tm=m.groups()
    return f"{y}-{MONTH.get(mo,'??')}-{int(d):02d}"+(f" {tm}" if tm else "")
def tm(dt):
    m=re.search(r'(\d{2}:\d{2}):\d{2}',dt or '')
    return m.group(1) if m else ''

PAIRS=[('EURUSD',r'(?i)\bEURUSD\b|\bEU\b|\bевро\b|\bEUR\b|\bевр[оы]\b'),
('GBPUSD',r'(?i)\bGBPUSD\b|\bGU\b|фунт|\bGBP\b'),
('XAUUSD',r'(?i)\bXAUUSD\b|\bXAU\b|золот|\bGOLD\b'),
('XAGUSD',r'(?i)\bXAGUSD\b|\bXAG\b|серебр'),
('USDJPY',r'(?i)\bUSDJPY\b|\bUJ\b|\bJPY\b|\bиен'),
('USOIL',r'(?i)\bUSOIL\b|\bWTI\b|нефт'),
('NZDUSD',r'(?i)\bNZDUSD\b|\bNZD\b'),('AUDUSD',r'(?i)\bAUDUSD\b|\bAUD\b'),
('USDCAD',r'(?i)\bUSDCAD\b|\bCAD\b'),('EURGBP',r'(?i)\bEURGBP\b'),
('DXY',r'(?i)\bDXY\b'),('BTCUSD',r'(?i)\bBTC\b|биткоин'),
('NQ',r'(?i)\bNQ\b|\bUS100\b|\bNAS100\b'),('SPX',r'(?i)\bSPX\b|\bUS500\b'),
('AAPL',r'(?i)\bAAPL\b'),('NVDA',r'(?i)\bNVDA\b')]

R_RE=re.compile(r'([+\-]?\d+(?:[.,]\d+)?)\s*R\b')
PCT_RE=re.compile(r'([+\-]\d+(?:[.,]\d+)?)\s*%')

MODELS=[('IDM',r'(?i)\bIDM\b|Inducement|Induced RTO'),('VC',r'(?i)\bVC\b|Volume Confirmation'),
('Market',r'(?i)\bmarket entry\b|по рынку|маркет'),('FVG',r'(?i)\bFVG\b|\bIMB\b|имбаланс'),
('SNR',r'(?i)\bSNR\b'),('RB',r'(?i)\bRB\b|Rejection Block'),('OB',r'(?i)\bOB\b|Order Block'),
('Breaker',r'(?i)\bBZ\b|Breaker'),('Position Adding',r'(?i)Position Adding|добор|доливк|перезаход'),
('Mean Reversion',r'(?i)Mean Reversion'),('Swing',r'(?i)\bswing\b|свинг')]
SESS=['LOKZ','NYKZ','LCKZ','NYM','LOM','Asia']
TFS=['1M','W1','D1','H12','H4','H1','M15','m15','M5','m5','M2']

def cat_of(t,m):
    if not t and not m['files']: return None
    if re.search(r'(?i)trade analysis|trade breakdown|breakdown \+|daily breakdown|разбор позици|детальн\w+ анализ позици',t): return 'TRADE_ANALYSIS'
    if R_RE.search(t) and re.search(r'(?i)позици|\btrade\b|сделк|план отработал|закрыт|following the plan',t): return 'TRADE_RESULT'
    if re.search(r'(?i)итоги|закрываю .*месяц|месяц закрыт|performance|закрыт в \+|результат\w* (месяц|квартал|год)',t): return 'PERIOD_RESULT'
    if re.search(r'(?i)trade idea|торгов\w+ иде|идея позици|рассматриваю',t): return 'TRADE_IDEA'
    if re.search(r'(?i)pre-session|trading plan|торговый план|план &|план на (сегодня|неделю|день)',t): return 'PLAN'
    if re.search(r'(?i)post-session|weekly review|daily report|monthly review',t): return 'REVIEW'
    if re.search(r'(?i)market note|заметк[аи]|note:',t): return 'NOTE'
    if re.search(r'(?i)analysis|анализ|нарратив|narrative',t) and any(re.search(p,t) for _,p in PAIRS): return 'ANALYSIS'
    if any(re.search(p,t) for _,p in PAIRS) and (m['tv'] or m['photos'] or m['files']): return 'CHART'
    return None

rows=[]
for m in M:
    t=(m['text'] or '')
    fnames=' '.join(m['files'])
    blob=t+' '+fnames
    c=cat_of(t,m)
    if not c: continue
    pairs=[n for n,p in PAIRS if re.search(p,blob)]
    # R from text and from filenames like "Trade 1 (GBP +3).png"
    Rs=R_RE.findall(t)
    fR=re.findall(r'\(([A-Z]{3,6})\s*([+\-]\d+(?:[.,]\d+)?)\)',fnames)
    rows.append(dict(
        date=iso(m['dt']).split(' ')[0], time=tm(m['dt']), msg=m['id'], cat=c,
        pairs='|'.join(pairs),
        direction='Long' if re.search(r'(?i)\bлонг|\blong\b|покупк|\bbuy\b',t) else ('Short' if re.search(r'(?i)\bшорт|\bshort\b|продаж|\bsell\b',t) else ''),
        R='|'.join(Rs) if Rs else '|'.join(f'{a} {b}' for a,b in fR),
        pct='|'.join(PCT_RE.findall(t)),
        models='|'.join(n for n,p in MODELS if re.search(p,blob)),
        session='|'.join(x for x in SESS if re.search(r'(?i)\b'+x+r'\b',t)),
        tfs='|'.join(x for x in dict.fromkeys(TFS) if re.search(r'\b'+x+r'\b',t)),
        charts=len(m['tv']), tv='|'.join(m['tv']),
        yt='|'.join(m['yt']), files='|'.join(f.split('/')[-1] for f in m['files']),
        photos=len(m['photos']),
        text=re.sub(r'\s+',' ',t)[:600],
    ))

rows.sort(key=lambda r:(r['date'],r['time']))
cols=list(rows[0].keys())
with open('edge_trades.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,cols); w.writeheader(); w.writerows(rows)

print('ROWS',len(rows))
print(collections.Counter(r['cat'] for r in rows))
print('by year',collections.Counter(r['date'][:4] for r in rows))
pc=collections.Counter()
for r in rows:
    for p in filter(None,r['pairs'].split('|')): pc[p]+=1
print('pairs',pc.most_common())
