from pathlib import Path
import collections, datetime, gzip, hashlib, json, math, os, shutil, statistics, subprocess
from urllib.request import urlopen

ROOT = Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02')
D = ROOT / 'improvement/2026-10-04'
R = D / 'runs/organic-ensemble-1017'
Q = R / 'qa'
S = Path('/Users/kazuki.tanaka/Documents/Codex/2026-10-04/task-2')
J = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
BH = lambda b: hashlib.sha256(b).hexdigest()
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()

def write_new(p, d):
    with p.open('x') as f:
        json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())

def write_derived(p, d):
    with p.open('w') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())

def allocation(folder):
    total = 0
    for b, ds, fs in os.walk(folder, followlinks=False):
        ds[:] = [n for n in ds if not Path(b, n).is_symlink()]
        total += sum(Path(b, n).stat().st_blocks * 512 for n in fs if not Path(b, n).is_symlink())
    return total

def stat(values):
    a = sorted(values)
    return {'n': len(a), 'median': statistics.median(a), 'p95': a[math.ceil(.95 * len(a)) - 1], 'min': a[0], 'max': a[-1]}

s = J(R / 'start.json')
q = J(Q / 'qualified-performance-summary.json')
c = J(Q / 'capacity-transcode-record.json')
finish = J(R / 'finish.json')
assert not (R / 'delivery-manifest.json').exists(), 'Already sealed; do not duplicate or overwrite.'
assert not (ROOT / 'improvement/.active-run').exists()
assert not Path(s['reused_qa_profile'] + '.active').exists()
assert J(Q / 'chrome-lifecycle.json')['exitCode'] == 0
assert not subprocess.run(['ps', '-p', '61609', '-o', 'pid='], capture_output=True, text=True).stdout.strip()
env = {**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, env=env, text=True).strip()
status = subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, env=env, text=True).rstrip('\n')
assert head == s['git_head_at_start'] and status == s['tracked_status_at_start']
for port, pid in [(5214, 20598), (5215, 61480)]:
    assert subprocess.check_output(['lsof', '-nP', f'-iTCP:{port}', '-sTCP:LISTEN', '-t'], text=True).strip() == str(pid)
cwd_top = subprocess.check_output(['lsof', '-a', '-p', '20598', '-d', 'cwd', '-Fn'], text=True)
cwd_trial = subprocess.check_output(['lsof', '-a', '-p', '61480', '-d', 'cwd', '-Fn'], text=True)
assert '\nn' + str(R.parent / 'growth-garden-0729/candidate') + '\n' in cwd_top
assert '\nn' + str(R / 'candidate') + '\n' in cwd_trial
process = subprocess.check_output(['ps', '-p', '20598,61480', '-o', 'pid=,ppid=,etime=,command='], text=True)

assert len(s['protected_state_sha256']) == 37
for n, h in s['protected_state_sha256'].items():
    assert H(D / n) == h, n
assert finish['candidateAdopted'] is False and finish['currentStates'] == 38
protected = {}
for stage, name in [(25, 'root-flow-0206'), (26, 'age-leaf-0342'), (27, 'program-state-0426'), (28, 'coherent-core-0514'), (29, 'grown-core-0554'), (30, 'garden-scale-0634'), (31, 'growth-garden-0729'), (32, 'aged-ensemble-0831'), (33, 'idle-causality-0935')]:
    P = R.parent / name
    assert H(P / 'delivery-manifest.json') == s[f'protected_stage{stage}_manifest_sha256']
    assert H(P / 'qa/final-receipt.json') == s[f'protected_stage{stage}_receipt_sha256']
    m = J(P / 'delivery-manifest.json')
    for n, d in m['files'].items():
        assert H(P / n) == d['sha256'], (stage, n)
    for n, target in m.get('read_only_references', {}).items():
        assert os.readlink(P / n) == target and (P / n).exists(), (stage, n)
    protected[str(stage)] = {'run': name, 'files': len(m['files']), 'aliases': len(m.get('read_only_references', {})), 'manifestSHA256': H(P / 'delivery-manifest.json'), 'receiptSHA256': H(P / 'qa/final-receipt.json')}
freeze = J(R / 'selected-scene-freeze.json')
assert len(freeze['fixedNativeSevenSHA256']) == 7
for n, h in (freeze['sourceSHA256'] | freeze['fixedNativeSevenSHA256']).items():
    assert H(R / n) == h, n
for n in ['render-partition.js', 'foliage-lod.js']:
    assert H(R / 'candidate/src' / n) == H(R.parent / 'program-state-0426/candidate/src' / n)
v = J(Q / 'final-display-invariants.json')
assert v['functional11Pass'] and v['dynamic6Pass'] and v['sameR31CameraLightsExactProjection3']
assert len(J(Q / 'integration-functional-current/results.json')['results']) == 11
assert J(Q / 'integration-functional-current/results.json')['passed']
assert len(J(Q / 'dynamic-selected-scene-proof.json')['results']) == 6
assert J(Q / 'dynamic-selected-scene-proof.json')['passed']
assert '✓ built' in (Q / 'build-final.log').read_text()
assert J(Q / 'completed-inline-sync.json')['inlineAndFullSameCompletedScene']
for entry in J(Q / 'completed-inline-sync.json')['entries']:
    p = R / 'candidate/public/stills' / (entry['name'] + '.webp')
    assert not p.is_symlink() and H(p) == entry['fullSHA256']
assert 'publicDir:false' in (R / 'candidate/vite.config.mjs').read_text()
assert "tail.startsWith('/stills/')" in (R / 'candidate/vite.config.mjs').read_text()
assert len(list(Q.rglob('*.jpg'))) == 48
assert len(list((Q / 'final-candidate-and-retina').glob('*.jpg'))) == 6
transcode = R / 'qa/garden-planting-shape-v01/results.json.gz'
assert H(transcode) == c['compressedSHA256']
assert BH(gzip.decompress(transcode.read_bytes())) == c['originalSHA256']
assert not (Q / 'garden-planting-shape-v01/results.json').exists()
assert c['temporaryLimitExceeded'] and c['overByBytes'] == 512000

# Re-read the durable raw arrays; this is offline verification, not a fresh qualification.
raw = collections.defaultdict(list)
ledger = {}
for p in sorted((Q / 'checkpoints').glob('*.json.gz')):
    compressed = p.read_bytes()
    decoded = gzip.decompress(compressed)
    d = json.loads(decoded)
    assert d['mode'] in ['frame', 'idle', 'cold'] and d['passed'] and d['ChromePID'] == 61609
    assert d['DPR'] == 1 and not d.get('diagnostic', False)
    assert not d.get('profilerEnabled', False) and not d.get('qualificationInstrumentationEnabled', False)
    raw[d['mode']].append(d)
    ledger[p.name] = {'savedGzipBytes': len(compressed), 'savedGzipSHA256': BH(compressed), 'decodedBytes': len(decoded), 'decodedSHA256': BH(decoded), 'mode': d['mode'], 'view': d['view']['name'], 'variant': d['variant'], 'cohort': d['cohort']}
assert {k: len(v) for k, v in raw.items()} == {'cold': 12, 'frame': 24, 'idle': 24}
definitions = [('CPU_submit_ms', 'median', .5, .15), ('CPU_submit_ms', 'p95', 1.5, .2), ('GPU_active_elapsed_ms', 'median', 1, .15), ('GPU_active_elapsed_ms', 'p95', 2, .15), ('GPU_idle_elapsed_ms', 'p95', 3, .15), ('cold_first3D_ms', 'median', 800, .1), ('CPU_idle_submit_ms', 'median', .75, .2), ('CPU_idle_submit_ms', 'p95', 1.5, .2), ('GPU_idle_elapsed_ms', 'median', 3, .2)]
gates, block_gates = [], []
for row in q['rows']:
    width = row['width']
    vs, blocks = {}, {}
    for variant in ['r31', 'candidate']:
        f = [d for d in raw['frame'] if d['view']['name'] == width and d['variant'] == variant]
        i = [d for d in raw['idle'] if d['view']['name'] == width and d['variant'] == variant]
        cold = [d for d in raw['cold'] if d['view']['name'] == width and d['variant'] == variant]
        assert len(f) == len(i) == 4 and len(cold) == 2
        assert all(d['state']['version'] == ('grown-v02' if variant == 'r31' else 'living-v01') and d['pixelRatio'] == 1 for d in f + i)
        vs[variant] = {'CPU_submit_ms': stat([x for d in f for x in d['cpuSubmitMs'][2:]]), 'GPU_active_elapsed_ms': stat([x for d in f for x in d['gpuElapsedMs'][2:]]), 'CPU_idle_submit_ms': stat([x for d in i for x in d['cpuSubmitMs']]), 'GPU_idle_elapsed_ms': stat([x for d in i for x in d['gpuElapsedMs']]), 'actual_idle_wait_ms': stat([x for d in i for x in d['actualIdleWaitMs']]), 'cold_first3D_ms': stat([d['navigationToFirst3DMs'] for d in cold]), 'cold_completed_still_ms': stat([d['timing']['completedStillMs'] for d in cold]), 'cold_FCP_ms': stat([next(p['startTime'] for p in d['actualPaintEntries'] if p['name'] == 'first-contentful-paint') for d in cold]), 'cold_encoded_body_bytes': stat([sum(p['encodedBodySize'] for p in d['resources']) for d in cold]), 'draw_calls': f[0]['drawCalls'], 'triangles': f[0]['triangles'], 'actual_camera': f[0]['state']['camera']}
        blocks[variant] = {b: {'CPU_idle_submit_ms': stat([x for d in i if d['orderBlock'] == b for x in d['cpuSubmitMs']]), 'GPU_idle_elapsed_ms': stat([x for d in i if d['orderBlock'] == b for x in d['gpuElapsedMs']])} for b in ['ABBA', 'BAAB']}
        assert vs[variant] == row['variants'][variant]
        assert blocks[variant] == row['idleOrderBlocks'][variant]
    assert vs['r31']['actual_camera'] == vs['candidate']['actual_camera']
    assert all(d['state']['camera'] == vs['r31']['actual_camera'] for a in raw.values() for d in a if d['view']['name'] == width)
    def gate(metric, quantile, fixed, ratio, b, candidate, block=None):
        tol = max(fixed, b * ratio)
        return {'width': width, 'metric': metric, 'quantile': quantile, 'baseline': b, 'candidate': candidate, 'delta': candidate - b, 'predeclared_allowed_delta': tol, 'passed': candidate - b <= tol, **({'block': block} if block else {})}
    for metric, quantile, fixed, ratio in definitions:
        gates.append(gate(metric, quantile, fixed, ratio, vs['r31'][metric][quantile], vs['candidate'][metric][quantile]))
    for block in ['ABBA', 'BAAB']:
        for metric, quantile, fixed, ratio in definitions:
            if metric in ['CPU_idle_submit_ms', 'GPU_idle_elapsed_ms']:
                block_gates.append(gate(metric, quantile, fixed, ratio, blocks['r31'][block][metric][quantile], blocks['candidate'][block][metric][quantile], block))
assert gates == q['gates'] and block_gates == q['orderBlockGates']
assert q['poolPassedCount'] == 26 and q['orderBlockPassedCount'] == 19 and not q['technicalQualificationPassed']
failures = [g for g in gates + block_gates if not g['passed']]
assert len(failures) == 6
component = J(Q / 'component-load-summary.json')
assert len(component['rawSHA256']) == 14
for n, h in component['rawSHA256'].items():
    assert H(Q / 'checkpoints' / n) == h

# Read-only localhost verification after the remote compaction error.
http = []
for row in J(Q / 'final-http-identity.json')['rows']:
    with urlopen(row['url'], timeout=10) as response:
        body = response.read()
        headers = dict(response.headers)
    assert len(body) == row['bytes'] and BH(body) == row['SHA256'] == H(Path(row['file']))
    http.append({'url': row['url'], 'bytes': len(body), 'SHA256': BH(body), 'contentEncoding': headers.get('Content-Encoding')})
free = os.statvfs(ROOT).f_bavail * os.statvfs(ROOT).f_frsize
assert free >= 2 * 1024 ** 3

# Conservative allocation guard before writing only new QA and derived metadata.
profile_final = allocation(s['reused_qa_profile'])
profile_samples = [s['profile_allocated_bytes_at_start'], profile_final, c['profileObservedPeak']]
for p in Q.rglob('results.json'):
    job = J(p)
    profile_samples.extend(job[k] for k in ['profileAllocatedBefore', 'profileAllocatedAfter'] if k in job)
job = json.loads(gzip.decompress(transcode.read_bytes()))
profile_samples.extend(job[k] for k in ['profileAllocatedBefore', 'profileAllocatedAfter'] if k in job)
profile_peak = max(profile_samples)
profile_charge = max(0, profile_peak - s['profile_allocated_bytes_at_start'])
cache_final = allocation(s['shared_mutable_cache'])
cache_charge = max(0, cache_final - s['cache_allocated_bytes_at_start'])
own_staging = sum(p.stat().st_blocks * 512 for p in S.glob('organic-ensemble-*.py') if p.is_file())
staging_positive = max(0, allocation(S) - s['staging_allocated_bytes_at_start'])
staging_charge = max(own_staging, staging_positive)
coors = {n: H(D / n) for n in ['HANDOFF.md', 'IMPROVEMENT_PLAN.md', 'run-state.json']}
new = {'organic-ensemble-study-state.json': H(D / 'organic-ensemble-study-state.json')}
coor_charge = sum((D / n).stat().st_blocks * 512 for n in coors)
state_charge = sum((D / n).stat().st_blocks * 512 for n in new)
guards = 8192
assert allocation(R) + profile_charge + cache_charge + staging_charge + coor_charge + state_charge + guards + 262144 <= 20971520

write_new(Q / 'independent-qualified-review.json', {'reviewer': 'volume_review', 'actual60GzipRawDecodedAndRecalculated': True, 'rawCounts': {'frame': 24, 'idle': 24, 'cold': 12}, 'activeSamplesEachVariantWidth': 236, 'idleSamplesEachVariantWidth': 28, 'coldSamplesEachVariantWidth': 2, 'poolPassed': 26, 'orderBlockPassed': 19, 'technicalQualificationPassed': False, 'statisticsAndToleranceDiscrepancies': 0, 'failures': failures, 'component14NotMixed': True, 'sourceCauseUnidentified': True, 'PCVisualImprovedMobile390320DPR2Nonregression': True, 'decodedTranscodeAllBytesSHAExact': True, 'allPeriodBudgetPassed': False, 'observedBudgetOverBytes': 512000, 'reviewerFileChanges': 0, 'rawHashIndexWasNotUsedForIndependentCalculation': True, 'hashIndexCorrectionApprovedAsDerivedMetadataOnly': True, 'oldSealedDeletion0RecordCheckedButNoWideFilesystemAudit': True})
write_new(Q / 'qualified-raw-integrity.json', {'atJST': NOW, 'readOnlyOfflineVerification': True, 'measurementRerunCount': 0, 'savedGzipAndDecodedAllBytesSHA256': ledger, '60CohortsFullyVerified': True, 'statisticsAnd51GatesExactAgainstExistingSummary': True, 'component14SeparateUnmodified': True})
old_summary_sha = H(Q / 'qualified-performance-summary.json')
old_helper_sha = H(Q / 'summarize.py')
assert q['rawSHA256'] == {}
original = {k: v for k, v in q.items() if k != 'rawSHA256'}
q['rawSHA256'] = {n: x['savedGzipSHA256'] for n, x in ledger.items()}
write_derived(Q / 'qualified-performance-summary.json', q)
assert original == {k: v for k, v in J(Q / 'qualified-performance-summary.json').items() if k != 'rawSHA256'}
helper = (Q / 'summarize.py').read_text()
old_glob = "glob('*.json'))if p.name.startswith(('frame-','idle-','cold-'))"
assert helper.count(old_glob) == 1
(Q / 'summarize.py').write_text(helper.replace(old_glob, "glob('*.json.gz'))if p.name.startswith(('frame-','idle-','cold-'))", 1))
write_new(Q / 'raw-hash-index-correction.json', {'atJST': NOW, 'reason': 'Qualified numeric loader correctly read gzip60; separate SHA index glob retained *.json and was empty.', 'oldSummarySHA256': old_summary_sha, 'correctedSummarySHA256': H(Q / 'qualified-performance-summary.json'), 'oldSummarizerSHA256': old_helper_sha, 'correctedSummarizerSHA256': H(Q / 'summarize.py'), 'metadataOnlyCorrectedField': 'rawSHA256', 'entriesBefore': 0, 'entriesAfter': 60, 'allStatisticsAndGatesUnchanged': True, 'rawCheckpointBytesUnchanged': True, 'measurementRerunCount': 0, 'thresholdChangeCount': 0})
write_new(Q / 'resume-local-protection.json', {'atJST': NOW, 'parentReportedRemoteCompactionError': {'upstreamStatus': 503, 'type': 'invalid_request_error', 'code': 'invalid_value', 'param': 'url'}, 'localResumePossible': True, 'noAuthenticationOrQuotaCauseInferred': True, 'noDuplicateRunCreated': True, 'writerAndProfileGuardsAlreadyRemoved': True, 'Chrome61609AlreadyExited': True, 'GitHEAD': head, 'trackedStatusExactAtStart': status, 'TOP20598AndCandidate61480CWDAndCommandsChecked': True, 'process': process, 'TOPCWD': cwd_top, 'candidateCWD': cwd_trial, 'http8Exact': http, 'protectedStages25Through33': protected, 'protectedOld37StatesExact': True, 'fixedNative7AndSelectedSourceExact': True, 'externalBaselineFromParentOnly': {'PR': 'https://github.com/denemon/exfract-bonsai-02/pull/9', 'reportedMergedAtJST': '2026-10-06T10:03:10+09:00', 'reportedMergeSHA': '123b70d3e6a4ca76506e8c98f5c6690313b8f00b', 'reportedScope': 'R19/R20 archive only, 291 files / 2 commits; separate from currentTOP adoption', 'externalPRNotIndependentlyFetched': True, 'localHEADProtected': head, 'pullResetRevertGitWriteCount': 0}, 'freeDiskBytes': free})
for p in sorted(S.glob('organic-ensemble-*.py')):
    target = Q / p.name
    assert not target.exists()
    shutil.copyfile(p, target)
assert all(H(Q / 'checkpoints' / n) == x['savedGzipSHA256'] for n, x in ledger.items())

mp, cp, rp = R / 'delivery-manifest.json', Q / 'capacity-final.json', Q / 'final-receipt.json'
assert not any(p.exists() for p in [mp, cp, rp])
write_new(cp, {})
write_new(rp, {})

def manifest():
    files, links = {}, {}
    for p in sorted(R.rglob('*')):
        if p.is_symlink():
            assert p.exists() and p.resolve().is_relative_to(ROOT)
            links[str(p.relative_to(R))] = os.readlink(p)
        elif p.is_file() and p not in [mp, rp]:
            files[str(p.relative_to(R))] = {'bytes': p.stat().st_size, 'sha256': H(p)}
    m = {'stage': 34, 'run': R.name, 'sealedAtJST': NOW, 'files': files, 'read_only_references': links, 'protected_old_state_sha256': s['protected_state_sha256'], 'new_state_sha256': new, 'coordinator_sha256_at_handoff': coors, 'protectedOldStates': 37, 'newStates': 1, 'currentStates': 38, 'candidateAdopted': False, 'selectedTOP': 'growth-garden-0729', 'PCOverallVisualImprovement': True, 'mobile390320DPR2Nonregression': True, 'poolPassed': 26, 'poolTotal': 27, 'orderBlockPassed': 19, 'orderBlockTotal': 24, 'technicalQualificationPassed': False, 'temporaryBudgetLimitExceeded': True, 'observedOverByBytes': 512000, 'allPeriodBudgetPassed': False, 'currentNewRawLosslessTranscodeCount': 1, 'oldSealedFileDeletionCount': 0, 'rawNumericDiscardCount': 0, 'sourceCauseUnidentified': True, 'wholeHighEndGardenComplete': False, 'overallGoalComplete': False, 'receiptExcludedToAvoidCircularHash': True, 'LibraryRetryCount': 0, 'LibraryImageIDs': []}
    write_derived(mp, m)
    return m

m = manifest()
run_before_seal = allocation(R)
reserve = 16384
charge = run_before_seal + reserve + guards + profile_charge + cache_charge + staging_charge + coor_charge + state_charge
assert charge <= 20971520
cap = {'stage': 34, 'runAllocatedPreFinalSeal': run_before_seal, 'manifestReceiptFinalizationReserve': reserve, 'conservativeRunCharge': run_before_seal + reserve, 'profileAtStart': s['profile_allocated_bytes_at_start'], 'profileObservedPeak': profile_peak, 'profileFinal': profile_final, 'profilePositiveCharge': profile_charge, 'profilePeakSampling': 'Capture before/after, observed transcode peak, and closed final; not a continuous profile allocation maximum.', 'cacheFinal': cache_final, 'cachePositiveCharge': cache_charge, 'ownStagingFullCharge': own_staging, 'stagingAggregatePositive': staging_positive, 'stagingCharge': staging_charge, 'coordinatorFullCharge': coor_charge, 'newStateCharge': state_charge, 'writerAndProfileGuardsPeakConservativeCharge': guards, 'totalPositiveChargeBytes': charge, 'totalPositiveMiB': charge / 1048576, 'limitBytes': 20971520, 'remainingBytes': 20971520 - charge, 'finalBudgetPass': True, 'allPeriodBudgetPass': False, 'temporaryBudgetLimitExceeded': True, 'observedConservativeChargeAtMiss': c['observedConservativeChargeBefore'], 'observedOverByBytes': 512000, 'currentNewRawLosslessTranscodeCount': 1, 'transcodeDecodedAllBytesSHAExact': True, 'oldSealedFileDeletionCount': 0, 'oldSealedRawOverwriteCount': 0, 'rawNumericDiscardCount': 0, 'freeDiskBytes': free, 'minimumFree2GiBPass': True, 'sharedReadOnlyAssetsReused': True, 'rawQualificationCohortsDurablyCheckpointed': 60, 'componentRawCohorts': 14, 'ChromeExit0': True, 'guardsRemoved': True, 'TOPPID': 20598, 'candidatePID': 61480}
write_derived(cp, cap)
m = manifest()
assert len(m['read_only_references']) == 8
receipt = {'stage': 34, 'run': R.name, 'sealedAtJST': NOW, 'manifestSHA256': H(mp), 'capacitySHA256': H(cp), 'newStateSHA256': new, 'coordinatorSHA256': coors, 'candidateAdopted': False, 'selectedTOP': 'growth-garden-0729', 'TOPPID': 20598, 'TOPSession': 63808, 'TOPURL': 'http://127.0.0.1:5214/', 'candidatePID': 61480, 'candidateSession': 69250, 'candidateURL': 'http://127.0.0.1:5215/compare/r34/', 'files': len(m['files']), 'validReadOnlyAliases': 8, 'protectedOldStates': 37, 'newStates': 1, 'currentStates': 38, 'protectedStages25Through33Exact': protected, 'historicalCompleteness': False, 'historicalExternalMissingActualPaths': 26, 'historicalExternalMissingManifestEntries': 4, 'historicalMissingNotRecreatedOrDeleted': True, 'actualNativeChangedVertices': 1066, 'nativeMaximumDisplacementMm': 56.30695590073669, 'worldMaximumDisplacementMm': 37.162590894486, 'nativeBoundaryNonmanifoldNonadjacentIntersections': 0, 'fixedNative7AndSelectedSourceExact': True, 'componentRawCohorts': 14, 'qualificationRawCohorts': 60, 'activeSamplesEachVariantWidth': 236, 'idleSamplesEachVariantWidth': 28, 'coldSamplesEachVariantWidth': 2, 'poolPassedConditions': 26, 'poolConditions': 27, 'orderBlockPassedConditions': 19, 'orderBlockConditions': 24, 'technicalQualificationPassed': False, 'sourceCauseUnidentified': True, 'oldPrimaryFailuresPreserved': True, 'noRepeatUntilPass': True, 'noThresholdChange': True, 'qualifiedRawAll60SavedAndDecodedSHARecorded': True, 'offlineRecomputedStatisticsAnd51GatesExact': True, 'summaryRawHashIndexCorrectedMetadataOnly': True, 'finalBuildPass': True, 'freshFunctionalCasesPass': 11, 'freshDynamicCasesPass': 6, 'actualNewJPEGs': 48, 'actualFinalJPEGs': 6, 'ownCompletedFullStills': 5, 'inlineAndFullCompletedSceneSynced': True, 'HTTP8BodySHAExactAfterResume': True, 'DPR2ActualDisplayCheckedWithCanvasCap1_6': True, 'PCVisualGainAndMobile390320DPR2Nonregression': True, 'wholeHighEndGardenComplete': False, 'overallGoalComplete': False, 'physicalPhoneSafariThermalFrequencyHighLODUnverified': True, 'runtimeRequestedModelMetadataUnverified': True, 'ChromePID': 61609, 'ChromeExitCode': 0, 'profileAndWriterGuardsRemoved': True, 'LibraryRetryCount': 0, 'LibraryImageIDs': [], 'GitHead': head, 'GitHeadUnchanged': True, 'noGitWritePushPRMergePublicationPurchaseAutomationOldProjectAccess': True, 'oldSealedFileDeletionCount': 0, 'oldSealedRawOverwriteCount': 0, 'currentNewRawLosslessTranscodeCount': 1, 'rawNumericDiscardCount': 0, 'reportSHA256': H(R / 'REPORT.md'), 'nextSHA256': H(R / 'NEXT_WHOLE_QUALITY.md'), 'positiveChargeBytes': charge, 'positiveMiB': charge / 1048576, 'remainingBytes': 20971520 - charge, 'finalBudgetPassed': True, 'allPeriodBudgetPassed': False, 'temporaryBudgetOverByBytes': 512000, 'freeDiskBytes': free}
write_derived(rp, receipt)
assert allocation(R) <= run_before_seal + reserve
for n, d in m['files'].items():
    assert (R / n).stat().st_size == d['bytes'] and H(R / n) == d['sha256'], n
for n, target in m['read_only_references'].items():
    assert os.readlink(R / n) == target and (R / n).exists()
for n, h in s['protected_state_sha256'].items():
    assert H(D / n) == h
for n, h in (new | coors).items():
    assert H(D / n) == h
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, env=env, text=True).strip() == head
assert subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, env=env, text=True).rstrip('\n') == status
print(json.dumps({'sealed': True, 'files': len(m['files']), 'aliases': 8, 'runAllocatedFinal': allocation(R), 'positiveBytes': charge, 'positiveMiB': charge / 1048576, 'remainingBytes': 20971520 - charge, 'allPeriodBudgetPass': False, 'temporaryOverByBytes': 512000, 'freeDiskBytes': free, 'manifestSHA256': H(mp), 'receiptSHA256': H(rp), 'capacitySHA256': H(cp), 'newStateSHA256': new, 'TOPPID': 20598, 'candidatePID': 61480, 'poolPass': 26, 'orderBlockPass': 19, 'candidateAdopted': False, 'allManifestFilesReverified': True}, indent=2))
