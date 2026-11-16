#!/usr/bin/env python3
"""Install the three sibling skills, backing up any existing versions first."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import tempfile

NAMES = ('app-video-page-capture', 'iphone-duo-design-guidelines', 'iphone-duo-adaptation-review')


def install(source, destination):
    for name in NAMES:
        if not (source / name / 'SKILL.md').is_file():
            raise ValueError(f'缺少 skill：{name}')
    destination.mkdir(parents=True, exist_ok=True)
    # Stage all new files before modifying any existing skill.
    with tempfile.TemporaryDirectory(prefix='.duo-install-', dir=destination.parent) as temp:
        staged = Path(temp)
        for name in NAMES:
            shutil.copytree(source / name, staged / name)
        backup = destination.parent / 'skill-backups' / ('iphone-duo-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
        existing = [name for name in NAMES if (destination / name).exists() or (destination / name).is_symlink()]
        if existing:
            backup.mkdir(parents=True)
        moved, installed = [], []
        try:
            for name in existing:
                (destination / name).rename(backup / name)
                moved.append(name)
            for name in NAMES:
                (staged / name).rename(destination / name)
                installed.append(name)
        except Exception:
            for name in installed:
                shutil.rmtree(destination / name)
            for name in moved:
                (backup / name).rename(destination / name)
            raise
    print(f'已安装 3 个 skill：{destination}')
    if existing:
        print(f'旧版备份：{backup}')
        print('恢复时，将备份中的对应目录复制回安装目录。')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, default=Path.home() / '.codex' / 'skills', help='安装目录（默认 ~/.codex/skills）')
    args = parser.parse_args()
    install(Path(__file__).resolve().parent / 'skills', args.dest.expanduser().resolve())
