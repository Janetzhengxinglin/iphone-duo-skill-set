#!/usr/bin/env python3
"""Compatibility entry: output belongs to iphone-duo-adaptation-review."""
import argparse
import sys
from pathlib import Path

def render(path):
    sibling=Path(__file__).resolve().parents[2]/'iphone-duo-adaptation-review'
    if not sibling.is_dir():
        raise RuntimeError('Install iphone-duo-adaptation-review to generate reports; rule judgment remains independent.')
    sys.path.insert(0,str(sibling/'scripts'))
    from build_report import build
    run=path.parent if path.is_file() else path
    return build(run,Path(__file__).resolve().parents[1],sibling/'assets/report-style.json')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('review',type=Path)
    print(render(p.parse_args().review.resolve()))
