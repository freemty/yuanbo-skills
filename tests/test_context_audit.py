#!/usr/bin/env python3
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'plugins/meta-audit/scripts'))
from context_audit import audit, resources
from skill_inventory import discover, parse_frontmatter

class Contracts(unittest.TestCase):
    def test_frontmatter(self):
        for value, expected in [('"Use when: reading URLs"', 'Use when: reading URLs'),
                                ("'Use when it''s needed'", "Use when it's needed"),
                                ('>\n  Use when reading\n  a long document', 'Use when reading a long document'),
                                ('|\n  first line\n  second line', 'first line\nsecond line')]:
            fm = parse_frontmatter('---\nname: demo\ndescription: '+value+'\nallowed-tools: Read, Bash\nmetadata:\n  host: codex\n---\nBody')
            self.assertEqual(fm['description'],expected)
            self.assertIn('allowed-tools',fm)
        self.assertIsNone(parse_frontmatter('---\nname: missing-close'))
        self.assertEqual(parse_frontmatter('---\nname: demo\ndescription: "Use when\n  reading text"\n---')['description'], 'Use when reading text')
        self.assertEqual(parse_frontmatter("---\nname: demo\ndescription: 'Use when\n  reading text'\n---")['description'], 'Use when reading text')
        self.assertIsNone(parse_frontmatter('---\nname: demo\ndescription: "text" invalid\n---'))

    def test_scope_references_and_policy(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'install.sh').touch()
            (root/'plugins').mkdir()
            skill=root/'skills/demo/SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('---\nname: demo\ndescription: "Use when: testing"\n---\nRead [ref](references/a.md).\n')
            ref=skill.parent/'references/a.md'
            ref.parent.mkdir()
            ref.write_text('Read [nested](b.md).\n' + 'MUST do only authorized work.\n'*10)
            (ref.parent/'b.md').write_text('Valid knowledge.')
            workspace=root/'.agents/skills/caveman/SKILL.md'
            workspace.parent.mkdir(parents=True)
            workspace.write_text('---\nname: caveman\ndescription: test\n---\n')
            (root/'projects/selfos/wiki').mkdir(parents=True)
            (root/'projects/selfos/wiki/SKILL.md').write_text('not an entrypoint')
            self.assertEqual(len(discover(root)),1)
            self.assertEqual(len(discover(root,True)),2)
            result=audit(root)
            self.assertEqual(result['summary']['errors'],0)
            self.assertTrue(result['skills'][0]['findings']) # warning, not failure
            self.assertEqual(len(result['skills'][0]['resources']),3)
            ref.write_text('Read [broken](missing.md).')
            self.assertGreater(audit(root)['summary']['errors'],0)
            ref.write_text('Example [link](...).')
            policy=skill.parent/'agents/openai.yaml'
            policy.parent.mkdir()
            policy.write_text('policy:\n  allow_implicit_invocation: maybe\n')
            self.assertGreater(audit(root)['summary']['errors'],0)
            policy.write_text('policy:\n  allow_implicit_invocation: false\n')
            self.assertEqual(audit(root)['summary']['errors'],0)

    def test_directory_and_wiki_skill_references(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            skill=root/'projects/selfos/.claude/skills/wiki/SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('Read `references/`.')
            ref=skill.parent/'references/contract.md'
            ref.parent.mkdir()
            ref.write_text('Read [missing](missing.md).')
            loaded, errors=resources(skill,root)
            self.assertIn(ref.resolve(),loaded)
            self.assertTrue(errors)

    def test_actual_repository(self):
        result=audit(ROOT)
        expected=discover(ROOT)
        self.assertEqual(result['summary']['skill_count'],len(expected))
        self.assertEqual(result['summary']['errors'],0)
        raw=subprocess.check_output([sys.executable,str(ROOT/'scripts/skill_inventory.py'),str(ROOT),'--null'])
        self.assertEqual([str(p['path']).encode() for p in expected],raw.rstrip(b'\0').split(b'\0'))
        self.assertTrue(str(expected[0]['path']).startswith(str(ROOT/'skills')))
        print(f"discovery parity: {len(expected)} public entries")

if __name__=='__main__':
    unittest.main()
