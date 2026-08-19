Digital Typewriter

Digital Typewriter is an open-source digital typewriter application for Linux, designed to provide a standalone typing environment using a mouse and numeric keypad, with a focus on compatibility with Fedora Workstation 44, GNOME, and Wayland.

Why Digital Typewriter?

In modern desktop environments using Wayland, creating a floating virtual keyboard that operates at the system level and interacts directly with other applications can be complex, especially when the keyboard needs to remain visible on top of other windows and input characters into external applications.

Instead of trying to circumvent these limitations, Digital Typewriter takes a different approach:

It provides a standalone typing space that combines a text editor and a numeric keypad within a single window.

This eliminates the need for the application to control other application windows or attempt to inject keystrokes into the system.

How does it work?

The main window consists of two parts:

┌───────────────────────────────────────┐
│ Digital Typewriter │
├────────────────────────────────────────┤
│ │
│ Writing Area │
│ │
│ Hello, this is my digital typewriter. │
│ This is a digital typewriter. │
│ │
├────────────────────────────────────────┤
│ Keyboard │
│ │
│ Q W E R T Y U I O P │
│ A S D F G H J K L │
│ Z X C V B N M │
│ │
│ English / Arabic │

└───────────────────────────────────────┘

The user types text by pressing the numeric keypad keys, and the characters are entered directly into the text editor within the application.

A traditional physical keyboard can also be used for typing within the text editor.

Does not rely on a floating keyboard.

Digital Typewriter is not a system floating keyboard.

The application does not create a separate keyboard window, nor does it attempt to keep it on top of other applications.

It also doesn't attempt to send input to:

Firefox
Chrome
LibreOffice
Terminal
or any external application.

Instead, the typing process takes place within the application's own text editor.

This design reduces reliance on the window management and text input mechanisms of desktop environments, making the application more suitable for working within GNOME + Wayland.

Arabic and English Support

The application currently supports two main languages:

🇬🇧 English

Using the UK English Keyboard layout.

Arabic

With support for:

Unicode.

Right-to-left typing.

Arabic characters.

Mixed text.

Switching between Arabic and English.

Example:

Today I am using Digital Typewriter.

This is the Arabic text.

English and Arabic can be written within the same document.

Features
🖱️ Mouse typing.

⌨️ Physical keyboard support.

🇬🇧 UK English layout. 🇸🇦 Arabic keyboard.

🔄 Switch between Arabic and English.

📝 Multi-line text editor.

↔️ Arabic RTL text direction support.

🌐 Unicode support.

📋 Copy text to clipboard.

🗑️ Clear text with confirmation.

↕️ Window resizing capability.

🔲 Keys adapt to window size.

🖥️ GNOME-friendly design.

🐧 Specifically designed for Fedora and modern Linux environments.

Compatibility

The project was developed and tested with a focus on:

Fedora Workstation 44
GNOME
Wayland
GTK 4
Python 3
PyGObject

The project also includes an RPM build mechanism suitable for Fedora.

GNOME Software

The project is designed to be distributed as an RPM package containing standard desktop components, including:

Desktop Entry
AppStream Metadata
Application ID
Application Icon
Standard System Installation Paths

It can therefore be installed as a Fedora package and recognized by GNOME Software.

What problem does the project attempt to solve?

Digital Typewriter does not claim to solve all Wayland virtual keyboard problems, nor does it attempt to replace the system's virtual keyboard.

Instead, it addresses a specific use case:

How can we provide a convenient way to type using the mouse on Fedora GNOME Wayland without creating a floating keyboard that controls other applications?

The solution is to provide a standalone application that combines:

A text editor and a numeric keypad

in a single window.

This makes the application particularly useful for users who want to type by clicking keys with the mouse, with support for Arabic and English, without relying on external input mechanisms.

Project Philosophy

The project is based on a simple principle:

Instead of trying to circumvent the limitations of the desktop environment, design the application to work with it.

Therefore, Digital Typewriter does not rely on:

set_keep_above
is_keep_above
XTest
X11-only APIs
Layer Shell
Keystroke injection into other applications

Instead, it prefers to use the standard GTK and Wayland interfaces.

Open Source Project

Digital Typewriter is an open-source project, designed to be scalable and contribute to by the Linux community.

Developers can contribute to:

Adding new languages.

Adding new keyboard layouts.

Improving RTL support.

Improving the user interface.

Adding file saving and opening.

Adding export to TXT and Markdown.

Adding printing.

Adding in-document search.

Adding new themes and customizations.

Improving accessibility.

Adding support for other Linux distributions.

The Future

Digital Typewriter could be developed in the future into a fully integrated writing environment, while maintaining
