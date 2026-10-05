from pathlib import Path
import json
from mathutils import Vector
R=Path(__file__).resolve().parents[1];s=(R/'sculpt/build_compact.py').read_text().split('bpy.context.view_layer.update();evaluated=')[0];scope={'__file__':str(R/'sculpt/build_compact.py')};exec(compile(s,str(R/'sculpt/build_compact.py'),'exec'),scope)
V=scope['V'];rows=scope['rows'];parts=scope['parts'];out={}
for name in ['Rear upper primary','Rear descending subordinate']:
 r=rows[name];sections=[[V[i]for i in ring]for ring in r];cost=[]
 for a,b in zip(sections,sections[1:]):cost.append([sum((Vector(a[k])-Vector(b[(k+j)%4])).length_squared for k in range(4))for j in range(4)])
 out[name]={'section_points':sections,'correspondence_costs_per_cyclic_shift':cost,'part':parts[name]}
p=R/'qa/phase-inspection.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
# One isolation case; no candidate export/native/image.
s=(R/'sculpt/build_compact.py').read_text().split('assert boundary==')[0];s='\n'.join(l for l in s.splitlines()if not l.startswith("branch('Rear descending subordinate'"));s=s.replace('qa/intersection-locations.json','qa/local-without-secondary-intersections.json').replace('qa/geometry-inspection.json','qa/local-without-secondary-inspection.json');exec(compile(s,str(R/'sculpt/build_compact.py'),'exec'),{'__file__':str(R/'sculpt/build_compact.py')})
