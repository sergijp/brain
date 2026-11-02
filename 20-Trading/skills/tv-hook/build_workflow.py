import json,os,sys
secrets=dict(l.strip().split('=',1) for l in open(os.path.expanduser('~/tv-hook/secrets.env')) if '=' in l)
PATH='tv-'+secrets['PATH_SECRET']
code = r'''
let b = $input.first().json.body;
if (typeof b === 'string') { try { b = JSON.parse(b); } catch (e) { return [{ json: { skip: true, reason: 'bad json' } }]; } }
if (!b || b.k !== $env.HOOK_SECRET) { return [{ json: { skip: true, reason: 'bad secret' } }]; }
const esc = s => String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const sgn = v => (Number(v) >= 0 ? '+' : '') + Number(v).toFixed(2);
let text = '';
const isTest = b.test === true || b.test === 'true';
if (b.ev === 'fill') {
  text = `🟢 <b>${esc(b.sym)} ${esc(b.side)} ${esc(b.entry)}</b>\nSL ${esc(b.sl)} · TP ${esc(b.tp)} · RR ${esc(b.rr)}\nРизик ${esc(b.risk)} · ${esc(b.lot)} лот ($${esc(b.usd)})\n<b>Сетап:</b> ${esc(b.setup)}\n<b>Біас:</b> ${esc(b.bias)}\n<b>Чому:</b> ${esc(b.why)}\n${esc(b.t)} UTC`;
} else if (b.ev === 'exit') {
  const icon = b.res === 'ЦІЛЬ' ? '🎯' : (String(b.res).indexOf('ЗАХИСТ') >= 0 ? '🛡' : (b.res === 'СТОП' ? '🔴' : '⏱'));
  text = `${icon} <b>${esc(b.sym)} ${esc(b.res)} ${esc(b.exit)} · ${sgn(b.r)}R</b>\nВхід ${esc(b.side)} ${esc(b.entry)} → вихід ${esc(b.exit)}\nРахунок дня: ${sgn(b.day)}R\n${esc(b.t)} UTC`;
} else if (b.ev === 'move') {
  text = `🛡 <b>${esc(b.sym)} ${esc(b.side)}: стоп перенесено</b>\nЗмінилась структура проти позиції (Shift). Вхід ${esc(b.entry)}\nСтоп ${esc(b.oldsl)} → <b>${esc(b.newsl)}</b> · пройдено до ${esc(b.mfe)}R\nРахунок дня: ${sgn(b.day)}R\n${esc(b.t)} UTC`;
} else if (b.ev === 'test') {
  text = `✅ <b>Тест вебхука TradingView → n8n → Telegram</b>\n${esc(b.msg || '')}`;
} else {
  return [{ json: { skip: true, reason: 'unknown event' } }];
}
if (isTest) text = '🧪 <b>ТЕСТ (не реальна подія)</b>\n' + text;
return [{ json: { skip: false, text, p: b } }];
'''
wf = {
 "name":"TradingView → Telegram (owner method)",
 "nodes":[
  {"parameters":{"httpMethod":"POST","path":PATH,"responseMode":"onReceived","options":{"rawBody":False}},
   "id":"n1","name":"Webhook","type":"n8n-nodes-base.webhook","typeVersion":2,"position":[0,0],"webhookId":"tv-owner-method"},
  {"parameters":{"jsCode":code},"id":"n2","name":"Format","type":"n8n-nodes-base.code","typeVersion":2,"position":[260,0]},
  {"parameters":{"conditions":{"options":{"caseSensitive":True,"leftValue":"","typeValidation":"strict"},"conditions":[{"id":"c1","leftValue":"={{ $json.skip }}","rightValue":False,"operator":{"type":"boolean","operation":"false","singleValue":True}}],"combinator":"and"},"options":{}},
   "id":"n3","name":"Send?","type":"n8n-nodes-base.if","typeVersion":2.2,"position":[520,0]},
  {"parameters":{"method":"POST","url":"http://127.0.0.1:5681/notify","sendBody":True,"specifyBody":"json","jsonBody":"={{ JSON.stringify({text: $json.text, p: $json.p}) }}","options":{"timeout":60000}},
   "id":"n5","name":"Screenshot","type":"n8n-nodes-base.httpRequest","typeVersion":4.2,"position":[780,-100],"onError":"continueErrorOutput"},
  {"parameters":{"method":"POST","url":"=https://api.telegram.org/bot{{ $env.TG_TOKEN }}/sendMessage","sendBody":True,"specifyBody":"json","jsonBody":"={{ JSON.stringify({chat_id: $env.TG_CHAT, text: $('Format').first().json.text, parse_mode: 'HTML'}) }}","options":{}},
   "id":"n4","name":"Telegram fallback","type":"n8n-nodes-base.httpRequest","typeVersion":4.2,"position":[1040,0]}
 ],
 "connections":{"Webhook":{"main":[[{"node":"Format","type":"main","index":0}]]},"Format":{"main":[[{"node":"Send?","type":"main","index":0}]]},"Send?":{"main":[[{"node":"Screenshot","type":"main","index":0}],[]]},"Screenshot":{"main":[[],[{"node":"Telegram fallback","type":"main","index":0}]]}},
 "settings":{"executionOrder":"v1"},"active":False,"id":"tvOwnerMethod01"
}
json.dump([wf],open(os.path.expanduser('~/tv-hook/workflow.json'),'w'),ensure_ascii=False,indent=1)
print('ok',PATH[:6]+'…')
