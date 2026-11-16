# 页面截图适配审查策略

规则包 0.5.1；默认 profile：three-form-screenshot。目标是发现新机型适配问题，优先三种基础形态，不扩展为一般交互优化。

## 优先级与官方来源对应

|检查层次|判断内容|对应官方依据|
|---|---|---|
|第一优先：可见显示缺陷|尺寸变化后遮挡、裁切、重叠、明显拉伸、错位；页面及弹层位置|[Three steps](https://developer.apple.com/iphone-duo/prepare/) 尺寸风险及媒体裁切；[Preparing your app](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Address-common-layout-and-resizing-considerations) 逐视图、sheet、popover 检查；[Layout 安全区域](https://developer.apple.com/design/human-interface-guidelines/layout#Guides-and-safe-areas)；[Duo 预留区域](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions)|
|第二层：平台布局适配|返回/关闭、工具栏、Tab、系统组件的方向、排列和容器例外|[Duo Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)；[开发文档竖向栏适配](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Optimize-bars-for-vertical-presentation)|

官方确定检查方向；按内容可读性及关键操作影响排序是项目选择，不是苹果官方分级。第一层优先金额、字段、主要操作和导航，成立的实际显示故障计入需要修改。第二层仅有指导差异时不计入显示故障；查明依赖的系统条件与容器例外后才列示。

## 三种形态

|形态|重点|默认页面级栏|
|---|---|---|
|合上外屏竖屏|右侧系统区域与摄像头附近；重要内容、固定按钮|侧边竖向；排除局部控件、文字项和 sheet 例外|
|完全展开内屏横屏|变宽后比例、裁切、重叠；内容与侧边区域关系|侧边竖向；多栏和 sheet 按容器判断|
|完全展开内屏竖屏|正文、金额、字段、按钮、弹层完整性|普通页面水平；sheet 另按 placement|

不画完全展开时的永久折叠禁区；不画未启用内屏摄像头的永久禁区。正常滚动提示、装饰背景延伸、未损失重要主体的等比图片裁切不自动算缺陷。没有比例基准时不凭留白或风格认定拉伸。

截图只判断已展示结果，不检查代码模式、实际点击热区、未展示的大字体和折叠连续性；不输出补录表或未验证页面标签。官方开发 skill 可以扫描代码辅助修复，本 skill 不据截图声称实现用了某个 API。

## 逐项查验与控件内容

默认执行[组件检查清单](component-checklist.md)，逐个可见实例保存检查结果。IOS-04捕获空白/不可辨识控件，不以未知业务功能拒绝观察；先排除装饰、空标题、进度和占位。用户提供的功能事实与截图观察分开。没有比较证据时机型因果记为不作归因，不挂待核实标签。通用显示缺陷单独归类，指导差异及可选体验建议不变成故障。

## 专题视频补充依据

第一优先的安全区域与不对称布局补充[Prepare your app 6:37](https://developer.apple.com/videos/play/tech-talks/111461/?time=397)；第二层的栏方向及例外补充[Raise the bar 3:36](https://developer.apple.com/videos/play/tech-talks/111462/?time=216)。系统浮层及生效预留区域补充[Adaptive layouts 5:23](https://developer.apple.com/videos/play/tech-talks/111463/?time=323)。这些解释既有判据，不改变项目排序；详细条件见[专题规律](official-video-principles.md)。
