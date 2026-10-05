"""Standalone vector engineering diagrams from exact control/slice coordinates."""
from pathlib import Path
import json,math,html,argparse
p=argparse.ArgumentParser();p.add_argument('--version',required=True);args=p.parse_args()
RUN=Path(__file__).resolve().parents[1];d=json.loads((RUN/'models'/f'{args.version}.json').read_text());sections=json.loads((RUN/'qa'/f'{args.version}-sections.json').read_text())
baseline=json.loads((RUN.parent/'wood-surface-0000/models/wood-v02.json').read_text())
style='<style>text{font-family:Arial,sans-serif;fill:#29332f;font-size:15px}.small{font-size:12px;fill:#526057}.title{font-size:21px;font-weight:bold}</style>'
def svg_head(w,h,title):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{style}<rect width="100%" height="100%" fill="#f1f0e9"/><text x="28" y="34" class="title">{html.escape(title)}</text>'
def loops(segments):
    points={};adj={};edges=set()
    for a,b in segments:
        ka=tuple(round(x,5) for x in a);kb=tuple(round(x,5) for x in b)
        if ka==kb:continue
        points[ka]=a;points[kb]=b;adj.setdefault(ka,set()).add(kb);adj.setdefault(kb,set()).add(ka);edges.add(tuple(sorted([ka,kb])))
    assert all(len(v)==2 for v in adj.values()),[(k,len(v)) for k,v in adj.items() if len(v)!=2]
    result=[]
    while edges:
        a,b=next(iter(edges));route=[a];previous=a;current=b;edges.remove(tuple(sorted([a,b])))
        while current!=a:
            route.append(current);nxt=next(x for x in adj[current] if x!=previous);edges.remove(tuple(sorted([current,nxt])));previous,current=current,nxt
        result.append([points[k] for k in route])
    return result
def inside(polygon):
    odd=False
    for a,b in zip(polygon,polygon[1:]+polygon[:1]):
        if (a[1]>0)!=(b[1]>0) and 0<(b[0]-a[0])*(-a[1])/(b[1]-a[1])+a[0]:odd=not odd
    return odd
def metrics(segments):
    contours=loops(segments);main=[x for x in contours if inside(x)];assert len(main)==1,len(main);line=main[0]
    area=abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(line,line[1:]+line[:1])))*.5
    return {'closed_contours':len(contours),'central_contour_area':area,'width':max(p[0] for p in line)-min(p[0] for p in line),'front_back_depth':max(p[1] for p in line)-min(p[1] for p in line),'front_extent':min(p[1] for p in line),'back_extent':max(p[1] for p in line),'raw_segments':len(segments)}
parts=[svg_head(1290,570,args.version+' / three perpendicular support sections')]
parts.append('<text x="28" y="61" class="small">Blue: protected wood-v02. Rust: local candidate. Central support contour only. Identical perpendicular planes. All raw cuts retained; units: metres.</text>')
summary=[]
for index,section in enumerate(sections['sections']):
    cx=218+index*425;cy=298;scale=450
    parts.append(f'<rect x="{cx-197}" y="88" width="394" height="400" fill="#faf9f5" stroke="#d5d8ce"/>')
    parts.append(f'<text x="{cx-180}" y="112">Above soil {section["height_above_soil"]:.2f} m</text>')
    for g in [-.3,-.2,-.1,0,.1,.2,.3]:
        x=cx+g*scale;y=cy-g*scale
        parts.append(f'<path d="M{x:.2f},132 V465 M{cx-181},{y:.2f} H{cx+181}" fill="none" stroke="#e0e3db" stroke-width="1"/>')
    parts.append(f'<text x="{cx-17}" y="136" class="small">BACK</text><text x="{cx-20}" y="476" class="small">FRONT</text>')
    measures={}
    for key,color in [('basis','#417891'),('candidate','#ac6244')]:
        measures[key]=metrics(section[key])
        contour=next(line for line in loops(section[key]) if inside(line))
        path=' '.join(('M' if i==0 else 'L')+f'{cx+point[0]*scale:.3f},{cy-point[1]*scale:.3f}' for i,point in enumerate(contour))+' Z'
        parts.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="#48514c"/>')
    b,c=measures['basis'],measures['candidate'];ratio=c['central_contour_area']/b['central_contour_area']
    parts.append(f'<text x="{cx-181}" y="516" class="small">Area {ratio*100:.2f}% of v02; depth {b["front_back_depth"]:.3f} → {c["front_back_depth"]:.3f} m</text>')
    parts.append(f'<text x="{cx-181}" y="537" class="small">Closed contour(s): {b["closed_contours"]} / {c["closed_contours"]}; central support contains axis.</text>')
    summary.append({'height_above_soil':section['height_above_soil'],**measures,'central_area_ratio':ratio})
parts.append('</svg>');(RUN/'qa'/f'{args.version}-sections.svg').write_text(''.join(parts))
(RUN/'qa'/f'{args.version}-section-metrics.json').write_text(json.dumps({'version':args.version,'method':'Join raw slice segments at 0.00001m precision, require degree2 closed contours, select the single contour containing the protected centreline and calculate area/depth. These structural measurements do not establish aesthetic quality.','sections':summary},indent=2)+'\n')

# Orthographic control-layout evidence: unchanged perimeter and independently
# editable added rail. It uses the actual net, without smoothing the lines.
parts=[svg_head(1290,680,args.version+' / local control edge layout')]
parts.append('<text x="28" y="62" class="small">Blue: original net. Dark green: authored net. Rust: new shoulder rail. Fixed perimeter: 40 controls; rear and attachments unchanged.</text>')
grid=d['grid_vertex_ids'];local_ids={k for row in grid for k in row}|{int(k) for k in d['added_vertex_parents']}
old_edges=set();new_edges=set()
for record,target in [(baseline,old_edges),(d,new_edges)]:
    for f in record['control_faces']:
        if all(k in local_ids for k in f):
            for j,k in enumerate(f):target.add(tuple(sorted([k,f[(j+1)%len(f)]])))
def projected(point,angle,cx):
    a=math.radians(angle);return cx+(point[0]*math.cos(a)+point[1]*math.sin(a))*620,595-(point[2]-.393)*780
for cx,angle in [(375,0),(1005,55)]:
    parts.append(f'<text x="{cx-260}" y="107">{"Front" if angle==0 else "55° oblique"} — control points before subdivision</text>')
    for record,edges,color in [(baseline,old_edges,'#78a2b4'),(d,new_edges,'#304e3d')]:
        path=[]
        for a,b in edges:
            if a>=len(record['control_vertices']) or b>=len(record['control_vertices']):continue
            x,y=projected(record['control_vertices'][a],angle,cx);xx,yy=projected(record['control_vertices'][b],angle,cx);path.append(f'M{x:.3f},{y:.3f} L{xx:.3f},{yy:.3f}')
        parts.append(f'<path d="{" ".join(path)}" fill="none" stroke="{color}" stroke-width="1.2"/>')
    for k in local_ids:
        x,y=projected(d['control_vertices'][k],angle,cx);color='#ad563d' if k in {int(n) for n in d['added_vertex_parents']} else '#2c4b3d';radius=3.1 if k>=2314 else 1.6
        parts.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{radius}" fill="{color}"/>')
parts.append('</svg>');(RUN/'qa'/f'{args.version}-control-net.svg').write_text(''.join(parts))
print(json.dumps({'version':args.version,'sections':summary},indent=2))
