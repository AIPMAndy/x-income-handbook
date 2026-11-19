/* X Content Experiment Workbench · all records stay in the current browser. */
(function () {
  'use strict';
  const KEY = 'andy-x-income-experiments-v1';
  const ALLOWED = ['教程', '真实经历', '开源工具', '观点', '其他'];
  const LIMIT = 200;
  const fmt = n => new Intl.NumberFormat('zh-CN', {maximumFractionDigits: 2}).format(n);
  const yuan = n => '¥ ' + fmt(n);
  const rate = (a, b) => b > 0 ? (a / b * 100).toFixed(2) + '%' : '—';
  function metrics(rows) {
    const sum = key => rows.reduce((n, r) => n + (Number(r[key]) || 0), 0);
    const impressions = sum('impressions'), visits = sum('visits'), leads = sum('leads'), orders = sum('orders');
    const revenue = sum('revenue'), cost = sum('cost');
    return {count: rows.length, impressions, visits, leads, orders, revenue, cost, contribution: revenue - cost,
      visitRate: rate(visits, impressions), leadRate: rate(leads, visits), orderRate: rate(orders, leads)};
  }
  // Escape formula-like CSV cells to prevent spreadsheet formula execution.
  function safeCsv(value) {
    let s = String(value == null ? '' : value);
    if (/^\s*[=+\-@\t\r]/.test(s)) s = "'" + s;
    return '"' + s.replace(/"/g, '""') + '"';
  }
  function csv(rows) {
    const keys = ['date','name','format','hypothesis','impressions','visits','leads','orders','revenue','cost','note'];
    const labels = ['记录日期','实验名称','内容类型','本次假设','曝光次数','主页访问','有效询盘','成交订单','已确认收入(元)','直接成本(元)','数据来源与复盘备注'];
    return '\ufeff' + [labels.map(safeCsv).join(','), ...rows.map(r => keys.map(k => safeCsv(r[k])).join(','))].join('\r\n') + '\r\n';
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {metrics, safeCsv, csv};
  if (typeof document === 'undefined') return;
  const $ = id => document.getElementById(id);
  const form = $('recordForm');
  let records = [];
  function status(message) { $('saveStatus').textContent = message; }
  function sanitize(obj) {
    if (!obj || typeof obj !== 'object' || typeof obj.name !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(obj.date)) return null;
    const r = {id: String(obj.id || ''), name: obj.name.slice(0, 90), date: obj.date,
      format: ALLOWED.includes(obj.format) ? obj.format : '其他', hypothesis: String(obj.hypothesis || '').slice(0, 160),
      note: String(obj.note || '').slice(0, 400)};
    for (const key of ['impressions','visits','leads','orders','revenue','cost']) {
      const n = Number(obj[key]);
      r[key] = Number.isFinite(n) && n >= 0 && n <= 1e9 ? n : 0;
    }
    return r.name.trim() ? r : null;
  }
  try {
    const raw = JSON.parse(localStorage.getItem(KEY) || '[]');
    if (Array.isArray(raw)) records = raw.slice(0, LIMIT).map(sanitize).filter(Boolean);
  } catch (_) { status('读取历史记录失败；原浏览器数据未被覆盖。'); }
  function persist(next) {
    try { localStorage.setItem(KEY, JSON.stringify(next)); records = next; return true; }
    catch (_) { status('本地保存失败：请检查浏览器的隐私模式或存储空间。'); return false; }
  }
  function visible() {
    const needle = $('search').value.trim().toLocaleLowerCase();
    const format = $('formatFilter').value;
    return [...records].filter(r => (format === '全部' || r.format === format) &&
      [r.name,r.hypothesis,r.note].join(' ').toLocaleLowerCase().includes(needle))
      .sort((a,b) => b.date.localeCompare(a.date));
  }
  function setText(id, value) { $(id).textContent = String(value); }
  function render() {
    const rows = visible(), m = metrics(rows);
    setText('experimentCount', m.count + ' 条实验记录');
    setText('totalImpressions', fmt(m.impressions));
    setText('totalVisits', fmt(m.visits));
    setText('totalLeads', fmt(m.leads));
    setText('totalOrders', fmt(m.orders));
    setText('netContribution', m.count ? yuan(m.contribution) : '—');
    setText('visitRate', m.visitRate); setText('leadRate', m.leadRate); setText('orderRate', m.orderRate);
    setText('funnelWarning', m.count ? '这是不同环节数据的观察性比率，并非同一批用户的可归因转化率。' :
      '没有记录时不输出比率。');
    const body = $('recordsBody'); body.replaceChildren();
    for (const r of rows) {
      const tr = document.createElement('tr');
      const make = (value) => { const td = document.createElement('td'); td.textContent = String(value); tr.appendChild(td); return td; };
      const summary = make(''); const title = document.createElement('strong'); title.textContent = r.name;
      const day = document.createElement('small'); day.textContent = r.date;
      summary.append(title, day);
      if (r.hypothesis || r.note) { const note = document.createElement('p'); note.textContent = r.hypothesis || r.note; summary.appendChild(note); }
      make(r.format); make(fmt(r.impressions)); make(fmt(r.leads)); make(fmt(r.orders)); make(yuan(r.revenue - r.cost));
      const action = make(''); const del = document.createElement('button'); del.type = 'button'; del.className = 'delete-btn';
      del.textContent = '删除'; del.setAttribute('aria-label', '删除实验：' + r.name);
      del.addEventListener('click', () => { if (confirm('永久删除「' + r.name + '」这条本机实验记录？')) {
        if (persist(records.filter(x => x.id !== r.id))) { status('已删除记录。'); render(); }
      }});
      action.appendChild(del); body.appendChild(tr);
    }
    $('emptyState').hidden = rows.length > 0;
    $('exportCsv').disabled = rows.length === 0;
    $('resetAll').disabled = records.length === 0;
  }
  const now = new Date();
  const localDate = [now.getFullYear(), String(now.getMonth()+1).padStart(2,'0'), String(now.getDate()).padStart(2,'0')].join('-');
  $('date').value = localDate;
  form.addEventListener('submit', e => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    if (records.length >= LIMIT) { status('已达到 200 条存储上限；请先导出备份、删除旧记录。'); return; }
    const values = {};
    for (const key of ['impressions','visits','leads','orders','revenue','cost']) {
      const input = $(key);
      const n = input.value === '' ? 0 : Number(input.value);
      if (!Number.isFinite(n) || n < 0 || n > 1e9 || (['impressions','visits','leads','orders'].includes(key) && !Number.isInteger(n))) {
        status('请检查数值：所有数量必须是非负整数，金额必须在允许范围内。'); input.focus(); return;
      }
      values[key] = n;
    }
    const item = sanitize({...values, id: String(Date.now()) + '-' + String(Math.random()).slice(2),
      name: $('name').value.trim(), date: $('date').value, format: $('format').value,
      hypothesis: $('hypothesis').value, note: $('note').value});
    if (!item) { status('请填写有效的实验名称与日期。'); return; }
    if (persist([item, ...records])) { form.reset(); $('date').value = localDate; status('已保存到当前浏览器。建议及时导出 CSV 备份。'); render(); $('name').focus(); }
  });
  $('search').addEventListener('input', render);
  $('formatFilter').addEventListener('change', render);
  $('exportCsv').addEventListener('click', () => {
    const rows = visible(); if (!rows.length) return;
    const file = new Blob([csv(rows)], {type:'text/csv;charset=utf-8'});
    const url = URL.createObjectURL(file); const a = document.createElement('a');
    a.href = url; a.download = 'x-content-experiments-' + localDate + '.csv';
    document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    status('已导出当前筛选的 ' + rows.length + ' 条记录。');
  });
  $('resetAll').addEventListener('click', () => {
    if (!records.length || !confirm('清空本设备全部实验记录？不可撤销，请先导出 CSV 备份。')) return;
    if (persist([])) { status('全部本机实验记录已清空。'); render(); }
  });
  $('copyWechat').addEventListener('click', async () => {
    try {
      if (navigator.clipboard && window.isSecureContext) await navigator.clipboard.writeText('AIPMAndy');
      else {
        const area = document.createElement('textarea'); area.value='AIPMAndy'; area.style.position='fixed'; area.style.left='-9999px';
        document.body.appendChild(area); area.select(); if (!document.execCommand('copy')) throw new Error('clipboard rejected'); area.remove();
      }
      status('微信号 AIPMAndy 已复制。');
    } catch (_) { status('复制受限，请手动复制微信号 AIPMAndy。'); }
  });
  render();
})();
