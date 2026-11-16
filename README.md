# iPhone Duo 适配审查 Skill Set

给 Codex 一个 App 录屏，提取稳定页面截图，对照苹果官方依据逐页审查，并输出带编号标注的问题报告。

## 包含什么

| Skill | 负责内容 |
|---|---|
| App 录屏页面截图 `app-video-page-capture` | App 页面筛选、稳定截图、去重、脱敏与证据留存 |
| iPhone Duo 设计规范 `iphone-duo-design-guidelines` | 按屏幕姿态检查可见布局，提供官方依据与适用条件 |
| iPhone Duo 适配审查 `iphone-duo-adaptation-review` | 串联截图和审查，归并、编号、标注并发布报告；交付后总结共性问题 |

工作流程：**完整截图 → 逐页审查与复查 → 同类问题归并 → 标注报告 → 聊天中总结共性问题**。

## 下载与安装

1. [下载 ZIP](https://github.com/Janetzhengxinglin/iphone-duo-skill-set/archive/refs/heads/main.zip)，解压。
2. 在解压目录执行：

   ```bash
   python3 install.py
   ```

   三个 skill 会一起安装到 `~/.codex/skills/`。同名旧版本会先备份，安装完成后显示备份位置。也可以手动复制 `skills/` 中的三个目录到该位置。
3. 在支持本地 skills 的 Codex 中重新打开会话。处理录屏的 Python 环境需要：

   ```bash
   python3 -m pip install -r requirements.txt
   ```

发布到 Figma 需要可用的 Figma 工具及目标文件编辑权限；发布到飞书需要已授权的飞书文档工具和写入 skill。它们不随本仓库安装。缺少发布工具时可保留本地 HTML 草稿，不能视为已交付到指定目标。

## 如何使用

把本地录屏交给 Codex，并说：

> 使用 $iphone-duo-adaptation-review 审查这个录屏。流程是充值，姿态是折叠态，报告输出到这个 Figma 或飞书链接：……

缺少流程、姿态或输出信息时，skill 会询问。选择 Figma 输出时，需要用户提供可编辑的目标文件链接；未提供会交互询问，不使用历史默认文件。重点支持 **折叠态、展开－横屏、展开－竖屏**，也支持混合录屏。仅审查 App 内页面，外部浏览器页面排除。

## 输出结果

- **主报告**：同类问题统一编号、示例说明一次；全部问题页面放入汇总，附准确标注和可点击的官方依据。
- **当前聊天**：报告交付后总结本轮共性问题，并询问是否另建飞书文档。
- **可选共性文档**：按“大类｜共性问题表现｜图片示例｜官方依据与修改建议”输出表格，描述客观现象。

全部截图、时间点和逐页审查记录保存在本轮任务目录，便于回溯；不在报告中展示技术索引。

## 依据与范围

依据包括 Apple 的 [iPhone Duo](https://developer.apple.com/iphone-duo/)、[准备指南](https://developer.apple.com/iphone-duo/prepare/)、[Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)、[官方设计视频](https://developer.apple.com/videos/play/tech-talks/111466/)和经核实的官方 UI Kit。完整来源、引用与例外见 [规范来源索引](skills/iphone-duo-design-guidelines/references/sources.json)。来源快照的核对日期见各条记录，使用时需留意官方更新。

审查优先处理可见适配缺陷；平台布局指导差异单独说明。截图审查不能替代交互测试、代码检查或 Apple 提交合规检查。脚本负责证据与排版，逐页判断由 Codex 执行。

本仓库不包含实际业务录屏、截图或报告。第三方参考材料的权利和用途见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

UI Kit 链接指向官方资源入口；使用时在可访问的资源副本中按 Frame 名称和版本查找，不依赖作者个人 Figma 副本。
