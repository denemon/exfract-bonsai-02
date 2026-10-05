from pathlib import Path
import json,subprocess,argparse,time
p=argparse.ArgumentParser();p.add_argument('--version',required=True);args=p.parse_args()
RUN=Path(__file__).resolve().parents[1];start=json.loads((RUN/'start.json').read_text());profile=Path(start['reused_qa_profile']);lock=Path(str(profile)+'.active');lock.mkdir()
rows=[]
try:
    for kind,w,h in [('sections',1290,570),('control-net',1290,680)]:
        source=RUN/'qa'/f'{args.version}-{kind}.svg';dest=source.with_suffix('.png');assert source.exists() and not dest.exists()
        command=['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless','--disable-background-networking','--disable-component-update','--disable-features=OptimizationHints,OptimizationHintsFetching,OptimizationTargetPrediction','--disable-sync','--disable-default-apps','--no-first-run','--no-default-browser-check','--hide-scrollbars','--force-device-scale-factor=1',f'--user-data-dir={profile}',f'--window-size={w},{h}',f'--screenshot={dest}','--timeout=10000',source.as_uri()]
        result=subprocess.run(command,capture_output=True,text=True,timeout=40)
        (RUN/'qa'/f'{args.version}-{kind}-chrome.log').write_text(result.stderr)
        assert result.returncode==0 and dest.exists(),result.stderr
        rows.append({'source':str(source.relative_to(RUN)),'png':str(dest.relative_to(RUN)),'viewport':[w,h],'browser':'Actual Mac Chrome headless, existing shared profile','return_code':result.returncode})
    (RUN/'qa'/f'{args.version}-diagram-captures.json').write_text(json.dumps(rows,indent=2)+'\n')
finally:lock.rmdir()
print(json.dumps(rows,indent=2))
