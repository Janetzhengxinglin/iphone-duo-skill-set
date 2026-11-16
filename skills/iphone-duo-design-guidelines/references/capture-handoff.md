# 从录屏截图到规则审查

默认 three-form-screenshot。由独立 app-video-page-capture 提供 capture.json 全部页面与证据，经 iphone-duo-adaptation-review 转换并编排。无需竞品截图 skill；不启动 Figma 基线比对或一般 App QA。外屏竖屏、完全展开内屏横屏与竖屏优先。外部浏览器与用户指定测试浮层排除，App 内嵌网页保留；截图保留系统区域和原比例。录屏仅作为截图来源。

每个页面状态保存来源时间、显示配置和未经标注的证据图。脱敏不覆盖受审对象。正常滚动、sheet 和菜单可以是不同截图状态；未出现的状态不生成未验证条目。外部原始文档不改，最终输出按用户授权。

## review.json

- schema_version=1.0、rule_version、audit_profile、title、scope。
- videos：id、sha256、duration_seconds；可选 file 用于核验视频。
- pages：id、title、context、evidence_ids。
- evidence：id、page_id、video_id、time_seconds、image、image_sha256、size_px、crop_from_raw_px。
- checks：每页每个当前 profile 规则一项，包含 rule_id、decision、observation、reason、applicability_facts、exceptions_checked、evidence_ids、missing_evidence（默认空）。
- findings：id、page_id、rule_id、decision、kind、group_id、number、title、observation、impact、recommendation、evidence_ids、annotations、basis。basis 为 source_id、quote、section、url，须匹配规则卡引用；可加 quote_zh 中文摘要供展示，不替代原文校验。
- annotations：evidence_id、region（展示图归一化 xywh）；可选 side=left/right。

同 group_id 跨页同 number，不同组不得共用 number。issue 的 kind 为 visible-defect，guidance_deviation 为 default-layout-guidance。原图、标注图、问题说明共享一份数据；坐标来自证据图，不当作运行时 pt。先 scripts/validate_review.py，再渲染与目视复核。

用户明确选择动态审查才读 [full-evidence.md](full-evidence.md)，不能自行添加交互测试。

## 0.5.1 必需的逐项检查记录

新审查 schema_version 仍为1.0，rule_version=0.5.1，新增 checklist_version=0.5.1 与 check_items。
每页 component_inventory：实例 id、type（page/button/toolbar/tab/system/media/sheet/keyboard/menu/camera）、evidence_id、region（归一化 xywh）。页面本体用一个page实例；可识别的每个按钮都列实例，空白控件不可漏识别。
check_items：page_id、check_id、component_id、decision、observation、reason、exceptions_checked、evidence_ids、finding_ids。每页18张截图卡都要筛选；有适用组件则每实例一项，没有对象用 component_id=null、not_applicable 和具体原因。unknown对象仅保留观察和筛选理由，不伪称所有控件通过。schema校验保障记录完整，不证明视觉识别完整。
findings新增 check_ids、cause_attribution（not_assessed/confirmed_duo_related），可选 functional_evidence={source:user/runtime,statement:...}。无行为证据不得声称没有功能，无比较证据不得声称Duo造成。通用可见问题仍用visible-defect，在展示中标明通用显示问题。check_items中的issue/guidance_deviation必须指向实际finding。
