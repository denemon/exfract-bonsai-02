from pathlib import Path
import json,struct,copy,hashlib,gzip
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/coherent-core-0514');old=R.parent/'ancient-volume-0810/site/public/models/hero-low.glb';native=R/'models/core-v01.glb'
def read(p):
 b=p.read_bytes();assert b[:4]==b'glTF';l=struct.unpack_from('<I',b,12)[0];j=json.loads(b[20:20+l]);start=20+l;bl=struct.unpack_from('<I',b,start)[0];return j,b[start+8:start+8+bl]
a,ab=read(old);b,bb=read(native);original=copy.deepcopy(a);offset=len(a['accessors']);a['accessors']+=copy.deepcopy(b['accessors']);replacements={};rows=[]
for sourceIndex,oldMesh,oldView in [(0,25,13),(1,24,12)]:
 mesh=copy.deepcopy(b['meshes'][sourceIndex]);prim=mesh['primitives'][0]
 for key in prim['attributes']:prim['attributes'][key]+=offset
 prim['indices']+=offset;view=b['bufferViews'][prim['extensions']['KHR_draco_mesh_compression']['bufferView']];replacements[oldView]=bb[view.get('byteOffset',0):view.get('byteOffset',0)+view['byteLength']];prim['extensions']['KHR_draco_mesh_compression']['bufferView']=oldView;prim['material']=3 if sourceIndex==0 else 2;a['meshes'][oldMesh]=mesh
 oldNode=next(n for n in a['nodes']if n.get('mesh')==oldMesh);oldNode['extras']=copy.deepcopy(b['nodes'][sourceIndex]['extras'])
chunks=[];cursor=0
for i,view in enumerate(a['bufferViews']):
 prior=original['bufferViews'][i];source=ab[prior.get('byteOffset',0):prior.get('byteOffset',0)+prior['byteLength']];data=replacements.get(i,source)
 padding=(-cursor)%4
 if padding:chunks.append(b'\0'*padding);cursor+=padding
 view['byteOffset']=cursor;view['byteLength']=len(data);view['buffer']=0;chunks.append(data);cursor+=len(data)
 if i not in replacements:assert data==source
 rows.append({'bufferView':i,'unchanged':i not in replacements,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
bin=b''.join(chunks);bin+=b'\0'*((-len(bin))%4);a['buffers']=[{'byteLength':len(bin)}];a['asset']['generator']='Local lossless GLB wood replacement; preserved native foliage/accessors/buffer bytes; no geometry re-encoding';a['extras']={'local_model':'core-v01','native_wood_export_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'foliage_preserved_bit_exactly':True}
for i,node in enumerate(a['nodes']):
 if node.get('mesh')not in [24,25]:assert node==original['nodes'][i]
for i,mesh in enumerate(a['meshes']):
 if i not in [24,25]:assert mesh==original['meshes'][i]
js=json.dumps(a,separators=(',',':')).encode();js+=b' '*((-len(js))%4);raw=struct.pack('<4sII',b'glTF',2,12+8+len(js)+8+len(bin))+struct.pack('<I4s',len(js),b'JSON')+js+struct.pack('<I4s',len(bin),b'BIN\0')+bin;compressed=gzip.compress(raw,compresslevel=9,mtime=0);out=R/'models/hero-core-v01.glb.gz';out.write_bytes(compressed);assert gzip.decompress(out.read_bytes())==raw
(R/'qa/compact-model-proof.json').write_text(json.dumps({'method':'Lossless binary substitution at the two existing wood nodes; unchanged foliage native node/mesh/accessor/instance data, repacked exact original bufferViews; no Draco re-encoding','native_version':'core-v01','original_glb_bytes':old.stat().st_size,'compact_raw_bytes':len(raw),'compact_gzip_bytes':len(compressed),'original_shared_gzip_bytes':(old.with_suffix('.glb.gz')).stat().st_size,'no_extra_wood_request':True,'raw_sha256':hashlib.sha256(raw).hexdigest(),'gzip_sha256':hashlib.sha256(compressed).hexdigest(),'all_other_nodes_meshes_equal':True,'old_accessors_retained_metadata_only':True,'buffers':rows},separators=(',',':'))+'\n')
print(json.dumps({'raw':len(raw),'gzip':len(compressed),'old_gzip':(old.with_suffix('.glb.gz')).stat().st_size}))
