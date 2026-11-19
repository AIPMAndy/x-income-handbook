"""SEO, source-of-truth and interaction contract for the standalone experiment workbench."""
import json
import re
import subprocess
import unittest
from html.parser import HTMLParser
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = "https://aipmandy.github.io/x-income-handbook/"
class IdParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            assert d["id"] not in self.ids, d["id"]
            self.ids.add(d["id"])
        for prop in ("href", "src"):
            if (v := d.get(prop, "")).startswith("#"):
                self.refs.append(v[1:])
class ExperimentTests(unittest.TestCase):
    def test_experiment_page_seo(self):
        html = (ROOT/"experiment.html").read_text(encoding="utf-8")
        self.assertIn(f'<link rel="canonical" href="{BASE}experiment.html">', html)
        self.assertIn('https://www.a6no1.cn/', html)
        self.assertIn('https://metaver.vip/services', html)
        self.assertIn('AIPMAndy', html)
        self.assertIn('不宣称其内容在本日逐项重新核验', html)
        scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        self.assertEqual(len(scripts), 1)
        graph = json.loads(scripts[0])
        self.assertEqual(graph["@type"], "WebPage")
        self.assertEqual(graph["url"], BASE+"experiment.html")
        self.assertTrue(all(x.startswith("https://") for x in graph["citation"]))
        self.assertIn("experiment.html", (ROOT/"sitemap.xml").read_text(encoding="utf-8"))
        parser = IdParser();parser.feed(html)
        self.assertTrue(all(ref in parser.ids for ref in parser.refs))
        for id in ("recordForm","totalLeads","recordsBody","exportCsv","copyWechat"):
            self.assertIn(id, parser.ids)
    def test_js_and_exports(self):
        script = (ROOT/"assets/experiment.js").read_text(encoding="utf-8")
        self.assertIn("localStorage", script)
        self.assertIn("safeCsv", script)
        self.assertIn("textContent", script)
        self.assertNotIn("innerHTML", script)
        for f in ("assets/experiment.css", "assets/experiment.js", "experiment.html", "scripts/experiment_unit.cjs"):
            self.assertTrue((ROOT/f).is_file())
        subprocess.run(["node","--check",str(ROOT/"assets/experiment.js")], check=True, cwd=ROOT)
        subprocess.run(["node",str(ROOT/"scripts/experiment_unit.cjs")], check=True, cwd=ROOT)
if __name__ == "__main__":
    unittest.main()
