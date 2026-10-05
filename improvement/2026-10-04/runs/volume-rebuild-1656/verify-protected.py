from pathlib import Path
import hashlib,json,tarfile,subprocess,datetime,os
root=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02');day=root/'improvement/2026-10-04';report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':[]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for file in ['source-manifest.json','production-manifest.json']:
 folder=day/'runs/0900-jst';m=json.loads((folder/file).read_text());bad=[name for name,d in m['files'].items() if sha(root/name)!=d['sha256']];assert not bad,bad
 archive=folder/m['archive'];assert sha(archive)==m['archive_sha256'];report['checks'].append({'set':'09best '+file,'files':len(m['files']),'live_files_match':True,'archive_sha256_match':True})
folder=day/'baseline-initial';m=json.loads((folder/'manifest.json').read_text());archive=folder/m['archive'];assert sha(archive)==m['archive_sha256']
with tarfile.open(archive) as t:
 for name,d in m['files'].items():assert hashlib.sha256(t.extractfile(name).read()).hexdigest()==d['sha256'],name
report['checks'].append({'set':'initial archive','files':len(m['files']),'all_inner_sha256_match':True,'archive_sha256_match':True})
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0');head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,env=env,text=True).strip();status=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=root,env=env,text=True);assert head=='576a85c5d9603572dfc6aff9249fcf1c1c26f43c';assert not status
report['git']={'head':head,'tracked_status':status,'read_only_commands':True};report['best_state']=json.loads((day/'best-state.json').read_text());report['passed']=True
Path('integrity-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'sets':report['checks'],'head':head}))
