"""Shared sequential evidence decoder; native platform schemas live in capture.py."""
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import subprocess


def execute(args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stderr[-2000:] or 'Video decoding failed')
    return result


def probe(video):
    data = json.loads(execute(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(video)]).stdout)
    stream = next((s for s in data['streams'] if s.get('codec_type') == 'video'), None)
    if stream is None:
        raise ValueError('No video stream')
    duration = float(stream.get('duration') or data['format'].get('duration') or 0)
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError('Invalid video duration')
    return {'duration_s': duration, 'encoded_width_px': stream['width'],
            'encoded_height_px': stream['height'],
            'has_audio': any(s.get('codec_type') == 'audio' for s in data['streams'])}


def dimensions(path):
    with Path(path).open('rb') as handle:
        header = handle.read(24)
    if not header.startswith(bytes([137,80,78,71,13,10,26,10])):
        raise ValueError('Expected lossless PNG')
    return struct.unpack('>II', header[16:24])


def sequential_sample(video, directory, interval=1.0):
    if not math.isfinite(interval) or interval < .1:
        raise ValueError('Sampling interval must be at least 0.1 seconds; supplement shorter states')
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    if any(directory.glob('sample-*.png')):
        raise ValueError('Samples already exist; use a new directory')
    # Retain the actual normalized presentation timestamp. Autorotation is enabled.
    tail=max(0.0,probe(video)['duration_s']-interval)
    filters = 'setpts=PTS-STARTPTS,select=gte(t\,selected_n*%s)+gte(t%s%s),showinfo' % (interval,chr(92)+',',tail)
    result = execute(['ffmpeg', '-hide_banner', '-loglevel', 'info', '-i', str(video),
                      '-vf', filters, '-vsync', '0', '-start_number', '0',
                      '-threads', '1', str(directory / 'sample-%05d.png')])
    times = []
    for line in result.stderr.splitlines():
        if 'Parsed_showinfo' in line and 'pts_time:' in line and ' n:' in line:
            times.append(float(line.split('pts_time:',1)[1].split()[0]))
    paths = sorted(directory.glob('sample-*.png'))
    if not paths or len(paths) != len(times):
        raise ValueError('Decoded frames and source timestamps do not match')
    rows = []
    for index, (path, timestamp) in enumerate(zip(paths, times)):
        width, height = dimensions(path)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append({'frame_index': index, 'time_s': timestamp, 'path': str(path),
                     'sha256': digest, 'visual_sha256': digest,
                     'width_px': width, 'height_px': height})
    return rows


def extract_frame(video, seconds, output):
    if not math.isfinite(seconds) or not 0 <= seconds < probe(video)['duration_s']:
        raise ValueError('Frame time outside recording')
    output = Path(output)
    if output.exists():
        raise ValueError('Evidence already exists; do not overwrite')
    output.parent.mkdir(parents=True, exist_ok=True)
    execute(['ffmpeg', '-v', 'error', '-i', str(video), '-vf',
             'setpts=PTS-STARTPTS,select=gte(t\,%s)' % seconds,
             '-vsync', '0', '-frames:v', '1', '-threads', '1', str(output)])
    if not output.is_file():
        raise ValueError('No frame at requested time')
    return dimensions(output)
