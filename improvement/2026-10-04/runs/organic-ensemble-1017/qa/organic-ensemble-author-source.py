from pathlib import Path
import json
S=Path('/Users/kazuki.tanaka/Documents/Codex/2026-10-04/task-2');R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/organic-ensemble-1017')
t=(S/'aged-ensemble-author-native.py').read_text().replace('runs/aged-ensemble-0831','runs/organic-ensemble-1017').replace("version='aged-v01';source=R.parent/'grown-core-0554/models/grown-v02-editable.blend'","version='living-v01';source=R.parent/'aged-ensemble-0831/models/aged-v01-editable.blend'")
t=t.replace('smooth(.58,.76,max(owners[k]))','smooth(.70,.88,max(owners[k]))').replace('smooth(.22,.40,contour)','smooth(.06,.28,contour)').replace('if d.length>.022:d*=.022/d.length','if d.length>.072:d*=.072/d.length')
tools=[
 {'name':'rising-main-bearing-volume','anchors':[[.04,-.14,.63],[.015,-.16,.83],[-.08,-.13,1.04],[-.17,-.065,1.225],[-.06,-.085,1.413]],'widths':[.095,.158,.182,.176,.108],'deltas':[[0,0,0],[.012,-.032,.005],[.018,-.060,.008],[-.012,-.048,.012],[0,-.004,0]]},
 {'name':'inner-turn-open-compression-plane','anchors':[[.14,-.075,.73],[.11,-.065,.88],[-.015,-.055,1.07],[-.145,-.012,1.265]],'widths':[.086,.12,.148,.10],'deltas':[[0,0,0],[-.009,.022,.004],[.012,.026,-.010],[0,0,0]]},
 {'name':'side-return-growth-thickness','anchors':[[.055,.08,.72],[.07,.09,.93],[-.13,.07,1.24],[-.11,.08,1.38]],'widths':[.09,.158,.16,.105],'deltas':[[0,0,0],[.009,.025,.002],[-.015,.041,.009],[0,0,0]]},
 {'name':'mother-fork-load-bearing-shoulder','anchors':[[-.13,-.09,1.30],[-.055,-.094,1.41],[.08,-.074,1.483],[.19,-.047,1.526],[.31,-.015,1.57]],'widths':[.098,.135,.108,.068,.042],'deltas':[[0,0,0],[-.010,-.025,.008],[.010,-.036,.032],[.006,-.014,.017],[0,0,0]]},
 {'name':'branch-under-return-with-open-exit','anchors':[[.011,-.067,1.425],[.12,-.072,1.478],[.24,-.050,1.514]],'widths':[.083,.064,.04],'deltas':[[0,0,0],[.003,.010,-.015],[0,0,0]]},
 {'name':'upper-stem-irregular-bearing-plane','anchors':[[-.03,-.055,1.46],[.085,-.030,1.55],[.155,-.006,1.66]],'widths':[.078,.099,.060],'deltas':[[0,0,0],[-.010,-.025,.008],[0,0,0]]}
]
a=t.index('tools=[');b=t.index('\ntree=BVHTree',a);t=t[:a]+'tools='+repr(tools)+t[b:]
t=t.replace("'stage':32","'stage':34").replace('Five','Five').replace("'five_view_tangent_contour_guard':True","'five_view_soft_tangent_guard':True").replace('Four coupled finite surface strokes defining one rising bearing face with side-opening compression and one supported mother-branch shoulder; no noise, longparallel grooves or ringcollar','Six coupled C2 finite large/middle volume strokes: uneven ascending front/back bearing planes, inner-turn compression opening along growth and a thick load-bearing fork shoulder. Direct closed surface authoring; no surface noise or ring dents.').replace('R29 major shape retained; finite bearing faces and short compression planes directly sculpted into closed native surface','R32 root and terminal domains retained; major/middle bearing volume and supported fork shoulder directly authored into closed native surface')
with(R/'qa/author-living-v01.py').open('x')as f:f.write(t)
v=(S/'aged-ensemble-verify-native-v01.py').read_text().replace('runs/aged-ensemble-0831','runs/organic-ensemble-1017').replace('aged-v01','living-v01').replace("'stage':32","'stage':34").replace("'exact_positions_and_119_changed_records':True","'exact_positions_and_changed_records':len(changed)").replace("'protected4106_exact':True","'protected_positions_exact':len(rec['protected_vertex_ids'])")
with(R/'qa/verify-living-v01.py').open('x')as f:f.write(v)
c=(S/'age-leaf-compact.py').read_text().replace('runs/age-leaf-0342','runs/organic-ensemble-1017').replace('age-v01','living-v01')
with(R/'qa/compact-living-v01.py').open('x')as f:f.write(c)
print('New native author/roundtrip/lossless compact helpers authored, old sources read-only.')
