# -*- coding: utf-8 -*-

"""
Digital Typewriter - النافذة الرئيسية
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gdk, Pango, GLib, Gio, Adw
from editor import TextEditor
from keyboard import DigitalKeyboard

class DigitalTypewriterWindow(Adw.ApplicationWindow):
    """النافذة الرئيسية للتطبيق"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # إنشاء المكونات الرئيسية
        self.editor = None
        self.keyboard = None
        self.setup_ui()
        self.set_size_request(450, 200)
        
        # تطبيق التنسيقات
        self.apply_styles()
        
        # تعيين إشارات النافذة
        self.connect('destroy', self.on_destroy)
        
        # تعيين اختصار Ctrl+Q للخروج
        self.setup_keyboard_shortcuts()
    
    def setup_keyboard_shortcuts(self):
        """إعداد اختصارات لوحة المفاتيح"""
        # إنشاء إجراء للخروج
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_action)
        self.add_action(quit_action)
        
        # إضافة اختصار Ctrl+Q
        self.get_application().set_accels_for_action("win.quit", ["<Ctrl>q"])
    
    def setup_ui(self):
        """إنشاء واجهة المستخدم"""
        # الصندوق الرأسي الرئيسي
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_box.set_margin_top(10)
        main_box.set_margin_bottom(10)
        main_box.set_margin_start(10)
        main_box.set_margin_end(10)
        
        # إضافة عنوان التطبيق
        header = self.create_header()
        main_box.append(header)
        
        # إنشاء محرر النص
        self.editor = TextEditor()
        self.editor.set_vexpand(True)
        self.editor.set_hexpand(True)
        
        # إطار حول محرر النص ليشبه ورقة الآلة الكاتبة
        editor_frame = Gtk.Frame()
        editor_frame.set_child(self.editor)
        editor_frame.set_margin_bottom(10)
        editor_frame.set_margin_top(5)
        editor_frame.add_css_class('editor-frame')
        main_box.append(editor_frame)
        
        # إنشاء لوحة المفاتيح الرقمية
        self.keyboard = DigitalKeyboard(self.editor)
        self.keyboard.set_vexpand(False)
        self.keyboard.set_hexpand(True)
        main_box.append(self.keyboard)
        
        # تعيين المحتوى الرئيسي
        self.set_content(main_box)
    
    def create_header(self):
        """إنشاء رأس النافذة مع الأزرار"""
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        header_box.set_margin_bottom(5)
        
        # عنوان التطبيق
        title_label = Gtk.Label()
        title_label.set_markup("<span size='large' weight='bold'>⌨️ Digital Typewriter</span>")
        title_label.set_halign(Gtk.Align.START)
        title_label.set_hexpand(True)
        header_box.append(title_label)
        
        # أزرار التحكم
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        # زر Copy
        copy_button = Gtk.Button.new_with_label("📋 Copy")
        copy_button.add_css_class('suggested-action')
        copy_button.connect('clicked', self.on_copy_clicked)
        button_box.append(copy_button)
        
        # زر Clear
        clear_button = Gtk.Button.new_with_label("🗑️ Clear")
        clear_button.add_css_class('destructive-action')
        clear_button.connect('clicked', self.on_clear_clicked)
        button_box.append(clear_button)
        
        # زر Exit
        exit_button = Gtk.Button.new_with_label("🚪 Exit")
        exit_button.add_css_class('destructive-action')
        exit_button.connect('clicked', self.on_exit_clicked)
        button_box.append(exit_button)
        
        header_box.append(button_box)
        
        return header_box
    
    def apply_styles(self):
        """تطبيق التنسيقات CSS"""
        css_provider = Gtk.CssProvider()
        try:
            # محاولة تحميل من ملف
            css_file = Gio.File.new_for_path('ui/styles.css')
            if css_file.query_exists(None):
                css_provider.load_from_file(css_file)
            else:
                # استخدام الأنماط المضمنة
                css = """
                    .editor-frame {
                        border: 2px solid #c0c0c0;
                        border-radius: 8px;
                        background-color: #ffffff;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                    }
                    .editor-frame textview {
                        padding: 15px;
                        font-size: 16px;
                    }
                    window {
                        background-color: #f0ebe3;
                    }
                    button {
                        min-height: 35px;
                        min-width: 35px;
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    button.key {
                        min-height: 45px;
                        min-width: 45px;
                        border: 1px solid #d0d0d0;
                        background-color: #f8f8f8;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }
                    button.key:hover {
                        background-color: #e8e8e8;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
                    }
                    button.key:active {
                        background-color: #d0d0d0;
                        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
                    }
                    button.key-special {
                        background-color: #e8e8e8;
                        font-size: 12px;
                    }
                    button.key-space {
                        min-width: 200px;
                    }
                    button.key-lang {
                        background-color: #4a90d9;
                        color: white;
                        font-weight: bold;
                    }
                    button.key-lang:hover {
                        background-color: #3a7bc8;
                    }
                    button.key-active {
                        background-color: #4a8a5c !important;
                        color: white !important;
                    }
                    textview {
                        font-family: "Cairo", "DejaVu Sans", "FreeSans", sans-serif;
                        font-size: 16px;
                    }
                    .suggested-action {
                        background-color: #4a8a5c;
                        color: white;
                        font-weight: bold;
                        border: none;
                        border-radius: 6px;
                        padding: 8px 16px;
                    }
                    .suggested-action:hover {
                        background-color: #3a7a4c;
                    }
                    .destructive-action {
                        background-color: #c0392b;
                        color: white;
                        font-weight: bold;
                        border: none;
                        border-radius: 6px;
                        padding: 8px 16px;
                    }
                    .destructive-action:hover {
                        background-color: #a83226;
                    }
                """
                css_provider.load_from_data(css.encode())
        except Exception as e:
            print(f"Error loading CSS: {e}")
            # استخدام CSS افتراضي
            css_provider.load_from_data(b"""
                textview {
                    font-family: sans-serif;
                    font-size: 16px;
                }
            """)
        
        # تطبيق CSS على النافذة
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def on_copy_clicked(self, button):
        """معالجة زر Copy"""
        try:
            if self.editor:
                success = self.editor.copy_to_clipboard()
                if success:
                    self.show_toast("✅ Text copied to clipboard")
                else:
                    self.show_toast("❌ Failed to copy text")
        except Exception as e:
            print(f"Error copying text: {e}")
            self.show_toast("❌ Error copying text")
    
    def on_clear_clicked(self, button):
        """معالجة زر Clear مع مربع تأكيد"""
        try:
            # التحقق من وجود نص للمسح
            if not self.editor:
                return
            
            text = self.editor.get_text()
            if not text or text.strip() == "":
                self.show_toast("📝 Document is already empty")
                return
            
            # إنشاء مربع حوار باستخدام Gtk.Dialog بدلاً من AlertDialog
            dialog = Gtk.Dialog()
            dialog.set_title("Clear Document")
            dialog.set_modal(True)
            dialog.set_transient_for(self)
            dialog.set_default_size(300, 100)
            
            # إضافة محتوى
            content_box = dialog.get_content_area()
            content_box.set_margin_top(20)
            content_box.set_margin_bottom(20)
            content_box.set_margin_start(20)
            content_box.set_margin_end(20)
            
            label = Gtk.Label()
            label.set_markup("<b>Are you sure you want to clear the document?</b>")
            label.set_halign(Gtk.Align.CENTER)
            content_box.append(label)
            
            label2 = Gtk.Label()
            label2.set_text("This action cannot be undone.")
            label2.set_halign(Gtk.Align.CENTER)
            content_box.append(label2)
            
            # إضافة أزرار
            cancel_button = dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
            clear_button = dialog.add_button("Clear", Gtk.ResponseType.OK)
            clear_button.add_css_class('destructive-action')
            
            # عرض مربع الحوار ومعالجة النتيجة
            dialog.connect('response', self.on_clear_dialog_response)
            dialog.show()
            
        except Exception as e:
            print(f"Error showing clear dialog: {e}")
            # في حالة الخطأ، قم بالمسح مباشرة
            if self.editor:
                self.editor.clear_text()
                self.show_toast("🗑️ Document cleared")
    
    def on_clear_dialog_response(self, dialog, response_id):
        """معالجة استجابة مربع حوار المسح"""
        try:
            if response_id == Gtk.ResponseType.OK:
                if self.editor:
                    self.editor.clear_text()
                    self.show_toast("🗑️ Document cleared")
            dialog.destroy()
        except Exception as e:
            print(f"Error in clear dialog response: {e}")
            if self.editor:
                self.editor.clear_text()
                self.show_toast("🗑️ Document cleared")
    
    def on_exit_clicked(self, button):
        """معالجة زر Exit"""
        self.on_quit_action(None, None)
    
    def on_quit_action(self, action, parameter):
        """معالجة إجراء الخروج"""
        try:
            # التحقق من وجود نص غير محفوظ
            if not self.editor:
                self.get_application().quit()
                return
            
            text = self.editor.get_text()
            if text and text.strip():
                # إنشاء مربع حوار باستخدام Gtk.Dialog
                dialog = Gtk.Dialog()
                dialog.set_title("Exit Digital Typewriter")
                dialog.set_modal(True)
                dialog.set_transient_for(self)
                dialog.set_default_size(350, 120)
                
                # إضافة محتوى
                content_box = dialog.get_content_area()
                content_box.set_margin_top(20)
                content_box.set_margin_bottom(20)
                content_box.set_margin_start(20)
                content_box.set_margin_end(20)
                
                label = Gtk.Label()
                label.set_markup("<b>You have unsaved text.</b>")
                label.set_halign(Gtk.Align.CENTER)
                content_box.append(label)
                
                label2 = Gtk.Label()
                label2.set_text("Are you sure you want to exit?")
                label2.set_halign(Gtk.Align.CENTER)
                content_box.append(label2)
                
                # إضافة أزرار
                cancel_button = dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
                exit_button = dialog.add_button("Exit", Gtk.ResponseType.OK)
                exit_button.add_css_class('destructive-action')
                
                # عرض مربع الحوار ومعالجة النتيجة
                dialog.connect('response', self.on_exit_dialog_response)
                dialog.show()
            else:
                # لا يوجد نص، اخرج مباشرة
                self.get_application().quit()
        except Exception as e:
            print(f"Error in quit action: {e}")
            # في حالة الخطأ، اخرج مباشرة
            self.get_application().quit()
    
    def on_exit_dialog_response(self, dialog, response_id):
        """معالجة استجابة مربع حوار الخروج"""
        try:
            if response_id == Gtk.ResponseType.OK:
                self.get_application().quit()
            dialog.destroy()
        except Exception as e:
            print(f"Error in exit dialog response: {e}")
            self.get_application().quit()
    
    def show_toast(self, message):
        """عرض رسالة منبثقة"""
        try:
            toast = Adw.Toast.new(message)
            toast.set_timeout(2)
            
            # الحصول على AdwToastOverlay إذا كان موجوداً
            content = self.get_content()
            
            # التحقق مما إذا كان المحتوى هو ToastOverlay
            if content and isinstance(content, Adw.ToastOverlay):
                content.add_toast(toast)
            else:
                # إنشاء ToastOverlay جديد
                overlay = Adw.ToastOverlay()
                if content:
                    self.set_content(None)
                    overlay.set_child(content)
                    overlay.add_toast(toast)
                    self.set_content(overlay)
                else:
                    self.set_content(overlay)
                    overlay.add_toast(toast)
        except Exception as e:
            print(f"Error showing toast: {e}")
    
    def focus_editor(self):
        """إعطاء التركيز لمحرر النص"""
        if self.editor:
            self.editor.grab_focus()
    
    def on_destroy(self, window):
        """معالجة إغلاق النافذة"""
        # حفظ أي بيانات إذا لزم الأمر
        pass