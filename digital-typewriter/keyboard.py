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
        self.current_lang = 'en'  # 'en' أو 'ar'
        self.shift_pressed = False
        self.caps_lock = False
        
        # إنشاء لوحة المفاتيح
        self.key_rows = []
        self.key_buttons = {}
        self.setup_keyboard()
        
        # تحميل التخطيط الحالي
        self.load_layout()
    
    def setup_keyboard(self):
        """إنشاء صفوف لوحة المفاتيح"""
        # تعريف صفوف المفاتيح - أضفت @ في الصف الأول بدلاً من `
        rows = [
            ['@', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
            ['CapsLock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'Enter'],
            ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift'],
            ['Ctrl', 'Alt', 'Space', 'Alt', 'Lang']
        ]
        
        # إنشاء كل صف
        for row_keys in rows:
            row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            row_box.set_halign(Gtk.Align.FILL)
            row_box.set_hexpand(True)
            row_box.set_homogeneous(False)  # السماح بأحجام مختلفة للمفاتيح
            
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
        
        # تعيين النص والميزات الخاصة
        if key_name in ['Backspace', 'Tab', 'CapsLock', 'Shift', 'Enter', 'Ctrl', 'Alt', 'Space', 'Lang']:
            button.add_css_class('key-special')
            
            if key_name == 'Space':
                button.add_css_class('key-space')
                button.set_label('␣')
                button.set_hexpand(True)
                button.set_halign(Gtk.Align.FILL)
            elif key_name == 'Lang':
                button.add_css_class('key-lang')
                button.set_label('EN / العربية')
                button.set_hexpand(True)
                button.set_halign(Gtk.Align.FILL)
            elif key_name == 'Backspace':
                button.set_label('⌫')
                button.set_hexpand(True)
                button.set_halign(Gtk.Align.FILL)
            elif key_name == 'Enter':
                button.set_label('↵')
                button.set_hexpand(True)
                button.set_halign(Gtk.Align.FILL)
            elif key_name == 'CapsLock':
                button.set_label('⇪')
                button.set_hexpand(True)
                button.set_halign(Gtk.Align.FILL)
            elif key_name in ['Shift', 'Tab']:
                button.set_label(key_name)
                button.set_hexpand(True)
                button.set_halign(Gtk.Align.FILL)
            else:
                button.set_label(key_name)
                button.set_hexpand(True)
                button.set_halign(Gtk.Align.FILL)
        else:
            # مفاتيح عادية - نجعلها تتسع بالتساوي
            button.set_label(key_name)
            button.set_hexpand(True)
            button.set_halign(Gtk.Align.FILL)
        
        # ربط إشارة النقر
        button.connect('clicked', self.on_key_clicked, key_name)
        
        return button
    
    def load_layout(self):
        """تحميل تخطيط اللغة الحالية"""
        if self.current_lang == 'en':
            self.layout = UK_LAYOUT
        else:
            self.layout = ARABIC_LAYOUT
        
        self.update_keys()
    
    def update_keys(self):
        """تحديث نص المفاتيح حسب اللغة والحالة"""
        for key_name, button in self.key_buttons.items():
            # تجاهل المفاتيح الخاصة التي لا تتغير
            if key_name in ['Backspace', 'Tab', 'CapsLock', 'Shift', 'Enter', 'Ctrl', 'Alt', 'Space', 'Lang']:
                continue
            
            if key_name in self.layout:
                # الحصول على الحرف حسب الحالة
                if self.current_lang == 'en':
                    if self.shift_pressed or self.caps_lock:
                        char = self.layout[key_name].get('shift', key_name)
                    else:
                        char = self.layout[key_name].get('normal', key_name)
                else:
                    # العربية - لا تدعم Shift/CapsLock
                    char = self.layout[key_name]
                
                # تحديث النص
                button.set_label(str(char))
    
    def on_key_clicked(self, button, key_name):
        """معالجة النقر على المفتاح"""
        # معالجة المفاتيح الخاصة
        if key_name == 'Backspace':
            self.editor.delete_backward()
            return
        elif key_name == 'Enter':
            self.editor.insert_newline()
            return
        elif key_name == 'Tab':
            self.editor.insert_text('    ')  # 4 مسافات
            return
        elif key_name == 'Space':
            self.editor.insert_text(' ')
            return
        elif key_name == 'Lang':
            self.toggle_language()
            return
        elif key_name == 'Shift':
            self.toggle_shift()
            return
        elif key_name == 'CapsLock':
            self.toggle_caps_lock()
            return
        elif key_name in ['Ctrl', 'Alt']:
            # مفاتيح تحكم لا تفعل شيئاً في هذا السياق
            return
        
        # إدخال الحرف
        char = self.get_character(key_name)
        if char:
            self.editor.insert_text(char)
        
        # إعادة تعيين Shift إذا كان مضغوطاً وليس CapsLock
        if self.shift_pressed and not self.caps_lock and self.current_lang == 'en':
            self.shift_pressed = False
            self.update_keys()
    
    def get_character(self, key_name):
        """الحصول على الحرف المناسب للمفتاح"""
        if key_name in self.layout:
            if self.current_lang == 'en':
                if self.shift_pressed or self.caps_lock:
                    return self.layout[key_name].get('shift', key_name)
                else:
                    return self.layout[key_name].get('normal', key_name)
            else:
                # العربية
                return self.layout[key_name]
        return None
    
    def toggle_language(self):
        """التبديل بين اللغات"""
        if self.current_lang == 'en':
            self.current_lang = 'ar'
        else:
            self.current_lang = 'en'
        
        # إعادة تعيين Shift و CapsLock عند تغيير اللغة
        self.shift_pressed = False
        self.caps_lock = False
        
        # تحديث لوحة المفاتيح
        self.load_layout()
        
        # تحديث لغة زر التبديل
        lang_button = self.key_buttons.get('Lang')
        if lang_button:
            if self.current_lang == 'en':
                lang_button.set_label('EN / العربية')
            else:
                lang_button.set_label('العربية / EN')
        
        # إزالة حالة CapsLock من الزر
        caps_button = self.key_buttons.get('CapsLock')
        if caps_button:
            caps_button.get_style_context().remove_class('key-active')
    
    def toggle_shift(self):
        """التبديل بين Shift مضغوط/غير مضغوط"""
        if self.current_lang == 'en':
            self.shift_pressed = not self.shift_pressed
            self.update_keys()
    
    def toggle_caps_lock(self):
        """التبديل بين CapsLock مفعل/معطل"""
        if self.current_lang == 'en':
            self.caps_lock = not self.caps_lock
            self.update_keys()
            
            # تحديث مظهر زر CapsLock
            caps_button = self.key_buttons.get('CapsLock')
            if caps_button:
                if self.caps_lock:
                    caps_button.get_style_context().add_class('key-active')
                else:
                    caps_button.get_style_context().remove_class('key-active')
    
    def set_language(self, lang):
        """تعيين اللغة مباشرة"""
        if lang in ['en', 'ar'] and lang != self.current_lang:
            self.current_lang = lang
            self.load_layout()