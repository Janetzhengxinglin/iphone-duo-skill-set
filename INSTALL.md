# 安装与联动检查

## 安装目录

一次安装以下三个目录，保留同级结构：

| Skill | 仓库路径 |
|---|---|
| App 录屏页面截图 | `skills/app-video-page-capture` |
| iPhone Duo 设计规范 | `skills/iphone-duo-design-guidelines` |
| iPhone Duo 适配审查 | `skills/iphone-duo-adaptation-review` |

在 Codex 中优先使用内置 `skill-installer`，一次指定这三个路径。已有同名 skill 时，先核对版本并备份，保留用户修改。

## 运行依赖

检查处理录屏的 Python 环境能否导入 `cv2`（OpenCV）和 `PIL.Image`（Pillow）；缺少时，在适用环境中安装根目录 `requirements.txt` 的依赖。

## 安装后检查

1. 用处理录屏的 Python 运行已安装的 `iphone-duo-adaptation-review/scripts/preflight.py`，检查三个目录、兼容版本和依赖。
2. 运行 `iphone-duo-design-guidelines/scripts/validate_rules.py`，核对规则来源完整性。
3. 首次审查时统一调用 `iphone-duo-adaptation-review`，全部过程数据保存在同一任务目录。

脚本路径按实际安装位置解析为绝对路径。Figma／飞书工具及目标写入权限在选择输出目标后检查。
