"""Offline adapter behavior, not a substitute for native/model live evaluation."""
import contextlib
import importlib.util
import io
import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('fetch', pathlib.Path(__file__).with_name('fetch.py'))
f = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = f
spec.loader.exec_module(f)


class FetchTests(unittest.TestCase):
    def test_short_post_and_attribution(self):
        root = {'id': '1', 'text': 'Hi', 'user': {'screenName': 'a'}}
        reply = {'id': '2', 'text': 'Follow-up', 'user': {'screenName': 'a'}}
        other = {'id': '3', 'text': 'Comment', 'user': {'screenName': 'b'}, 'media': [{'url': 'https://example.org/m', 'type': 'video'}]}
        result = f.format_conversation([other, root, reply], 'https://x.com/a/status/1')
        self.assertEqual(result.status, 'ok')
        self.assertLess(result.content.index('Root post'), result.content.index('Author replies'))
        self.assertIn('Other accounts', result.content)
        self.assertIn('not inspected', result.content)
        with self.assertRaises(ValueError):
            f.format_conversation([other], 'https://x.com/a/status/1')

    def test_quality(self):
        self.assertEqual(f.assess('A valid short statement.', 'https://example.org', 'test').status, 'ok')
        for content in ['# Access denied\n' + 'Try again ' * 200, '[Home](/) [Login](/login)', '<html><nav>Home</nav><script>hello</script></html>']:
            with self.assertRaises(ValueError):
                f.assess(content, 'https://example.org', 'test')
        self.assertEqual(f.assess('Title and description', 'https://youtube.com/watch?v=a', 'test').content_kind, 'video_metadata')
        self.assertEqual(f.assess('Abstract only', 'https://arxiv.org/abs/1234.56789', 'test').status, 'partial')

    def test_html_video_is_not_video_observation(self):
        result=f.assess('<html><article>A demo description</article></html>','https://youtu.be/a','raw')
        self.assertEqual(result.content_kind,'video_metadata')
        self.assertEqual(result.status,'partial')
        self.assertTrue(any('frames' in item for item in result.limitations))

    def test_caption_formats(self):
        fixtures = {
            'vtt': 'WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nHello <b>world</b>\n',
            'srt': '1\n00:00:01,000 --> 00:00:02,000\nHello world\n',
            'json3': json.dumps({'events': [{'tStartMs': 1000, 'dDurationMs': 1000, 'segs': [{'utf8': 'Hello world'}]}]}),
            'srv1': '<transcript><text start="1" dur="1">Hello world</text></transcript>',
        }
        for ext, raw in fixtures.items():
            self.assertEqual(f.parse_captions(raw, ext), ['[00:00:01.000 --> 00:00:02.000] Hello world'])

    def test_video_coverage(self):
        data = {'title': 'Demo', 'description': 'A demo'}
        with patch.object(f, '_run', return_value=json.dumps(data)):
            result = f.fetch_via_ytdlp('https://youtu.be/a', None)
            self.assertEqual((result.status, result.content_kind), ('partial', 'video_metadata'))
        data['subtitles'] = {'en': [{'ext': 'vtt', 'url': 'https://example.org/caption'}]}
        with patch.object(f, '_run', return_value=json.dumps(data)), patch.object(f, 'fetch_url', return_value='00:00:01.000 --> 00:00:02.000\nHello\n'):
            result = f.fetch_via_ytdlp('https://youtu.be/a', None)
            self.assertEqual(result.content_kind, 'video_captions')
            self.assertTrue(any('No frames' in x for x in result.limitations))

    def test_cli_envelope_and_markdown(self):
        with patch.object(f, 'PLATFORM_ROUTES', []), patch.object(f, 'GENERIC_STRATEGIES', [('fixture', lambda _: 'Short content')]):
            for fmt in ['markdown', 'json']:
                with tempfile.TemporaryDirectory() as tmp:
                    out = pathlib.Path(tmp) / 'output'
                    with patch.object(sys, 'argv', ['fetch.py', 'https://example.org', '--format', fmt, '-o', str(out)]):
                        self.assertEqual(f.main(), 0)
                    text = out.read_text()
                    if fmt == 'json':
                        result = json.loads(text)
                        self.assertEqual(set(result), {'source_url', 'retrieved_at', 'backend', 'status', 'content_kind', 'content', 'limitations'})
                        self.assertEqual(result['content'], 'Short content')
                    else:
                        self.assertIn('Short content', text)
                        self.assertIn('Coverage: ok', text)
        self.assertEqual(f.fetch_result('file:///tmp/a')['status'], 'unsupported')

    def test_missing_adapter_and_blocked(self):
        with patch.object(f.shutil, 'which', return_value=None), patch.object(f, 'GENERIC_STRATEGIES', [('offline', lambda _: 'Fallback content')]):
            self.assertEqual(f.fetch_result('https://youtu.be/a')['status'], 'partial')
        with patch.object(f, 'PLATFORM_ROUTES', []), patch.object(f, 'GENERIC_STRATEGIES', [('gate', lambda _: '# Access denied')]):
            self.assertEqual(f.fetch_result('https://example.org')['status'], 'blocked')


if __name__ == '__main__':
    unittest.main()
