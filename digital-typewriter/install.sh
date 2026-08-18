#!/bin/bash

# Digital Typewriter - سكريبت التثبيت
# يعمل على Fedora 44

set -e

echo "========================================"
echo "  Digital Typewriter - آلة كاتبة رقمية"
echo "========================================"
echo

# الألوان للعرض
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# دالة لعرض الرسائل
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}▶ $1${NC}"
}

# الحصول على اسم المستخدم
USER_NAME=$(whoami)
USER_HOME=$(eval echo ~$USER_NAME)

# التحقق من وجود Fedora
if ! grep -q "Fedora" /etc/os-release; then
    print_error "هذا السكريبت مصمم لـ Fedora فقط"
    exit 1
fi

print_info "تثبيت المتطلبات الأساسية..."

# تثبيت الحزم المطلوبة
sudo dnf install -y python3 python3-pip python3-gobject gtk4 libadwaita gtk4-devel

if [ $? -ne 0 ]; then
    print_error "فشل تثبيت المتطلبات الأساسية"
    exit 1
fi

print_success "تم تثبيت المتطلبات الأساسية"

print_info "تثبيت متطلبات Python..."

# تثبيت متطلبات Python
pip3 install --user pygobject

if [ $? -ne 0 ]; then
    print_error "فشل تثبيت متطلبات Python"
    exit 1
fi

print_success "تم تثبيت متطلبات Python"

# إنشاء مجلد التطبيق
APP_DIR="$HOME/.local/share/digital-typewriter"
mkdir -p "$APP_DIR"
mkdir -p "$APP_DIR/assets"
mkdir -p "$APP_DIR/ui"
mkdir -p "$APP_DIR/layouts"

print_info "نسخ ملفات التطبيق..."

# نسخ الملفات الرئيسية
cp -f main.py "$APP_DIR/"
cp -f app.py "$APP_DIR/"
cp -f editor.py "$APP_DIR/"
cp -f keyboard.py "$APP_DIR/"

# نسخ المجلدات
cp -rf ui/* "$APP_DIR/ui/" 2>/dev/null || true
cp -rf layouts/* "$APP_DIR/layouts/" 2>/dev/null || true
cp -rf assets/* "$APP_DIR/assets/" 2>/dev/null || true

# جعل main.py قابل للتنفيذ
chmod +x "$APP_DIR/main.py"

print_success "تم نسخ ملفات التطبيق"

# تثبيت Desktop Entry
print_info "تثبيت Desktop Entry..."

DESKTOP_FILE="$HOME/.local/share/applications/digital-typewriter.desktop"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Digital Typewriter
Name[ar]=الآلة الكاتبة الرقمية
Comment=آلة كاتبة رقمية مستقلة تدعم العربية والإنجليزية
Comment[ar]=آلة كاتبة رقمية مستقلة تدعم العربية والإنجليزية
Exec=/usr/bin/python3 $APP_DIR/main.py
Icon=$APP_DIR/assets/icon.svg
Terminal=false
Categories=Office;Utility;TextEditor;
Keywords=typewriter;keyboard;arabic;english;
StartupWMClass=digital-typewriter
StartupNotify=true
EOF

# تحديث قاعدة بيانات Desktop
update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true

print_success "تم تثبيت Desktop Entry"

# إنشاء رابط رمزي للتشغيل من الطرفية
print_info "إنشاء رابط للتشغيل من الطرفية..."

mkdir -p "$HOME/.local/bin"
ln -sf "$APP_DIR/main.py" "$HOME/.local/bin/digital-typewriter"
chmod +x "$HOME/.local/bin/digital-typewriter"

# إضافة المسار إلى PATH إذا لم يكن موجوداً
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bash_profile" 2>/dev/null || true
fi

print_success "تم إنشاء الرابط"

echo
echo "========================================"
echo -e "${GREEN}تم تثبيت Digital Typewriter بنجاح!${NC}"
echo "========================================"
echo
echo "يمكنك تشغيل التطبيق بعدة طرق:"
echo "  1. من قائمة التطبيقات: ابحث عن Digital Typewriter"
echo "  2. من الطرفية: digital-typewriter"
echo "  3. من مجلد التطبيق: python3 $APP_DIR/main.py"
echo
echo "لبدء الكتابة، استخدم لوحة المفاتيح الرقمية"
echo "في أسفل نافذة التطبيق."
echo