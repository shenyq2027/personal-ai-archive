from pathlib import Path
import importlib.util
import shutil
import subprocess
import tempfile
import os
source=Path(__file__).resolve().parents[1]
def run(args,cwd,ok=True):
 p=subprocess.run(args,cwd=cwd,text=True,capture_output=True)
 if ok and p.returncode: raise AssertionError(p.stdout+p.stderr)
 return p
with tempfile.TemporaryDirectory(prefix='archive-test-') as tmp:
 t=Path(tmp);remote=t/'remote.git';work=t/'archive'
 run(['git','init','--bare',str(remote)],t)
 shutil.copytree(source,work,ignore=shutil.ignore_patterns('.git','__pycache__'))
 run(['git','init','-b','main'],work)
 run(['git','config','user.name','Archive Test'],work);run(['git','config','user.email','archive-test@example.invalid'],work)
 run(['git','add','.'],work);run(['git','commit','-m','initial'],work)
 old=run(['git','rev-parse','HEAD'],work).stdout.strip()
 run(['git','remote','add','origin',str(remote)],work);run(['git','push','-u','origin','main'],work)
 # New snapshot changes content, deletes a file, and adds a file.
 (work/'workflow/preferences.md').write_text('# AI-WRITABLE: changed\n')
 (work/'archive/project-template.md').unlink()
 (work/'memory/new.md').write_text('# AI-WRITABLE: added later\n')
 run(['git','add','-A'],work);run(['git','commit','-m','changed snapshot'],work);run(['git','push'],work)
 # Bad SHA rejected without creating branch or changing history.
 before=run(['git','rev-parse','HEAD'],work).stdout
 assert run(['python3','scripts/restore.py','bad','--local-only'],work,False).returncode != 0
 assert run(['git','rev-parse','HEAD'],work).stdout==before
 # Ignored private files must never be overwritten by a historical snapshot.
 (work/'.git/info/exclude').write_text('archive/project-template.md\n')
 (work/'archive/project-template.md').write_text('private local note')
 p=run(['python3','scripts/restore.py',old,'--local-only'],work,False)
 assert p.returncode and 'ignored local file' in p.stderr
 assert (work/'archive/project-template.md').read_text()=='private local note'
 (work/'archive/project-template.md').unlink()
 print('PASS: ignored private files are preserved on restore collision')
 # Full recovery must recreate the exact tracked tree, including deletion/recreation.
 run(['python3','scripts/restore.py',old,'--local-only'],work)
 recovered=run(['git','rev-parse','HEAD^{tree}'],work).stdout
 assert recovered==run(['git','rev-parse',old+'^{tree}'],work).stdout
 assert not (work/'memory/new.md').exists()
 assert (work/'archive/project-template.md').exists()
 # Main still points to the later snapshot; restored tree is isolated in a new commit.
 assert run(['git','rev-parse','main'],work).stdout==before
 assert run(['git','rev-parse','HEAD'],work).stdout!=old+'\n'
 print('PASS: full snapshot recovery, added/deleted file handling, isolated PR branch, invalid SHA rejection')
 run(['git','switch','main'],work)
 run(['python3','scripts/restore.py',old,'--core-only','--local-only'],work)
 assert (work/'archive/project-template.md').exists() and not (work/'memory/new.md').exists()
 print('PASS: five-directory Actions recovery')
 # Structural and secret checks must fail on actual bad files, not just pass good fixtures.
 run(['python3','scripts/validate.py'],work)
 (work/'memory/bad.md').write_text('wrong header\n[broken](missing.md)\n'+'ghp_'+'a'*36+'\n')
 p=run(['python3','scripts/validate.py'],work,False)
 assert p.returncode and all(term in p.stderr for term in ['Missing AI header','Broken/unsafe','Possible secret'])
 (work/'memory/bad.md').unlink()
 (work/'memory/link.md').symlink_to('/etc/passwd')
 p=run(['python3','scripts/validate.py'],work,False);assert p.returncode and 'Symlink forbidden' in p.stderr
 print('PASS: bad headers, broken links, secret patterns and symlink detection')
