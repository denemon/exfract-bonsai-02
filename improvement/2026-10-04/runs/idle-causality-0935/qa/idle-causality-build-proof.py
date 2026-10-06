from pathlib import Path
import json,subprocess,hashlib
ROOT=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02');R=ROOT/'improvement/2026-10-04/runs/idle-causality-0935';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert (R/'qa/qualified-performance-summary.json').exists();rows=[]
for label,name in [('selected-r31','growth-garden-0729'),('candidate-r32','aged-ensemble-0831')]:
 P=R.parent/name;out=R/'qa'/('compiled-'+label);assert not out.exists()
 m=J(P/'delivery-manifest.json');before={n:H(P/n)for n in m['files']};assert all(before[n]==d['sha256']for n,d in m['files'].items())
 p=subprocess.run(['node',str(ROOT/'node_modules/vite/bin/vite.js'),'build','--config',str(P/'candidate/vite.config.mjs'),'--configLoader','native','--outDir',str(out)],cwd=P/'candidate',capture_output=True,text=True)
 with(R/'qa'/('build-'+label+'.log')).open('x')as f:f.write(p.stdout+p.stderr)
 assert p.returncode==0,p.stderr
 files={str(x.relative_to(out)):{'sha256':H(x),'bytes':x.stat().st_size,'exactProtectedProduction':H(x)==H(P/'candidate/dist'/x.relative_to(out))}for x in out.rglob('*')if x.is_file()};assert all(d['exactProtectedProduction']for d in files.values())
 assert all(H(P/n)==h for n,h in before.items())
 rows.append({'label':label,'run':name,'buildPassed':True,'freshIsolatedOutput':str(out),'files':files,'protectedFilesUnchanged':len(before),'protectedSourceAndProductionSHAExact':True})
with(R/'qa/final-build-proof.json').open('x')as f:json.dump({'rows':rows,'passed':True,'currentFrozenR31AndR32BuildsBothBitExactProduction':True,'oldDistOverwriteCount':0},f,indent=2)
print(json.dumps({'builds':2,'bothPass':True,'allGeneratedFilesExactProtectedProduction':True,'protectedOldFilesUnchanged':sum(r['protectedFilesUnchanged']for r in rows)},indent=2))
