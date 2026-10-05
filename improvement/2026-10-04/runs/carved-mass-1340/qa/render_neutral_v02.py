from pathlib import Path
p=Path(__file__).with_name('render_neutral.py')
s=p.read_text().replace('carved-v01-editable.blend','carved-v02-editable.blend').replace('qa/neutral-render.json','qa/neutral-render-v02.json').replace('qa/neutral','qa/neutral-v02')
# Keep metadata filename explicit after common prefix replacement.
s=s.replace('neutral-v02-render-v02','neutral-render-v02')
exec(compile(s,str(p),'exec'))
