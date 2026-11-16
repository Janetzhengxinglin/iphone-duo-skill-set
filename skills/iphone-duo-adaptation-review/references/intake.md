# 交互与任务数据

一次用交互工具收集缺失字段；不可用则用简短问题：
- 流程，自由填写，允许多个流程。
- 姿态三推荐项：折叠态、展开－横屏、展开－竖屏。支持自由填写混合，逐段记录，不默认一种。
  - 折叠态：合上后的外屏竖屏，后台 form=outer。
  - 展开－横屏：完全展开后的内屏横屏，后台 form=inner-landscape。
  - 展开－竖屏：完全展开后的内屏竖屏，后台 form=inner-portrait。
  - 接受“展开-横屏/展开-竖屏”和原有完整形态名称，转换成同一后台标识。交互与报告均使用简短名称，不改变适用规则。
- 输出 Figma / 飞书文档，以及对应文件或文档库链接。Figma 目标必须由用户提供可编辑文件链接，缺少时交互询问，不取历史目标、不自动新建替代；已提供不重复问。
- 内容：适配缺陷＋平台布局差异 / 仅适配缺陷。首项推荐，指导差异不混算显示缺陷。
不问截图时间点/采样配置，不让用户逐页截图。目标/样式更改只重排版，不重做有效审查。

intake.json：schema_version=1.0、flow（非空）、form（outer/inner-landscape/inner-portrait/mixed）、output（figma/lark）、target（相应URL）、content（defects-and-guidance/defects-only）、video（本地文件）；可选 ignored_overlays（测试浮层描述列表）。

review.json 沿规范契约，另加 report_groups：group_id、problem_type、problem_point（简短组说明）、basis_zh（准确中文）、representative_evidence_ids（可多张）。每个展示组有其所属发现的代表图；有不同位置/现象需多图覆盖。AI 根据本次事实填写，不用占位通用话。逐页观察留 findings，不重复拼进组说明。basis 必须匹配规范原文引用，摘要不替代原文校验。
