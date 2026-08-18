# -*- coding: utf-8 -*-

"""
Digital Typewriter - تطبيق GTK الرئيسي
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from ui.main_window import DigitalTypewriterWindow

class DigitalTypewriterApp(Adw.Application):
    """التطبيق الرئيسي للآلة الكاتبة الرقمية"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = None
        
        # تعيين معرف التطبيق
        self.set_application_id('com.digitaltypewriter.app')
    
    def do_activate(self):
        """تنشيط التطبيق وعرض النافذة الرئيسية"""
        if not self.window:
            # إنشاء النافذة الرئيسية إذا لم تكن موجودة
            self.window = DigitalTypewriterWindow(application=self)
            self.window.set_default_size(450, 200)
            self.window.set_title("Digital Typewriter - آلة كاتبة رقمية")
            
            # في GTK 4، نستخدم set_position من خلال إعدادات النافذة
            # أو نتركها تظهر في المنتصف بشكل افتراضي
        
        # عرض النافذة
        self.window.present()
        
        # إعطاء التركيز لمحرر النص
        self.window.focus_editor()
    
    def do_startup(self):
        """بدء التطبيق وتسجيل الإجراءات"""
        Adw.Application.do_startup(self)
        
        # تسجيل إجراء الخروج
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit)
        self.add_action(quit_action)
        
        # إضافة اختصارات لوحة المفاتيح - استخدام set_accels_for_action بدلاً من set_accelerators_for_action
        self.set_accels_for_action("app.quit", ["<Ctrl>q"])
    
    def on_quit(self, action, parameter):
        """معالجة إجراء الخروج"""
        self.quit()