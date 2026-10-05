from pathlib import Path
import bpy,bmesh,json
from mathutils import Vector
R=Path(__file__).resolve().parents[1];source=(R/'sculpt/build_compact.py').read_text();exec(compile(source.split('bpy.context.view_layer.update();evaluated=')[0],str(R/'sculpt/build_compact.py'),'exec'))
bm=bmesh.new();bm.from_mesh(mesh);bm.normal_update()
if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(mesh)
bm.free()
target=Vector((.65,.275,1.57));tests=[]
for band in [0,1]:
 for k in range(4):
  ids=[rows['Rear upper primary'][band][k],rows['Rear upper primary'][band][(k+1)%4],rows['Rear upper primary'][band+1][(k+1)%4],rows['Rear upper primary'][band+1][k]]
  cen=sum((Vector(V[i])for i in ids),Vector())/4;n=(Vector(V[ids[1]])-Vector(V[ids[0]])).cross(Vector(V[ids[2]])-Vector(V[ids[1]])).normalized();direction=(target-cen).normalized()
  tests.append({'band':band,'sector':k,'center':list(cen),'normal_by_indices':list(n),'normal_dot_target':n.dot(direction),'ids':ids})
result={'parts':parts,'ports':tests,'points':V,'faces':faces}
p=R/'qa/port-inspection-before-repair.json';assert not p.exists();p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(tests),flush=True)
