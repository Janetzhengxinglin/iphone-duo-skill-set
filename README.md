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

Codex 会根据素材关联性和工作量选择执行方式：简单或连续流程由主智能体处理；材料可独立处理且有明确收益时，使用子智能体按阶段分工；默认集中巡检和问题重点复查，不另设独立全量质检或第二轮全量原图复读。各任务保留独立结果和完整覆盖记录，最终由主智能体核对并发布。环境不支持子智能体时按相同覆盖要求继续执行。

审查入口 0.2.14 保留统一输出要求：标题下只留一句结论；官方区优先逐项对应的抽象图解、一句说明和出处；图文共用边线，编号就近放在图外；参考图紧凑适中，底部保留全部独立问题与重复来源映射。实际预览验收与图片预算规则见 [视觉呈现与验收](skills/iphone-duo-adaptation-review/references/output-presentation.md)。

长录屏会保留完整候选索引，将连续完全相同的候选折叠为首尾代表帧，再分批读取图片。短暂状态和变化画面仍需检查；默认清晰整页拼图覆盖全部页面，疑点打开原图，复查集中于问题和报告；严格双轮仅在明确要求时执行。图片输入日志与检查点保存在任务目录，接近读取预算时交接到新上下文。具体执行方法见 [图片处理协议](skills/app-video-page-capture/references/image-processing.md)。

### 2026-11-24 图片读取更新

图片预算覆盖采集、全页巡检、重点复查和报告预览：

| 改动 | 原因 |
|---|---|
| 默认每次 1–2 张，最多 2 张；当前批分析并保存后再读下一批 | 减少单次输入，避免循环或并行一次返回多批图片 |
| 增加读图前 `check`，同时检查数量、总像素、最长边和文件大小 | 单张超大拼图也可能超限，文件压缩不能替代像素预算 |
| 首次超限后降为单张、默认像素预算减半，禁止原样失败组合重试 | 重试应实际降低输入负担，并保留失败记录 |
| 同一上下文两次失败或累计预算耗尽时保存进度、接续到新上下文 | 分批和等待不会清空聊天历史 |
| 保留全部证据、全页巡检和问题回查记录 | 节省每次输入不能演变成少审或漏审 |

默认本批总像素 400 万、单图最长边 2560、总文件大小 8 MiB、累计约 30 次图片输入均是本地保守预算，可按实际输入调整，不能保证平台永不超限。脚本检查不拦截图片工具；执行者必须先检查再读取。超大原图保留原文件和整页检查要求，候选预览可拆分或缩小，细节图按覆盖区域补查。

当前采集 skill 为 0.1.4，审查入口为 0.2.14；2026-11-25 回退到集中批量巡检和重点复查，苹果规则包仍为 0.5.1。执行方法见 [集中批量审核](skills/iphone-duo-adaptation-review/references/batch-execution.md)。

## 依据与范围

依据包括 Apple 的 [iPhone Duo](https://developer.apple.com/iphone-duo/)、[准备指南](https://developer.apple.com/iphone-duo/prepare/)、[Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)、[官方设计视频](https://developer.apple.com/videos/play/tech-talks/111466/)和官方 UI Kit。完整来源、引用与例外见 [规范来源索引](skills/iphone-duo-design-guidelines/references/sources.json)。

审查优先处理可见适配缺陷；平台布局指导差异单独说明。审查范围是截图可见内容，交互测试、代码检查及 Apple 提交合规检查需另行开展。
