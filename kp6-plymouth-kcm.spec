#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.2.3
%define		qtver		5.15.2
%define		kpname		plymouth-kcm

Summary:	KDE Config Module for Plyouth
Name:		kp6-%{kpname}
Version:	6.2.3
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	80b6397d3e154f00266baefeb17967af
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= 5.15.0
BuildRequires:	Qt6Gui-devel >= 5.15.0
BuildRequires:	Qt6Network-devel >= 5.15.0
BuildRequires:	Qt6Qml-devel >= 5.15.2
BuildRequires:	Qt6Quick-devel >= 5.15.0
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= 5.82
BuildRequires:	kf6-karchive-devel >= 5.82
BuildRequires:	kf6-kconfig-devel >= 5.82
BuildRequires:	kf6-kdeclarative-devel >= 5.82
BuildRequires:	kf6-ki18n-devel >= 5.82
BuildRequires:	kf6-kio-devel >= 5.82
BuildRequires:	kf6-knewstuff-devel >= 5.82
BuildRequires:	ninja
BuildRequires:	plymouth-devel
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
Obsoletes:	kp5-%{kpname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KDE Config Module for Plymouth.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kplymouththemeinstaller
%{_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmplymouth.service
%{_datadir}/dbus-1/system.d/org.kde.kcontrol.kcmplymouth.conf
%{_datadir}/knsrcfiles/plymouth.knsrc
%{_datadir}/polkit-1/actions/org.kde.kcontrol.kcmplymouth.policy
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_plymouth.so
%{_desktopdir}/kcm_plymouth.desktop
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/plymouthhelper
