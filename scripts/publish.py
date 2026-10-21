#!/usr/bin/env python3
"""Publish an initialized archive and verify remote protection. Requires GitHub CLI."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
GH = os.environ.get('PERSONAL_ARCHIVE_GH') or shutil.which('gh')

def run(args, capture=True):
    return subprocess.check_output(args, cwd=ROOT, text=True).strip() if capture else subprocess.check_call(args, cwd=ROOT)

def api(path, method='GET', data=None):
    args = [GH, 'api', path, '--method', method]
    if data is not None:
        args += ['--input', '-']
    p = subprocess.run(args, input=json.dumps(data) if data is not None else None,
                       cwd=ROOT, text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip())
    return json.loads(p.stdout) if p.stdout.strip() else None

def main():
    if not GH:
        raise RuntimeError('GitHub CLI missing; install from https://cli.github.com/')
    run([sys.executable, 'scripts/validate.py'], capture=False)
    run([GH, 'auth', 'status'], capture=False)
    if run(['git', 'rev-parse', '--show-toplevel']) != str(ROOT):
        raise RuntimeError('Initialize this folder as a separate Git repository first.')
    if run(['git', 'status', '--porcelain']):
        raise RuntimeError('Commit reviewed local changes before publishing.')
    if run(['git', 'branch', '--show-current']) != 'main':
        raise RuntimeError('Initial publication must run from main.')
    owner = api('user')['login']
    name = owner + '/personal-ai-archive'
    # Query via owner repository list to distinguish absence from authorization/network failure.
    repos = json.loads(run([GH, 'api', '--paginate', '--slurp', 'user/repos?per_page=100&affiliation=owner']))
    exists = any(repo['full_name'].lower() == name.lower() for page in repos for repo in page)
    if not exists:
        api('user/repos', 'POST', {'name':'personal-ai-archive', 'private':False,
            'description':'Portable personal AI memory: Markdown profiles, preferences and lessons',
            'auto_init':False})
    repo = api('repos/' + name)
    if repo['private']:
        raise RuntimeError('Existing repository is private; refusing to change visibility automatically.')
    url = repo['clone_url']
    origins = run(['git', 'remote']).splitlines()
    if 'origin' in origins:
        origin = run(['git', 'remote', 'get-url', 'origin'])
        if origin.rstrip('/') != url.rstrip('/'):
            raise RuntimeError('Unexpected origin; refusing to overwrite remote.')
    else:
        run(['git', 'remote', 'add', 'origin', url])
    run([GH, 'auth', 'setup-git'], capture=False)
    # Ordinary push rejects unrelated or diverged existing history; never force.
    run(['git', 'push', '-u', 'origin', 'main'], capture=False)
    api('repos/' + name, 'PATCH', {'default_branch':'main', 'delete_branch_on_merge':True,
        'allow_auto_merge':True, 'allow_squash_merge':True})
    protection = {'required_status_checks':{'strict':True, 'contexts':['archive-validation']},
        'enforce_admins':True, 'required_pull_request_reviews':{
            'dismiss_stale_reviews':True, 'require_code_owner_reviews':False,
            'required_approving_review_count':0},
        'restrictions':None, 'required_linear_history':False,
        'allow_force_pushes':False, 'allow_deletions':False,
        'block_creations':False, 'required_conversation_resolution':True,
        'lock_branch':False, 'allow_fork_syncing':False}
    api('repos/' + name + '/branches/main/protection', 'PUT', protection)
    api('repos/' + name + '/actions/permissions/workflow', 'PUT',
        {'default_workflow_permissions':'read', 'can_approve_pull_request_reviews':True})
    check = api('repos/' + name + '/branches/main/protection')
    assert check['enforce_admins']['enabled']
    assert not check['allow_force_pushes']['enabled']
    assert not check['allow_deletions']['enabled']
    assert check['required_status_checks']['strict']
    assert 'archive-validation' in check['required_status_checks']['contexts']
    assert 'required_pull_request_reviews' in check
    settings = api('repos/' + name + '/actions/permissions/workflow')
    assert settings['default_workflow_permissions'] == 'read'
    final = api('repos/' + name)
    assert not final['private'] and final['default_branch'] == 'main'
    remote = run(['git', 'ls-remote', 'origin', 'refs/heads/main']).split()[0]
    local = run(['git', 'rev-parse', 'HEAD'])
    assert remote == local
    print(json.dumps({'repository':final['html_url'], 'visibility':'public', 'commit':remote,
                      'main_protection_verified':True, 'actions_default_permission':'read'}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError, AssertionError) as e:
        sys.exit('Publication not fully verified: ' + str(e))
