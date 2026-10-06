from pathlib import Path
import json
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/organic-ensemble-1017');P=R.parent/'idle-causality-0935'
d=json.loads((P/'qa/performance-protocol.json').read_text());d.update({'stage':34,'run':R.name,'candidate':'living-v01/aged-growth-v01/unequal-occupied-v02/grown-interior-crowns-v02/stable','urls':{'r31':'http://127.0.0.1:5215/compare/r31/','candidate':'http://127.0.0.1:5215/compare/r34/'},'diagnosticConditions':[],'componentIsolation':'One finite14cohort active pairedforward/reverse seven-code-condition390 run, uninstrumented, no profile. Shapes/material/near/far and exactR31content control separated via explicit source flags. Not qualification or proof of driver/GC cause.','R32AndR33FailuresUnresolvedAndRetained':True,'qualificationRepeatCountAllowed':0,'thresholdChangeCount':0})
with(R/'qa/performance-protocol.json').open('x')as f:json.dump(d,f,indent=2)
t=(P/'qa/cohort.mjs').read_text().replace('runs/idle-causality-0935','runs/organic-ensemble-1017').replace("['diagnostic','frame','idle','cold']","['factor','frame','idle','cold']").replace('ChromePID:34202','ChromePID:61609').replace("'20598,20741'","'20598,61609'")
a=t.index('const variants=');b=t.index('const variant=sequences',a)
variants="""const control='?candidate=grown-v02&wood-surface=baseline&near-shape=baseline&near-growth=baseline&far-shape=baseline&terrain-density=baseline';
const variants={r31:config.urls.r31,candidate:config.urls.candidate,control:config.urls.candidate+control,shape:config.urls.candidate+control.replace('grown-v02','living-v01'),near:config.urls.candidate+'?candidate=grown-v02&wood-surface=baseline&far-shape=baseline',far:config.urls.candidate+control.replace('&far-shape=baseline',''),surface:config.urls.candidate+control.replace('wood-surface=baseline','wood-surface=aged-v01')};
const seq=['r31','control','shape','near','far','surface','candidate'];const sequences={frame:['r31','candidate','candidate','r31','candidate','r31','r31','candidate'],idle:['r31','candidate','candidate','r31','candidate','r31','r31','candidate'],cold:['r31','candidate','candidate','r31'],factor:[...seq,...seq.slice().reverse()]};"""
t=t[:a]+variants+t[b:];t=t.replace("const diagnostic=mode==='diagnostic',idle=mode!=='frame'","const diagnostic=false,idle=mode==='idle'").replace("mode!=='diagnostic'","true").replace("'old-both'","'old-both'")
with(R/'qa/cohort.mjs').open('x')as f:f.write(t)
with(R/'qa/component-batch.py').open('x')as f:f.write("""from pathlib import Path
import subprocess,os
R=Path(__file__).resolve().parents[1]
with(R/'qa/component-console.log').open('x')as log:
 for c in range(14):
  p=subprocess.run(['node','qa/cohort.mjs','factor','mobile-390',str(c)],cwd=R,capture_output=True,text=True);log.write(p.stdout+p.stderr);log.flush();os.fsync(log.fileno());print(p.stdout.strip(),flush=True);assert p.returncode==0,p.stderr
print('COMPONENT14_COMPLETE_EXCLUSIVE_RAW',flush=True)
""")
print('Fixed9tolerances retained; finite component14 protocol and exclusive checkpoint writer prepared.')
