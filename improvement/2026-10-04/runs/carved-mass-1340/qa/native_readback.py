from pathlib import Path
import bpy,bmesh,json,hashlib
R=Path(__file__).resolve().parents[1];results=[]
for version,recordfile in [('carved-v01','sculpt-record.json'),('carved-v02','sculpt-record-v02.json')]:
 record=json.loads((R/'sculpt'/recordfile).read_text());native=R/'models'/f'{version}-editable.blend';bpy.ops.wm.open_mainfile(filepath=str(native));objects=[o for o in bpy.data.objects if o.type=='MESH'];assert len(objects)==1;o=objects[0];me=o.data
 positions=hashlib.sha256(json.dumps([list(v.co)for v in me.vertices]).encode()).hexdigest();faces=hashlib.sha256(json.dumps([list(f.vertices)for f in me.polygons]).encode()).hexdigest();assert positions==record['positions_sha256'] and faces==record['faces_sha256'];assert o['authoring_version']==version and len(o.modifiers)==0
 groups={g.name:[v.index for v in me.vertices if any(a.group==g.index for a in v.groups)]for g in o.vertex_groups}
 if version=='carved-v01':assert groups==record['groups']
 else:
  assert [(name,len(ids))for name,ids in groups.items()]==[tuple(v)for v in record['groups']]
  assert {u.name:hashlib.sha256(json.dumps([list(v.uv)for v in u.data]).encode()).hexdigest()for u in me.uv_layers}==record['uv_sha256']
 assert len(me.uv_layers)==3 and len(me.color_attributes)==1
 bm=bmesh.new();bm.from_mesh(me);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();assert boundary==nonmanifold==0 and volume>0
 sections=[]
 for z in [.36,.45,.52,.65,.98,1.18]:
  cross={};links={}
  for poly in me.polygons:
   keys=[];vs=list(poly.vertices)
   for a,b in zip(vs,vs[1:]+vs[:1]):
    A=me.vertices[a].co;B=me.vertices[b].co
    if (A.z-z)*(B.z-z)<0:
     key=tuple(sorted((a,b)));cross[key]=list(A.lerp(B,(z-A.z)/(B.z-A.z)));keys.append(key)
   if len(keys)==2:
    a,b=keys;links.setdefault(a,set()).add(b);links.setdefault(b,set()).add(a)
  pending=set(links);components=[]
  while pending:
   first=pending.pop();stack=[first];ids=[first]
   while stack:
    for j in links[stack.pop()]:
     if j in pending:pending.remove(j);stack.append(j);ids.append(j)
   components.append({'sample_count':len(ids),'closed_loop':all(len(links[i])==2 for i in ids),'min':[min(cross[i][k]for i in ids)for k in range(3)],'max':[max(cross[i][k]for i in ids)for k in range(3)]})
  sections.append({'height_z':z,'components':components})
 results.append({'version':version,'native_readable':True,'exact_positions_faces_match_saved_record':True,'groups_preserved':True,'uv_and_provisional_roles_preserved':True,'modifiers':len(o.modifiers),'boundary':boundary,'nonmanifold':nonmanifold,'volume':volume,'native_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'sections':sections,'resaved':False,'aesthetic_selection':False})
(R/'qa/native-readback.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps([{'version':v['version'],'exact_readback':True,'section_components':[len(s['components'])for s in v['sections']]}for v in results]),flush=True)
