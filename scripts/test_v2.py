"""Guardrails introduced after adversarial audit v2."""
import unittest, json, re
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/content.json').read_text(encoding='utf8'))
class IDS(HTMLParser):
    def __init__(self):super().__init__();self.ids=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k=='id':self.ids.append(v)

class AuditV2Tests(unittest.TestCase):
    def test_26_unique_workshops(self):
        self.assertEqual(len(set(c['workshop_title'] for c in DATA['chapters'])),26)
    def test_workshop_steps_have_depth(self):
        self.assertTrue(all(len(c['workshop_steps'])>=3 for c in DATA['chapters']))
    def test_every_chapter_acceptance(self):
        self.assertTrue(all(len(c['acceptance'])>=12 for c in DATA['chapters']))
    def test_every_chapter_failure_guide(self):
        self.assertTrue(all(len(c['if_stuck'])>=14 for c in DATA['chapters']))
    def test_workshops_in_markdown(self):
        for c in DATA['chapters']:
            with self.subTest(c=c['id']):
                txt=(ROOT/'chapters'/f"{c['id']}.md").read_text(encoding='utf8')
                self.assertIn(c['workshop_title'],txt)
                self.assertIn(c['acceptance'],txt)
                self.assertIn(c['if_stuck'],txt)
    def test_24_templates_are_manifested(self):
        import json
        m=json.loads((ROOT/'data/templates.js').read_text(encoding='utf8').removeprefix('window.X_TEMPLATES = ').removesuffix(';\n'))
        self.assertEqual(len(m),24)
        self.assertTrue(all((ROOT/t['url']).is_file() for t in m))
    def test_rewards_and_subscriptions_are_not_mixed(self):
        a=(ROOT/'templates/22-policy-check-matrix.md').read_text(encoding='utf8')
        self.assertIn('2,000',a)
        self.assertIn('5,000,000',a)
        self.assertIn('500,000',a)
        self.assertIn('500',a)
    def test_paid_partnership_bans_explained(self):
        for f in ['templates/22-policy-check-matrix.md','index.html']:
            with self.subTest(f=f):self.assertIn('加密货币',(ROOT/f).read_text(encoding='utf8'))
    def test_monetization_tutorial_exclusion(self):
        self.assertIn('赚钱教学',(ROOT/'research/sources.md').read_text(encoding='utf8'))
    def test_calc_probability_present(self):
        app=(ROOT/'assets/app.js').read_text(encoding='utf8')
        self.assertIn('Math.pow(1-rate,leads)',app)
        self.assertIn('contentHours',app)
        self.assertIn('hoursPerOrder',app)
    def test_checklist_does_not_request_identity(self):
        html=(ROOT/'index.html').read_text(encoding='utf8')
        for disallowed in ['passportNumber','identityNumber','creditCardNumber']:
            self.assertNotIn(disallowed,html)
    def test_unique_element_ids(self):
        parser=IDS();parser.feed((ROOT/'index.html').read_text(encoding='utf8'))
        self.assertEqual(len(parser.ids),len(set(parser.ids)))
    def test_existing_controls_bind(self):
        html=(ROOT/'index.html').read_text(encoding='utf8')
        parser=IDS();parser.feed(html)
        for id in ['rewardViews','rewardVerified','rewardRegion','rewardAge','rewardPremium','rewardResult','zeroOrders','hourly','contentHours','hoursPerOrder']:
            self.assertIn(id,parser.ids)
    def test_mobile_nav_exists(self):
        self.assertIn('mobile-quicknav',(ROOT/'index.html').read_text(encoding='utf8'))
    def test_no_unverified_income_guarantees(self):
        docs=' '.join(p.read_text(encoding='utf8') for p in (ROOT/'chapters').glob('*.md'))
        self.assertIsNone(re.search(r'保证.{0,5}(月入|首单|收益)',docs))
    def test_release_log_transparency(self):
        self.assertIn('未能获取新版有效截图',(ROOT/'research/adversarial-dialogue.md').read_text(encoding='utf8'))

if __name__=='__main__':unittest.main()
