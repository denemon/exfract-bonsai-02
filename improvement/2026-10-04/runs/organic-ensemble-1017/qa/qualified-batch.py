from pathlib import Path
import subprocess,os
R=Path(__file__).resolve().parents[1]
with(R/'qa/qualified-console.log').open('x')as log:
 for mode,count in [('idle',8),('frame',8),('cold',4)]:
  for view in ['pc','mobile-390','mobile-320']:
   for c in range(count):
    p=subprocess.run(['node','qa/cohort.mjs',mode,view,str(c)],cwd=R,capture_output=True,text=True);log.write(p.stdout+p.stderr);log.flush();os.fsync(log.fileno());print(p.stdout.strip(),flush=True);assert p.returncode==0,p.stderr
print('QUALIFIED60_RAW_EXCLUSIVE_COMPLETE',flush=True)
