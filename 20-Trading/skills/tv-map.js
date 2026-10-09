// tv-map v3 — карта за методом власника (owner-method.md). EURUSD/GBPUSD (п=0.0001) і GER40 (п=1 пункт).
// ЗОНИ — D, H4, H1 (FVG + OB). РІВНІ — денні/H1-свінги (непрочесані), PDH/PDL/PDC, Asia H/L, Day H/L, Day/London Open.
// M5 — лише ATR і структура. Знятий рівень НЕ видаляється: підпис «ЗНЯТО». Закритий FVG/OB — не видаляється, стає INV/MIT.
// Виклики (на потрібному ТФ): __LEVELS(look,band) · __ZONES(tf,__FVGSCAN(),band) · __OBS(tf,look,disp,band) · __SESS() · __POOLS()

window.__RD=function(){var w=window.TradingViewApi._activeChartWidgetWV.value();var d=w.chartModel().mainSeries().data();var B=[];d.each(function(i,b){var v=b.value||b;if(v&&v.length)B.push(v);return false;});return B;};
window.__RDi=window.__RD;
window.__W=function(){return window.TradingViewApi._activeChartWidgetWV.value();};
window.__CFG=function(){var n=window.__W().chartModel().mainSeries().symbolInfo().name;
  if(/GER40|DE40|DAX/i.test(n))return {P:1,clus:3,sweep:1,fvg:3,nm:'GER40',dec:1};
  return {P:0.0001,clus:1,sweep:0.3,fvg:1,nm:n,dec:5};};
window.__TFMIN=function(B){var n=B.length,m=1e9;for(var i=Math.max(1,n-6);i<n;i++){var d=(B[i][0]-B[i-1][0])/60;if(d<m)m=d;}return m;};
window.__TFN=function(B){var m=window.__TFMIN(B);return m>=1440?'D':m>=240?'H4':m>=60?'H1':'M'+m;};

// існуючі малюнки: горизонтальні лінії і прямокутники
window.__EXIST=function(){var W=window.__W(),sh=W.getAllShapes(),L=[],R=[];
  for(var k=0;k<sh.length;k++){var e,pp,q,txt='';try{e=W.getShapeById(String(sh[k].id));pp=e._source.properties();q=e.getPoints();}catch(x){continue;}
    try{txt=pp.text.value()||'';}catch(x){}
    if(sh[k].name==='horizontal_line'&&q&&q[0])L.push({id:String(sh[k].id),p:q[0].price,t:txt});
    else if(sh[k].name==='rectangle'&&q&&q.length>1)R.push({id:String(sh[k].id),lo:Math.min(q[0].price,q[1].price),hi:Math.max(q[0].price,q[1].price),t0:Math.min(q[0].time,q[1].time),t:txt,pp:pp});}
  return {L:L,R:R};};

window.__HL=function(p,label,col,lw,ls){var W=window.__W(),B=window.__RD();var t=B[B.length-1][0];
  try{W.createMultipointShape([{time:t,price:p}],{shape:'horizontal_line',overrides:{linecolor:col,linewidth:lw||1,linestyle:ls==null?2:ls,showLabel:true,text:label,textcolor:col,horzLabelsAlign:'right',vertLabelsAlign:'bottom'}});return 1;}catch(x){return 0;}};

// непрочесані свінги (фрактал k барів з обох боків) за останні look барів
window.__SWINGS=function(B,k,look,sweep){var n=B.length,res=[];
  for(var i=Math.max(k,n-look);i<n-k;i++){var h=B[i][2],l=B[i][3],isH=true,isL=true;
    for(var j=1;j<=k;j++){if(B[i-j][2]>h||B[i+j][2]>h)isH=false;if(B[i-j][3]<l||B[i+j][3]<l)isL=false;}
    if(isH){var s1=false;for(var m=i+1;m<n;m++)if(B[m][2]>h+sweep){s1=true;break;}if(!s1)res.push({p:h,t:B[i][0],hi:1});}
    if(isL){var s2=false;for(var m2=i+1;m2<n;m2++)if(B[m2][3]<l-sweep){s2=true;break;}if(!s2)res.push({p:l,t:B[i][0],hi:0});}}
  return res;};
window.__CLUST=function(arr,tol){arr=arr.slice().sort(function(a,b){return a.p-b.p;});var g=[],c=null;
  for(var i=0;i<arr.length;i++){if(c&&arr[i].p-c.hi<=tol){c.hi=arr[i].p;c.n++;c.s+=arr[i].p;c.t=Math.max(c.t,arr[i].t);}else{c={lo:arr[i].p,hi:arr[i].p,n:1,s:arr[i].p,t:arr[i].t};g.push(c);}}
  return g;};

// рівні ліквідності з поточного ТФ (D або H1): look — скільки барів назад, band — відстань від ціни в п
window.__LEVELS=function(look,band){var C=window.__CFG(),B=window.__RD(),n=B.length,cur=B[n-1][4],tf=window.__TFN(B);
  var sw=window.__SWINGS(B,2,look,C.sweep*C.P),ex=window.__EXIST().L,add=0;
  [1,0].forEach(function(hi){
    var arr=sw.filter(function(s){return s.hi===hi&&Math.abs(s.p-cur)<=band*C.P;});
    window.__CLUST(arr,C.clus*C.P).forEach(function(c){var p=c.s/c.n,dup=false;
      for(var j=0;j<ex.length;j++){if(Math.abs(ex[j].p-p)<=Math.max(C.clus,1)*C.P*0.6&&/BSL|SSL/.test(ex[j].t)){dup=true;break;}}
      if(dup)return;
      var rg=c.n>1?(' x'+c.n+' '+c.lo.toFixed(C.dec)+'–'+c.hi.toFixed(C.dec)):'';
      var lab=(hi?'BSL ':'SSL ')+tf+rg+' '+new Date(c.t*1000).toISOString().substr(5,5);
      add+=window.__HL(p,lab,hi?'#ef5350':'#26a69a',tf==='D'?2:1,2);});});
  return {tf:tf,swings:sw.length,added:add};};

// сесійні рівні: PDH/PDL/PDC, Asia H/L (22:00–06:00 UTC), Day H/L/Open, London Open 07:00 UTC
window.__SESS=function(){var C=window.__CFG(),B=window.__RD(),n=B.length,last=B[n-1][0],d0=Math.floor(last/86400)*86400,ex=window.__EXIST().L,add=0;
  function rng(a,b){var hi=-1e9,lo=1e9,op=null,cl=null,c=0;for(var i=0;i<n;i++){var t=B[i][0];if(t>=a&&t<b){if(op===null)op=B[i][1];if(B[i][2]>hi)hi=B[i][2];if(B[i][3]<lo)lo=B[i][3];cl=B[i][4];c++;}}return c?{hi:hi,lo:lo,op:op,cl:cl,c:c}:null;}
  var pd=null,k=1;while(!pd&&k<=4){pd=rng(d0-k*86400,d0-(k-1)*86400);k++;}
  var asia=rng(d0-7200,d0+21600),day=rng(d0,d0+86400),lo7=rng(d0+25200,d0+25500),it=[];
  if(pd){it.push([pd.hi,'BSL PDH','#ef5350']);it.push([pd.lo,'SSL PDL','#26a69a']);it.push([pd.cl,'PDC','#2962ff']);}
  if(asia){it.push([asia.hi,'BSL ASIA H','#ef5350']);it.push([asia.lo,'SSL ASIA L','#26a69a']);}
  if(day){it.push([day.hi,'BSL DAY H','#ef5350']);it.push([day.lo,'SSL DAY L','#26a69a']);it.push([day.op,'DAY OPEN','#2962ff']);}
  if(lo7)it.push([lo7.op,'LDN OPEN 07:00','#2962ff']);
  it.forEach(function(x){var dup=false;for(var j=0;j<ex.length;j++){if(ex[j].t.indexOf(x[1])>=0&&Math.abs(ex[j].p-x[0])<=C.clus*C.P*0.5){dup=true;break;}}
    if(!dup)add+=window.__HL(x[0],x[1]+' '+x[0].toFixed(C.dec),x[2],1,(x[1].indexOf('OPEN')>=0||x[1]==='PDC')?3:2);});
  return {pd:pd,asia:asia,day:day,added:add};};

// FVG: [t, lo, hi, bull, state] ; state open|part|inv
window.__FVGSCAN=function(minPts){var C=window.__CFG(),B=window.__RD(),n=B.length,P=C.P,m=(minPts||C.fvg)*P,F=[];
  for(var i=2;i<n;i++){var a=B[i-2],c=B[i];
    if(c[3]>a[2]&&c[3]-a[2]>=m){var lo=a[2],hi=c[3],st='open';
      for(var j=i+1;j<n;j++){if(B[j][3]<=lo){st='inv';break;}if(B[j][3]<hi){hi=B[j][3];st='part';}}
      if(hi-lo>=0.3*P||st==='inv')F.push([a[0],lo,hi,1,st]);}
    if(c[2]<a[3]&&a[3]-c[2]>=m){var l2=c[2],h2=a[3],s2='open';
      for(var j2=i+1;j2<n;j2++){if(B[j2][2]>=h2){s2='inv';break;}if(B[j2][2]>l2){l2=B[j2][2];s2='part';}}
      if(h2-l2>=0.3*P||s2==='inv')F.push([a[0],l2,h2,0,s2]);}}
  return F;};

window.__TFCOL=function(tf){return tf==='D'?'#ab47bc':tf==='H4'?'#ff9800':'#29b6f6';};

// малює/оновлює FVG-зони. Нічого не видаляє.
window.__ZONES=function(tf,F,bandPts){var W=window.__W(),C=window.__CFG(),P=C.P;
  var B=window.__RD(),n=B.length,cur=B[n-1][4],t=B[n-1][0],R=t+21600,band=(bandPts||160)*P,col=window.__TFCOL(tf),gray='#787b86';
  var rs=window.__EXIST().R,have={},upd=0,add=0;
  rs.forEach(function(r){var txt=r.t;if(txt.indexOf(tf+' FVG')!==0&&txt.indexOf('INV '+tf)!==0)return;
    var hit=-1;for(var m=0;m<F.length;m++){if(Math.abs(F[m][1]-r.lo)<C.sweep*P&&Math.abs(F[m][2]-r.hi)<C.sweep*P){hit=m;break;}}
    if(hit>=0){have[hit]=1;return;}
    if(txt.indexOf('INV')!==0){try{r.pp.text.setValue('INV '+txt);r.pp.color.setValue(gray);r.pp.backgroundColor.setValue(gray);upd++;}catch(x){}}});
  for(var m=0;m<F.length;m++){if(have[m])continue;var f=F[m];
    if(Math.abs(f[1]-cur)>band&&Math.abs(f[2]-cur)>band)continue;
    var c=f[4]==='inv'?gray:col;
    var lab=(f[4]==='inv'?'INV ':'')+tf+' FVG '+(f[3]?'↑':'↓')+(f[4]==='part'?' (залишок)':'');
    try{W.createMultipointShape([{time:f[0],price:f[1]},{time:R,price:f[2]}],{shape:'rectangle',overrides:{color:c,linewidth:1,backgroundColor:c,fillBackground:true,transparency:tf==='H4'||tf==='D'?75:80,showLabel:true,text:lab,textcolor:c}});add++;}catch(x){}}
  return {tf:tf,scanned:F.length,added:add,inverted:upd};};

// OB: зсув (тіло ≥ disp×середнього діапазону) + FVG; зона = остання протилежна свічка перед зсувом; без закриття крізь зону
window.__OBSCAN=function(look,disp){var C=window.__CFG(),B=window.__RD(),n=B.length,res=[],seen={};
  var s=0,c0=0;for(var i=Math.max(0,n-60);i<n;i++){s+=B[i][2]-B[i][3];c0++;}var avg=s/(c0||1);
  for(var d=Math.max(4,n-look);d<n-1;d++){var body=B[d][4]-B[d][1];
    var bull=body>=disp*avg&&B[d+1][3]>B[d-1][2],bear=-body>=disp*avg&&B[d+1][2]<B[d-1][3];
    if(!bull&&!bear)continue;
    for(var j=d-1;j>=d-4;j--){var isOpp=bull?(B[j][4]<B[j][1]):(B[j][4]>B[j][1]);if(!isOpp)continue;
      var lo=B[j][3],hi=B[j][2],mit=false,tst=false;
      for(var m=d+1;m<n;m++){if(bull){if(B[m][4]<lo-C.sweep*C.P){mit=true;break;}if(B[m][3]<hi)tst=true;}else{if(B[m][4]>hi+C.sweep*C.P){mit=true;break;}if(B[m][2]>lo)tst=true;}}
      if(!mit&&!seen[B[j][0]]){seen[B[j][0]]=1;res.push([B[j][0],lo,hi,bull?1:0,tst?1:0]);}
      break;}}
  return res;};
window.__OBS=function(tf,look,disp,bandPts){var W=window.__W(),C=window.__CFG(),P=C.P,B=window.__RD(),n=B.length,cur=B[n-1][4],R=B[n-1][0]+21600,band=(bandPts||200)*P;
  var O=window.__OBSCAN(look,disp||1.5),rs=window.__EXIST().R,add=0,mit=0;
  rs.forEach(function(r){if(r.t.indexOf(tf+' OB')!==0)return;var up=r.t.indexOf('↑')>=0,bad=false;
    for(var i=0;i<n;i++){if(B[i][0]<=r.t0)continue;if(up?(B[i][4]<r.lo-C.sweep*P):(B[i][4]>r.hi+C.sweep*P)){bad=true;break;}}
    if(bad){try{r.pp.text.setValue('MIT '+r.t);r.pp.color.setValue('#787b86');r.pp.backgroundColor.setValue('#787b86');mit++;}catch(x){}}});
  rs=window.__EXIST().R;
  O.forEach(function(o){if(Math.abs(o[1]-cur)>band&&Math.abs(o[2]-cur)>band)return;var dup=false;
    for(var i=0;i<rs.length;i++){if(rs[i].t.indexOf('OB')>=0&&Math.abs(rs[i].lo-o[1])<=C.sweep*P&&Math.abs(rs[i].hi-o[2])<=C.sweep*P){dup=true;break;}}
    if(dup)return;var c=o[3]?'#26a69a':'#ef5350';
    try{W.createMultipointShape([{time:o[0],price:o[1]},{time:R,price:o[2]}],{shape:'rectangle',overrides:{color:c,linewidth:1,backgroundColor:c,fillBackground:true,transparency:82,showLabel:true,text:tf+' OB '+(o[3]?'↑':'↓'),textcolor:c}});add++;}catch(x){}});
  return {tf:tf,found:O.length,added:add,mitigated:mit};};

// щотіку: позначає зняті пули. НІЧОГО НЕ ВИДАЛЯЄ.
window.__POOLS=function(){var W=window.__W(),C=window.__CFG(),B=window.__RD(),n=B.length,P=C.P,mk=0,sw=[];
  var sh=W.getAllShapes();
  for(var k=0;k<sh.length;k++){if(sh[k].name!=='horizontal_line')continue;
    var e,pp,pr=null;try{e=W.getShapeById(String(sh[k].id));pp=e._source.properties();var q=e.getPoints();pr=q&&q[0]?q[0].price:null;}catch(x){continue;}
    if(pr==null)continue;var txt='';try{txt=pp.text.value()||'';}catch(x){}
    var isB=/BSL/.test(txt),isS=/SSL/.test(txt);if((!isB&&!isS)||/ЗНЯТО/.test(txt))continue;
    var hit=false;for(var j=Math.max(1,n-1500);j<n;j++){if(isB&&B[j][2]>pr+C.sweep*P){hit=true;break;}if(isS&&B[j][3]<pr-C.sweep*P){hit=true;break;}}
    if(!hit)continue;
    try{pp.text.setValue('ЗНЯТО '+txt);pp.linestyle.setValue(1);pp.linewidth.setValue(1);mk++;sw.push(pr.toFixed(C.dec));}catch(x){}}
  return {marked:mk,swept:sw};};
'__MAP v3 installed: __LEVELS / __SESS / __FVGSCAN / __ZONES / __OBS / __POOLS';
