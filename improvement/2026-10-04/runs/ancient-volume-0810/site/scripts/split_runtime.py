from pathlib import Path
import json,struct,copy,gzip,hashlib,argparse
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--bounds',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();assert not a.output.exists();a.output.mkdir()
b=a.source.read_bytes();n,typ=struct.unpack_from('<II',b,12);d=json.loads(b[20:20+n]);offset=20+n;blen,btype=struct.unpack_from('<II',b,offset);blob=b[offset+8:offset+8+blen];source=copy.deepcopy(d);bounds={x['variant']:x for x in json.loads(a.bounds.read_text())['results'][0]['foliageTemplateBounds']}
def glb(g,data,out):
 views=set()
 for ac in g['accessors']:
  if 'bufferView'in ac:views.add(ac['bufferView'])
 for m in g['meshes']:
  for prim in m['primitives']:
   x=prim.get('extensions',{}).get('KHR_draco_mesh_compression')
   if x:views.add(x['bufferView'])
 old=g['bufferViews'];new=[];body=bytearray();mapping={}
 for i in sorted(views):
  v=copy.deepcopy(old[i]);begin=v.get('byteOffset',0);raw=data[begin:begin+v['byteLength']];body.extend(b'\0'*((-len(body))%4));v['buffer']=0;v['byteOffset']=len(body);body.extend(raw);mapping[i]=len(new);new.append(v)
 for ac in g['accessors']:
  if 'bufferView'in ac:ac['bufferView']=mapping[ac['bufferView']]
 for m in g['meshes']:
  for prim in m['primitives']:
   x=prim.get('extensions',{}).get('KHR_draco_mesh_compression')
   if x:x['bufferView']=mapping[x['bufferView']]
 g['bufferViews']=new;g['buffers']=[{'byteLength':len(body)}];js=json.dumps(g,separators=(',',':')).encode();js+=b' '*((-len(js))%4);body.extend(b'\0'*((-len(body))%4));out.write_bytes(struct.pack('<III',0x46546c67,2,12+8+len(js)+8+len(body))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(body),0x004e4942)+body)
low={int(m['name'].split()[-1]):m for m in d['meshes']if m['name'].startswith('Volumetric scale shoot low ')};high={int(m['name'].split()[-1]):m for m in d['meshes']if m['name'].startswith('Volumetric scale shoot ')and ' low 'not in m['name']};assert len(low)==len(high)==len(bounds)==12
fine={'asset':copy.deepcopy(d['asset']),'extensionsUsed':['KHR_draco_mesh_compression'],'extensionsRequired':['KHR_draco_mesh_compression'],'scene':0,'scenes':[{'nodes':list(range(12))}],'nodes':[],'meshes':[],'accessors':[],'bufferViews':copy.deepcopy(d['bufferViews']),'materials':copy.deepcopy(d['materials'])}
for variant,m in sorted(high.items()):
 fine['nodes'].append({'name':f'Exact detailed foliage template {variant:02d}','mesh':len(fine['meshes']),'extras':{'high_template_variant':variant}});mesh=copy.deepcopy(m)
 for prim in mesh['primitives']:
  ids=list(prim['attributes'].values())+[prim['indices']];mapping={}
  for i in ids:
   if i not in mapping:mapping[i]=len(fine['accessors']);fine['accessors'].append(copy.deepcopy(d['accessors'][i]))
  prim['attributes']={k:mapping[i]for k,i in prim['attributes'].items()};prim['indices']=mapping[prim['indices']]
 fine['meshes'].append(mesh)
 m['primitives']=copy.deepcopy(low[variant]['primitives']);m.setdefault('extras',{})['deferred_high_bounds']=bounds[variant]
glb(fine,blob,a.output/'foliage-high.glb');glb(d,blob,a.output/'hero-low.glb')
for name in ['hero-low','foliage-high']:
 q=a.output/(name+'.glb');(a.output/(name+'.glb.gz')).write_bytes(gzip.compress(q.read_bytes(),compresslevel=9,mtime=0))
# The exact Draco bytes and instance transform bytes are split, never re-encoded.
rows={q.name:{'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}for q in a.output.iterdir()}
result={'source':str(a.source),'source_sha256':hashlib.sha256(b).hexdigest(),'source_bytes':len(b),'quality':'Original Draco geometry bytes, exact instance transforms and materials;12 high leaf prototypes fetched only on inspection. Authored high geometry envelopes preserved from actual decoded browser geometry.','files':rows,'initial_model_saving_bytes':len(b)-rows['hero-low.glb.gz']['bytes'],'detailed_template_count':12,'source_geometry_buffers_byte_identical':True};(a.output/'split-manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
