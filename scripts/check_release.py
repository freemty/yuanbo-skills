#!/usr/bin/env python3
"""Offline manifest, invocation, executable hook and release-version parity."""
import json
from pathlib import Path
import re
import sys
from skill_inventory import discover, parse_frontmatter

ROOT=Path(__file__).resolve().parents[1]

def check(root=ROOT):
    errors=[]
    for plugin in sorted((root/'plugins').iterdir()):
        manifests=[p for p in [plugin/'package.json',plugin/'.claude-plugin/plugin.json',plugin/'.codex-plugin/plugin.json'] if p.is_file()]
        values={}
        for path in manifests:
            try:
                data=json.loads(path.read_text())
                version=data['version']
                if not re.fullmatch(r'\d+\.\d+\.\d+',version): raise ValueError('invalid version')
                values[path]=version
                if '.codex-plugin' in str(path) and 'agents' in data:
                    errors.append(f'{path}: Codex manifest declares agents')
                for key in ('skills','agents','hooks'):
                    entries=data.get(key,[])
                    if isinstance(entries,str): entries=[entries]
                    for entry in entries:
                        if not (plugin/entry).exists():
                            errors.append(f'{path}: missing {key} component {entry}')
            except (KeyError,ValueError,TypeError) as exc:
                errors.append(f'{path}: {exc}')
        if len(set(values.values()))>1:
            errors.append(f'{plugin}: version parity {list(values.values())}')
        expected=next(iter(values.values()),None)
        for readme in [plugin/'README.md',plugin/'README_ZH.md',plugin/'CLAUDE.md']:
            if not readme.is_file(): continue
            text=readme.read_text()
            for version in re.findall(r'version-(\d+\.\d+\.\d+)-|Version (\d+\.\d+\.\d+)',text):
                if next(v for v in version if v)!=expected:
                    errors.append(f'{readme}: release documentation version differs')
        hook_config=plugin/'hooks/hooks.json'
        if hook_config.exists():
            config=json.loads(hook_config.read_text())['hooks']
            for groups in config.values():
                for group in groups:
                    for handler in group['hooks']:
                        command=handler['command']
                        if 'run-hook.cmd' in command:
                            name=command.split()[-1]
                            if not (plugin/'hooks'/name).is_file():
                                errors.append(f'{hook_config}: missing handler {name}')
                            if not (plugin/'hooks/run-hook.cmd').stat().st_mode & 0o111:
                                errors.append(f'{plugin}: hook runner is not executable')
    for item in discover(root):
        path=item['path']
        fm=parse_frontmatter(path.read_text())
        if fm and fm.get('disable-model-invocation')=='true':
            policy=path.parent/'agents/openai.yaml'
            if not policy.exists() or not re.search(r'^\s+allow_implicit_invocation:\s*false\s*$',policy.read_text(),re.M):
                errors.append(f'{path}: explicit skill lacks matching Codex policy')
    recipes=json.loads((root/'plugins/meta-audit/hook-recipes/recipes.json').read_text())
    for recipe in recipes:
        if recipe.get('status')!='adapter-template-not-installed' or recipe.get('mutates') is not False or not recipe.get('argv'):
            errors.append(f'Invalid declarative hook recipe: {recipe.get("id")}')
    return errors

if __name__=='__main__':
    errors=check()
    for error in errors: print('ERROR',error)
    if not errors: print('release manifest, policy, recipe and hook parity passed')
    raise SystemExit(bool(errors))
