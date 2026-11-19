const assert = require('node:assert/strict');
const {metrics, safeCsv, csv} = require('../assets/experiment.js');
const empty = metrics([]);
assert.deepEqual({count:empty.count,visit:empty.visitRate,lead:empty.leadRate,order:empty.orderRate},{count:0,visit:'—',lead:'—',order:'—'});
const rows = [
  {date:'2026-11-19',name:'真实实验A',format:'教程',hypothesis:'A',impressions:1000,visits:50,leads:5,orders:1,revenue:400,cost:100,note:'X Analytics'},
  {date:'2026-11-20',name:'真实实验B',format:'开源工具',hypothesis:'B',impressions:2000,visits:150,leads:10,orders:2,revenue:600,cost:200,note:'CRM'}
];
const m = metrics(rows);
assert.equal(m.count,2);
assert.equal(m.impressions,3000);
assert.equal(m.visits,200);
assert.equal(m.leads,15);
assert.equal(m.orders,3);
assert.equal(m.contribution,700);
assert.equal(m.visitRate,'6.67%');
assert.equal(m.leadRate,'7.50%');
assert.equal(m.orderRate,'20.00%');
assert.equal(metrics([{impressions:0,visits:0,leads:0,orders:0,revenue:0,cost:5}]).contribution,-5);
assert.equal(safeCsv('=1+1'),'"\'=1+1"');
assert.equal(safeCsv(' hello "world"'),'" hello ""world"""');
assert.match(csv([{...rows[0],name:'=HYPERLINK("bad")'}]), /'=HYPERLINK/);
assert.equal(csv(rows).charCodeAt(0),0xFEFF);
console.log('PASS experiment aggregation, zero denominators, cost boundary, CSV formula protection and BOM');
