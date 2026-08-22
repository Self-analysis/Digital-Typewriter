# -*- coding: utf-8 -*-

"""
Digital Typewriter - لوحة المفاتيح الرقمية
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')

from gi.repository import Gtk, Gdk, GLib
from layouts.uk import UK_LAYOUT
from layouts.arabic import ARABIC_LAYOUT

class DigitalKeyboard(Gtk.Box):
    """لوحة المفاتيح الرقمية مع دعم اللغات"""
    
    def __init__(self, editor):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.editor = editor
        self.current_lang = 'en'
        self.shift_pressed = False
        self.caps_lock = False
        self.key_rows = []
        self.key_buttons = {}
        self.setup_keyboard()
        self.load_layout()
    
    def setup_keyboard(self):
        """إنشاء صفوف لوحة المفاتيح"""
        rows = [
            ['@', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
            ['CapsLock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", ':', 'Enter'],
            ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift'],
            ['Ctrl', 'Alt', 'Space', 'Alt', 'Lang']
        ]
        for row_keys in rows:
            row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            row_box.set_halign(Gtk.Align.FILL)
            row_box.set_hexpand(True)
            row_box.set_homogeneous(False)
            for key in row_keys:
                button = self.create_key_button(key, row_keys)
                row_box.append(button)
                self.key_buttons[key] = button
            self.append(row_box)
            self.key_rows.append(row_box)
    
    def create_key_button(self, key_name, row_keys):
        """إنشاء زر للمفتاح"""
        button = Gtk.Button()
        button.add_css_class('key')
        if key_name in ['Backspace', 'Tab', 'CapsLock', 'Shift', 'Enter', 'Ctrl', 'Alt', 'Space', 'Lang']:
            button.add_css_class('key-special')
            if key_name == 'Space':
                button.add_css_class('key-space')
                button.set_label('␣')
            elif key_name == 'Lang':
                button.add_css_class('key-lang')
                button.set_label('EN / العربية')
            elif key_name == 'Backspace':
                button.set_label('⌫')
            elif key_name == 'Enter':
                button.set_label('↵')
            elif key_name == 'CapsLock':
                button.set_label('⇪')
            else:
                button.set_label(key_name)
        else:
            button.set_label(key_name)
        button.set_hexpand(True)
        button.set_halign(Gtk.Align.FILL)
        button.connect('clicked', self.on_key_clicked, key_name)
        return button
    
    def load_layout(self):
        self.layout = UK_LAYOUT if self.current_lang == 'en' else ARABIC_LAYOUT
        self.update_keys()
    
    def update_keys(self):
        for key_name, button in self.key_buttons.items():
            if key_name in ['Backspace', 'Tab', 'CapsLock', 'Shift', 'Enter', 'Ctrl', 'Alt', 'Space', 'Lang', ':']:
                continue
            if key_name in self.layout:
                if self.current_lang == 'en':
                    char = self.layout[key_name].get('shift' if (self.shift_pressed or self.caps_lock) else 'normal', key_name)
                else:
                    char = self.layout[key_name]
                button.set_label(str(char))
    
    def on_key_clicked(self, button, key_name):
        if key_name == 'Backspace':
            self.editor.delete_backward()
        elif key_name == 'Enter':
            self.editor.insert_newline()
        elif key_name == 'Tab':
            self.editor.insert_text('    ')
        elif key_name == 'Space':
            self.editor.insert_text(' ')
        elif key_name == 'Lang':
            self.toggle_language()
        elif key_name == 'Shift':
            self.toggle_shift()
        elif key_name == 'CapsLock':
            self.toggle_caps_lock()
        elif key_name in ['Ctrl', 'Alt']:
            pass
        elif key_name == ':':
            self.editor.insert_text(':')
        else:
            char = self.get_character(key_name)
            if char:
                self.editor.insert_text(char)
            if self.shift_pressed and not self.caps_lock and self.current_lang == 'en':
                self.shift_pressed = False
                self.update_keys()
        # إعادة التركيز إلى محرر النص حتى يبقى مؤشر الكتابة ظاهراً بعد النقر بالماوس.
        self.editor.grab_focus()
        self.editor.text_view.set_cursor_visible(True)
    
    def get_character(self, key_name):
        if key_name in self.layout:
            if self.current_lang == 'en':
                return self.layout[key_name].get('shift' if (self.shift_pressed or self.caps_lock) else 'normal', key_name)
            return self.layout[key_name]
        return None
    
    def toggle_language(self):
        self.current_lang = 'ar' if self.current_lang == 'en' else 'en'
        self.shift_pressed = False
        self.caps_lock = False
        self.load_layout()
        lang_button = self.key_buttons.get('Lang')
        if lang_button:
            lang_button.set_label('EN / العربية' if self.current_lang == 'en' else 'العربية / EN')
        caps_button = self.key_buttons.get('CapsLock')
        if caps_button:
            caps_button.get_style_context().remove_class('key-active')
    
    def toggle_shift(self):
        if self.current_lang == 'en':
            self.shift_pressed = not self.shift_pressed
            self.update_keys()
    
    def toggle_caps_lock(self):
        if self.current_lang == 'en':
            self.caps_lock = not self.caps_lock
            self.update_keys()
            caps_button = self.key_buttons.get('CapsLock')
            if caps_button:
                if self.caps_lock:
                    caps_button.get_style_context().add_class('key-active')
                else:
                    caps_button.get_style_context().remove_class('key-active')
    
    def set_language(self, lang):
        if lang in ['en', 'ar'] and lang != self.current_lang:
            self.current_lang = lang
            self.load_layout()
