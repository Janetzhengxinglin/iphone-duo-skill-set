"""Behavioral regressions for either packaged native capture adapter."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(os.environ.get('FOLDABLE_SKILLS_ROOT',str(Path(__file__).resolve().parents[1]/'skills')))
PLATFORMS=[(c,r) for c,r in [('android-foldable-page-capture','android-foldable-adaptation-review'),('app-video-page-capture','iphone-duo-adaptation-review')] if (ROOT/c).is_dir()]

def call(script,*args,ok=True):
    result=subprocess.run([sys.executable,str(script),*map(str,args)],text=True,capture_output=True)
    if ok and result.returncode:raise AssertionError(result.stderr+result.stdout)
    if not ok and not result.returncode:raise AssertionError('Expected rejection')
    return result

def read(path):return json.loads(Path(path).read_text())
def write(path,data):Path(path).write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg required')
class CaptureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not PLATFORMS:raise RuntimeError('No native skill package')
        cls.temp=tempfile.TemporaryDirectory();cls.base=Path(cls.temp.name)
        cls.videos=[]
        for number,color in enumerate(['white','gray']):
            path=cls.base/('source%d.mkv'%number)
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=%s:s=320x240:r=10:d=4'%color,'-vf',"drawbox=x=0:y=0:w=100:h=100:color=red:t=fill:enable='between(t,1,1.9)',drawbox=x=0:y=0:w=100:h=100:color=blue:t=fill:enable='between(t,0.5,0.59)'",'-c:v','ffv1',str(path)],check=True)
            cls.videos.append(path)
        cls.runs={}
        for capture,review in PLATFORMS:
            script=ROOT/capture/'scripts/capture.py';runs=[]
            for index,video in enumerate(cls.videos):
                run=cls.base/(capture+str(index));call(script,'sample',video,run);runs.append(run)
            cls.runs[capture]=runs
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def adapter(self,capture,run):
        android=capture.startswith('android');index=read(run/('sample.json' if android else 'candidates/index.json'))
        rows=index['candidates'];times=[r['time_s' if android else 'time_seconds'] for r in rows]
        flags={'all_candidates_classified':True,'all_intervals_reviewed':True,'notes':'Synthetic fixture classifications; not a real UI audit'}
        if android:
            pages=[{'id':'P%d'%i,'name':'Fixture','context_id':'CTX','time_s':t,'candidate_id':rows[i]['id'],'state':'fixture','selection_reason':'Full source frame'} for i,t in enumerate(times)]
            spec={'contexts':[{'id':'CTX','display':'outer','orientation':'portrait'}],'pages':pages,'candidate_classifications':[{'id':r['id'],'classification':'app_state','reason':'Synthetic'} for r in rows],'capture_review':flags}
        else:
            pages=[{'id':'P%d'%i,'title':'Fixture','state':'fixture','form':'outer','time_seconds':t,'candidate_id':rows[i]['id']} for i,t in enumerate(times)]
            spec={'pages':pages,'coverage':[{'candidate_id':r['id'],'disposition':'retained','reason':'Synthetic','page_id':'P%d'%i} for i,r in enumerate(rows)],'capture_review':flags}
        return android,index,spec
    def clone(self,capture,label):
        target=self.base/(capture+label+str(len(list(self.base.iterdir()))));shutil.copytree(self.runs[capture][0],target);return target
    def finalized(self,capture,label,privacy=False,source=0):
        run=self.base/(capture+label+str(len(list(self.base.iterdir()))));shutil.copytree(self.runs[capture][source],run)
        android,index,spec=self.adapter(capture,run)
        if privacy and not android:spec['pages'][1]['privacy']=[{'region':[.28,0,.1,.1],'type':'account','reason':'Synthetic private field'}]
        write(run/'spec.json',spec);call(ROOT/capture/'scripts/capture.py','finalize',run,run/'spec.json')
        return run,android,index,spec
    def test_source_grid_and_exact_grouping(self):
        digests=[]
        for capture,_ in PLATFORMS:
            run=self.runs[capture][0];android,index,spec=self.adapter(capture,run)
            self.assertEqual(len(index['candidates']),13)
            self.assertEqual([p['time_s' if android else 'time_seconds'] for p in spec['pages'][:4]],[0,1,2,3])
            rows=index['candidates'];hashes=[r['visual_sha256'] for r in rows]
            self.assertNotEqual(hashes[0],hashes[1]);self.assertEqual(hashes[0],hashes[2]);digests.append(hashes)
        if len(digests)==2:self.assertEqual(*digests)
    def test_candidate_is_final_raw_evidence(self):
        for capture,_ in PLATFORMS:
            run,android,index,spec=self.finalized(capture,'exact')
            for row,e in zip(index['candidates'],read(run/'capture.json')['evidence']):
                raw=run/(e['path'] if android else e['raw_image'])
                self.assertEqual(sha(raw),row['sha256' if android else 'raw_sha256'])
    def test_missing_coverage_and_intervals_rejected(self):
        for capture,_ in PLATFORMS:
            for missing in ['coverage','intervals']:
                run=self.clone(capture,missing);android,index,spec=self.adapter(capture,run)
                if missing=='coverage':spec['candidate_classifications' if android else 'coverage'].pop()
                else:spec['capture_review']['all_intervals_reviewed']=False
                write(run/'spec.json',spec);call(ROOT/capture/'scripts/capture.py','finalize',run,run/'spec.json',ok=False)
                self.assertFalse((run/'capture.json').exists())
    def test_candidate_time_mismatch_rejected(self):
        for capture,_ in PLATFORMS:
            run=self.clone(capture,'mismatch');android,index,spec=self.adapter(capture,run)
            spec['pages'][0]['candidate_id']=index['candidates'][1]['id']
            write(run/'spec.json',spec);call(ROOT/capture/'scripts/capture.py','finalize',run,run/'spec.json',ok=False)
    def test_supplementary_brief_state_preserved(self):
        for capture,_ in PLATFORMS:
            script=ROOT/capture/'scripts/capture.py';early=self.base/(capture+'brief.png');normal=self.base/(capture+'normal.png')
            call(script,'frame',self.videos[0],.5,early);call(script,'frame',self.videos[0],0,normal)
            self.assertNotEqual(sha(early),sha(normal))
            call(script,'frame',self.videos[0],.5,early,ok=False)
    def test_sheets_full_coverage_budget_and_tamper(self):
        for capture,_ in PLATFORMS:
            run,android,index,spec=self.finalized(capture,'sheets');out=run/'review-sheets'
            call(ROOT/capture/'scripts/review_sheets.py',run/'capture.json',out)
            manifest=read(out/'manifest.json');self.assertEqual(len(manifest['sheets']),4)
            cells=[c for sheet in manifest['sheets'] for c in sheet['cells']];self.assertEqual({c['page_id'] for c in cells},{p['id'] for p in spec['pages']})
            batch=run/'batch.json';write(batch,[manifest['sheets'][0]['path']])
            call(ROOT/capture/'scripts/image_batches.py','check',run/'ledger.json',batch,'--session','fixture','--stage','review')
            with Path(cells[0]['path']).open('ab') as handle:handle.write(b'tamper')
            call(ROOT/capture/'scripts/review_sheets.py',run/'capture.json',run/'tampered-sheets',ok=False)
    def test_native_merge_and_seed(self):
        for capture,review in PLATFORMS:
            one,android,_,_=self.finalized(capture,'merge-one');two,_,_,_=self.finalized(capture,'merge-two',source=1)
            workflow=ROOT/review/'scripts/workflow.py';run=self.base/(capture+'merged')
            call(workflow,'merge',run,one/'capture.json',two/'capture.json')
            data=read(run/'capture.json');self.assertEqual(len(data['pages']),26)
            self.assertEqual(len({p['id'] for p in data['pages']}),26)
            self.assertEqual(len(data['capture_sources']),2)
            for e in data['evidence']:
                path=run/(e['path'] if android else e['image']);self.assertEqual(sha(path),e['sha256' if android else 'image_sha256'])
            call(workflow,'merge',self.base/(capture+'duplicate'),one/'capture.json',one/'capture.json',ok=False)
            if android:call(workflow,'prepare',run);call(workflow,'seed',run)
            else:
                intake={'schema_version':'1.0','flow':'Fixture','form':'outer','output':'figma','content':'defects-only','target':'https://www.figma.com/design/fixture/test','video':str(self.videos[0])}
                write(run/'intake-source.json',intake);call(workflow,'init',run/'intake-source.json',run);call(workflow,'seed',run)
            self.assertEqual(len(read(run/'review-input.json' if android else run/'review.json')['pages']),26)
    def test_final_frame_and_supplementary_page(self):
        for capture,_ in PLATFORMS:
            run=self.clone(capture,'supplement');android,index,spec=self.adapter(capture,run)
            self.assertAlmostEqual(index['candidates'][-1]['time_s' if android else 'time_seconds'],3.9)
            if android:
                spec['pages'].append({'id':'brief','name':'Brief error','context_id':'CTX','time_s':.5,'state':'error','selection_reason':'Independently located short state'})
            else:
                spec['pages'].append({'id':'brief','title':'Brief error','form':'outer','time_seconds':.5,'state':'error'})
                spec['supplementary_pages']=[{'page_id':'brief','time_seconds':.5,'reason':'Short state located in interval review'}]
            write(run/'spec.json',spec);call(ROOT/capture/'scripts/capture.py','finalize',run,run/'spec.json')
            data=read(run/'capture.json');self.assertEqual(len(data['pages']),14)
            if not android:self.assertEqual(len(data['coverage']),13);self.assertEqual(data['supplementary_pages'][0]['page_id'],'brief')
    def test_variable_frame_rate_and_rotation(self):
        for capture,_ in PLATFORMS:
            video=self.base/(capture+'variable.mkv')
            subprocess.run(['ffmpeg','-v','error','-i',str(self.videos[0]),'-vf',"select='eq(n,0)+eq(n,4)+eq(n,12)+eq(n,23)+eq(n,39)'",'-vsync','0','-c:v','ffv1',str(video)],check=True)
            run=self.base/(capture+'variable');call(ROOT/capture/'scripts/capture.py','sample',video,run)
            android,index,spec=self.adapter(capture,run)
            self.assertEqual([r['time_s' if android else 'time_seconds'] for r in index['candidates']],[0,1.2,2.3,3.9])
            coded=self.base/(capture+'coded.mp4');rotated=self.base/(capture+'rotated.mp4')
            subprocess.run(['ffmpeg','-v','error','-i',str(self.videos[0]),'-c:v','libx264','-pix_fmt','yuv420p',str(coded)],check=True)
            subprocess.run(['ffmpeg','-v','error','-display_rotation','90','-i',str(coded),'-c','copy',str(rotated)],check=True)
            rotated_run=self.base/(capture+'rotated');call(ROOT/capture/'scripts/capture.py','sample',rotated,rotated_run)
            android,index,_=self.adapter(capture,rotated_run);row=index['candidates'][0]
            self.assertEqual([row['width_px'],row['height_px']] if android else row['size_px'],[240,320])
    def test_privacy_preserves_raw(self):
        for capture,_ in PLATFORMS:
            if capture.startswith('android'):continue
            run,_,index,_=self.finalized(capture,'privacy',privacy=True);data=read(run/'capture.json');e=data['evidence'][1]
            self.assertEqual(sha(run/e['raw_image']),index['candidates'][1]['raw_sha256'])
            self.assertEqual(len(data['privacy_audit']),1)
            self.assertNotEqual(sha(run/e['raw_image']),sha(run/e['image']))

if __name__=='__main__':unittest.main()
