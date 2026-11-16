# Three steps to make your app shine on iPhone Duo

来源：https://developer.apple.com/iphone-duo/prepare/
核对：2026-11-09，Asia/Shanghai
范围：页面介绍及 Step 1–3 完整文本；导航、SDK 对照和商店发布部分不纳入审查来源。内联代码按网页文本分行保留。

Apps built with the iOS 27 SDK and later resize dynamically on iPhone Duo. Unfold it and your app expands to fill the inner display; fold it and your app returns to the outer display. Hardcoded screen sizes, fixed orientations, and device assumptions can break layouts, leading to stretched, clipped, or misplaced content. Follow these steps to make sure your app is ready for iPhone Duo.

Step 1: Run the app resizability skill

In

Xcode

, ask the coding assistant to “

get my app ready for iPhone Duo.

” The skill scans your project for the patterns described in Step 2. For each issue it finds, it explains the problem and suggests a fix.

If you use a different coding agent, export the skill by running this in Terminal:

xcrun agent skills export

The skill finds most issues, but not all of them. Use the list below to review what it flags and catch anything it misses.

Step 2: Fix patterns

Stop sizing from the main screen

On iPhone Duo, your app’s size changes whenever the device folds or unfolds, and it doesn’t always match the size of the screen. Search your project for

UIScreen.main

and replace each use:

Size from the view or window.

Replace

UIScreen.main.bounds

with

view.bounds

or

window.bounds

. In SwiftUI, use

GeometryReader

or

onGeometryChange

.

Re-read the size whenever it changes.

Reading the size once at launch or in

viewIsAppearing

isn’t enough, because a fold can resize your app in the middle of a session. Do size-dependent layout in

layoutSubviews

or

viewDidLayoutSubviews

, and use

viewWillTransition(to:with:)

for work that needs to run when the size changes.

Get scale from the trait collection.

Use

traitCollection.displayScale

in UIKit or

@Environment(\.displayScale)

in SwiftUI.

Create windows from a scene.

Replace

UIWindow(frame: UIScreen.main.bounds)

with

UIWindow(windowScene:)

.

Don’t store a

UIScreen

.

When screen information is needed, access it dynamically with

view.window?.windowScene?.screen

.

Avoid using orientation to make layout decisions

On iPhone Duo, the device’s orientation doesn’t tell you what shape your app is. Search for these properties and remove any layout logic that depends on them:

UIDevice.current.orientation

statusBarOrientation

interfaceOrientation

, including

windowScene.effectiveGeometry.interfaceOrientation

.

To find out whether your app is wider than it is tall, compare the width and height of the space you have:

view.bounds

in a view controller,

superview.bounds

in a view, or the size from

GeometryReader

in SwiftUI.

Stop assuming idiom or size class identifies the device

With iPhone Duo and resizable iPhone Mirroring, an iPhone app can have

any combination of size classes

. On the inner display, your app should look like a natural extension of its iPad layout. For more information, see

Prepare your app for iPhone Duo

.

Don’t choose a layout by idiom.

Search for

userInterfaceIdiom == .phone

and

== .pad

. Base layout choices on size classes or available space instead.

Don’t treat “regular width” as “iPad.”

Code that shows an iPad-only layout when

horizontalSizeClass == .regular

, or that assumes iPhone is always compact, will now run that layout on iPhone too.

Remove checks for specific device sizes.

Comparisons such as

bounds.height == 844

or a list of known iPhone sizes won’t match iPhone Duo.

Check full-bleed media.

Hero images and video set to

.scaleAspectFill

or

.aspectRatio(contentMode: .fill)

can lose important content on wider displays. Use the current size classes or aspect ratio to choose between fill and fit, or set a focal point.

Step 3: Test resizing

Test resizing using these tools to make sure your app runs as expected.

The iOS resizable simulator

in Device Hub.

iPhone Mirroring

on macOS 27. Resize the window to extreme sizes in both directions.

The iPhone Duo simulator

in Xcode 27.1.

Note:

The iPhone Duo simulator is the best way to test the full native experience.
