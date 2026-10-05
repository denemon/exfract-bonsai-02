from pathlib import Path
import argparse,hashlib,json
from PIL import Image
import numpy as np
parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
args.output.mkdir(parents=True,exist_ok=True);assert not any(args.output.iterdir()),'Choose an empty output directory'
rows=[]
for name in ['mineral','moss']:
 source=args.source/(name+'.png');target=args.output/(name+'.webp');im=Image.open(source).convert('RGBA');im.save(target,'WEBP',quality=86,method=6,exact=True)
 original=np.array(im);decoded=np.array(Image.open(target).convert('RGBA'));assert np.array_equal(original[:,:,3],decoded[:,:,3]),'Microheight alpha changed'
 rows.append({'name':name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'runtime_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'runtime_bytes':target.stat().st_size,'height_alpha_identical':True,'rgb_mean_absolute_error_255':float(np.abs(original[:,:,:3].astype(float)-decoded[:,:,:3].astype(float)).mean())})
(args.output/'compression.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
