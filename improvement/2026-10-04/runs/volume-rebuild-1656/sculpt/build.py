from pathlib import Path
import sys,subprocess,shutil,gzip,hashlib,json,argparse
root=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser();parser.add_argument('version');parser.add_argument('--support',default=str(root/'models/hero-v20.blend'));args=parser.parse_args();version=args.version
if not version.startswith('v') or not version[1:].isdigit():raise ValueError('Use vNN')
prefix=root/'models'/('hero-'+version)
if any(prefix.with_suffix(s).exists() for s in ['.json','.blend','.glb']):raise FileExistsError('Version already exists')
subprocess.run([sys.executable,str(root/'sculpt/field.py'),'--out',str(root/'models'),'--version',version],check=True,cwd=root)
subprocess.run(['node',str(root/'sculpt/extract.mjs'),str(prefix)],check=True,cwd=root)
shutil.copy2(root/'sculpt/extract.mjs',prefix.parent/(prefix.name+'.extract.mjs'))
subprocess.run(['/Applications/Blender.app/Contents/MacOS/Blender','--background','--factory-startup','--python-exit-code','1','--python',str(root/'sculpt/assemble.py'),'--','--prefix',str(prefix),'--support',str(Path(args.support).resolve())],check=True,cwd=root)
shutil.copy2(prefix.with_suffix('.glb'),root/'site/public/models/hero.glb')
# Reproducible intermediate arrays consume much more disk than the model itself.
# Preserve their exact bytes in verified gzip files, rather than keep raw duplicates.
archives=[]
for suffix in ['.field.f32','.triangles.f32']:
 p=prefix.with_suffix(suffix);raw=p.read_bytes();archive=p.with_name(p.name+'.gz')
 if archive.exists():raise FileExistsError(archive)
 with gzip.open(archive,'wb',compresslevel=6) as f:f.write(raw)
 with gzip.open(archive,'rb') as f:restored=f.read()
 assert restored==raw
 archives.append({'file':p.name,'archive':archive.name,'bytes':len(raw),'archive_bytes':archive.stat().st_size,'sha256':hashlib.sha256(raw).hexdigest()});p.unlink()
prefix.with_suffix('.archive.json').write_text(json.dumps(archives,indent=2));print(json.dumps({'installed':str(prefix.with_suffix('.glb')),'archives':archives}))
