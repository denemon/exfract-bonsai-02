from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];source=(R/'sculpt/build_compact.py').read_text().split('assert boundary==')[0];results={}
for name,exclude in [('without-secondary',['Rear descending subordinate']),('without-rear',['Rear descending subordinate','Rear upper primary']),('torso-only',['Short low left shoulder','Left rear shoulder support','Rear upper primary','Right upper support','Rear descending subordinate'])]:
 lines=source.splitlines();s='\n'.join(line for line in lines if not any(line.startswith("branch('"+key+"'")for key in exclude))
 s=s.replace('qa/intersection-locations.json','qa/measured-isolated-'+name+'-intersections.json').replace('qa/geometry-inspection.json','qa/measured-isolated-'+name+'-inspection.json')
 scope={'__file__':str(R/'sculpt/build_compact.py')};exec(compile(s,str(R/'sculpt/build_compact.py'),'exec'),scope);results[name]=scope['inspection']
p=R/'qa/measured-isolated-connection-results.json';assert not p.exists();p.write_text(json.dumps(results,indent=2)+'\n')
