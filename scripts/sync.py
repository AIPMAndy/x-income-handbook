#!/usr/bin/env python3
"""Synchronize machine-readable chapter source with static JS and Markdown."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def render(ch, sources, updated):
    steps='\n'.join(f'{i}. {x}' for i,x in enumerate(ch['steps'],1))
    pitfalls='\n'.join(f'- {x}' for x in ch['pitfalls'])
    workshop='\n'.join(f'{i}. {x}' for i,x in enumerate(ch.get('workshop_steps',[]),1))
    refs='\n'.join(f'- {sources[i]["name"]}：{sources[i]["url"]}' for i in ch['sources'])
    return (f'# {ch["id"]} · {ch["title"]}\n\n> {ch["subtitle"]}\n\n'
            f'## 为什么要做\n\n{ch["why"]}\n\n## 具体操作\n\n{steps}\n\n'
            f'## 场景演练｜{ch.get("workshop_title","实践")}\n\n{ch.get("workshop_case","")}\n\n'
            f'### 跟着做\n\n{workshop}\n\n'
            f'### 完成标准\n\n{ch.get("acceptance","")}\n\n'
            f'### 卡住时怎么处理\n\n{ch.get("if_stuck","")}\n\n'
            f'## 常见误区\n\n{pitfalls}\n\n## 本章交付\n\n'
            f'- 产物：{ch["deliverable"]}\n- 观察指标：{ch["metric"]}\n\n'
            f'## 可核验来源\n\n{refs}\n\n---\n'
            f'内容核验日期：{updated}。平台规则可能调整，请以官方当前页面和本人账号的资格提示为准。\n')

def sync():
    data=json.loads((ROOT/'data/content.json').read_text(encoding='utf8'))
    (ROOT/'data/content.js').write_text('window.X_GUIDE = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n',encoding='utf8')
    for ch in data['chapters']:
        (ROOT/'chapters'/f'{ch["id"]}.md').write_text(render(ch,data['sources'],data['updated']),encoding='utf8')
    print(f'Synced {len(data["chapters"])} chapters and data/content.js')

if __name__=='__main__':sync()
