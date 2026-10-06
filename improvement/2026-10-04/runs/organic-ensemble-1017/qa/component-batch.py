from pathlib import Path
import subprocess,os
R=Path(__file__).resolve().parents[1]
with(R/'qa/component-console.log').open('x')as log:
 for c in range(14):
  p=subprocess.run(['node','qa/cohort.mjs','factor','mobile-390',str(c)],cwd=R,capture_output=True,text=True);log.write(p.stdout+p.stderr);log.flush();os.fsync(log.fileno());print(p.stdout.strip(),flush=True);assert p.returncode==0,p.stderr
print('COMPONENT14_COMPLETE_EXCLUSIVE_RAW',flush=True)
