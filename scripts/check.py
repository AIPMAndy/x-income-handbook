#!/usr/bin/env python3
"""CI validation for static docs and source accuracy safeguards."""
import json, re, sys
from pathlib import Path
from sync import render
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def check(ok, message):
    if not ok:errors.append(message)

def main():
    data=json.loads((ROOT/'data/content.json').read_text(encoding='utf8'))
    html=(ROOT/'index.html').read_text(encoding='utf8')
    js=(ROOT/'data/content.js').read_text(encoding='utf8')
    app=(ROOT/'assets/app.js').read_text(encoding='utf8')
    ids=[x['id'] for x in data['chapters']]
    check(len(ids)>=24,'Expected >=24 chapters')
    check(len(set(ids))==len(ids),'Duplicate chapter ID')
    check(len(data['routes'])==7,'Expected 7 monetization routes')
    check(len(data['days'])==30,'Expected 30 day tasks')
    check([x['day'] for x in data['days']]==list(range(1,31)),'Day numbers not consecutive')
    check(all(3<=len(c['steps'])<=7 for c in data['chapters']),'Chapter steps must be 3–7')
    check(all(c['deliverable'] and c['metric'] for c in data['chapters']),'Chapter deliverables/metrics missing')
    check(all(c['pitfalls'] for c in data['chapters']),'Chapter risk warning missing')
    check(all(c['sources'] for c in data['chapters']),'Chapter sources missing')
    check(all(all(0<=i<len(data['sources']) for i in c['sources']) for c in data['chapters']),'Invalid source index')
    check(all(s['url'].startswith('https://') for s in data['sources']),'Source must use HTTPS')
    check('500,000' in js and '500' in js,'Current creator reward thresholds missing')
    check('2026-09-07' in (ROOT/'research/sources.md').read_text(encoding='utf8'),'Retired revenue sharing date missing')
    check('30 天' in html,'30-day plan not visible')
    check('AIPMAndy' in html and 'metaver.vip' in html,'Brand contacts missing')
    check('aria-label=' in html,'Accessibility labels missing')
    check('prefers-reduced-motion' in (ROOT/'assets/style.css').read_text(encoding='utf8'),'Reduced motion CSS missing')
    check('localStorage' in app,'Local task progress missing')
    check('navigator.clipboard' in app,'Contact copy action missing')
    check('window.X_TEMPLATES' in (ROOT/'data/templates.js').read_text(encoding='utf8'),'Template manifest missing')
    check('https://github.com/AIPMAndy/x-income-handbook' in html,'Repository links missing')
    check(not re.search(r'保证.{0,8}(涨粉|赚钱|盈利)',html),'Unsupported earning guarantee found in HTML')
    expected='window.X_GUIDE = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n'
    check(js==expected,'content.js is not synchronized with content.json; run scripts/sync.py')
    for ch in data['chapters']:
        p=ROOT/'chapters'/f'{ch["id"]}.md'
        check(p.exists(),f'Missing {p.name}')
        if p.exists():check(p.read_text(encoding='utf8')==render(ch,data['sources'],data['updated']),f'Drift in chapters/{p.name}')
    for t in json.loads((ROOT/'data/templates.js').read_text(encoding='utf8').removeprefix('window.X_TEMPLATES = ').removesuffix(';\n')):
        check((ROOT/t['url']).exists(),f'Missing template {t["url"]}')
    required=['index.html','assets/app.js','assets/style.css','404.html','robots.txt','sitemap.xml','README.md','LICENSE','.github/workflows/pages.yml','.github/workflows/ci.yml','research/sources.md','research/red-team.md']
    for f in required:check((ROOT/f).is_file(),f'Missing {f}')
    if errors:
        for e in errors:print('FAIL:',e)
        print(f'{len(errors)} validation error(s)')
        return 1
    print(f'PASS: {len(ids)} chapters, {len(data["routes"])} routes, {len(data["days"])} tasks, {len(data["sources"])} sources; sources and chapters synchronized.')
    return 0
if __name__=='__main__':sys.exit(main())
