#!/usr/bin/env python3
"""Check the installed skill set before starting capture; not a visual QA test."""
import importlib
import shutil
import json
from pathlib import Path
import re
import sys


SUPPORTED = {
    'app-video-page-capture': '0.1.5',
    'iphone-duo-design-guidelines': '0.5.1',
}
REQUIRED = {
    'app-video-page-capture': ['SKILL.md', 'scripts/capture.py', 'scripts/sequential_frames.py', 'scripts/review_sheets.py', 'scripts/image_batches.py', 'references/capture-contract.md', 'references/image-processing.md'],
    'iphone-duo-design-guidelines': ['SKILL.md', 'scripts/validate_rules.py', 'scripts/validate_review.py',
        'scripts/checklist.py', 'references/rules.json', 'references/component-checklist.json',
        'references/audit-profiles.json', 'references/capture-handoff.md'],
    'iphone-duo-adaptation-review': ['SKILL.md', 'scripts/workflow.py', 'scripts/build_report.py', 'scripts/validate_handoffs.py', 'references/agent-coordination.md',
        'references/intake.md', 'references/report.md', 'references/figma-output.md',
        'references/lark-output.md', 'references/common-problems.md', 'assets/report-style.json'],
}


def check(skills_root):
    errors, versions = [], {}
    for name, files in REQUIRED.items():
        root = skills_root / name
        for relative in files:
            if not (root / relative).is_file():
                errors.append(f'缺少 {name}/{relative}，请补齐整套 skill。')
        if (root / 'SKILL.md').is_file():
            text = (root / 'SKILL.md').read_text()
            if not re.search(r'^name:\s*' + re.escape(name) + r'\s*$', text, re.M):
                errors.append(f'{name} 的 skill 名称不匹配。')
            match = re.search(r'(?:版本|规则包)\s*(\d+\.\d+\.\d+)', text)
            versions[name] = match.group(1) if match else None
            if name in SUPPORTED and versions[name] != SUPPORTED[name]:
                errors.append(f'{name} 版本不兼容：本入口支持 {SUPPORTED[name]}，请安装同一发布包的三个 skill。')

    refs = skills_root / 'iphone-duo-design-guidelines' / 'references'
    for filename in ['rules.json', 'component-checklist.json', 'audit-profiles.json']:
        try:
            version = json.loads((refs / filename).read_text())['version']
            if version != SUPPORTED['iphone-duo-design-guidelines']:
                errors.append(f'{filename} 的规则版本不匹配。')
        except (OSError, ValueError, KeyError) as exc:
            errors.append(f'无法读取 {filename}：{exc}')

    for module, package in [('PIL.Image', 'Pillow')]:
        try:
            importlib.import_module(module)
        except Exception as exc:
            errors.append(f'当前 Python 无法加载 {package}：{exc}；请检查可用运行环境或安装截图依赖。')
    for executable in ['ffmpeg','ffprobe']:
        if not shutil.which(executable): errors.append('缺少 '+executable)
    return {'ready': not errors, 'versions': versions, 'errors': errors,
            'scope': '安装完整性、支持版本和 Python 依赖；不验证视觉审查质量或 Figma/飞书访问权限。'}


if __name__ == '__main__':
    result = check(Path(__file__).resolve().parents[2])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result['ready'] else 1)
