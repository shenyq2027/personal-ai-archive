#!/usr/bin/env python3
"""Dependency-free structural checks; never a guarantee of public safety."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ['identity/profile.md', 'identity/goals.md', 'workflow/preferences.md',
            'workflow/tools.md', 'workflow/priorities.md', 'memory/inbox.md',
            'memory/lessons.md', 'memory/decisions.md', 'skills/inventory.md',
            'skills/learning-plan.md', 'archive/project-template.md', 'START-HERE.md',
            'AGENTS.md', 'ai-integration.md', 'SECURITY.md', 'docs/setup-report.md']
PATTERNS = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
            r'\bgh[pousr]_[A-Za-z0-9]{30,}\b',
            r'\bgithub_pat_[A-Za-z0-9_]{30,}\b',
            r'\bAKIA[A-Z0-9]{16}\b', r'\bsk-[A-Za-z0-9_-]{32,}\b']

def validate(root=ROOT):
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append('Missing required file: ' + name)
    files = [p for p in root.rglob('*') if '.git' not in p.relative_to(root).parts
             and '__pycache__' not in p.parts]
    for p in files:
        if p.is_symlink():
            errors.append('Symlink forbidden: ' + str(p.relative_to(root)))
            continue
        if not p.is_file():
            continue
        if p.stat().st_size > 1024 * 1024:
            errors.append('File exceeds 1 MB: ' + str(p.relative_to(root)))
            continue
        if p.name.startswith('.env') or p.suffix in {'.pem', '.key'}:
            errors.append('Credential file forbidden: ' + str(p.relative_to(root)))
        try:
            content = p.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            errors.append('Non-UTF-8 file forbidden: ' + str(p.relative_to(root)))
            continue
        if any(re.search(pattern, content) for pattern in PATTERNS):
            errors.append('Possible secret in ' + str(p.relative_to(root)))
        if p.suffix != '.md':
            continue
        if not re.match(r'^# AI-(?:READONLY|WRITABLE): .+', content):
            errors.append('Missing AI header: ' + str(p.relative_to(root)))
        for link in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', content):
            if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', link) or link.startswith('#'):
                continue
            target = (p.parent / unquote(link.split('#')[0])).resolve()
            if not target.is_relative_to(root.resolve()) or not target.exists():
                errors.append('Broken/unsafe relative link in ' + str(p.relative_to(root)) + ': ' + link)
    return errors

if __name__ == '__main__':
    problems = validate()
    if problems:
        print('\n'.join(problems), file=sys.stderr)
        sys.exit(1)
    print('PASS: required structure, AI headers, UTF-8 files, links and secret-pattern checks')
    print('NOTE: automated checks do not establish consent or detect all sensitive content.')
