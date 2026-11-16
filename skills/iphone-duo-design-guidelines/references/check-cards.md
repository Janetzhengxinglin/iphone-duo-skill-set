# 检查卡：判据、例外与官方依据

规则包0.5.1；检查动作与编号由项目制定，官方原文保留在JSON。

## CHK-01 · 重要文字与控件完整性

对象：page；模式：screenshot；规则：DUO-01

检查：逐区查看标题、金额、字段、正文和主要操作的边界。

成立条件：重要信息或控件被裁切、重叠、明显错位。

例外：正常滚动首屏未显示全部内容不算裁切；测试素材排除。

官方依据：重要文字和控件应随可用空间调整，避免裁切、重叠。

- [duo-prepare · Address common layout and resizing considerations](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Address-common-layout-and-resizing-considerations)：Confirm your views resize well in each supported orientation and pose.
- [layout · Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability)：Be prepared for text-size changes. People use Supporting Dynamic Type to increase text size to be more readable, which occurs at the system level. Apps that don’t respond to this setting can be difficult or impossible to use for people who rely on this feature. Support Dynamic Type by adjusting your layout to accommodate text at larger sizes. For example, horizontally adjacent views may need to stack vertically to provide more space for text; table rows or other containers may need to grow in height so that text isn’t cropped or doesn’t overlap other content; and table rows with a single line of text by default might need to grow vertically to accommodate multiple lines of text.

## CHK-02 · 系统区域遮挡

对象：page；模式：screenshot；规则：IOS-01

检查：沿系统栏、导航栏、Tab、键盘及浮层边界检查前景内容。

成立条件：重要信息或控件轮廓被系统 UI 稳定覆盖。

例外：装饰背景和系统自身外壳不报错；不据间距猜热区。

官方依据：遵守安全区域，避免系统UI和硬件遮挡内容与控件。

- [layout · Guides and safe areas](https://developer.apple.com/design/human-interface-guidelines/layout#Guides-and-safe-areas)：A safe area defines the area within a window that isn’t covered on the edge by a hardware feature or another view within the window, like a toolbar, tab bar, or status bar. Respecting the safe area is essential to make sure system UI and hardware features like the Dynamic Island don’t obstruct content and controls. For developer guidance, see SafeAreaRegions and Positioning content relative to the safe area.

## CHK-03 · 比例与拉伸

对象：page；模式：screenshot；规则：DUO-01

检查：查看图标、图像及控件有无明显非等比变形。

成立条件：有原图或同内容比例基准可确认的明显拉伸。

例外：单纯留白、单栏及视觉风格不作变形依据。

官方依据：背景艺术应保持原始宽高比，以缩放适应空间。

- [layout · Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability)：When necessary, scale background artwork in response to display changes. Viewing your app or game in a different context — such as on a screen with a different aspect ratio — might make your artwork appear cropped, letterboxed, or pillarboxed. If this happens, don’t change the aspect ratio of the artwork; instead, scale it so that it fills the screen completely. Note that since windows can be very wide and short or tall and narrow, background artwork may often need to extend beyond what is typically visible in a more standard display aspect ratio.

## CHK-04 · 媒体主体裁切

对象：media；模式：screenshot；规则：DUO-01

检查：核对已经展示的图片或视频重要主体是否损失。

成立条件：有可比较素材证明重要主体被容器裁掉。

例外：背景允许等比填充裁切，不强制全部改 fit。

官方依据：背景可延伸，但不能因此损失重要图像主体。

- [layout · Visual hierarchy](https://developer.apple.com/design/human-interface-guidelines/layout#Visual-hierarchy)：If scaling a background image to the full window edge results in components like sidebars or inspectors covering important parts of the image, you can use a background extension effect to flip and blur the image, mirroring it beneath adjacent components and providing the appearance that the background image extends beneath them. For developer guidance, see backgroundExtensionEffect() and UIBackgroundExtensionView.
- [layout · Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability)：When necessary, scale background artwork in response to display changes. Viewing your app or game in a different context — such as on a screen with a different aspect ratio — might make your artwork appear cropped, letterboxed, or pillarboxed. If this happens, don’t change the aspect ratio of the artwork; instead, scale it so that it fills the screen completely. Note that since windows can be very wide and short or tall and narrow, background artwork may often need to extend beyond what is typically visible in a more standard display aspect ratio.

## CHK-05 · 按钮图标或文字内容

对象：button；模式：screenshot；规则：IOS-04

检查：逐个检查包括淡色、玻璃背景在内的按钮；是否有可辨识图标、文字或进度指示。

成立条件：已确认是控件却只剩背景，没有可辨识的用途内容；或内容本身无法读辨。

例外：加载指示器、已说明的骨架/占位、装饰和空标题区域不是空按钮；禁用态仍有可辨识内容不报错。

官方依据：每个按钮应清楚表达用途，可以使用图标、文字或两者；工具栏控件不能让人猜测。

- [buttons · Content](https://developer.apple.com/design/human-interface-guidelines/buttons#Content)：Ensure that each button clearly communicates its purpose. Depending on the platform, a button can contain a symbol (or icon), a text label, or both to help people understand what it does.
- [toolbars · Actions](https://developer.apple.com/design/human-interface-guidelines/toolbars#Actions)：Make sure the meaning of each control is clear. Don’t make people guess or experiment to figure out what a toolbar item does. Prefer simple, recognizable symbols for items instead of text, except for actions like edit that aren’t well-represented by symbols. For guidance on symbols that represent common actions, see Standard icons.

## CHK-06 · 按钮内容与背景区分

对象：button；模式：screenshot；规则：IOS-04

检查：特别看白底白图标、彩色背景上标签及透明控件；记录实际读辨结果。

成立条件：控件内容在当前背景上实际不可辨识。

例外：不凭淡色或审美判错；不从截图直接宣布 WCAG 数值不达标。

官方依据：前景文字与图标应与背景有足够区分，保证可读。

- [buttons · Style](https://developer.apple.com/design/human-interface-guidelines/buttons#Style)：Avoid applying a similar color to button labels and content layer backgrounds. If your app already has bright, colorful content in the content layer, prefer using the default monochromatic appearance of button labels. For more guidance, see Liquid Glass color.
- [toolbars · Best practices](https://developer.apple.com/design/human-interface-guidelines/toolbars#Best-practices)：Avoid applying a similar color to toolbar item labels and content layer backgrounds. If your app already has bright, colorful content in the content layer, prefer using the default monochromatic appearance of toolbars. For more guidance, see Liquid Glass color.
- [accessibility · Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision)：Strive to meet color contrast minimum standards. To ensure all information in your app is legible, it’s important that there’s enough contrast between foreground text and icons and background colors. Two popular standards of measure for color contrast are the Web Content Accessibility Guidelines (WCAG) and the Accessible Perceptual Contrast Algorithm (APCA). Use standard contrast calculators to ensure your UI meets acceptable levels. Accessibility Inspector uses the following values from WCAG Level AA as guidance in determining whether your app’s colors have an acceptable contrast.

## CHK-07 · 相邻文字控件是否混在一起

对象：toolbar；模式：screenshot；规则：DUO-01

检查：看相邻标签是否因重叠或挤压变成无法区分的内容。

成立条件：文字发生可见重叠或裁切，无法区分按钮。

例外：不要把正常紧凑分组误判为故障；不要求改设计风格。

官方依据：相邻文字操作应分开，避免看起来像同一个操作。

- [toolbars · Item groupings](https://developer.apple.com/design/human-interface-guidelines/toolbars#Item-groupings)：Keep actions with text labels separate. Placing an action with a text label next to an action with a symbol can create the illusion of a single action with a combined text and symbol, leading to confusion and misinterpretation. If your toolbar includes multiple text-labeled buttons, the text of those buttons may appear to run together, making the buttons indistinguishable. Add separation by inserting fixed space between the buttons. For developer guidance, see UIBarButtonItem.SystemItem.fixedSpace.

## CHK-08 · 页面级栏方向与位置

对象：toolbar；模式：screenshot；规则：DUO-04

检查：对照当前形态和容器判断返回、工具栏、Tab 的呈现。

成立条件：适用且排除例外后与默认侧栏不同，记指导差异。

例外：内屏竖屏水平；sheet、inspector、split pane、宽文字和自定义视图另核对。

官方依据：外屏与内屏横屏默认侧边栏，内屏竖屏普通页面保留水平栏。

- [duo-hig · Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)：On iPhone Duo, toolbars, tab bars, and navigation controls that are typically at the top and bottom of the display move to the side, preserving vertical space for content and keeping controls within easy reach. The exception is the inner display in portrait, which has enough vertical space to keep standard horizontal bars.
- [duo-hig · Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)：In general, don’t override the default bar placement. The position of controls on the vertical axis is one of the core patterns of iPhone Duo. Keeping controls in familiar positions helps people get to know how your app works right away, and reinforces the unified platform experience.
- [duo-prepare · Optimize bars for vertical presentation](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Optimize-bars-for-vertical-presentation)：Check the navigation bars, toolbars, and tab bars in your app to see if the system presents them vertically on the side of the display. This happens on the outer display when the device is closed, and for some views in the leading or trailing position on the inner display when the device is open.

## CHK-09 · 系统组件排列

对象：system；模式：screenshot；规则：DUO-04

检查：记录状态栏与灵动岛方向及 App 前景是否避让。

成立条件：已确认默认侧栏适用时记录系统呈现差异。

例外：系统显示差异单独记开发适配线索；不要求 App 手绘或移动状态栏。

官方依据：侧边区域包括灵动岛、状态栏、工具栏和Tab；位置与硬件保持一致。

- [duo-hig · Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)：Controls on the side include both system and app elements: the Dynamic Island, the status bar, the toolbar (including navigation buttons), and the tab bar.
- [duo-hig · Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)：Because controls on the vertical axis stay aligned with the hardware, they hold the same position relative to the camera on the outer display, and stay on the same side in right-to-left languages.

## CHK-10 · 主导航在竖栏中的顺序

对象：toolbar；模式：screenshot；规则：DUO-08

检查：已有竖栏里返回/关闭是否位于主导航区域，重要动作其次。

成立条件：语义可辨识且顺序明确违背指导。

例外：没有返回不要求新增；不从空图标猜动作。

官方依据：竖栏顶部优先返回或关闭，其次是Done等重要操作。

- [duo-hig · Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)：Follow the standard placement order for toolbar items. Reserve the top of the vertical axis for primary navigation controls, like Back or Close, followed by prominent actions, like Done. This preserves familiar navigation patterns while keeping important actions within reach. Keep remaining toolbar items in their original groupings; the system provides a vertical space between items from the top and bottom bars to keep them distinct.
- [duo-prepare · Organize items in your bars](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Organize-items-in-your-bars)：Organize your items for optimal placement when the system presents navigation bars, toolbars, and tab bars vertically. Reserve the top for primary navigation controls, like Back or Close, followed by prominent actions, such as Done. If you use a navigation controller, the system adds the Back button automatically.

## CHK-11 · 局部控件归属

对象：toolbar；模式：screenshot；规则：DUO-04

检查：区分页面级栏和控制局部列表、正文的按钮。

成立条件：仅页面级栏进入默认侧栏差异判断。

例外：搜索 Cancel、内容筛选、正文按钮不能仅因横排被报错。

官方依据：属于局部内容区域的控件应留在它影响的内容附近。

- [duo-hig · Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)：Locate controls near the content they affect. When controls belong to a content area other than the one along the trailing edge, keep them with that area rather than moving them to the side. Proximity makes the relationship between controls and content clear. For example, controls that affect the list of emails in Mail stay above the leading pane to indicate that they apply to the list, rather than the contents of an individual email.

## CHK-12 · 宽文字及自定义项例外

对象：toolbar；模式：screenshot；规则：DUO-04

检查：遇到保留水平位置的文字按钮或自定义视图先核对例外。

成立条件：无例外且属于默认页面级栏才报指导差异。

例外：不能把 Kit 的 Preferred Axis 或单个图层名当强制方向。

官方依据：只有文字而无图标的项目，以及custom view，有不竖向呈现的例外。

- [duo-hig · Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)：Keep text-based buttons to a minimum. Labels that include text stay in a horizontal bar, so prefer a symbol wherever one works.
- [duo-prepare · Organize items in your bars](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Organize-items-in-your-bars)：If your item has a title and doesn’t have an icon, the system doesn’t present it vertically.
- [duo-prepare · Organize items in your bars](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Organize-items-in-your-bars)：If your item uses a custom view rather than a title or icon, the system doesn’t present it vertically.

## CHK-13 · Tab 可见内容

对象：tab；模式：screenshot；规则：IOS-04

检查：查看实际展示的每个 Tab 内容是否可辨识、完整，缩小态按当前呈现判断。

成立条件：Tab 呈现为无内容的控件，或标签/图标实际不可辨识。

例外：系统压缩态不强制显示所有标签；未见的 Tab 不猜丢失；选中态不要求设计自定义版本。

官方依据：Tab标签帮助表达导航含义；图标在不同呈现中自动适应。

- [tab-bars · Best practices](https://developer.apple.com/design/human-interface-guidelines/tab-bars#Best-practices)：Include tab labels to help with navigation. A tab label appears beneath or beside a tab bar icon, and can aid navigation by clearly describing the type of content or functionality the tab contains. Use single words whenever possible.
- [tab-bars · Best practices](https://developer.apple.com/design/human-interface-guidelines/tab-bars#Best-practices)：Consider using SF Symbols to provide familiar, scalable tab bar icons. When you use SF Symbols, tab bar icons automatically adapt to different contexts. For example, the tab bar can be regular or compact, depending on the device and orientation. Tab bar icons appear above tab labels in compact views, whereas in regular views, the icons and labels appear side by side. Prefer filled symbols or icons for consistency with the platform.

## CHK-14 · Tab 与正文交叠

对象：tab；模式：screenshot；规则：IOS-01

检查：检查浮动 Tab 遮住的是装饰/可滚动内容还是重要固定操作。

成立条件：重要固定控件或信息稳定被覆盖。

例外：Liquid Glass 背景透出内容本身合法；模态覆盖背景 Tab 不判错。

官方依据：Tab的玻璃背景允许透出内容，但安全区应避免重要固定内容被覆盖。

- [tab-bars · iOS](https://developer.apple.com/design/human-interface-guidelines/tab-bars#iOS)：A tab bar floats above content at the bottom of the screen. Its items rest on a Liquid Glass background that allows content beneath to peek through.
- [layout · Guides and safe areas](https://developer.apple.com/design/human-interface-guidelines/layout#Guides-and-safe-areas)：A safe area defines the area within a window that isn’t covered on the edge by a hardware feature or another view within the window, like a toolbar, tab bar, or status bar. Respecting the safe area is essential to make sure system UI and hardware features like the Dynamic Island don’t obstruct content and controls. For developer guidance, see SafeAreaRegions and Positioning content relative to the safe area.

## CHK-15 · sheet 与弹层边界

对象：sheet；模式：screenshot；规则：DUO-01

检查：检查标题、内容、确认和关闭操作是否完整；栏方向按 placement。

成立条件：已经展示的弹层内容或关键操作裁切、重叠。

例外：方向本身不自动失败；内屏居中/leading 水平、trailing 竖向；外屏允许关闭竖栏。

官方依据：逐个检查view、sheet、popover的位置；sheet栏方向取决于屏幕和placement。

- [duo-prepare · Address common layout and resizing considerations](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Address-common-layout-and-resizing-considerations)：Identify any views, sheets, or popovers that position awkwardly when you fold or open iPhone Duo.
- [duo-prepare · Optimize bars for vertical presentation](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Optimize-bars-for-vertical-presentation)：Sheets. On the outer display, the system presents bars vertically for sheets by default. Use toolbarVerticalBehavior(_:) in SwiftUI or preferredVerticalBarBehavior in UIKit to disable vertical presentation for your bars. For sheets on the inner display, the system presents the toolbar horizontally for centered or leading placements, and vertically for trailing placements. Set presentationPlacement(_:) in SwiftUI or preferredPlacement in UIKit to indicate where you want the system to place the sheet.

## CHK-16 · 摄像头区域

对象：camera；模式：screenshot；规则：DUO-05

检查：外屏检查始终生效的前摄；内屏只在截图或可信信息表明启用时检查。

成立条件：重要内容被生效摄像头区域遮挡。

例外：完全展开没有永久折叠禁区；内屏未启用相机不画禁区。

官方依据：外屏摄像头区域始终生效，内屏摄像头区域只在使用相机时生效。

- [duo-hig · Reserved regions](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions)：The outer front-facing camera. This region is always present, and expands into the Dynamic Island for Live Activities. When controls are on the side, the system automatically accounts for it and arranges elements accordingly.
- [duo-hig · Reserved regions](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions)：The inner front-facing camera. This region is only present when the camera is active. When it’s inactive, the camera isn’t visible; when the camera activates, the UI moves aside to indicate the presence of the camera.
- [duo-prepare · Adapt to reserved regions in your views](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Adapt-to-reserved-regions-in-your-views)：A reserved region can be active or inactive. For example, a reserved region that represents the fold is active when iPhone Duo is partially open, but inactive when it is fully open.

## CHK-17 · 已展示键盘与固定操作

对象：keyboard；模式：screenshot；规则：IOS-01

检查：有键盘的截图检查字段、提示和固定操作与键盘边界。

成立条件：已展示的重要内容被键盘覆盖或裁切。

例外：无键盘截图不产生键盘测试；不据截图判断滚动和焦点行为。

官方依据：系统或其他视图覆盖边缘后，重要内容和控件应处于安全区域。

- [layout · Guides and safe areas](https://developer.apple.com/design/human-interface-guidelines/layout#Guides-and-safe-areas)：A safe area defines the area within a window that isn’t covered on the edge by a hardware feature or another view within the window, like a toolbar, tab bar, or status bar. Respecting the safe area is essential to make sure system UI and hardware features like the Dynamic Island don’t obstruct content and controls. For developer guidance, see SafeAreaRegions and Positioning content relative to the safe area.

## CHK-18 · 菜单与加载状态的显示完整性

对象：menu；模式：screenshot；规则：IOS-04

检查：有菜单/进度截图时检查已展示项目、图标和加载指示。

成立条件：已展示操作无可辨识内容；菜单文字裁切关联 DUO-01。

例外：加载时系统可能隐藏原图标而展示指示器，不判图标丢失；省略号溢出菜单不是空白控件。

官方依据：加载时系统可能显示进度指示并隐藏原图标；溢出菜单使用省略号。

- [buttons · iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/buttons#iOS-iPadOS)：Configure a button to display an activity indicator when you need to provide feedback about an action that doesn’t instantly complete. Displaying an activity indicator within a button can save space in your user interface while clearly communicating the reason for the delay. To help clarify what’s happening, you can also configure the button to display a different label alongside the activity indicator. For example, the label “Checkout” could change to “Checking out…” while the activity indicator is visible. When a delay occurs after people click or tap your configured button, the system displays the activity indicator next to the original or alternative label, hiding the button image, if there is one.
- [duo-hig · Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)：Use the system overflow menu. If your app has its own overflow menu, move those actions into the system menu so people find everything in one place. Reserve the ellipsis symbol for overflow, and give other menus a distinct symbol. For developer guidance, see ToolbarOverflowMenu (SwiftUI) and additionalOverflowItems (UIKit).

## CHK-19 · 不同姿态功能与状态连续性

对象：page；模式：extended；规则：DUO-02

检查：仅有用户授权的连续证据时核对状态、功能与导航层级。

成立条件：连续证据证明切换导致状态或功能丢失。

例外：独立截图不证明连续性。

官方依据：跨显示屏与姿态应保留功能、状态和信息层级。

- [duo-hig · Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices)：Create a consistent experience across displays. Keep functionality and the state of elements the same between displays. Maintain your app’s information hierarchy, but show an additional level of hierarchy on the larger inner display if it makes sense for your content. Mail, for example, shows either a list of emails (primary) or an email (secondary) when the device is closed. When it’s open, it shows both side by side.
- [duo-hig · Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices)：Maintain the same functionality across device poses. Controls may overflow and content may move or change size as the interface adapts to the available area. Provide access to the same controls and content regardless of how someone holds or views the device. For guidance, see Dynamic layouts and Vertical controls.
- [layout · Size classes](https://developer.apple.com/design/human-interface-guidelines/layout#Size-classes)：Keep functionality the same as size classes change, and keep layout changes recognizable and familiar to the platform. Don’t change your app’s functionality based on the space it occupies. However, you can change the amount of functionality that’s visible onscreen as the amount of space changes. Consider taking advantage of larger spaces to switch from a Tab bars to a Sidebars or expose functionality that might otherwise be grouped into an overflow menu.

## CHK-20 · 溢出菜单操作可访问性

对象：toolbar；模式：extended；规则：DUO-09

检查：使用已授权交互检查压缩后操作是否仍能访问。

成立条件：对照操作清单及菜单证据确认关键操作消失。

例外：没打开菜单不猜功能丢失；频率和重要性不从图标猜。

官方依据：有限空间时可压缩到系统溢出菜单，仍要提供操作访问。

- [duo-hig · Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)：Prioritize frequently used toolbar items to keep them easily available. Items overflow from bottom to top by default. Assign each item a visibility priority to change that order, starting with whole groups and then individual items within a group if you need finer control. For developer guidance, see ToolbarItemVisibilityPriority (SwiftUI) or UIBarButtonItemVisibilityPriority (UIKit).
- [duo-hig · Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)：When space is limited, preserve either the toolbar or tab bar based on the experience that the view provides. In navigation-focused experiences, move toolbar items into the overflow menu so the tab bar and primary destinations remain accessible. This is the default bar compression behavior.
- [duo-hig · Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)：In task-oriented experiences, minimize the tab bar to preserve the toolbar actions that are central to completing the task. This mirrors the minimized tab bar behavior present on other iPhone devices. For developer guidance, see ToolbarVerticalCompressionBehavior (SwiftUI) and UIVerticalBarCompressionBehavior (UIKit).
- [duo-hig · Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)：Use the system overflow menu. If your app has its own overflow menu, move those actions into the system menu so people find everything in one place. Reserve the ellipsis symbol for overflow, and give other menus a distinct symbol. For developer guidance, see ToolbarOverflowMenu (SwiftUI) and additionalOverflowItems (UIKit).

## CHK-21 · 工具栏图标与标题配置

对象：toolbar；模式：developer；规则：DUO-13

检查：开发检查 toolbar item 的 icon、title、custom view 与容器配置。

成立条件：配置证据表明应有内容缺失或项目不适应系统呈现。

例外：截图未显示标题不等于代码没标题；没有图标但有标题时系统保留水平，并非官方空圆替代。

官方依据：非纯文字工具栏项应同时提供标题和符号，供不同呈现使用。

- [duo-hig · Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)：Provide both a title and a symbol for each toolbar item that isn’t text-only. Giving both lets the system pick the right representation for the context. Include a title even when an item shows a symbol, because the system uses the title in overflow menus and expanded forms. For developer guidance, see Label (SwiftUI) and UIBarButtonItem (UIKit).
- [duo-prepare · Organize items in your bars](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Organize-items-in-your-bars)：When you create toolbar items, specify both an icon and a title for items that you want to have the most adaptability. iPhone Duo might present items vertically, horizontally, or in an overflow menu:
- [duo-prepare · Organize items in your bars](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Organize-items-in-your-bars)：The system uses an icon for an item it presents vertically.
- [duo-prepare · Organize items in your bars](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Organize-items-in-your-bars)：The system uses an icon or a title for an item it presents horizontally, preferring an icon.
- [duo-prepare · Organize items in your bars](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Organize-items-in-your-bars)：The system uses an icon and title for an item in an overflow menu.
- [duo-prepare · Organize items in your bars](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Organize-items-in-your-bars)：If your item has a title and doesn’t have an icon, the system doesn’t present it vertically.
- [duo-prepare · Organize items in your bars](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Organize-items-in-your-bars)：If your item uses a custom view rather than a title or icon, the system doesn’t present it vertically.

## CHK-22 · 布局代码与兼容条件

对象：page；模式：developer；规则：DUO-01

检查：开发授权时检查窗口尺寸、trait、SDK 与容器支持。

成立条件：由代码或配置证据确认固定屏幕假设导致布局问题。

例外：截图只描述结果，不证明 API 和构建版本。

官方依据：从容器或窗口取得可用空间，不用固定机型尺寸；SDK条件须由开发检查。

- [duo-prepare · Overview](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Overview)：Build your app with the latest version of Xcode to use all of the available screen space on iPhone Duo. When you build with Xcode 26 and earlier, your app doesn’t extend under the status bar and camera. For more information, see Prepare your app for iPhone Duo. Then, take the first step in preparing your app for iPhone Duo by testing it in a simulator or on iPhone Duo. For more information, see Running your app on simulated or physical devices.
- [duo-prepare · Address common layout and resizing considerations](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Address-common-layout-and-resizing-considerations)：Size your views relative to their container rather than to fixed iPhone dimensions.
- [duo-prepare · Address common layout and resizing considerations](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Address-common-layout-and-resizing-considerations)：Make layout calculations based on your scene or containing view’s bounds rather than screen dimensions.
- [duo-prepare · Address common layout and resizing considerations](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Address-common-layout-and-resizing-considerations)：Adopt Auto Layout in UIKit to make your views resizable.
- [duo-prepare · Address common layout and resizing considerations](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Address-common-layout-and-resizing-considerations)：Use automatic trait tracking to observe horizontalSizeClass and verticalSizeClass changes to adapt your interface to different sizes. Don’t use userInterfaceIdiom or UIInterfaceOrientation for layout decisions in your UIKit app. For more information, see Adapting your app when traits change.

## CHK-23 · 大字体与本地化

对象：page；模式：extended；规则：IOS-02

检查：有授权和对应字号/语言证据时检查换行、裁切和重叠。

成立条件：变体证据中重要文本裁切、重叠。

例外：默认不补测未展示的字号或语言。

官方依据：支持文字大小及语言变化，布局应增长或换行以避免文字裁切重叠。

- [layout · Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability)：Text-size changes
- [layout · Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability)：Locale-based internationalization features like left-to-right/right-to-left layout direction, date/time/number formatting, font variation, and text length
- [layout · Adaptability](https://developer.apple.com/design/human-interface-guidelines/layout#Adaptability)：Be prepared for text-size changes. People use Supporting Dynamic Type to increase text size to be more readable, which occurs at the system level. Apps that don’t respond to this setting can be difficult or impossible to use for people who rely on this feature. Support Dynamic Type by adjusting your layout to accommodate text at larger sizes. For example, horizontally adjacent views may need to stack vertically to provide more space for text; table rows or other containers may need to grow in height so that text isn’t cropped or doesn’t overlap other content; and table rows with a single line of text by default might need to grow vertically to accommodate multiple lines of text.
- [accessibility · Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision)：Support larger text sizes. Make sure people can adjust the size of your text or icons to make them more legible, visible, and comfortable to read. Ideally, give people the option to enlarge text by at least 200 percent (or 140 percent in watchOS apps). Your interface can support font size enlargement either through custom UI, or by adopting Dynamic Type. Dynamic Type is a systemwide setting that lets people adjust the size of text for comfort and legibility. For more guidance, see Supporting Dynamic Type.

## CHK-24 · 热区、间距与对比度测量

对象：button；模式：extended；规则：IOS-03

检查：用运行时热区及校准颜色执行已授权测量。

成立条件：符合适用阈值及例外后才作数值判断。

例外：Buttons 44x44 hit region 与 Accessibility 44 默认/28 最小不能混用；截图外形不等于热区。

官方依据：控件尺寸、热区和对比度有各自适用条件，不把外形尺寸等同热区。

- [buttons · Best practices](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices)：Make buttons easy for people to use. It’s essential to include enough space around a button so that people can visually distinguish it from surrounding components and content. Giving a button enough space is also critical for helping people select or activate it, regardless of the method of input they use. As a general rule, a button needs a hit region of at least 44x44 pt — in visionOS, 60x60 pt — to ensure that people can select it easily, whether they use a fingertip, a pointer, their eyes, or a remote.
- [accessibility · Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility)：Offer sufficiently sized controls. Controls that are too small are hard for many people to interact with and select. Strive to meet the recommended minimum control size for each platform to ensure controls and menus are comfortable for all when tapping and clicking.
- [accessibility · Mobility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility)：Consider spacing between controls as important as size. Include enough padding between elements to reduce the chance that someone taps the wrong control. In general, it works well to add about 12 points of padding around elements that include a bezel. For elements without a bezel, about 24 points of padding works well around the element’s visible edges.
- [accessibility · Vision](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision)：Strive to meet color contrast minimum standards. To ensure all information in your app is legible, it’s important that there’s enough contrast between foreground text and icons and background colors. Two popular standards of measure for color contrast are the Web Content Accessibility Guidelines (WCAG) and the Accessible Perceptual Contrast Algorithm (APCA). Use standard contrast calculators to ensure your UI meets acceptable levels. Accessibility Inspector uses the following values from WCAG Level AA as guidance in determining whether your app’s colors have an acceptable contrast.

## CHK-25 · 部分折叠避让

对象：page；模式：extended；规则：DUO-06

检查：部分折叠证据中核对生效折叠区域。

成立条件：关键操作被生效折叠区域覆盖。

例外：三种基础完全展开形态不启用；正常可滚动内容不强制离开曲面。

官方依据：部分展开时折叠区域生效，控件要避让；完全展开不生效。

- [duo-hig · Reserved regions](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions)：The folding region. This region is conditional based on how a person uses the device. When the device is partially open, the folding region divides the inner display into multiple usable regions, excluding the region at the center as the display folds.
- [duo-prepare · Address common layout and resizing considerations](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Address-common-layout-and-resizing-considerations)：Identify elements or controls in your views that appear in the fold, and are difficult to see or interact with.
- [duo-prepare · Adapt to reserved regions in your views](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Adapt-to-reserved-regions-in-your-views)：A reserved region can be active or inactive. For example, a reserved region that represents the fold is active when iPhone Duo is partially open, but inactive when it is fully open.

## CHK-26 · 两栏与层级拓展

对象：page；模式：optional；规则：DUO-12

检查：需要体验优化时参考 arrangement/split/sidebar。

成立条件：只输出可选方案，不生成适配故障。

例外：单栏、留白和未采用两栏本身不是违规。

官方依据：更大空间可采用split或arrangement等布局，这是可选实现。

- [duo-hig · Arrangement views](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Arrangement-views)：Consider an arrangement view when your layout already resembles one. A layout that places two views side by side or one above the other, such as an HStack or VStack, translates directly to a split arrangement. A layout that layers one view over another, such as a ZStack, translates to an overlay arrangement.
- [duo-hig · Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices)：Create a consistent experience across displays. Keep functionality and the state of elements the same between displays. Maintain your app’s information hierarchy, but show an additional level of hierarchy on the larger inner display if it makes sense for your content. Mail, for example, shows either a list of emails (primary) or an email (secondary) when the device is closed. When it’s open, it shows both side by side.
