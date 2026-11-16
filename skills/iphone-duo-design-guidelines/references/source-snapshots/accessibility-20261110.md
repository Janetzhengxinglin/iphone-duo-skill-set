# accessibility

来源：https://developer.apple.com/design/human-interface-guidelines/accessibility
核对：2026-11-10；正文（含跨平台部分），图片另作定位参考。

accessibility-P002
When you design for accessibility, you reach a larger audience and create a more inclusive experience. An accessible interface allows people to experience your app or game regardless of their capabilities or how they use their devices. Accessibility makes information and interactions available to everyone. An accessible interface is:

accessibility-P003
Intuitive. Your interface uses familiar and consistent interactions that make tasks straightforward to perform.

accessibility-P004
Perceivable. Your interface doesn’t rely on any single method to convey information. People can access and interact with your content, whether they use sight, hearing, speech, or touch.

accessibility-P005
Adaptable. Your interface adapts to how people want to use their device, whether by supporting system accessibility features or letting people personalize settings.

accessibility-P006
As you design your app, audit the accessibility of your interface. Use Accessibility Inspector to highlight accessibility issues with your interface and to understand how your app represents itself to people using system accessibility features. You can also communicate how accessible your app is on the App Store using Accessibility Nutrition Labels. To learn more about how to evaluate and indicate accessibility feature support, see Accessibility Nutrition Labels in App Store Connect help.

## Vision

accessibility-P009
The people who use your interface may be blind, color blind, or have low vision or light sensitivity. They may also be in situations where lighting conditions and screen brightness affect their ability to interact with your interface.

accessibility-P010
Support larger text sizes. Make sure people can adjust the size of your text or icons to make them more legible, visible, and comfortable to read. Ideally, give people the option to enlarge text by at least 200 percent (or 140 percent in watchOS apps). Your interface can support font size enlargement either through custom UI, or by adopting Dynamic Type. Dynamic Type is a systemwide setting that lets people adjust the size of text for comfort and legibility. For more guidance, see Supporting Dynamic Type.

accessibility-P011
Use recommended defaults for custom type sizes. Each platform has different default and minimum sizes for system-defined type styles to promote readability. If you’re using custom type styles, follow the recommended defaults.

accessibility-P012
Platform

accessibility-P013
Default size

accessibility-P014
Minimum size

accessibility-P015
iOS, iPadOS

accessibility-P016
17 pt

accessibility-P017
11 pt

accessibility-P018
macOS

accessibility-P019
13 pt

accessibility-P020
10 pt

accessibility-P021
tvOS

accessibility-P022
29 pt

accessibility-P023
23 pt

accessibility-P024
visionOS

accessibility-P025
17 pt

accessibility-P026
12 pt

accessibility-P027
watchOS

accessibility-P028
16 pt

accessibility-P029
12 pt

accessibility-P030
Bear in mind that font weight can also impact how easy text is to read. If you’re using a custom font with a thin weight, aim for larger than the recommended sizes to increase legibility. For more guidance, see Typography.

accessibility-P033
Strive to meet color contrast minimum standards. To ensure all information in your app is legible, it’s important that there’s enough contrast between foreground text and icons and background colors. Two popular standards of measure for color contrast are the Web Content Accessibility Guidelines (WCAG) and the Accessible Perceptual Contrast Algorithm (APCA). Use standard contrast calculators to ensure your UI meets acceptable levels. Accessibility Inspector uses the following values from WCAG Level AA as guidance in determining whether your app’s colors have an acceptable contrast.

accessibility-P034
Text size

accessibility-P035
Text weight

accessibility-P036
Minimum contrast ratio

accessibility-P037
Up to 17 pts

accessibility-P038
All

accessibility-P039
4.5:1

accessibility-P040
18 pts

accessibility-P041
All

accessibility-P042
3:1

accessibility-P043
All

accessibility-P044
Bold

accessibility-P045
3:1

accessibility-P046
If your app doesn’t provide this minimum contrast by default, ensure it at least provides a higher contrast color scheme when the system setting Increase Contrast is turned on. If your app supports Dark Mode, make sure to check the minimum contrast in both light and dark appearances.

accessibility-P051
Prefer system-defined colors. These colors have their own accessible variants that automatically adapt when people adjust their color preferences, such as enabling Increase Contrast or toggling between the light and dark appearances. For guidance, see Color.

accessibility-P054
Convey information with more than color alone. Some people have trouble differentiating between certain colors and shades. For example, people who are color blind may have particular difficulty with pairings such as red-green and blue-orange. Offer visual indicators, like distinct shapes or icons, in addition to color to help people perceive differences in function and changes in state. Consider allowing people to customize color schemes such as chart colors or game characters so they can personalize your interface in a way that’s comfortable for them.

accessibility-P059
Describe your app’s interface and content for VoiceOver. VoiceOver is a screen reader that lets people experience your app’s interface without needing to see the screen. For more guidance, see VoiceOver.

## Hearing

accessibility-P062
The people who use your interface may be deaf or hard of hearing. They may also be in noisy or public environments.

accessibility-P063
Support text-based ways to enjoy audio and video. It’s important that dialogue and crucial information about your app or game isn’t communicated through audio alone. Depending on the context, give people different text-based ways to experience their media, and allow people to customize the visual presentation of that text:

accessibility-P064
Captions give people the textual equivalent of audible information in video or audio-only content. Captions are great for scenarios like game cutscenes and video clips where text synchronizes live with the media.

accessibility-P065
Subtitles allow people to read live onscreen dialogue in their preferred language. Subtitles are great for TV shows and movies.

accessibility-P066
Audio descriptions are interspersed between natural pauses in the main audio of a video and supply spoken narration of important information that’s presented only visually.

accessibility-P067
Transcripts provide a complete textual description of a video, covering both audible and visual information. Transcripts are great for longer-form media like podcasts and audiobooks where people may want to review content as a whole or highlight the transcript as media is playing.

accessibility-P068
For developer guidance, see Selecting subtitles and alternative audio tracks.

accessibility-P069
Use haptics in addition to audio cues. If your interface conveys information through audio cues — such as a success chime, error sound, or game feedback — consider pairing that sound with matching haptics for people who can’t perceive the audio or have their audio turned off. In iOS and iPadOS, you can also use Music Haptics and Audio graphs to let people experience music and infographics through vibration and texture. For guidance, see Playing haptics.

accessibility-P071
Augment audio cues with visual cues. This is especially important for games and spatial apps where important content might be taking place off screen. When using audio to guide people towards a specific action, also add in visual indicators that point to where you want people to interact.

## Mobility

accessibility-P074
Ensure your interface offers a comfortable experience for people with limited dexterity or mobility.

accessibility-P075
Offer sufficiently sized controls. Controls that are too small are hard for many people to interact with and select. Strive to meet the recommended minimum control size for each platform to ensure controls and menus are comfortable for all when tapping and clicking.

accessibility-P076
Platform

accessibility-P077
Default control size

accessibility-P078
Minimum control size

accessibility-P079
iOS, iPadOS

accessibility-P080
44x44 pt

accessibility-P081
28x28 pt

accessibility-P082
macOS

accessibility-P083
28x28 pt

accessibility-P084
20x20 pt

accessibility-P085
tvOS

accessibility-P086
66x66 pt

accessibility-P087
56x56 pt

accessibility-P088
visionOS

accessibility-P089
60x60 pt

accessibility-P090
28x28 pt

accessibility-P091
watchOS

accessibility-P092
44x44 pt

accessibility-P093
28x28 pt

accessibility-P094
Consider spacing between controls as important as size. Include enough padding between elements to reduce the chance that someone taps the wrong control. In general, it works well to add about 12 points of padding around elements that include a bezel. For elements without a bezel, about 24 points of padding works well around the element’s visible edges.

accessibility-P099
Support simple gestures for common interactions. For many people, with or without disabilities, complex gestures can be challenging. For interactions people do frequently in your app or game, use the simplest gesture possible — avoid custom multifinger and multihand gestures — so repetitive actions are both comfortable and easy to remember.

accessibility-P100
Offer alternatives to gestures. Make sure your UI’s core functionality is accessible through more than one type of physical interaction. Gestures can be less comfortable for people who have limited dexterity, so offer onscreen ways to achieve the same outcome. For example, if you use a swipe gesture to dismiss a view, also make a button available so people can tap or use an assistive device.

accessibility-P103
Let people use Voice Control to give guidance and enter information verbally. With Voice Control, people can interact with their devices entirely by speaking commands. They can perform gestures, interact with screen elements, dictate and edit text, and more. To ensure a smooth experience, label interface elements appropriately. For developer guidance, see Voice Control.

accessibility-P104
Integrate with Siri and Shortcuts to let people perform tasks using voice alone. When your app supports Siri and Shortcuts, people can automate the important and repetitive tasks they perform regularly. They can initiate these tasks from Siri, the Action button on their iPhone or Apple Watch, and shortcuts on their Home Screen or in Control Center. For guidance, see Siri.

accessibility-P105
Support mobility-related assistive technologies. Features like VoiceOver, AssistiveTouch, Full Keyboard Access, Pointer Control, and Switch Control offer alternative ways for people with low mobility to interact with their devices. Conduct testing and verify that your app or game supports these technologies, and that your interface elements are appropriately labeled to ensure a great experience. For more information, see Performing accessibility testing for your app.

## Speech

accessibility-P108
Apple’s accessibility features help people with speech disabilities and people who prefer text-based interactions to communicate effectively using their devices.

accessibility-P109
Let people use the keyboard alone to navigate and interact with your app. People can turn on Full Keyboard Access to navigate apps using their physical keyboard. The system also defines accessibility keyboard shortcuts and a wide range of other keyboard shortcuts that many people use all the time. Avoid overriding system-defined keyboard shortcuts and evaluate your app to ensure it works well with Full Keyboard Access. For additional guidance, see Keyboards. For developer guidance, see Support Full Keyboard Access in your iOS app.

accessibility-P110
Support Switch Control. Switch Control is an assistive technology that lets people control their devices through separate hardware, game controllers, or sounds such as a click or a pop. People can perform actions like selecting, tapping, typing, and drawing when your app or game supports the ability to navigate using Switch Control. For developer guidance, see Switch Control.

## Cognitive

accessibility-P113
When you minimize complexity in your app or game, all people benefit.

accessibility-P114
Keep actions simple and intuitive. Ensure that people can navigate your interface using easy-to-remember and consistent interactions. Prefer system gestures and behaviors people are already familiar with over creating custom gestures people must learn and retain.

accessibility-P115
Minimize use of time-boxed interface elements. Views and controls that auto-dismiss on a timer can be problematic for people who need longer to process information, and for people who use assistive technologies that require more time to traverse the interface. Prefer dismissing views with an explicit action.

accessibility-P116
Consider offering difficulty accommodations in games. Everyone has their own way of playing and enjoying games. To support a variety of cognitive abilities, consider adding the ability to customize the difficulty level of your game, such as offering options for people to reduce the criteria for successfully completing a level, adjust reaction time, or enable control assistance.

accessibility-P117
Let people control audio and video playback. Avoid autoplaying audio and video content without also providing controls to start and stop it. Make sure these controls are discoverable and easy to act upon, and consider global settings that let people opt out of auto-playing all audio and video. For developer guidance, see Animated images and isVideoAutoplayEnabled.

accessibility-P118
Allow people to opt out of flashing lights in video playback. People might want to avoid bright, frequent flashes of light in the media they consume. A Dim Flashing Lights setting allows the system to calculate, mitigate, and inform people about flashing lights in a piece of media. If your app supports video playback, ensure that it responds appropriately to the Dim Flashing Lights setting. For developer guidance, see Flashing lights.

accessibility-P119
Be cautious with fast-moving and blinking animations. When you use these effects in excess, it can be distracting, cause dizziness, and in some cases even result in epileptic episodes. People who are prone to these effects can turn on the Reduce Motion accessibility setting. When this setting is active, ensure your app or game responds by reducing automatic and repetitive animations, including zooming, scaling, and peripheral motion. Other best practices for reducing motion include:

accessibility-P120
Tightening animation springs to reduce bounce effects

accessibility-P121
Tracking animations directly with people’s gestures

accessibility-P122
Avoiding animating depth changes in z-axis layers

accessibility-P123
Replacing transitions in x-, y-, and z-axes with fades to avoid motion

accessibility-P124
Avoiding animating into and out of blurs

accessibility-P125
Optimize your app’s UI for Assistive Access. Assistive Access is an accessibility feature in iOS and iPadOS that allows people with cognitive disabilities to use a streamlined version of your app. Assistive Access sets a default layout and control presentation for apps that reduces cognitive load, such as the following layout of the Camera app.

accessibility-P128
To optimize your app for this mode, use the following guidelines when Assistive Access is turned on:

accessibility-P129
Identify the core functionality of your app and consider removing noncritical workflows and UI elements.

accessibility-P130
Break up multistep workflows so people can focus on a single interaction per screen.

accessibility-P131
Always ask for confirmation twice whenever people perform an action that’s difficult to recover from, such a deleting a file.

accessibility-P132
For developer guidance, see Assistive Access.

## Platform considerations

accessibility-P134
No additional considerations for iOS, iPadOS, macOS, tvOS, or watchOS.

## visionOS

accessibility-P136
visionOS offers a variety of accessibility features people can use to interact with their surroundings in ways that are comfortable and work best for them, including head and hand Pointer Control, and a Zoom feature.

accessibility-P138
Prioritize comfort. The immersive nature of visionOS means that interfaces, animations, and interactions have a greater chance of causing motion sickness, and visual and ergonomic discomfort for people. To ensure the most comfortable experience, consider these tips:

accessibility-P139
Keep interface elements within a person’s field of view. Prefer horizontal layouts to vertical ones that might cause neck strain, and avoid demanding the viewer’s attention in different locations in quick succession.

accessibility-P140
Reduce the speed and intensity of animated objects, particularly in someone’s peripheral vision.

accessibility-P141
Be gentle with camera and video motion, and avoid situations where someone may feel like the world around them is moving without their control.

accessibility-P142
Avoid anchoring content to the wearer’s head, which may make them feel stuck and confined, and also prevent them from using assistive technologies like Pointer Control.

accessibility-P143
Minimize the need for large and repetitive gestures, as these can become tiresome and may be difficult depending on a person’s surroundings.

accessibility-P144
For additional guidance, see Create accessible spatial experiences and Design considerations for vision and motion.

## Resources

## Related

accessibility-P147
Inclusion

accessibility-P148
Typography

accessibility-P149
VoiceOver

## Developer documentation

accessibility-P151
Building accessible apps

accessibility-P152
Accessibility

accessibility-P153
Overview of Accessibility Nutrition Labels

## Videos

## Change log

accessibility-P156
Date

accessibility-P157
Changes

accessibility-P158
June 9, 2025

accessibility-P159
Added guidance and links for Assistive Access, Switch Control, and Accessibility Nutrition Labels.

accessibility-P160
March 7, 2025

accessibility-P161
Expanded and refined all guidance. Moved Dynamic Type guidance to the Typography page, and moved VoiceOver guidance to a new VoiceOver page.

accessibility-P162
June 10, 2024

accessibility-P163
Added a link to Apple’s Unity plug-ins for supporting Dynamic Type.

accessibility-P164
December 5, 2023

accessibility-P165
Updated visionOS Zoom lens artwork.

accessibility-P166
June 21, 2023

accessibility-P167
Updated to include guidance for visionOS.
