"""Output-blind, known-family-closed public DEV audio inventory; no final data."""
from pathlib import Path
import datetime,hashlib,json,tarfile,time,urllib.request
from src.data.contracts import require_development_role
OUT=Path(__file__).parent
RAW=Path('exports/public-audio-development');RAW.mkdir(parents=True,exist_ok=True)
ASSETS=(('dev-clean','42e2234ba48799c1f50f24a7926300a1'),('dev-other','c8d0bcc9cca99d4f8b62fcc847357931'))
start=time.perf_counter();started=datetime.datetime.now(datetime.timezone.utc).isoformat();archives=[]
for name,official_md5 in ASSETS:
 url='https://www.openslr.org/resources/12/'+name+'.tar.gz';archive=RAW/(name+'.tar.gz')
 if not archive.exists():
  with urllib.request.urlopen(url,timeout=120) as response,archive.open('xb') as f:
   while block:=response.read(1024*1024):f.write(block)
 md5=hashlib.file_digest(archive.open('rb'),'md5').hexdigest()
 if md5!=official_md5:raise RuntimeError('official archive MD5 mismatch: '+name)
 archives.append({'name':name,'url':url,'official_checksum_url':'https://www.openslr.org/resources/12/md5sum.txt','md5':md5,'sha256':hashlib.file_digest(archive.open('rb'),'sha256').hexdigest(),'bytes':archive.stat().st_size})
role_path=Path('experiments/manifests/public_lspc_roles.development.attempt02.jsonl')
roles={row['upstream_audio_filepath']:row for row in map(json.loads,role_path.read_text().splitlines())}
with tarfile.open('exports/source-qualification/ls_pc_manifest.tar.gz') as t:
 rows=[json.loads(line) for name,_ in ASSETS for line in t.extractfile(name+'.json')]
by_group={}
for row in rows:
 role=roles[row['audio_filepath']]
 if 2<=row['duration']<=12 and role['role']=='hpo_development':by_group.setdefault(role['source_group_id'],[]).append(row)
def order(value):return hashlib.sha256(('DEV_AUDIO_TIMING_42:'+value).encode()).hexdigest()
selected=[]
for group in sorted(by_group,key=order)[:20]:
 row=min(by_group[group],key=lambda r:order(r['audio_filepath']));role=roles[row['audio_filepath']]
 require_development_role(role)
 selected.append(row|{'speaker':row['audio_filepath'].split('/')[1],'chapter':row['audio_filepath'].split('/')[2],'role':role['role'],'purpose':'DEVELOPMENT_ASR_TIMING_ONLY','source_group_id':group,'families':role['families'],'reference_policy':'text and text_raw retained; final policy not frozen'})
if not 2<=len(selected)<=20:raise ValueError('bounded DEV timing panel requires 2–20 eligible source groups')
if len({r['speaker'] for r in selected})!=len(selected):raise ValueError('distinct source groups did not imply distinct speakers')
for name,_ in ASSETS:
 with tarfile.open(RAW/(name+'.tar.gz')) as t:
  for row in selected:
   if not row['audio_filepath'].startswith(name+'/'):continue
   data=t.extractfile(t.getmember('LibriSpeech/'+row['audio_filepath'])).read()
   target=RAW/row['audio_filepath'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
   row.update(audio_relative_path=str(target),audio_sha256=hashlib.sha256(data).hexdigest(),audio_bytes=len(data))
receipt={'classification':'PUBLIC_DEVELOPMENT_AUDIO_ONLY_NOT_SEALED','started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selection':'up to20 distinct book/project/reader-closed HPO groups hash-selected BEFORE ASR; one2–12-second clip each','archives':archives,'license':'CC BY 4.0','license_url':'https://www.openslr.org/12/','elapsed_seconds':time.perf_counter()-start,'selected_cases':len(selected),'requested_quota':20,'quota_status':'AVAILABLE_ELIGIBLE_GROUP_SUPPLY_'+str(len(selected)),'selected_audio_seconds':sum(r['duration'] for r in selected),'cases':selected,'role_manifest_path':str(role_path),'role_manifest_sha256':hashlib.sha256(role_path.read_bytes()).hexdigest(),'development_role_barrier_passed':True,'source_groups':len(by_group),'selected_source_groups':len({r['source_group_id'] for r in selected}),'source_barrier_status':'PASS_BOOK_PROJECT_DEVELOPMENT_CLOSURE','no_owner_private_audio':True,'no_final_audio':True,'no_human_listening':True,'rejected_initial_selection':'book_overlap_rejection.json','full_training_near_duplicate_and_external_tokenizer_overlap':'PENDING'}
(OUT/'manifest.book_closed.attempt03.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='cases'}),flush=True)
