from pathlib import Path
import json
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/organic-ensemble-1017');P=R.parent/'idle-causality-0935';S=Path('/Users/kazuki.tanaka/Documents/Codex/2026-10-04/task-2')
t=(S/'growth-garden-static-verify.mjs').read_text().replace('runs/growth-garden-0729','runs/organic-ensemble-1017').replace('/compare/r31/','/compare/r34/').replace("'grown-v02'","'living-v01'").replace("'near-shore-v02'","'organic-occupied-v01'").replace('existingChromePID:72496','existingChromePID:61609')
a=t.index(',old=await readFile(');b=t.index(';captures.push',a);t=t[:a]+',same=false'+t[b:];a=t.index('const same=results.every');b=t.index('await writeFile(join(out',a);t=t[:a]+"const same=false;for(const {v,bytes}of captures)await writeFile(join(target,v.name+'.webp'),bytes,{flag:'wx'});\n"+t[b:]
with(R/'qa/capture-own-final-stills.mjs').open('x')as f:f.write(t)
for name in['verify-own-functional.mjs','verify-selected-dynamic-qualified.mjs']:
 t=(P/'qa'/name).read_text().replace('runs/idle-causality-0935','runs/organic-ensemble-1017').replace('/compare/r32/','/compare/r34/').replace('aged-v01','living-v01').replace('aged-r32-final-v01','organic-r34-final-v02').replace('low-occupied-rootshade-v01','organic-occupied-v01').replace('34202','61609')
 with(R/'qa'/name).open('x')as f:f.write(t)
t=(S/'aged-ensemble-inline-freeze.py').read_text().replace('runs/aged-ensemble-0831','runs/organic-ensemble-1017').replace('/compare/r32/','/compare/r34/').replace('aged-r32-final-v01','organic-r34-final-v02').replace('fixed-aged-shape-v01','fixed-living-shape-v01').replace('aged-v01/normal-aged-growth-v01/low-occupied-rootshade-v01','living-v01/normal-aged-growth-v01/organic-occupied-v02').replace("'background/distant-crowns.js'","'background/distant-crowns.js','background/broadleaf-support.js'").replace('aged-v01/aged-growth-v01/low-occupied-rootshade-v01','living-v01/aged-growth-v01/organic-occupied-v02')
with(R/'qa/inline-and-source-freeze.py').open('x')as f:f.write(t)
j={'name':'final-candidate-and-retina','cases':[]}
for dpr in[1,2]:
 for name,w,h in[('pc',1440,900),('mobile-390',390,844),('mobile-320',320,568)]:
  j['cases'].append({'name':name+('-dpr2'if dpr==2 else''),'w':w,'h':h,'dpr':dpr,'url':'http://127.0.0.1:5215/compare/r34/','eval':'(()=>{const g=window.__garden,p=g.stats.garden.planting;return {retina:{devicePixelRatio,rendererPixelRatio:g.renderer.getPixelRatio(),drawingBuffer:[g.renderer.domElement.width,g.renderer.domElement.height]},version:g.stats.model.authoringVersion,near:p.leafInstances,far:p.evergreenStats.instances,rootContacts:g.stats.garden.terrain.rootContacts,contacts:g.stats.garden.contacts,smallStones:g.stats.garden.scatteredSmallStoneObjects}})()'})
with(R/'qa/jobs/final-candidate-and-retina.json').open('x')as f:json.dump(j,f,separators=(',',':'))
print('Own final5WebP, inline synchronization, functional11/dynamic6 and6actualDPRphotos prepared; not executed or claimed yet.')
