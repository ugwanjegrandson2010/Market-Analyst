const units = [
  { id:'u0', title:'Unit 0: Foundations', q:'What matters most in trading?', a:'Risk management' },
  { id:'u1', title:'Unit 1: Traditional Markets', q:'What does SMA indicate?', a:'Trend direction' },
  { id:'u2', title:'Unit 2: Blockchain & Crypto', q:'What is a private key?', a:'Control to funds' },
  { id:'u3', title:'Unit 3: Indicators', q:'RSI above 70 means?', a:'Overbought' },
  { id:'u4', title:'Unit 4: Algo Trading', q:'What bias is dangerous in backtests?', a:'Look-ahead' },
  { id:'u5', title:'Unit 5: Mining & Infra', q:'What raises mining difficulty?', a:'More hash rate' },
  { id:'u6', title:'Unit 6: Risk & Psychology', q:'Max risk per trade (beginner)?', a:'1%' },
  { id:'u7', title:'Unit 7: Compliance', q:'Why taxes?', a:'Legal/accurate reporting' },
];

function loadProgress(){ return JSON.parse(localStorage.getItem('progress')||'{}'); }
function saveProgress(p){ localStorage.setItem('progress', JSON.stringify(p)); }
const progress = loadProgress();

function renderUnits(){
  const container = document.getElementById('units');
  container.innerHTML = units.map((u,idx) => {
    const unlocked = idx===0 || progress[units[idx-1].id];
    const passed = progress[u.id];
    return `<div class="row"><span>${u.title} ${passed?'✅':''}</span>
      ${unlocked && !passed ? `<span><input data-id="${u.id}" placeholder="Answer: ${u.a}"><button data-check="${u.id}">Check</button></span>` : (passed?'<span>Done</span>':'<span>Locked</span>')}</div>`;
  }).join('');
  container.querySelectorAll('button[data-check]').forEach(b=>{
    b.addEventListener('click',()=>{
      const id=b.dataset.check; const inp=container.querySelector(`input[data-id="${id}"]`);
      const u=units.find(x=>x.id===id);
      if (inp.value.trim().toLowerCase() === u.a.toLowerCase()) {
        progress[id]=true; saveProgress(progress); renderUnits(); alert('Passed! Unit unlocked.');
      } else alert('Try again. Hint: '+u.a);
    });
  });
}
renderUnits();

// Playground
function sampleCsv(){
  let lines=['timestamp,close'];
  let p=100;
  for (let i=0;i<60;i++){ p += (Math.random()-0.48)*2; lines.push(`day${i+1},${p.toFixed(2)}`); }
  return lines.join('\n');
}
document.getElementById('csv').value = sampleCsv();

function sma(values, n){
  const out=[]; for(let i=0;i<values.length;i++){
    if(i<n-1){out.push(null);} else {
      let s=0; for(let j=i-n+1;j<=i;j++) s+=values[j]; out.push(s/n);
    }
  } return out;
}
function rsi(values,n=14){
  const out=[]; let gains=0,losses=0;
  for(let i=0;i<values.length;i++){
    if(i===0){out.push(null);continue;}
    const ch=values[i]-values[i-1];
    if(i<=n){ if(ch>0) gains+=ch; else losses-=ch; out.push(null); if(i===n){ const rs=gains/n; const rl=losses/n; out[i]=100-100/(1+rs/(rl||1)); } continue; }
    const g=ch>0?ch:0, l=ch<0?-ch:0;
    gains=(gains*(n-1)+g)/n; losses=(losses*(n-1)+l)/n;
    const rs=gains/losses; out.push(100-100/(1+rs));
  }
  return out;
}

function plot(){
  const text=document.getElementById('csv').value.trim();
  const rows=text.split('\n').slice(1);
  const closes=rows.map(r=>parseFloat(r.split(',')[1]));
  const labels=rows.map(r=>r.split(',')[0]);
  const s20=sma(closes,5); const r14=rsi(closes,14);
  if(window.playChart) window.playChart.destroy();
  const ctx=document.getElementById('playChart');
  window.playChart=new Chart(ctx,{type:'line',data:{labels,datasets:[
    {label:'Close',data:closes,borderColor:'#38bdf8',pointRadius:0},
    {label:'SMA5',data:s20,borderColor:'#f59e0b',pointRadius:0},
    {label:'RSI×2',data:r14.map(v=>v==null?null:v*2),borderColor:'#a78bfa',pointRadius:0}
  ]},options:{responsive:true}});
}
document.getElementById('plotBtn').addEventListener('click',plot);
plot();

// Paper trading
const KEY='paperState';
function loadPaper(){ const s=localStorage.getItem(KEY); return s?JSON.parse(s):{cash:10000,positions:{},trades:[]} ;}
function savePaper(s){ localStorage.setItem(KEY,JSON.stringify(s)); }
function renderPaper(){
  const s=loadPaper();
  const pnl = Object.entries(s.positions).map(([sym,p])=>`${sym}: ${p.qty} @ ${p.price}`).join('<br>')||'None';
  document.getElementById('paper').innerHTML = `
    <div class="row"><span>Cash</span><span>${s.cash.toFixed(2)}</span></div>
    <div class="row"><span>Positions</span><span>${pnl}</span></div>
    <label>Symbol <input id="psym" value="AAPL"></label>
    <label>Qty <input id="pqty" type="number" value="10"></label>
    <label>Price <input id="pprice" type="number" value="100"></label>
    <button id="buyBtn">Buy</button><button id="sellBtn">Sell</button>
    <div id="trades">${s.trades.slice(-5).map(t=>`${t.side} ${t.qty} ${t.sym} @ ${t.price}`).join('<br>')}</div>`;
  document.getElementById('buyBtn').onclick=()=>trade('buy');
  document.getElementById('sellBtn').onclick=()=>trade('sell');
}
function trade(side){
  const s=loadPaper();
  const sym=document.getElementById('psym').value.toUpperCase();
  const qty=Number(document.getElementById('pqty').value);
  const price=Number(document.getElementById('pprice').value);
  const cost=qty*price;
  if(side==='buy'){
    if(cost>s.cash){ alert('Not enough cash'); return; }
    s.cash-=cost; s.positions[sym]=s.positions[sym]||{qty:0,price:0};
    const p=s.positions[sym]; const newq=p.qty+qty; p.price=(p.price*p.qty+price*qty)/newq; p.qty=newq;
  } else {
    const p=s.positions[sym]; if(!p||p.qty<qty){ alert('Not enough shares'); return; }
    p.qty-=qty; s.cash+=cost; if(p.qty===0) delete s.positions[sym];
  }
  s.trades.push({side,qty,sym,price,ts:Date.now()});
  savePaper(s); renderPaper();
}
renderPaper();
