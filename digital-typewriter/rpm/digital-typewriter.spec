Name:           digital-typewriter
Version:        1.0.0
Release:        1%{?dist}
Summary:        Digital typewriter with UK English and Arabic keyboard
License:        MIT
URL:            https://github.com/Self-analysis/Digital-Typewriter
BuildArch:      noarch

Requires:       python3
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita
Requires:       desktop-file-utils
Requires:       appstream

%description
Standalone GTK digital typewriter with a built-in UK English and Arabic keyboard and a multi-line text editor.

%prep

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_datadir}/digital-typewriter
install -d %{buildroot}%{_datadir}/applications
install -d %{buildroot}%{_datadir}/metainfo
install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -d %{buildroot}%{_bindir}

cp -a ../digital-typewriter/* %{buildroot}%{_datadir}/digital-typewriter/
rm -rf %{buildroot}%{_datadir}/digital-typewriter/rpm
install -m 0644 %{buildroot}%{_datadir}/digital-typewriter/digital-typewriter.desktop %{buildroot}%{_datadir}/applications/com.digitaltypewriter.app.desktop
install -m 0644 %{buildroot}%{_datadir}/digital-typewriter/com.digitaltypewriter.app.metainfo.xml %{buildroot}%{_datadir}/metainfo/com.digitaltypewriter.app.metainfo.xml
install -m 0644 %{buildroot}%{_datadir}/digital-typewriter/assets/icon.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/com.digitaltypewriter.app.svg
ln -s %{_datadir}/digital-typewriter/main.py %{buildroot}%{_bindir}/digital-typewriter

%check
python3 -m py_compile %{buildroot}%{_datadir}/digital-typewriter/*.py

desktop-file-validate %{buildroot}%{_datadir}/applications/com.digitaltypewriter.app.desktop

%files
%{_bindir}/digital-typewriter
%{_datadir}/digital-typewriter/
%{_datadir}/applications/com.digitaltypewriter.app.desktop
%{_datadir}/metainfo/com.digitaltypewriter.app.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/com.digitaltypewriter.app.svg

%post
update-desktop-database &> /dev/null || :
gtk-update-icon-cache -q -f %{_datadir}/icons/hicolor || :

%postun
update-desktop-database &> /dev/null || :
gtk-update-icon-cache -q -f %{_datadir}/icons/hicolor || :
