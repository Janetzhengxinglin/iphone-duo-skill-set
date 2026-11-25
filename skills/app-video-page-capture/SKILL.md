---
name: app-video-page-capture
description: Extract stable App page and layout-state screenshots from local recordings for adaptation review. Preserve keyboard and overlay states and traceable evidence, independently of competitor research.
---

# App 录屏页面截图

从录屏提取可审查的 App 页面状态。独立于竞品截图，运行时不调用 flow-video-review；不判断规范、不发布报告。版本 0.1.4；批量执行回退 2026-11-25。

1. 取得流程、姿态、本次项目目录，独立调用只问缺失的流程/姿态。交互选项统一为“折叠态、展开－横屏、展开－竖屏”，分别映射 outer、inner-landscape、inner-portrait；混合姿态逐页记录。不要向用户展示后台英文标识。
2. 读 [截图与交接](references/capture-contract.md)。执行 `python3 scripts/capture.py sample VIDEO RUN_DIR`，生成候选缩略图、拼图和索引。依赖 OpenCV/Pillow；缺少时先查本机运行时，不自行全局安装。
3. 顺序看拼图，识别 App 边界、页面、状态。候选采样不等于页面识别完成。快速变化、短暂错误、键盘/弹窗片段用 `frame VIDEO SECONDS OUTPUT` 补帧；必要时更小 --interval 到新的候选目录。不能仅按图像差异去重。
4. 编写 selection.json 的页面状态与全部候选分类。无需用户填写时间点。先看全部候选及可疑时间间隔，未出现的状态不造。
5. `python3 scripts/capture.py finalize RUN_DIR SELECTION_JSON` 保存原始全尺寸图、紧范围脱敏图与 capture.json；脚本核对来源与尺寸，集中清晰拼图巡检时确认比例、裁边、稳定性和脱敏；疑点查看原图。

只收集 App 内画面；外部浏览器/桌面排除，App 内嵌网页保留。跳过转场和无意义加载。相同页面/姿态/状态合并，键盘、弹窗、菜单、错误提示、布局不同的滚动状态分别保留，不设竞品输入状态上限。

忽略指定测试浮层但不擦除后猜内容。系统状态栏和摄像头区域保留，不能当测试浮层。只裁明确的录屏外边框，不裁系统或 App 内容，不拉伸。只模糊仍可读私人值，已脱敏不重复处理；保留标签控件和受审布局，原图与脱敏图分开存。

交接前必须遍历本次全部录屏、分类全部候选并完成全部选帧及集中质量核对。只在完整 capture.json 和全部截图准备好后统一交接，不逐张或分批触发适配审查。候选阶段只确认页面状态、不先挑问题页；成品清晰拼图的质量确认可与适配巡检同时完成，分别保留实际观察，不重复读取同图作独立全量质检。截图编号和时间点仅后台，项目素材、页面名、数量或结论不进入 skill。

## 交接前自测

执行 [截图与交接](references/capture-contract.md) 中的集中覆盖核对，确认采样、去重、裁边和脱敏没有丢失应保留状态或制造假缺陷。回查记录留在项目目录；发现遗漏时修订完整 capture.json 后再交接。联动审查入口时，将本轮截图阶段的执行问题交给入口统一复盘，不把具体页面写入 skill。

## 图片处理与读取预算

采样、选帧和质量回查前读取 [图片筛选与接续](references/image-processing.md)。使用压缩候选拼图及完整分组索引分类，图片按预算分批输入；文件生成不等于已读取或审查完成。

按图片协议执行读取前预算检查、记账和接续；每个业务流程连续工作，疑点才额外打开原图。
