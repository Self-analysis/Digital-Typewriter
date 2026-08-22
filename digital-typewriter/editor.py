# -*- coding: utf-8 -*-

"""Digital Typewriter - محرر النص"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')

from gi.repository import Gtk, Gdk, Pango, GLib

class TextEditor(Gtk.ScrolledWindow):
    """محرر النص متعدد الأسطر مع دعم RTL ومؤشر كتابة واضح."""
    
    def __init__(self):
        super().__init__()
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.set_propagate_natural_height(True)
        self.set_propagate_natural_width(True)
        
        self.text_view = Gtk.TextView()
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.text_view.set_accepts_tab(True)
        self.text_view.set_hexpand(True)
        self.text_view.set_vexpand(True)
        self.text_view.set_editable(True)
        self.text_view.set_cursor_visible(True)
        self.text_view.set_can_focus(True)
        
        css = """
            textview {
                font-family: "Cairo", "DejaVu Sans", "FreeSans", sans-serif;
                font-size: 16px;
                caret-color: #1a73e8;
            }
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode())
        self.text_view.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        self.buffer = self.text_view.get_buffer()
        self.text_view.set_direction(Gtk.TextDirection.LTR)
        self.text_view.set_top_margin(10)
        self.text_view.set_bottom_margin(10)
        self.text_view.set_left_margin(15)
        self.text_view.set_right_margin(15)
        self.set_child(self.text_view)
        self.buffer.connect('changed', self.on_text_changed)
    
    def insert_text(self, text):
        if not text:
            return
        self.text_view.grab_focus()
        cursor_iter = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        self.buffer.insert(cursor_iter, text)
        self.buffer.place_cursor(cursor_iter)
        self.text_view.set_cursor_visible(True)
        self.scroll_to_cursor()
        self.text_view.set_direction(Gtk.TextDirection.RTL if self.is_arabic(text) else Gtk.TextDirection.LTR)
    
    def delete_backward(self):
        self.text_view.grab_focus()
        cursor_iter = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        if cursor_iter.starts_line() and cursor_iter.get_line_offset() == 0:
            if cursor_iter.get_line() == 0:
                return
            prev_line = cursor_iter.copy()
            prev_line.backward_line()
            prev_line.forward_to_line_end()
            self.buffer.delete(prev_line, cursor_iter)
            return
        prev_iter = cursor_iter.copy()
        if prev_iter.backward_char():
            self.buffer.delete(prev_iter, cursor_iter)
        self.text_view.set_cursor_visible(True)
        self.scroll_to_cursor()
    
    def delete_forward(self):
        self.text_view.grab_focus()
        cursor_iter = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        next_iter = cursor_iter.copy()
        if next_iter.forward_char():
            self.buffer.delete(cursor_iter, next_iter)
    
    def insert_newline(self):
        self.insert_text('\n')
    
    def get_text(self):
        return self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter(), True)
    
    def clear_text(self):
        self.buffer.delete(self.buffer.get_start_iter(), self.buffer.get_end_iter())
        self.text_view.grab_focus()
        self.text_view.set_cursor_visible(True)
    
    def copy_to_clipboard(self):
        try:
            text = self.get_text()
            if not text:
                return False
            display = Gdk.Display.get_default()
            if not display:
                return False
            clipboard = display.get_clipboard()
            from gi.repository import GObject
            content_provider = Gdk.ContentProvider.new_for_value(GObject.Value(GObject.TYPE_STRING, text))
            clipboard.set_content(content_provider)
            return True
        except Exception as e:
            print(f"Error in copy_to_clipboard: {e}")
            return False
    
    def paste_from_clipboard(self):
        try:
            display = Gdk.Display.get_default()
            if display:
                clipboard = display.get_clipboard()
                if clipboard:
                    clipboard.read_text_async(None, self.on_paste_text)
        except Exception as e:
            print(f"Error pasting text: {e}")
    
    def on_paste_text(self, clipboard, result):
        try:
            text = clipboard.read_text_finish(result)
            if text:
                self.insert_text(text)
        except Exception as e:
            print(f"Error in paste result: {e}")
    
    def scroll_to_cursor(self):
        cursor_iter = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        self.text_view.scroll_to_iter(cursor_iter, 0.0, True, 0.0, 0.0)
    
    def on_text_changed(self, buffer):
        text = self.get_text()
        if text:
            self.text_view.set_direction(Gtk.TextDirection.RTL if any('\u0600' <= c <= '\u06FF' for c in text) else Gtk.TextDirection.LTR)
        self.text_view.set_cursor_visible(True)
    
    def is_arabic(self, text):
        return bool(text) and any('\u0600' <= c <= '\u06FF' for c in text)
    
    def grab_focus(self):
        self.text_view.grab_focus()
        self.text_view.set_cursor_visible(True)
