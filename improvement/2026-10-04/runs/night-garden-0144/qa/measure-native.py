import bpy,json
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath='/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/local-edges-0056/models/edge-v02-editable.blend')
rows=[]
for ob in bpy.context.scene.objects:
 if ob.type!='MESH' or ob.get('foliage_lod_template') or any(x in ob.name.lower() for x in ['canopy','foliage','twig','shoot','particle','terminal']):continue
 ps=[ob.matrix_world@Vector(p) for p in ob.bound_box];lo=[min(p[i] for p in ps)*.66 for i in range(3)];hi=[max(p[i] for p in ps)*.66 for i in range(3)]
 rows.append({'name':ob.name,'native_scaled_xyz_min':lo,'native_scaled_xyz_max':hi,'world_x_y_z_min':[lo[0],lo[2],-hi[1]],'world_x_y_z_max':[hi[0],hi[2],-lo[1]]})
print('MEASURE_JSON '+json.dumps(rows))
