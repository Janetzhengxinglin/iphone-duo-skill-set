---
name: iphone-duo-design-guidelines
description: Review visible App layout on iPhone Duo screenshots using verified Apple guidance, prioritizing three basic display forms. Identify visible defects and platform layout differences, and output precise numbered annotations with official links.
---

# iPhone Duo 设计规范

本 skill 将苹果原文、适用条件、例外与截图证据关联，形成可追溯的页面判断。规则包 0.5.1；读取流程修订 2026-11-24。规则编号和检查优先级由项目制定，不是苹果认证标准。

## 审查范围与优先级

先读 [审查策略](references/audit-policy.md) 和 [判断协议](references/decision-protocol.md)。默认 `three-form-screenshot`：优先折叠态（合上后的外屏竖屏）、展开－横屏（完全展开内屏横屏）、展开－竖屏（完全展开内屏竖屏）。交互用这三个简短名称，后台映射仍为 outer、inner-landscape、inner-portrait。录屏仅用于提取稳定页面，判断截图可见内容；浏览器和用户指定测试浮层排除，系统区域保留。

问题发现数量、同页问题数量和问题类型数量均无上限。按优先级完成全部适用检查，所有有截图证据及官方依据的成立问题都记录；优先级只决定顺序，不限制低优先级发现的数量。不预设历史问题类型，不因已发现若干类问题而停止，也不为凑数制造问题。

先读 [组件检查清单](references/component-checklist.md)，查询当前形态的检查卡。每页先识别可见组件（包括空白但形似控件的背景），按组件逐个实例检查，并保存 check_items；不要只找已有问题编号或凭印象挑规则。第一优先是实际遮挡、裁切、重叠、明显拉伸或错位，以及实际控件没有可辨识图标、文字或进度指示，尤其影响金额、字段、主要操作及导航控件的缺陷。第二层检查返回/关闭、工具栏、Tab、系统组件的方向与排列，核对当前形态、容器及官方例外。指导差异和显示故障分开计数；只有显示故障计入需要修改。

不从截图推断不能点击、代码根因、隐藏功能、未展示的文字放大或切换连续性，不给页面挂待核实、未验证、配置待确认、证据有限标签。两栏、sidebar 和姿态专用体验是可选优化。发布条件不在本 skill 范围内。

## 官方依据与查找

[rules.json](references/rules.json) 保存原文、条件、例外与判据；[sources.json](references/sources.json) 保存 17 项来源、读取范围及快照 hash；[来源覆盖](references/source-coverage.md) 与 [逐段覆盖表](references/source-coverage.json) 说明官方段落如何进入查验。[优先级与来源对应](references/audit-policy.md) 用于快速找到检查依据。

HIG 确定设计原则，开发文档确认容器和系统条件，视频解释设计意图，Apple UI Kit 提供指定版本示例。Three steps 的尺寸风险和媒体裁切指导已关联布局规则；其中官方 App resizability skill 是开发协作工具，本 skill 不扫描代码或代替它修复实现。民间 Kit 不能独立作为报错依据。

运行 `python3 scripts/lookup_rules.py outer`、`inner-landscape` 或 `inner-portrait`；弹层可加 `--topic sheet`。日常引用已核查快照，不必每次重读全部来源；官方更新、新情境或冲突影响结论时复核相关正文并升级版本。来源不明确的候选不进入问题清单。遇到栏方向、安全区域、系统浮层或预留区域，读[官方专题审查规律](references/official-video-principles.md)，再引用对应规则中的精确时间点。

完全展开内屏没有永久折叠禁区；外屏摄像头区域始终存在，内屏只在相机启用时生效。普通内屏竖屏为水平栏，sheet、split view、局部控件和宽文字项有例外；不是所有按钮都移到侧边。来源冲突读 [conflicts.json](references/conflicts.json)，Kit 判断读 [kit-index.json](references/kit-index.json)。

## 报告与标注

录屏联动读 [capture-handoff.md](references/capture-handoff.md)，由独立 app-video-page-capture 提供截图，iphone-duo-adaptation-review 编排与生成报告。本 skill 负责逐页判断和官方依据，不收集输出偏好或发布报告。独立截图审查可直接提交同样的证据数据。逐项检查不能省略；通用显示问题捕获但不自动归因于 Duo。全部截图与结论后台保留，报告仅展示所选范围的问题页面；共性说明集中一次，代表图可多张。展示和发布约定见审查入口 skill，原报告保留。

默认文字包含问题点、问题类型及可点击官方依据；编号放截图两侧，统一样式与颜色，引线指向准确对象。用户的执行指令不写入交付画板。渲染器只展示数据，不能把指导差异改写为故障。

输出 review.json，显式标明 profile 和规则版本；运行 scripts/validate_review.py，渲染后目视检查标注。HTML 可用于本地试审；外部写入按用户当前授权执行。

## 扩展与维护

只有用户明确要求动态行为、测量或更广泛审查才启用 `full-evidence`，读 [扩展证据模式](references/full-evidence.md)。完整参考库不意味着每次都检查所有规则。

新增规则先核对官方原文与定位，写明条件、例外及可观察判据。运行 scripts/validate_rules.py 和 skill-creator quick_validate.py；修改查询或渲染逻辑后验证真实输入输出。结构验证不代表完整规范覆盖或 AI 判断质量认证。

## 完成前自测

按 [判断协议](references/decision-protocol.md) 的第二轮视觉复查，从原图重新审视全部受审页面及各组件实例，检查漏报和误报，再核对发现是否完整进入汇总。自测与改进候选保存在本次项目，不写入报告正文。联动审查由入口统一执行 [持续改进](../iphone-duo-adaptation-review/references/continuous-improvement.md)；独立截图审查也执行其中的证据核实与通用方法更新条件。

## 大批量图片读取

逐页判断与第二轮复查遵守 [图片处理协议](../app-video-page-capture/references/image-processing.md)，独立使用时同样分批、记录累计输入和保存接续检查点。候选拼图不代替原图判断，读取预算不减少页面、组件或两轮复查范围。

每次读图前必须执行该协议的本地 check；默认一次 1–2 张、最多 2 张，同时检查像素与尺寸。当前批完成分析并保存结果后再读下一批；失败后单张降量，连续失败或累计预算耗尽则保存进度接续，不能原样重试或减少验收范围。候选、原图、复查与报告预览共用同一累计日志。
