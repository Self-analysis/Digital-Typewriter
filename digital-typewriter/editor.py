# -*- coding: utf-8 -*-

"""
Digital Typewriter - محرر النص
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')

from gi.repository import Gtk, Gdk, Pango, GLib

class TextEditor(Gtk.ScrolledWindow):
    """محرر النص متعدد الأسطر مع دعم RTL"""
    
    def __init__(self):
        super().__init__()
        
        # إعدادات التمرير
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.set_propagate_natural_height(True)
        self.set_propagate_natural_width(True)
        
        # إنشاء TextView
        self.text_view = Gtk.TextView()
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.text_view.set_accepts_tab(True)
        self.text_view.set_hexpand(True)
        self.text_view.set_vexpand(True)
        
        # إعدادات الخط - الطريقة الصحيحة في GTK 4
        css = """
            textview {
                font-family: "Cairo", "DejaVu Sans", "FreeSans", sans-serif;
                font-size: 16px;
            }
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode())
        self.text_view.get_style_context().add_provider(
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        # إعدادات النص
        self.buffer = self.text_view.get_buffer()
        
        # دعم النصوص ثنائية الاتجاه (Bidirectional)
        self.text_view.set_direction(Gtk.TextDirection.LTR)
        
        # تمكين التحديد بالماوس
        self.text_view.set_editable(True)
        self.text_view.set_cursor_visible(True)
        
        # إعدادات المسافات
        self.text_view.set_top_margin(10)
        self.text_view.set_bottom_margin(10)
        self.text_view.set_left_margin(15)
        self.text_view.set_right_margin(15)
        
        # إضافة TextView إلى ScrolledWindow
        self.set_child(self.text_view)
        
        # تعيين إشارات
        self.buffer.connect('changed', self.on_text_changed)
    
    def insert_text(self, text):
        """إدراج نص في موضع المؤشر"""
        if not text:
            return
        
        # الحصول على موضع المؤشر
        cursor_iter = self.buffer.get_iter_at_mark(
            self.buffer.get_insert()
        )
        
        # إدراج النص
        self.buffer.insert(cursor_iter, text)
        
        # تحريك المؤشر إلى نهاية النص المدرج
        new_iter = cursor_iter.copy()
        new_iter.forward_chars(len(text))
        self.buffer.move_mark(self.buffer.get_insert(), new_iter)
        
        # جعل النص مرئياً
        self.scroll_to_cursor()
        
        # التعامل مع اللغة العربية (RTL)
        if self.is_arabic(text):
            self.text_view.set_direction(Gtk.TextDirection.RTL)
        else:
            self.text_view.set_direction(Gtk.TextDirection.LTR)
    
    def delete_backward(self):
        """حذف حرف واحد للخلف"""
        cursor_iter = self.buffer.get_iter_at_mark(
            self.buffer.get_insert()
        )
        
        # التحقق من وجود نص قبل المؤشر
        if cursor_iter.starts_line() and cursor_iter.get_line_offset() == 0:
            # في بداية السطر - تحقق من وجود سطر سابق
            if cursor_iter.starts_line() and cursor_iter.get_line() == 0:
                return  # في بداية المستند
            # حذف نهاية السطر السابق
            prev_line = cursor_iter.copy()
            prev_line.backward_line()
            prev_line.forward_to_line_end()
            self.buffer.delete(prev_line, cursor_iter)
            return
        
        # الحصول على موضع الحرف السابق
        prev_iter = cursor_iter.copy()
        if not prev_iter.backward_char():
            return  # لا يوجد حرف سابق
        
        # حذف الحرف
        self.buffer.delete(prev_iter, cursor_iter)
    
    def delete_forward(self):
        """حذف حرف واحد للأمام"""
        cursor_iter = self.buffer.get_iter_at_mark(
            self.buffer.get_insert()
        )
        
        next_iter = cursor_iter.copy()
        if not next_iter.forward_char():
            return  # نهاية النص
        
        self.buffer.delete(cursor_iter, next_iter)
    
    def insert_newline(self):
        """إدراج سطر جديد"""
        self.insert_text("\n")
    
    def get_text(self):
        """الحصول على كل النص"""
        start_iter = self.buffer.get_start_iter()
        end_iter = self.buffer.get_end_iter()
        return self.buffer.get_text(start_iter, end_iter, True)
    
    def clear_text(self):
        """مسح كل النص"""
        start_iter = self.buffer.get_start_iter()
        end_iter = self.buffer.get_end_iter()
        self.buffer.delete(start_iter, end_iter)
    
    def copy_to_clipboard(self):
        """نسخ النص إلى الحافظة - الطريقة الصحيحة لـ GTK 4/Wayland"""
        try:
            text = self.get_text()
            if not text:
                return False
            
            # الطريقة الصحيحة في GTK 4
            display = Gdk.Display.get_default()
            if not display:
                raise Exception("No display found")
            
            # الحصول على الحافظة
            clipboard = display.get_clipboard()
            if not clipboard:
                raise Exception("No clipboard found")
            
            # في GTK 4، نستخدم Gdk.ContentProvider
            # لنسخ النص، نستخدم Gdk.ContentProvider.new_for_value
            from gi.repository import GdkPixbuf, GObject
            
            # إنشاء ContentProvider للنص
            content_provider = Gdk.ContentProvider.new_for_value(GObject.Value(GObject.TYPE_STRING, text))
            
            # تعيين المحتوى في الحافظة
            clipboard.set_content(content_provider)
            
            return True
            
        except Exception as e:
            print(f"Error in copy_to_clipboard: {e}")
            
            # محاولة طريقة بديلة
            try:
                # استخدام Gtk.TextBuffer للنسخ
                # نسخ النص المحدد أو كل النص
                clipboard = display.get_clipboard()
                
                # إنشاء Value للنص
                value = GObject.Value()
                value.init(GObject.TYPE_STRING)
                value.set_string(text)
                
                # إنشاء ContentProvider
                provider = Gdk.ContentProvider.new_for_value(value)
                clipboard.set_content(provider)
                return True
            except Exception as e2:
                print(f"Alternative copy method failed: {e2}")
                return False
    
    def paste_from_clipboard(self):
        """لصق من الحافظة"""
        try:
            display = Gdk.Display.get_default()
            if display:
                clipboard = display.get_clipboard()
                if clipboard:
                    # في GTK 4، نستخدم read_text_async للقراءة
                    clipboard.read_text_async(None, self.on_paste_text)
        except Exception as e:
            print(f"Error pasting from clipboard: {e}")
    
    def on_paste_text(self, clipboard, result):
        """معالجة نتيجة لصق النص"""
        try:
            # استخدام read_text_finish للحصول على النص
            if hasattr(clipboard, 'read_text_finish'):
                text = clipboard.read_text_finish(result)
                if text:
                    self.insert_text(text)
            else:
                # طريقة بديلة للقراءة
                text = clipboard.read_text()
                if text:
                    self.insert_text(text)
        except Exception as e:
            print(f"Error pasting text: {e}")
    
    def scroll_to_cursor(self):
        """تمرير العرض إلى موضع المؤشر"""
        cursor_iter = self.buffer.get_iter_at_mark(
            self.buffer.get_insert()
        )
        self.text_view.scroll_to_iter(
            cursor_iter,
            0.0,
            True,
            0.0,
            0.0
        )
    
    def on_text_changed(self, buffer):
        """معالجة تغيير النص"""
        # تحديث اتجاه النص بناءً على المحتوى
        text = self.get_text()
        if text:
            # فحص ما إذا كان النص يحتوي على عربية
            if any('\u0600' <= c <= '\u06FF' for c in text):
                self.text_view.set_direction(Gtk.TextDirection.RTL)
            else:
                self.text_view.set_direction(Gtk.TextDirection.LTR)
    
    def is_arabic(self, text):
        """التحقق مما إذا كان النص عربياً"""
        if not text:
            return False
        return any('\u0600' <= c <= '\u06FF' for c in text)
    
    def grab_focus(self):
        """إعطاء التركيز للمحرر"""
        self.text_view.grab_focus()