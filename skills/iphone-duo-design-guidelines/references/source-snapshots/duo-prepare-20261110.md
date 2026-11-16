# duo-prepare

来源：https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo
核对：2026-11-10；正文（含跨平台部分），图片另作定位参考。

## Overview

duo-prepare-P002
iPhone Duo is a foldable phone, with a compact outer display and a large inner display. Both displays include a front camera, and the inner front-facing camera is hidden when not in use. As iPhone Duo is opened, closed, partially folded, and rotated, content transitions between displays and adjusts for rotated positions. When partially folded, views adapt to the folding region of the display.

duo-prepare-P005
Resizing is a key feature for your app on iPhone Duo. If your app already works on iPad and Mac or you’ve prepared your app to resize in iPhone Mirroring, you’re well on your way to supporting iPhone Duo. If not, adopt standard layout controls and containers, and use size classes and scene geometry to improve your app’s resizing. Then, handle reserved regions such as the fold to resize your app and handle folded layouts. Evaluate whether an arrangement view can assist your app’s layout to handle the fold.

duo-prepare-P006
iPhone Duo presents navigation bars, toolbars, and tab bars together vertically on the side of the display in some poses. Review and organize your app’s bars to ensure frequently used controls stay visible, and less frequently used controls appear in an overflow menu when there’s limited space.

duo-prepare-P008
Build your app with the latest version of Xcode to use all of the available screen space on iPhone Duo. When you build with Xcode 26 and earlier, your app doesn’t extend under the status bar and camera. For more information, see Prepare your app for iPhone Duo. Then, take the first step in preparing your app for iPhone Duo by testing it in a simulator or on iPhone Duo. For more information, see Running your app on simulated or physical devices.

## Address common layout and resizing considerations

duo-prepare-P010
Because iPhone Duo supports multiple screen sizes, layouts, and orientations, your app needs to adapt gracefully across all of them. Check how your app appears on both displays, when closed, open, or partially folded. Rotate iPhone Duo in each pose to see how your app’s layout reacts.

duo-prepare-P012
Navigate through your app, checking each view, sheet, and popover to identify things you can improve:

duo-prepare-P013
Confirm your views resize well in each supported orientation and pose.

duo-prepare-P014
Inspect how the system presents your app’s navigation bars, toolbars, and tab bars vertically on the side of the display.

duo-prepare-P015
Identify any views, sheets, or popovers that position awkwardly when you fold or open iPhone Duo.

duo-prepare-P016
Identify elements or controls in your views that appear in the fold, and are difficult to see or interact with.

duo-prepare-P017
Follow these recommendations to avoid common issues, and improve your app’s resizability:

duo-prepare-P018
Prefer system-provided layouts and containers, such as split views, tab bars, arrangement views, and navigation stacks. These handle resizing, automatically adjusting for the outer display, fully open or folded inner display, and camera occlusions.

duo-prepare-P019
Size your views relative to their container rather than to fixed iPhone dimensions.

duo-prepare-P020
Make layout calculations based on your scene or containing view’s bounds rather than screen dimensions.

duo-prepare-P021
Adopt Auto Layout in UIKit to make your views resizable.

duo-prepare-P022
Use automatic trait tracking to observe horizontalSizeClass and verticalSizeClass changes to adapt your interface to different sizes. Don’t use userInterfaceIdiom or UIInterfaceOrientation for layout decisions in your UIKit app. For more information, see Adapting your app when traits change.

## Optimize bars for vertical presentation

duo-prepare-P024
Check the navigation bars, toolbars, and tab bars in your app to see if the system presents them vertically on the side of the display. This happens on the outer display when the device is closed, and for some views in the leading or trailing position on the inner display when the device is open.

duo-prepare-P025
If the system doesn’t present your bars vertically, check that you’re using the bar support that navigation containers, such as a tab view or navigation stack, provide. In SwiftUI, add the toolbar(content:) modifier to a NavigationStack or NavigationSplitView. In UIKit, set toolbar items on a view controller that you add to a navigation controller, instead of creating a custom bar for your view based on UIToolbar, UINavigationBar, or UITabBar.

duo-prepare-P026
The system handles the selection of horizontal and vertical bar presentation differently in some contexts:

duo-prepare-P027
Inspectors. The system presents bars in inspectors horizontally.

duo-prepare-P028
Split views. In a split view displaying multiple views, the system shows bars horizontally for the sidebar or content view, and vertically for the detail view.

duo-prepare-P029
Sheets. On the outer display, the system presents bars vertically for sheets by default. Use toolbarVerticalBehavior(_:) in SwiftUI or preferredVerticalBarBehavior in UIKit to disable vertical presentation for your bars. For sheets on the inner display, the system presents the toolbar horizontally for centered or leading placements, and vertically for trailing placements. Set presentationPlacement(_:) in SwiftUI or preferredPlacement in UIKit to indicate where you want the system to place the sheet.

duo-prepare-P030
In a custom view, you may need to know if the system presents bars vertically to adjust your layout. Use the toolbarVerticalEdge environment value in SwiftUI or the verticalBarEdge trait in UIKit to determine if the system presents bars vertically.

duo-prepare-P031
If your view has a hero or background image, extend it under a vertical bar using backgroundExtensionEffect() in SwiftUI, or UIBackgroundExtensionView in UIKit.

## Organize items in your bars

duo-prepare-P033
Organize your items for optimal placement when the system presents navigation bars, toolbars, and tab bars vertically. Reserve the top for primary navigation controls, like Back or Close, followed by prominent actions, such as Done. If you use a navigation controller, the system adds the Back button automatically.

duo-prepare-P034
Use semantic placements, such as ToolbarItemPlacement in SwiftUI, to organize toolbar items into related groups. Use topBarPinnedTrailing placement in SwiftUI for prominent navigation items such as a Done button, or pinnedTrailingGroup in UIKit. For a custom Back or Close button, create a ToolbarItem with cancellationAction placement in SwiftUI, or add an item in leadingItemGroups in UIKit.

duo-prepare-P035
Manage inclusion in vertical layouts with the axisBehavior(_:) modifier on your item in SwiftUI, or set axisBehavior on your item in UIKit. Manage the order in which the system selects items to go in the overflow menu with the visibilityPriority(_:) modifier in SwiftUI or by setting visibilityPriority in UIKit. Put items directly in the overflow menu in SwiftUI with ToolbarOverflowMenu, or additionalOverflowItems in UIKit.

duo-prepare-P036
When you create toolbar items, specify both an icon and a title for items that you want to have the most adaptability. iPhone Duo might present items vertically, horizontally, or in an overflow menu:

duo-prepare-P037
The system uses an icon for an item it presents vertically.

duo-prepare-P038
The system uses an icon or a title for an item it presents horizontally, preferring an icon.

duo-prepare-P039
The system uses an icon and title for an item in an overflow menu.

duo-prepare-P040
If your item has a title and doesn’t have an icon, the system doesn’t present it vertically.

duo-prepare-P041
If your item uses a custom view rather than a title or icon, the system doesn’t present it vertically.

## Arrange views in different poses

duo-prepare-P043
ArrangementView in SwiftUI and UIArrangementViewController in UIKit represent an arrangement view, which is a layout container for a primary view and a secondary view that you can use to adjust to the different device poses. Arrangement views offer two styles of preferred arrangements: split and overlay.

duo-prepare-P044
In a split arrangement, the arrangement view presents the primary and secondary views side by side when the containing view is wider than it is tall; or it places the primary view on top and the secondary view below it when the containing view is taller than it is wide. The arrangement view adjusts the placement of the primary and secondary views to adapt to reserved regions, such as the folding region. Use this type of arrangement when you lay out your primary and secondary views with containers such as HStack or VStack.

duo-prepare-P045
In an overlay arrangement, the arrangement view positions the primary view on top of the secondary view when there aren’t any active reserved regions that are divisions. This is true when iPhone Duo is closed or fully open. When iPhone Duo is partially open, the overlay arrangement places the primary view in the trailing or bottom part of the display relative to the fold, and the secondary view in the leading or top part of the display relative to the fold. Use this type of arrangement when you place a primary view over a secondary view with a container such as a ZStack.

duo-prepare-P046
For both styles of arrangement, you can limit which axis you want to use for the arrangement. For example, if you want to show only the primary view in a vertical layout and you want to show the primary view next to the secondary view in a horizontal layout, set the axis on the style as the following examples show:

duo-prepare-P047
Avoid placing an arrangement view inside a navigation split view, list, scroll view, or other container that might cause part of your view to become inaccessible.

## Adapt to reserved regions in your views

duo-prepare-P049
While framework-provided views and containers automatically adjust to work around the fold or the front-facing camera on the inner display, your custom views need a flexible approach to identify divisions and occlusions. iOS represents these as reserved regions. A division occurs when a folding region divides a large view into smaller views. An occlusion is an area of a view where a hardware element, such as the camera, covers your content so it isn’t visible. The inner front-facing camera can block your view when it’s active, and the outer front-facing camera always occludes your view.

duo-prepare-P052
In SwiftUI, use a GeometryReader to get a GeometryProxy, then get an array of ReservedRegion instances from reservedRegions(kind:options:layoutDirectionBehavior:). In UIKit, get an array of UIView.ReservedRegion instances from reservedRegions(kind:options:). Inspect the frames of the reserved regions, and adjust your views accordingly.

duo-prepare-P053
A reserved region can be active or inactive. For example, a reserved region that represents the fold is active when iPhone Duo is partially open, but inactive when it is fully open.

## Improve your app’s camera handling

duo-prepare-P055
If your app uses AVKit or AVFoundation to capture photos or videos, your app can capture photos and video from the outer display camera, inner display camera, and rear camera on iPhone Duo. When a person opens, closes, and rotates the phone, your app may change which display it’s on, and the camera you’re using may point in the opposite direction. For more information about how to update your app to handle these situations, see Choosing a camera by the direction it faces.

duo-prepare-P056
When iPhone Duo is fully open and capturing photos or video with the rear camera, it can show content on the outer display in addition to showing your app on the inner display. For more information on configuring your camera app to do this, see Registering a camera capture accessory on iPhone Duo.

## Videos
