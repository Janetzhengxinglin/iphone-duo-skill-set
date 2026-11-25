# 截图与证据契约

从竞品 skill 剥离稳定帧读取、紧范围脱敏、清晰图导出和视觉复核；独立实现采样及交接。不继承竞品目录、流程箭头、审核前用户审批、输入最多两张、省略键盘的规则。

source/ 原视频副本；candidates/ 拼图索引；evidence/raw/ 原图；evidence/images/ 受审图；capture.json 交接。都在本次项目，不进 skill。

sample 默认每0.5秒采样并保留首末帧，变化分数仅提示补看。视觉确认全部拼图，补查快速间隔；--interval 可缩小。覆盖记录验证不证明视觉识别完整。

交互名称：折叠态=合上后的外屏竖屏（outer）；展开－横屏=完全展开内屏横屏（inner-landscape）；展开－竖屏=完全展开内屏竖屏（inner-portrait）。接受用户使用普通连字符“展开-横屏/展开-竖屏”的写法，后台标识不变。

selection.json：
- pages 每项 id（唯一后台ID）、title（页面名和必要状态）、state、form（outer/inner-landscape/inner-portrait）、time_seconds、container（默认page）。可选 crop_px=[x,y,w,h] 仅去录屏外边框；privacy=[{region:[x,y,w,h],type,reason,allow_large:false}]，归一化坐标在裁边后图中。
- coverage 每项 candidate_id、disposition（retained/duplicate/browser/non_app/transition/loading）、reason；retained/duplicate 需 page_id 对应 pages。全部候选分类，不同页面/姿态/状态不合并。最终帧可选邻近更稳定时间。

阶段交接条件：完整录屏范围已遍历；全部候选已分类；独立页面和布局状态已去重或保留；必要补帧已完成，所选图已有完整来源及清晰拼图索引；capture.json 与图片一致。满足这些条件后统一交接，才进入设计规范审查。候选选帧不筛选适配问题；成品拼图巡检时可同时确认质量和适配，不增加独立全量人工质检。

capture.json 包含 schema_version、videos、pages、evidence、coverage、candidate_index、privacy_audit。outer context 是 display=outer,orientation=portrait,posture=closed；inner 是 display=inner,orientation=landscape/portrait,posture=open，container独立记录。
evidence：time_seconds、image、raw_image、image_sha256、raw_sha256、size_px、crop_from_raw_px。编号、时间点不显示。受审图保原尺寸；不能把脱敏造成的模糊/空白视为 App 缺陷。忽略测试浮层记录于任务配置，证据不擦除。

## 覆盖回查

交接前重新顺序检查全部候选索引，并重点核对标为重复、转场或加载的片段是否夹带独立页面、短暂提示或布局状态。对采样可能跳过的快速变化区间补看原视频；不能用已选页面数量或差异分数证明覆盖完整。

集中巡检清晰整页拼图，疑点打开原图：App 与系统边界、比例、稳定性、裁边、脱敏范围应一致。正常滚动、键盘、菜单和系统权限弹窗的不同状态不能因背景页面相同而直接合并。排除项沿用本次授权范围。

在本轮采集记录中保存实际核对范围、分类纠正和补帧结果，不强制另建独立全量自测阶段或文件。只有完成实际回查才记录完成，不能从 selection.json 自动推断视觉复查通过。独立使用时在本项目记录截图方法的改进候选；联动使用时由审查入口集中复盘。
