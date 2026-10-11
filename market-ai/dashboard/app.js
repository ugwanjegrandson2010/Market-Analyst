const $ = (id) => document.getElementById(id);
let priceChart, volumeChart;
const state = { backend: '', symbol: 'AAPL', data: null };

function backendUrl() { return $('#backendUrl').value.trim().replace(/\/$/, ''); }
function symbol() { return $('#symbol').value.trim().toUpperCase(); }
function setStatus(msg, ok=true) { const el=$('statusBar'); el.textContent=msg; el.style.color = ok?'#93c5fd':'#fca5a5'; }

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

async function refresh() {
  state.backend = backendUrl();
  state.symbol = symbol();
  setStatus(`Loading ${state.symbol}...`);
  try {
    const [history, analysis] = await Promise.all([
      fetchJson(`${state.backend}/api/market/${state.symbol}`),
      fetchJson(`${state.backend}/api/analyze/${state.symbol}`),
    ]);
    state.data = { history, analysis };
    render(history, analysis);
    // risk optional
    fetchJson(`${state.backend}/api/risk/analyze/${state.symbol}`)
      .then(r => renderRisk(r)).catch(e => $('risk').innerHTML = `<p>${e.message}</p>`);
    setStatus(`Loaded ${state.symbol}.`);
  } catch (e) {
    setStatus(`Error: ${e.message}`, false);
  }
}

function render(history, analysis) {
  const latest = history[history.length-1];
  $('latestPrice').textContent = Number(latest.close).toFixed(2);
  $('latestMeta').innerHTML = `Open ${latest.open} · High ${latest.high} · Low ${latest.low} · Volume ${latest.volume}`;

  renderPriceChart(history);
  renderVolumeChart(history);
  renderIndicators(analysis.indicators || {});
  renderSignals(analysis.signals || []);
  renderConfluence(analysis.confluence || {});
  renderPrediction(analysis.prediction || {});
  renderCaution(analysis);
}

function renderPriceChart(history) {
  const labels = history.map(x => new Date(x.timestamp).toLocaleDateString());
  const close = history.map(x => x.close);
  const ctx = document.getElementById('priceChart');
  if (priceChart) priceChart.destroy();
  priceChart = new Chart(ctx, {
    type: 'line',
    data: { labels, datasets: [{ label: 'Close', data: close, borderColor:'#38bdf8', tension:.2, pointRadius:0 }]},
    options: { responsive:true, plugins:{ legend:{display:true} } }
  });
}
function renderVolumeChart(history) {
  const labels = history.map(x => new Date(x.timestamp).toLocaleDateString());
  const vol = history.map(x => x.volume);
  const ctx = document.getElementById('volumeChart');
  if (volumeChart) volumeChart.destroy();
  volumeChart = new Chart(ctx, {
    type: 'bar',
    data: { labels, datasets: [{ label:'Volume', data: vol, backgroundColor:'#475569' }]},
    options: { responsive:true, plugins:{ legend:{display:true} } }
  });
}

function row(k,v){ return `<div class="row"><span>${k}</span><span>${v}</span></div>`; }

function renderIndicators(i) {
  const html = [
    row('SMA20', i.sma20?.toFixed?.(4) ?? i.sma20),
    row('SMA50', i.sma50?.toFixed?.(4) ?? i.sma50),
    row('EMA12', i.ema12?.toFixed?.(4) ?? i.ema12),
    row('EMA26', i.ema26?.toFixed?.(4) ?? i.ema26),
    row('RSI14', i.rsi14?.toFixed?.(2) ?? i.rsi14),
    row('MACD', i.macd?.toFixed?.(4) ?? i.macd),
    row('MACD signal', i.macd_signal?.toFixed?.(4) ?? i.macd_signal),
    row('Latest close', i.latest_close),
  ].join('');
  $('indicators').innerHTML = html;
}

function renderSignals(signals) {
  if (!signals.length) { $('signals').innerHTML = '<p>No signals.</p>'; return; }
  $('signals').innerHTML = signals.map(s => {
    const cls = (s.direction||'').toLowerCase().includes('bull') ? 'bull' : 'bear';
    return `<div class="row"><span>${s.indicator}: ${s.description}</span>
      <span class="tag ${cls}">${s.direction} ${Math.round((s.confidence||0)*100)}%</span></div>`;
  }).join('');
}

function renderConfluence(c) {
  $('confluence').innerHTML = `
    <div class="big">${c.market_bias || '-' } <span class="delta">${Math.round((c.confidence||0)*100)}%</span></div>
    <p>${(c.reasons||[]).join('<br>')}</p>`;
}

function renderPrediction(p) {
  $('prediction').innerHTML = `
    <div class="big">${(p.direction||'-').toUpperCase()}</div>
    <div class="row"><span>Probability up</span><span>${Math.round((p.probability_up||0)*100)}%</span></div>
    <div class="row"><span>Trained samples</span><span>${p.trained_samples ?? '-'}</span></div>
    <p class="note">${p.note || ''}</p>`;
}

function renderRisk(r) {
  $('risk').innerHTML = `
    <div class="big">${r.risk_level || r.level || '-'}</div>
    <pre style="white-space:pre-wrap;">${JSON.stringify(r, null, 2)}</pre>`;
}

function renderCaution(a) {
  const c = a.confluence || {};
  const pred = a.prediction || {};
  let text = '';
  // Trend explanation
  const rsi = a.indicators?.rsi14;
  const close = a.indicators?.latest_close;
  const sma50 = a.indicators?.sma50;
  const macd = a.indicators?.macd;
  text += `<p><b>Why it may move:</b> `;
  if (close != null && sma50 != null) {
    text += close < sma50 ? `Price sits below its 50-period average, a bearish tilt. ` : `Price sits above its 50-period average, a bullish tilt. `;
  }
  if (rsi != null) {
    if (rsi > 70) text += `RSI is overbought (${rsi.toFixed(1)}), suggesting pullback risk. `;
    else if (rsi < 30) text += `RSI is oversold (${rsi.toFixed(1)}), suggesting bounce potential. `;
    else text += `RSI is neutral (${rsi.toFixed(1)}), no strong momentum signal. `;
  }
  if (macd != null) {
    text += macd >= 0 ? `MACD positive, momentum favors upside. ` : `MACD negative, momentum favors downside. `;
  }
  text += `</p>`;
  text += `<p><b>Caution:</b> Signals can conflict. Confluence bias is ${c.market_bias || 'unknown'} at ${Math.round((c.confidence||0)*100)}% confidence, but the model predicts ${(pred.direction||'unknown').toUpperCase()} with ${Math.round((pred.probability_up||0)*100)}% upside probability. Treat this as educational information, not a guarantee. Prices are volatile; only risk what you can afford to lose.</p>`;
  text += `<p><b>Beginner tips:</b> Use multiple timeframes, size positions small, set stop-losses, and never invest based on one indicator.</p>`;
  $('caution').innerHTML = text;
}

// harvest button
$('refreshBtn').addEventListener('click', refresh);
$('harvestBtn').addEventListener('click', async () => {
  setStatus('Harvesting...');
  try {
    const r = await fetchJson(`${backendUrl()}/api/harvest/${symbol()}`);
    setStatus('Harvest complete.'); console.log(r);
  } catch (e) { setStatus('Harvest error: '+e.message, false); }
});
// enter key
document.addEventListener('keydown', (e) => { if (e.key === 'Enter') refresh(); });

refresh();
