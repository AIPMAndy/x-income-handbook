import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/content.json').read_text(encoding='utf8'))

class DataQualityTests(unittest.TestCase):
    def test_26_chapters(self):self.assertEqual(len(D['chapters']),26)
    def test_7_routes(self):self.assertEqual(len(D['routes']),7)
    def test_30_tasks(self):self.assertEqual(len(D['days']),30)
    def test_sequential_chapter_ids(self):self.assertEqual([c['id'] for c in D['chapters']],[f'{i:02d}' for i in range(1,27)])
    def test_sequential_days(self):self.assertEqual([d['day'] for d in D['days']],list(range(1,31)))
    def test_route_ids_unique(self):self.assertEqual(len(set(x['id'] for x in D['routes'])),7)
    def test_source_indices_valid(self):
        for c in D['chapters']:
            with self.subTest(c=c['id']):self.assertTrue(all(isinstance(x,int) and 0<=x<len(D['sources']) for x in c['sources']))
    def test_every_chapter_has_steps(self):
        for c in D['chapters']:
            with self.subTest(c=c['id']):self.assertGreaterEqual(len(c['steps']),3)
    def test_every_chapter_has_pitfalls(self):
        for c in D['chapters']:
            with self.subTest(c=c['id']):self.assertGreaterEqual(len(c['pitfalls']),1)
    def test_every_chapter_has_deliverable(self):self.assertTrue(all(c['deliverable'] for c in D['chapters']))
    def test_every_chapter_has_metric(self):self.assertTrue(all(c['metric'] for c in D['chapters']))
    def test_every_source_https(self):self.assertTrue(all(s['url'].startswith('https://') for s in D['sources']))
    def test_creator_rewards_documented(self):self.assertIn('500,000',' '.join(next(c for c in D['chapters'] if c['id']=='19')['steps']))
    def test_china_mainland_disclosure(self):self.assertIn('未列出中国大陆',' '.join(next(c for c in D['chapters'] if c['id']=='19')['steps']))
    def test_replies_excluded_from_threshold(self):self.assertIn('回复不计入门槛',' '.join(next(c for c in D['chapters'] if c['id']=='19')['steps']))
    def test_no_guaranteed_income_in_first_chapter(self):self.assertNotIn('保证赚钱',D['chapters'][0]['why'])
    def test_sources_have_names(self):self.assertTrue(all(s['name'] for s in D['sources']))
    def test_sources_no_duplicates(self):self.assertEqual(len(set(s['url'] for s in D['sources'])),len(D['sources']))
    def test_contact_on_homepage(self):self.assertIn('AIPMAndy',(ROOT/'index.html').read_text(encoding='utf8'))
    def test_official_policy_on_homepage(self):self.assertIn('original-content-rewards',(ROOT/'index.html').read_text(encoding='utf8'))
    def test_template_count(self):self.assertEqual(len(list((ROOT/'templates').iterdir())),24)
    def test_document_coverage(self):self.assertEqual(len(list((ROOT/'chapters').glob('*.md'))),26)
    def test_local_progress_is_local(self):self.assertIn('localStorage',(ROOT/'assets/app.js').read_text(encoding='utf8'))
    def test_deployment_config(self):self.assertIn('actions/deploy-pages@v4',(ROOT/'.github/workflows/pages.yml').read_text(encoding='utf8'))
    def test_legal_disclaimer(self):self.assertIn('不构成税务',(ROOT/'README.md').read_text(encoding='utf8'))

if __name__=='__main__':unittest.main()
