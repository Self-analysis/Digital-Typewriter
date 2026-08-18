#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Digital Typewriter - آلة كاتبة رقمية
نقطة الدخول الرئيسية للتطبيق
"""

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, GLib
from app import DigitalTypewriterApp

def main():
    """الدالة الرئيسية لتشغيل التطبيق"""
    app = DigitalTypewriterApp(
        application_id='com.digitaltypewriter.app',
        flags=Gio.ApplicationFlags.FLAGS_NONE
    )
    
    # تشغيل التطبيق
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)

if __name__ == '__main__':
    main()