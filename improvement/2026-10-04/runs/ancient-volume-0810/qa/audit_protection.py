from pathlib import Path
import os,json,hashlib,tarfile,subprocess
ROOT=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02');DAY=ROOT/'improvement/2026-10-04';RUN=DAY/'runs/ancient-volume-0810'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024**2),b''):h.update(block)
    return h.hexdigest()
protected={}
for part in ['source','production']:
    folder=DAY/'runs/0900-jst';m=json.loads((folder/(part+'-manifest.json')).read_text())
    assert sha(folder/m['archive'])==m['archive_sha256']
    for name,entry in m['files'].items():assert sha(ROOT/name)==entry['sha256'],name
    protected['root_'+part+'_files']=len(m['files'])
folder=DAY/'baseline-initial';m=json.loads((folder/'manifest.json').read_text())
assert sha(folder/m['archive'])==m['archive_sha256']
with tarfile.open(folder/m['archive']) as tar:
    for name,entry in m['files'].items():assert hashlib.sha256(tar.extractfile(name).read()).hexdigest()==entry['sha256'],name
protected['initial_archive_entries']=len(m['files'])
folder=DAY/'runs/volume-rebuild-1656';m=json.loads((folder/'delivery-manifest.json').read_text());archive_checks=[]
for name,entry in m['archives'].items():
    assert sha(folder/name)==entry['sha256']
    for f,e in entry['files'].items():assert sha(folder/f)==e['sha256'],f
    archive_checks.append({'archive':name,'live_files':len(entry['files'])})
protected['stage_two_archives_and_files']=archive_checks
for prior in ['local-structure-2122','anatomy-2150','integrated-form-2245','wood-surface-0000','local-edges-0056','night-garden-0144','night-finish-0235','growth-ground-0335','space-ground-0430']:
    folder=DAY/'runs'/prior;m=json.loads((folder/'delivery-manifest.json').read_text())
    for name,entry in m['files'].items():assert sha(folder/name)==entry['sha256'],(prior,name)
    links=m.get('read_only_references',m.get('symlinks',{}))
    for name,target in links.items():assert os.readlink(folder/name)==target and (folder/name).exists(),(prior,name)
    protected[prior]={'delivery_files':len(m['files']),'symlinks':len(links),'manifest_sha256':sha(folder/'delivery-manifest.json')}
env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'}
protected['git_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,env=env,text=True).strip()
protected['tracked_status']=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,env=env,text=True).strip()
assert protected['git_head']=='576a85c5d9603572dfc6aff9249fcf1c1c26f43c' and not protected['tracked_status']
for name in ['best-state.json','candidate-state.json','geometry-state.json','integrated-study-state.json','wood-study-state.json','local-edge-study-state.json','night-garden-study-state.json','night-finish-study-state.json','growth-ground-study-state.json','space-ground-study-state.json']:
    protected[name]={'sha256':sha(DAY/name)}
start=json.loads((RUN/'start.json').read_text())
assert sha(Path(start['protected_basis_native']))==start['protected_basis_native_sha256']
assert protected['space-ground-0430']['manifest_sha256']==start['protected_stage11_manifest_sha256']
for name,h in start['protected_state_sha256'].items():assert sha(DAY/name)==h
protected['authorized_reused_profile']='Only local-structure-2122/qa/browser-profile was reused, which is excluded from that stage delivery manifest.'
protected['old_project']='No writes to the old project. A read-only filename search on resume listed sibling project paths; their contents and tracked files were not changed.'
output=RUN/'integrity-verification-after-records.json';assert not output.exists();output.write_text(json.dumps(protected,indent=2)+'\n')
print(json.dumps(protected,indent=2))
