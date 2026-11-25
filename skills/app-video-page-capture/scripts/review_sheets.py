"""Create readable whole-page review sheets and source mappings using ffmpeg."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('capture'); p.add_argument('output')
    p.add_argument('--pages-per-sheet', type=int, choices=[1, 2, 4], default=4)
    args = p.parse_args()
    source = Path(args.capture).resolve(); out = Path(args.output).resolve()
    if out.exists(): p.error('输出目录已存在，保留旧版本并使用新目录')
    data = json.loads(source.read_text(encoding='utf-8'))
    evidence = {e['id']: e for e in data['evidence']}
    rows = []
    for page in data['pages']:
        eid = page.get('image_evidence_id') or page['evidence_ids'][0]
        e = evidence[eid]; path = Path(e.get('path') or e['image'])
        digest = e.get('sha256') or e['image_sha256']
        if not path.is_absolute(): path = source.parent / path
        path = path.resolve()
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest: p.error('证据改变: '+page['id'])
        rows.append({'page_id': page['id'], 'path': str(path), 'sha256': digest, 'evidence_id': eid})
    if not rows or len({r['page_id'] for r in rows}) != len(rows): p.error('页面清单为空或 ID 重复')
    out.mkdir(parents=True)
    sheets = []
    for start in range(0, len(rows), args.pages_per_sheet):
        chunk = rows[start:start+args.pages_per_sheet]; cols = min(2, len(chunk))
        cmd = ['ffmpeg', '-v', 'error', '-filter_complex_threads', '1']
        for row in chunk: cmd += ['-i', row['path']]
        filters = ['[%d:v]scale=600:800:force_original_aspect_ratio=decrease,pad=600:800:(ow-iw)/2:(oh-ih)/2:white,setsar=1[t%d]'%(i,i) for i in range(len(chunk))]
        if len(chunk) == 1: filters.append('[t0]null[out]')
        else:
            layout = '|'.join('%d_%d'%((i%cols)*600,(i//cols)*800) for i in range(len(chunk)))
            filters.append(''.join('[t%d]'%i for i in range(len(chunk)))+'xstack=inputs=%d:layout=%s:fill=white[out]'%(len(chunk),layout))
        dest = out/('sheet-%03d.png'%len(sheets))
        cmd += ['-filter_complex', ';'.join(filters), '-map', '[out]', '-frames:v', '1', '-threads', '1', str(dest)]
        subprocess.run(cmd, check=True, capture_output=True)
        cells = [{**row, 'cell_bbox_px': [(i%cols)*600,(i//cols)*800,600,800]} for i,row in enumerate(chunk)]
        sheets.append({'path': str(dest), 'width_px': cols*600, 'height_px': math.ceil(len(chunk)/cols)*800, 'cells': cells})
    manifest = {'source_capture': str(source), 'capture_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'sheets': sheets}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('已生成',len(sheets),'张清晰整页拼图；覆盖',len(rows),'页；未执行视觉审查。索引:',out/'manifest.json')


if __name__ == '__main__': main()
