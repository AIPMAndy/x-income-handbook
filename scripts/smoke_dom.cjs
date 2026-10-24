/** Browserless smoke check of static app startup and key outputs. Not a visual/a11y audit. */
const fs=require('fs'),vm=require('vm'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const elements={};
for(const match of html.matchAll(/<([a-z]+)([^>]*\sid="([^"]+)"[^>]*)>/g)){
 const [,tag,attrs,id]=match;
 const value=(attrs.match(/value="([^"]*)"/)||[])[1]||'';
 elements[id]={tagName:tag.toUpperCase(),value,checked:false,dataset:{},innerHTML:'',textContent:'',style:{},
  classList:{add(){},remove(){}},addEventListener(){},querySelector(){return{scrollTop:0}},showModal(){this.open=true},close(){this.open=false}};
}
const document={body:{insertAdjacentHTML(){}},documentElement:{scrollTop:0,scrollHeight:1000},getElementById(id){if(!elements[id])throw new Error('Missing #'+id);return elements[id]},addEventListener(){}};
const callbacks=[];const window={addEventListener(type,fn){callbacks.push({type,fn})},confirm(){return true},isSecureContext:false};
const storage=new Map();const localStorage={getItem(k){return storage.get(k)},setItem(k,v){storage.set(k,v)}};
const location={hash:'',href:'https://example.com/x-income-handbook/'};
const ctx=vm.createContext({document,window,localStorage,location,history:{replaceState(){}},navigator:{},console,URL,setTimeout(){},clearTimeout(){},innerHeight:844});
for(const file of ['data/content.js','data/templates.js','assets/app.js'])vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
assert(elements.chapterGrid.innerHTML.includes('CHAPTER / 14'));
assert(elements.templateList.innerHTML.includes('24-experiment-decisions.md'));
assert.strictEqual(elements.zeroOrders.textContent,'12.2%');
assert(elements.hourly.textContent.includes('/小时'));
assert(elements.rewardResult.innerHTML.includes('不应预测官方奖励'));
assert(elements.dayGrid.innerHTML.includes('DAY 30'));
assert.strictEqual(elements.chapterCount.textContent,'展示 26 / 26 个章节');
console.log('PASS browserless runtime: chapters, templates, calculator, eligibility, roadmap');
