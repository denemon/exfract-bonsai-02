from pathlib import Path
from PIL import Image
import io,base64,json,hashlib,re
r=Path(__file__).resolve().parent;rules=[];images=[]
conditions=[('desktop',None),('wide','(min-aspect-ratio:2/1)'),('square','(max-aspect-ratio:4/3)'),('portrait','(orientation:portrait)'),('320','(orientation:portrait) and (max-width:340px)'),('tall','(max-aspect-ratio:2/5)')]
for name,condition in conditions:
 img=Image.open(r/'qa/final-still-source'/f'{name}.png').convert('RGB');img.thumbnail((384,512),Image.Resampling.LANCZOS);stream=io.BytesIO();img.save(stream,'WEBP',quality=62,method=6);b=stream.getvalue();data=base64.b64encode(b).decode();rule='main{background-image:url(data:image/webp;base64,'+data+');}'
 if condition:rule='@media '+condition+'{'+rule+'}'
 rules.append(rule);images.append({'view':name,'size':img.size,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
s=(r/'site/index.html').read_text();s=re.sub(r'\s*<style id="initial-scene">.*?</style>','',s,flags=re.S);s=s.replace('    <title>庭</title>','    <title>庭</title>\n    <style id="initial-scene">main{background-size:cover;background-position:center}'+''.join(rules)+'</style>')
(r/'site/index.html').write_text(s);(r/'site/public/initial-still-manifest.json').write_text(json.dumps({'model':'hero-v23.glb','source':'same six actual WebGL screenshots as high-resolution stills','images':images,'total_image_bytes':sum(x['bytes'] for x in images)},indent=2)+'\n');print({'inline_image_bytes':sum(x['bytes'] for x in images),'html_bytes':len(s.encode())})
