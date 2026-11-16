# iPhone Duo 适配审查 Skill Set

给 Codex 一个 App 录屏，提取稳定页面截图，对照苹果官方依据逐页审查，并输出带编号标注的问题报告。

## 包含什么

| Skill | 负责内容 |
|---|---|
| App 录屏页面截图 `app-video-page-capture` | App 页面筛选、稳定截图、去重、脱敏与证据留存 |
| iPhone Duo 设计规范 `iphone-duo-design-guidelines` | 按屏幕姿态检查可见布局，提供官方依据与适用条件 |
| iPhone Duo 适配审查 `iphone-duo-adaptation-review` | 串联截图和审查，归并、编号、标注并发布报告；交付后总结共性问题 |

工作流程：**完整截图 → 逐页审查与复查 → 同类问题归并 → 标注报告 → 聊天中总结共性问题**。

## 安装

在 Codex 中发送：

```text
请使用 $skill-installer 安装完整的 iPhone Duo 适配审查 Skill Set，并配置依赖、完成联动检查。
仓库：https://github.com/Janetzhengxinglin/iphone-duo-skill-set
```

安装完成后，在下一轮对话中开始审查。

<details>
<summary>手动下载安装</summary>

1. [下载 ZIP](https://github.com/Janetzhengxinglin/iphone-duo-skill-set/archive/refs/heads/main.zip) 并解压。
2. 在解压目录执行：

```bash
python3 install.py
python3 -m pip install -r requirements.txt
```

三个 skill 安装到 `~/.codex/skills/`，已有同名版本会先备份。

[安装与联动检查详情](INSTALL.md)

</details>

## 开始审查

提交录屏，并发送：

```text
使用 $iphone-duo-adaptation-review 审查这个录屏。
流程：充值；姿态：折叠态；输出：Figma／飞书目标链接。
```

| 需要提供 | 填写内容 |
|---|---|
| 录屏 | 本地 App 录屏文件 |
| 流程 | 如充值、支付、提现 |
| 姿态 | 折叠态、展开－横屏、展开－竖屏；支持混合 |
| 输出 | Figma 或飞书目标链接，需有写入权限 |

缺少信息时，Codex 会询问。总入口自动串联三个 skill，仅审查 App 内页面。

发布到 Figma 需要 Figma 工具；发布到飞书需要已授权的文档工具。

## 输出结果

- **主报告**：同类问题统一编号、示例说明一次；全部问题页面放入汇总，附准确标注和可点击的官方依据。
- **当前聊天**：报告交付后总结本轮共性问题，并询问是否另建飞书文档。
- **可选共性文档**：按“大类｜共性问题表现｜图片示例｜官方依据与修改建议”输出表格，描述客观现象。

全部截图和逐页审查记录保留，便于复查。

## 依据与范围

依据包括 Apple 的 [iPhone Duo](https://developer.apple.com/iphone-duo/)、[准备指南](https://developer.apple.com/iphone-duo/prepare/)、[Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)、[官方设计视频](https://developer.apple.com/videos/play/tech-talks/111466/)和官方 UI Kit。完整来源、引用与例外见 [规范来源索引](skills/iphone-duo-design-guidelines/references/sources.json)。

审查优先处理可见适配缺陷；平台布局指导差异单独说明。审查范围是截图可见内容，交互测试、代码检查及 Apple 提交合规检查需另行开展。
