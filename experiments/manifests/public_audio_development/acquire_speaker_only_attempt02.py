"""Output-blind 20-speaker public DEV audio timing inventory; never final data."""
from pathlib import Path
import datetime,hashlib,json,tarfile,time,urllib.request
from src.data.contracts import require_development_role
OUT=Path(__file__).parent
RAW=Path('exports/public-audio-development');RAW.mkdir(parents=True,exist_ok=True)
URL='https://www.openslr.org/resources/12/dev-clean.tar.gz'
MD5='42e2234ba48799c1f50f24a7926300a1'
archive=RAW/'dev-clean.tar.gz'
start=time.perf_counter(); started=datetime.datetime.now(datetime.timezone.utc).isoformat()
if not archive.exists():
 with urllib.request.urlopen(URL,timeout=120) as response,archive.open('xb') as f:
  while block:=response.read(1024*1024):f.write(block)
md5=hashlib.file_digest(archive.open('rb'),'md5').hexdigest()
if md5!=MD5:raise RuntimeError('official archive MD5 mismatch')
with tarfile.open('exports/source-qualification/ls_pc_manifest.tar.gz') as t:
 rows=[json.loads(line) for line in t.extractfile('dev-clean.json')]
role_path=Path('experiments/manifests/public_lspc_roles.development.jsonl')
roles={row['upstream_audio_filepath']:row for row in map(json.loads,role_path.read_text().splitlines())}
by_speaker={}
for row in rows:
 if 2<=row['duration']<=12 and roles[row['audio_filepath']]['role']=='hpo_development':
  speaker=row['audio_filepath'].split('/')[1]
  by_speaker.setdefault(speaker,[]).append(row)
def order(value):return hashlib.sha256(('DEV_AUDIO_TIMING_42:'+value).encode()).hexdigest()
selected=[]
for speaker in sorted(by_speaker,key=order)[:20]:
 row=min(by_speaker[speaker],key=lambda r:order(r['audio_filepath']))
 role=roles[row['audio_filepath']];require_development_role(role)
 selected.append(row|{'speaker':speaker,'chapter':row['audio_filepath'].split('/')[2],
  'role':role['role'],'purpose':'DEVELOPMENT_ASR_TIMING_ONLY','source_group_id':role['source_group_id'],
  'reference_policy':'text and text_raw retained; final policy not frozen'})
with tarfile.open(archive) as t:
 for row in selected:
  member=t.getmember('LibriSpeech/'+row['audio_filepath']);data=t.extractfile(member).read()
  target=RAW/row['audio_filepath'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
  row.update(audio_relative_path=str(target),audio_sha256=hashlib.sha256(data).hexdigest(),audio_bytes=len(data))
 for name in ('LibriSpeech/CHAPTERS.TXT','LibriSpeech/SPEAKERS.TXT','LibriSpeech/LICENSE.TXT'):
  try:(RAW/Path(name).name).write_bytes(t.extractfile(name).read())
  except KeyError:pass
receipt={'classification':'PUBLIC_DEVELOPMENT_AUDIO_ONLY_NOT_SEALED','started_utc':started,
 'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selection':'20 distinct speakers hash-selected before ASR; one 2–12-second clip per speaker',
 'archive_url':URL,'official_checksum_url':'https://www.openslr.org/resources/12/md5sum.txt',
 'archive_md5':md5,'archive_sha256':hashlib.file_digest(archive.open('rb'),'sha256').hexdigest(),
 'archive_bytes':archive.stat().st_size,'license':'CC BY 4.0','license_url':'https://www.openslr.org/12/',
 'elapsed_seconds':time.perf_counter()-start,'selected_cases':len(selected),
 'role_manifest_sha256':hashlib.sha256(role_path.read_bytes()).hexdigest(),
 'development_role_barrier_passed':True,'source_groups':len({r['source_group_id'] for r in selected}),
 'selected_audio_seconds':sum(r['duration'] for r in selected),'cases':selected,
 'no_owner_private_audio':True,'no_final_audio':True,'no_human_listening':True}
(OUT/'manifest.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='cases'}),flush=True)
