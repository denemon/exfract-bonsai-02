from pathlib import Path
import os,json,hashlib,tarfile,subprocess
ROOT=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02');DAY=ROOT/'improvement/2026-10-04';RUN=DAY/'runs/irregular-volume-1200'
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
for prior in ['local-structure-2122','anatomy-2150','integrated-form-2245','wood-surface-0000','local-edges-0056','night-garden-0144','night-finish-0235','growth-ground-0335','space-ground-0430','ancient-volume-0810','ensemble-0915','hand-junction-1029','compact-mass-1106']:
    folder=DAY/'runs'/prior;m=json.loads((folder/'delivery-manifest.json').read_text())
    for name,entry in m['files'].items():assert sha(folder/name)==entry['sha256'],(prior,name)
    links=m.get('read_only_references',m.get('symlinks',{}))
    for name,target in links.items():assert os.readlink(folder/name)==target and (folder/name).exists(),(prior,name)
    protected[prior]={'delivery_files':len(m['files']),'symlinks':len(links),'manifest_sha256':sha(folder/'delivery-manifest.json')}
env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'}
protected['git_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,env=env,text=True).strip()
protected['tracked_status']=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,env=env,text=True).rstrip('\n')
protected['git_head_at_start']='576a85c5d9603572dfc6aff9249fcf1c1c26f43c'
protected['external_git_change']=protected['git_head']!=protected['git_head_at_start']
protected['parent_external_notice']='Parent reports external archived completed studies/PR5; active run excluded. Local archival commits observed read-only. No Git write by this worker.'
protected['tracked_status_allowed_coordinator_paths']=['improvement/2026-10-04/HANDOFF.md','improvement/2026-10-04/IMPROVEMENT_PLAN.md','improvement/2026-10-04/run-state.json']
for row in protected['tracked_status'].splitlines():
 assert row[3:] in protected['tracked_status_allowed_coordinator_paths'],row
for name in ['best-state.json','candidate-state.json','geometry-state.json','integrated-study-state.json','wood-study-state.json','local-edge-study-state.json','night-garden-study-state.json','night-finish-study-state.json','growth-ground-study-state.json','space-ground-study-state.json','ancient-volume-study-state.json','ensemble-study-state.json','hand-junction-study-state.json','compact-mass-study-state.json']:
    protected[name]={'sha256':sha(DAY/name)}
start=json.loads((RUN/'start.json').read_text())
assert sha(Path(start['protected_basis_native']))==start['protected_basis_native_sha256']
assert protected['compact-mass-1106']['manifest_sha256']==start['protected_stage15_manifest_sha256']
for name,h in start['protected_state_sha256'].items():assert sha(DAY/name)==h
protected['authorized_reused_profile']='Only local-structure-2122/qa/browser-profile was reused, which is excluded from that stage delivery manifest.'
protected['authorized_shared_mutable_cache']='Stage14 qa/vite-cache explicitly excluded from immutable delivery manifest; shared in stage16; included in footprint.'
protected['old_project']='No writes to the old project. No old-project access in this stage.'
output=RUN/(os.environ.get('AUDIT_OUTPUT','integrity-verification-after-records.json'));assert not output.exists();output.write_text(json.dumps(protected,indent=2)+'\n')
print(json.dumps(protected,indent=2))
