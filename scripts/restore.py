#!/usr/bin/env python3
"""Create a recovery branch/PR; do not rewrite main or execute restored code."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CORE = ['identity', 'workflow', 'memory', 'skills', 'archive']

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

def restore(target, core_only=False):
    if git('status', '--porcelain'):
        raise RuntimeError('Working tree must be clean.')
    subprocess.check_call(['git', 'fetch', 'origin', 'main'], cwd=ROOT)
    if not re.fullmatch(r'[0-9a-fA-F]{40}', target):
        raise RuntimeError('Use a full 40-character commit SHA.')
    git('cat-file', '-e', target + '^{commit}')
    subprocess.check_call(['git', 'merge-base', '--is-ancestor', target, 'origin/main'], cwd=ROOT)
    tree = git('ls-tree', '-r', target)
    if any(line.startswith('120000 ') or line.startswith('160000 ') for line in tree.splitlines()):
        raise RuntimeError('Refusing snapshot with symlinks/submodules.')
    # read-tree can overwrite ignored local files: reject any path collision first.
    target_paths = git('ls-tree', '-r', '--name-only', '-z', target).split('\0')
    ignored = git('ls-files', '--others', '--ignored', '--exclude-standard', '-z').split('\0')
    for local in filter(None, ignored):
        if any(path and (path == local or path.startswith(local + '/') or local.startswith(path + '/'))
               for path in target_paths):
            raise RuntimeError('Snapshot conflicts with an ignored local file; move it outside the repository first.')
    branch = 'restore/' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    git('switch', '-c', branch, 'origin/main')
    if core_only:
        git('restore', '--source=' + target, '--staged', '--worktree', '--', *CORE)
    else:
        git('read-tree', '--reset', '-u', target)
    if not git('diff', '--cached', '--name-only'):
        raise RuntimeError('No changes: requested snapshot already matches.')
    git('commit', '-m', 'restore: recover snapshot ' + target)
    return branch

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('commit')
    p.add_argument('--core-only', action='store_true', help='Restore only the five personal archive directories')
    p.add_argument('--local-only', action='store_true', help='Create local recovery branch without pushing or PR')
    a = p.parse_args()
    try:
        if git('rev-parse', '--show-toplevel') != str(ROOT):
            raise RuntimeError('Run from the separately initialized archive repository.')
        branch = restore(a.commit, a.core_only)
        print('Created local recovery branch:', branch)
        if not a.local_only:
            gh = os.environ.get('PERSONAL_ARCHIVE_GH') or shutil.which('gh')
            if not gh:
                raise RuntimeError('Local recovery created; gh missing, no PR published.')
            subprocess.check_call(['git', 'push', '-u', 'origin', branch], cwd=ROOT)
            body = ('Restores ' + ('the five personal archive directories' if a.core_only else 'the complete tracked file tree')
                    + ' to commit ' + a.commit + '.\n\nReview the diff and current validation results before merging. '
                    'Main history and remote protection settings are preserved.\n')
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.md') as f:
                f.write(body);f.flush()
                subprocess.check_call([gh,'pr','create','--base','main','--head',branch,
                    '--title','restore: recover archive snapshot ' + a.commit[:12], '--body-file',f.name], cwd=ROOT)
    except (RuntimeError, subprocess.CalledProcessError) as e:
        sys.exit('Recovery not fully published: ' + str(e))
