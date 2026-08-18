#!/bin/bash

# Digital Typewriter - سكريبت الإزالة

echo "========================================"
echo "  إزالة Digital Typewriter"
echo "========================================"
echo

# الألوان
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}▶ $1${NC}"
}

# تأكيد الإزالة
read -p "هل أنت متأكد أنك تريد إزالة Digital Typewriter؟ (y/N): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "تم الإلغاء."
    exit 0
fi

print_info "جاري إزالة Digital Typewriter..."

# إزالة Desktop Entry
print_info "إزالة Desktop Entry..."
rm -f ~/.local/share/applications/digital-typewriter.desktop
update-desktop-database ~/.local/share/applications/ 2>/dev/null || true
print_success "تم إزالة Desktop Entry"

# إزالة الرابط من PATH
print_info "إزالة الرابط..."
rm -f ~/.local/bin/digital-typewriter
print_success "تم إزالة الرابط"

# إزالة مجلد التطبيق
print_info "إزالة ملفات التطبيق..."
rm -rf ~/.local/share/digital-typewriter
print_success "تم إزالة ملفات التطبيق"

# إزالة الملفات المؤقتة
print_info "إزالة الملفات المؤقتة..."
rm -rf ~/.cache/digital-typewriter
rm -rf ~/.config/digital-typewriter
print_success "تم إزالة الملفات المؤقتة"

echo
echo "========================================"
echo -e "${GREEN}✅ تم إزالة Digital Typewriter بنجاح!${NC}"
echo "========================================"
echo
echo "إذا كنت تريد إزالة المتطلبات أيضاً:"
echo "  sudo dnf remove python3-gobject gtk4 libadwaita"
echo