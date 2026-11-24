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
```

Codex 会询问缺少的流程名称、屏幕姿态和报告输出位置，按提示补充即可。已经提供的信息不会重复询问。

支持折叠态、展开－横屏、展开－竖屏及混合录屏，仅审查 App 内页面。

输出到 Figma 或飞书时，需提供有写入权限的目标链接，并配置对应工具。

## 输出结果

- **主报告**：同类问题统一编号、示例说明一次；全部问题页面放入汇总，附准确标注和可点击的官方依据。
- **当前聊天**：报告交付后总结本轮共性问题，并询问是否另建飞书文档。
- **可选共性文档**：按“大类｜共性问题表现｜图片示例｜官方依据与修改建议”输出表格，描述客观现象。

全部截图和逐页审查记录保留，便于复查。

长录屏会保留完整候选索引，将连续完全相同的候选折叠为首尾代表帧，再分批读取图片。短暂状态和变化画面仍需检查；两轮审查保持全页面覆盖。图片输入日志与检查点保存在任务目录，接近读取预算时交接到新上下文。具体执行方法见 [图片处理协议](skills/app-video-page-capture/references/image-processing.md)。

### 2026-11-24 图片读取更新

本次更新覆盖采集、逐页审查、第二轮复查和报告预览：

| 改动 | 原因 |
|---|---|
| 默认每次 1–2 张，最多 2 张；当前批分析并保存后再读下一批 | 减少单次输入，避免循环或并行一次返回多批图片 |
| 增加读图前 `check`，同时检查数量、总像素、最长边和文件大小 | 单张超大拼图也可能超限，文件压缩不能替代像素预算 |
| 首次超限后降为单张、默认像素预算减半，禁止原样失败组合重试 | 重试应实际降低输入负担，并保留失败记录 |
| 同一上下文两次失败或累计预算耗尽时保存进度、接续到新上下文 | 分批和等待不会清空聊天历史 |
| 保留全部证据、待审清单和两轮覆盖要求 | 节省每次输入不能演变成少审或漏审 |

默认本批总像素 400 万、单图最长边 2560、总文件大小 8 MiB、累计约 30 次图片输入均是本地保守预算，可按实际输入调整，不能保证平台永不超限。脚本检查不拦截图片工具；执行者必须先检查再读取。超大原图保留原文件和整页检查要求，候选预览可拆分或缩小，细节图按覆盖区域补查。

采集 skill 升至 0.1.4，审查入口升至 0.2.11；规范 skill 增加读取流程规则，苹果规则包仍为 0.5.1。

## 依据与范围

依据包括 Apple 的 [iPhone Duo](https://developer.apple.com/iphone-duo/)、[准备指南](https://developer.apple.com/iphone-duo/prepare/)、[Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)、[官方设计视频](https://developer.apple.com/videos/play/tech-talks/111466/)和官方 UI Kit。完整来源、引用与例外见 [规范来源索引](skills/iphone-duo-design-guidelines/references/sources.json)。

审查优先处理可见适配缺陷；平台布局指导差异单独说明。审查范围是截图可见内容，交互测试、代码检查及 Apple 提交合规检查需另行开展。
