# -*- coding: utf-8 -*-

"""Digital Typewriter - النافذة الرئيسية."""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gdk, Gio, Adw
from editor import TextEditor
from keyboard import DigitalKeyboard

class DigitalTypewriterWindow(Adw.ApplicationWindow):
    """النافذة الرئيسية مع دعم تحريكها عبر GTK4/Wayland."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.editor = None
        self.keyboard = None
        self.setup_ui()
        self.set_size_request(450, 200)
        self.apply_styles()
        self.setup_keyboard_shortcuts()

    def setup_keyboard_shortcuts(self):
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_action)
        self.add_action(quit_action)
        self.get_application().set_accels_for_action("win.quit", ["<Ctrl>q"])

    def setup_ui(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_box.set_margin_top(10)
        main_box.set_margin_bottom(10)
        main_box.set_margin_start(10)
        main_box.set_margin_end(10)
        main_box.append(self.create_header())

        self.editor = TextEditor()
        self.editor.set_vexpand(True)
        self.editor.set_hexpand(True)
        editor_frame = Gtk.Frame()
        editor_frame.set_child(self.editor)
        editor_frame.set_margin_bottom(10)
        editor_frame.set_margin_top(5)
        editor_frame.add_css_class('editor-frame')
        main_box.append(editor_frame)

        self.keyboard = DigitalKeyboard(self.editor)
        self.keyboard.set_vexpand(False)
        self.keyboard.set_hexpand(True)
        main_box.append(self.keyboard)
        self.set_content(main_box)

    def create_header(self):
        """رأس النافذة: سحب المساحة الفارغة يحرك التطبيق."""
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        header_box.set_margin_bottom(5)
        header_box.set_margin_start(4)
        header_box.set_margin_end(4)
        header_box.add_css_class('window-drag-area')

        title_label = Gtk.Label()
        title_label.set_markup("<span size='large' weight='bold'>⌨️ Digital Typewriter</span>")
        title_label.set_halign(Gtk.Align.START)
        title_label.set_hexpand(True)
        header_box.append(title_label)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        copy_button = Gtk.Button.new_with_label("📋 Copy")
        copy_button.add_css_class('suggested-action')
        copy_button.connect('clicked', self.on_copy_clicked)
        button_box.append(copy_button)
        clear_button = Gtk.Button.new_with_label("🗑️ Clear")
        clear_button.add_css_class('destructive-action')
        clear_button.connect('clicked', self.on_clear_clicked)
        button_box.append(clear_button)
        exit_button = Gtk.Button.new_with_label("🚪 Exit")
        exit_button.add_css_class('destructive-action')
        exit_button.connect('clicked', self.on_exit_clicked)
        button_box.append(exit_button)
        header_box.append(button_box)

        # GTK4/Wayland: طلب تحريك النافذة من مدير النوافذ، بدون X11 أو set_keep_above.
        drag = Gtk.GestureDrag.new()
        drag.set_button(1)
        drag.connect('drag-begin', self.on_header_drag_begin)
        header_box.add_controller(drag)
        return header_box

    def on_header_drag_begin(self, gesture, start_x, start_y):
        """تحريك النافذة عند سحب رأسها بزر الماوس الأيسر."""
        try:
            surface = self.get_surface()
            device = gesture.get_device()
            if surface and device and hasattr(surface, 'begin_move'):
                surface.begin_move(device, 1, start_x, start_y, 0)
        except Exception as e:
            print(f"Window move unavailable: {e}")

    def apply_styles(self):
        css_provider = Gtk.CssProvider()
        css = """
            .editor-frame { border: 2px solid #c0c0c0; border-radius: 8px; background-color: #ffffff; }
            .window-drag-area { min-height: 42px; }
            textview { font-family: "Cairo", "DejaVu Sans", "FreeSans", sans-serif; font-size: 16px; }
            button { min-height: 35px; min-width: 35px; border-radius: 4px; font-weight: bold; }
            button.key { min-height: 45px; min-width: 45px; }
            button.key-special { font-size: 12px; }
            button.key-space { min-width: 200px; }
            button.key-lang { font-weight: bold; }
            button.key-active { font-weight: bold; }
            .suggested-action, .destructive-action { font-weight: bold; border-radius: 6px; padding: 8px 16px; }
        """
        css_provider.load_from_data(css.encode())
        display = Gdk.Display.get_default()
        if display:
            Gtk.StyleContext.add_provider_for_display(display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def on_copy_clicked(self, button):
        if self.editor:
            self.show_toast("✅ Text copied to clipboard" if self.editor.copy_to_clipboard() else "❌ Failed to copy text")

    def on_clear_clicked(self, button):
        if not self.editor:
            return
        if not self.editor.get_text().strip():
            self.show_toast("📝 Document is already empty")
            return
        dialog = Gtk.Dialog()
        dialog.set_title("Clear Document")
        dialog.set_modal(True)
        dialog.set_transient_for(self)
        content = dialog.get_content_area()
        content.set_margin_top(20); content.set_margin_bottom(20); content.set_margin_start(20); content.set_margin_end(20)
        content.append(Gtk.Label(label="Are you sure you want to clear the document?"))
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        clear_button = dialog.add_button("Clear", Gtk.ResponseType.OK)
        clear_button.add_css_class('destructive-action')
        dialog.connect('response', self.on_clear_dialog_response)
        dialog.present()

    def on_clear_dialog_response(self, dialog, response_id):
        if response_id == Gtk.ResponseType.OK and self.editor:
            self.editor.clear_text()
            self.show_toast("🗑️ Document cleared")
        dialog.destroy()

    def on_exit_clicked(self, button):
        self.on_quit_action(None, None)

    def on_quit_action(self, action, parameter):
        if not self.editor or not self.editor.get_text().strip():
            self.get_application().quit()
            return
        dialog = Gtk.Dialog()
        dialog.set_title("Exit Digital Typewriter")
        dialog.set_modal(True)
        dialog.set_transient_for(self)
        content = dialog.get_content_area()
        content.set_margin_top(20); content.set_margin_bottom(20); content.set_margin_start(20); content.set_margin_end(20)
        content.append(Gtk.Label(label="You have unsaved text. Are you sure you want to exit?"))
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        exit_button = dialog.add_button("Exit", Gtk.ResponseType.OK)
        exit_button.add_css_class('destructive-action')
        dialog.connect('response', self.on_exit_dialog_response)
        dialog.present()

    def on_exit_dialog_response(self, dialog, response_id):
        dialog.destroy()
        if response_id == Gtk.ResponseType.OK:
            self.get_application().quit()

    def show_toast(self, message):
        try:
            content = self.get_content()
            if isinstance(content, Adw.ToastOverlay):
                content.add_toast(Adw.Toast.new(message))
                return
            overlay = Adw.ToastOverlay()
            self.set_content(None)
            overlay.set_child(content)
            self.set_content(overlay)
            overlay.add_toast(Adw.Toast.new(message))
        except Exception as e:
            print(f"Error showing toast: {e}")

    def focus_editor(self):
        if self.editor:
            self.editor.grab_focus()
