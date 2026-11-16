# 官方专题的审查规律

用于解释已有规则的适用条件，日常按姿态、组件查找，不必每次重读全部视频。六个专题的完整官方文字稿已阅读；Group Lab未纳入本次判错依据。快照与时间点在sources.json和source-coverage.json中登记。原文决定条件，下列中文为审查归纳，不是苹果新增认证条款。

|判断规律|检查方式与例外|已有规则|官方定位|
|---|---|---|---|
|先姿态，再容器，再控件内容|普通内屏竖屏水平；竖栏依赖容器贴边，split view仅detail参与。sheet按placement判断。纯文字、自定义项和键盘附属栏有横排例外。不能把工具栏条件推广为所有系统组件都允许同样例外。|DUO-04、DUO-10、DUO-13|[容器](https://developer.apple.com/videos/play/tech-talks/111462/?time=216)、[内容](https://developer.apple.com/videos/play/tech-talks/111462/?time=426)、[键盘](https://developer.apple.com/videos/play/tech-talks/111462/?time=600)|
|前景与背景分开判断安全区域|交互控件放安全区域内；背景可铺满并延伸到栏后。安全区域和边距可不对称，竖栏也可能位于左侧。仅凭背景延伸、左右留白不同不报错。|IOS-01、DUO-11|[安全区域](https://developer.apple.com/videos/play/tech-talks/111461/?time=397)、[不对称](https://developer.apple.com/videos/play/tech-talks/111461/?time=432)|
|预留区域必须确认生效条件|完全展开时折叠区域不生效；内屏摄像头启用时才生效。部分折叠扩展审查中，关联控件一起避让，连续滚动内容不强制移位。|DUO-05、DUO-06|[折叠条件](https://developer.apple.com/videos/play/tech-talks/111463/?time=447)、[摄像头条件](https://developer.apple.com/videos/play/tech-talks/111463/?time=482)|
|系统自适应不能当成错位或功能缺失|系统浮层会围绕预留区域重新定位；工具栏空间不足可把项目收入overflow。只判断实际可见遮挡、裁切；单图不证明收起项目无法访问。|DUO-09、DUO-10、DUO-11|[浮层](https://developer.apple.com/videos/play/tech-talks/111463/?time=323)、[收起](https://developer.apple.com/videos/play/tech-talks/111462/?time=700)|
|默认行为有针对性例外|底部控件密集的单页应用、工具栏仅一个关闭按钮的控件密集sheet，可考虑关闭竖栏。例外不解除可读性和遮挡检查。|DUO-04、DUO-10|[关闭竖栏的场景](https://developer.apple.com/videos/play/tech-talks/111462/?time=860)|
|扩展能力按场景使用|多屏、多场景、铰链效果及相机API不变成所有页面必改项。相机页面可检查实际可见比例、主体裁切与明显方向问题；截图不证明镜头切换、会话连续性或API配置。|DUO-01；其余为扩展实现背景|[多显示与场景](https://developer.apple.com/videos/play/tech-talks/111464/)、[相机布局](https://developer.apple.com/videos/play/tech-talks/111465/?time=423)|

HIG提供设计原则，开发文档与专题视频共同确认系统、容器及内容条件，UI Kit提供版本化示例。详细专题可以补充概览省略的条件，不能因来源类型而自动忽略明确原文；冲突影响结论时复核条件与版本。

默认仍是折叠态、展开－横屏、展开－竖屏的App截图审查。规则和优先级由项目组织；开发API、SDK版本、多窗口能力及商店提交要求不能由截图推断。
