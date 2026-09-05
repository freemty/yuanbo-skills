#!/usr/bin/env python3
"""Enumerate authored instruction surfaces for a review ledger (read-only)."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from skill_inventory import discover

ROOT=Path(__file__).resolve().parents[1]
BASELINE='b6aee12f8d23149d1ecfeed1ea1c60ed6c2adf0c'
TEXT_SUFFIXES={'.md','.py','.sh','.json','.yaml','.yml','.tex','.cls','.html','.css','.mplstyle','.cmd'}

def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()

def in_scope(path):
    parts=Path(path).parts
    if any(p in {'__pycache__','node_modules'} for p in parts): return False
    if path.startswith('projects/selfos/'):
        return path.startswith('projects/selfos/.claude/skills/')
    if path.startswith(('scripts/','tests/')): return True
    if not path.startswith(('skills/','plugins/')): return False
    # Exclude historical research/archive/product data; keep executable references.
    if any(marker in '/'+path for marker in ('/docs/','/profiles/','/overviews/','/outputs/')): return False
    return Path(path).name in {'SKILL.md','skill.md'} or any(
        p in {'references','guides','agents','scripts','hooks','templates','template'} for p in parts)

def inventory():
    modules=[]
    for line in git(ROOT,'ls-tree','-r',BASELINE).splitlines():
        meta,path=line.split('\t',1)
        if meta.startswith('160000 '):
            modules.append((path,meta.split()[2]))
    repositories=[('',BASELINE)]+modules
    records={}
    for prefix,base in repositories:
        repo=ROOT/prefix
        tracked=git(repo,'ls-files','--cached','--others','--exclude-standard').splitlines()
        previous=git(repo,'ls-tree','-r','--name-only',base).splitlines()
        changed=set(git(repo,'diff','--name-only',base).splitlines())
        for name in sorted(set(tracked+previous)):
            path=str(Path(prefix)/name)
            local=ROOT/path
            if not in_scope(path) or (local.suffix not in TEXT_SUFFIXES and 'hooks' not in local.parts): continue
            if local.is_dir() or local.is_symlink(): continue
            before=name in previous
            exists=local.is_file()
            if not before and not exists: continue
            action='delete' if not exists else 'rewrite' if not before or name in changed else 'retain'
            reason='Preserve domain knowledge, schema or existing adapter; test coverage is reported separately.'
            if action=='rewrite': reason='Capability/evidence or scope contract revised; see batch diffs and regression report.'
            if action=='delete': reason='Removed redundant or conflicting instruction; retained in Git history.'
            if '/cc-navigator/references/' in path and 'ecosystem-' not in path:
                reason='Preserve dated external source notes as historical examples, not execution mandates.'
            if path.endswith('claude-code-agents.md'):
                reason='Claude-only host schema examples retained and scope clarified; not portable role requirements.'
            if path.endswith('web-fetcher/references/routing-and-fallbacks.md'):
                action='merge'; reason='Replaced by capability-selection, source-adapters and media-evidence references.'
            records[path]={'path':path,'action':action,'reason':reason,
                'sha256':hashlib.sha256(local.read_bytes()).hexdigest() if exists else None}
    entries=[{'path':str(x['path'].relative_to(ROOT)),'scope':x['scope']} for x in discover(ROOT)]
    return {'baseline':BASELINE,'entries':entries,'resources':[records[p] for p in sorted(records)]}

if __name__=='__main__':
    print(json.dumps(inventory(),ensure_ascii=False,indent=2))
