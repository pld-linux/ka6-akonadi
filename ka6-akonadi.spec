#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.08.1
%define		kfver		5.53.0
%define		qtver		5.15.2
%define		kaname		akonadi
Summary:	Akonadi - The PIM Storage Service
Name:		ka6-%{kaname}
Version:	24.08.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	9927b5f043eae41ed45b1336d3510afb
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Designer-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6Sql-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6UiTools-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	Qt6Xml-devel >= %{qtver}
BuildRequires:	boost-devel >= 1.34.0
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	ka6-kaccounts-integration-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kfver}
BuildRequires:	kf6-kcompletion-devel >= %{kfver}
BuildRequires:	kf6-kconfig-devel >= %{kfver}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kfver}
BuildRequires:	kf6-kcoreaddons-devel >= %{kfver}
BuildRequires:	kf6-kcrash-devel >= %{kfver}
BuildRequires:	kf6-kdbusaddons-devel >= %{kfver}
BuildRequires:	kf6-ki18n-devel >= %{kfver}
BuildRequires:	kf6-kiconthemes-devel >= %{kfver}
BuildRequires:	kf6-kio-devel >= %{kfver}
BuildRequires:	kf6-kitemmodels-devel >= %{kfver}
BuildRequires:	kf6-kitemviews-devel >= %{kfver}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kfver}
BuildRequires:	kf6-kwindowsystem-devel >= %{kfver}
BuildRequires:	kf6-kxmlgui-devel >= %{kfver}
BuildRequires:	libaccounts-qt6-devel >= 1.16
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Conflicts:	akonadi-libs >= 1.0.0
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Akonadi is a personal information management (PIM) framework for KDE
Akonadi will function as an extensible data storage for all PIM
applications.

Besides data storage, Akonadi has several other components including
search, and a library (cache) for easy access and notification of data
changes.

%description -l pl.UTF-8
Akonadi jest szkieletem zarządzania informacjami osobistymi (PIM) dla
KDE. Będzie on funkcjonował jako rozszerzalny magazyn danych dla
wszystkich aplikacji PIM.

Oprócz magazynu danych, Akonadi ma wiele innych komponentów, między
innymi przeszukiwanie i bibliotekę (buforowanie) dla łatwego dostępu i
powiadomieniach o zmianach danych.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%package apparmor
Summary:	Files for apparmor
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description apparmor
Files for apparmor.


%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build
#install -d $RPM_BUILD_ROOT%{_includedir}/KF6/Akonadi
#install -d $RPM_BUILD_ROOT%{_libdir}/qt6/plugins/pim5/kontact
#install -d $RPM_BUILD_ROOT%{_libdir}/qt6/plugins/pim5/kcms
install -d $RPM_BUILD_ROOT%{_libdir}/qt6/qml/org/kde/akonadi

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/akonadi_agent_launcher
%attr(755,root,root) %{_bindir}/akonadi_agent_server
%attr(755,root,root) %{_bindir}/akonadi_control
%attr(755,root,root) %{_bindir}/akonadi_rds
%attr(755,root,root) %{_bindir}/akonadictl
%attr(755,root,root) %{_bindir}/akonadiserver
%attr(755,root,root) %{_bindir}/asapcat
%attr(755,root,root) %{_bindir}/akonadi-db-migrator
%dir /etc/xdg/akonadi
/etc/xdg/akonadi/mysql-global-mobile.conf
/etc/xdg/akonadi/mysql-global.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.Akonadi.*.xml
%{_datadir}/dbus-1/services/org.freedesktop.Akonadi.Control.service
%{_datadir}/mime/packages/akonadi-mime.xml
%attr(755,root,root) %{_bindir}/akonadi2xml
%attr(755,root,root) %{_bindir}/akonadi_knut_resource
%attr(755,root,root) %{_bindir}/akonadiselftest
%attr(755,root,root) %{_bindir}/akonaditest
%dir %{_datadir}/akonadi
%dir %{_datadir}/akonadi/agents
%{_datadir}/akonadi/agents/knutresource.desktop
%{_datadir}/config.kcfg/resourcebase.kcfg
%{_iconsdir}/hicolor/128x128/apps/akonadi.png
%{_iconsdir}/hicolor/16x16/apps/akonadi.png
%{_iconsdir}/hicolor/22x22/apps/akonadi.png
%{_iconsdir}/hicolor/256x256/apps/akonadi.png
%{_iconsdir}/hicolor/32x32/apps/akonadi.png
%{_iconsdir}/hicolor/48x48/apps/akonadi.png
%{_iconsdir}/hicolor/64x64/apps/akonadi.png
%{_iconsdir}/hicolor/scalable/apps/akonadi.svgz
%dir %{_libdir}/qt6/qml/org/kde/akonadi
%attr(755,root,root) %{_libdir}/libKPim6AkonadiAgentBase.so.*.*
%ghost %{_libdir}/libKPim6AkonadiAgentBase.so.6
%attr(755,root,root) %{_libdir}/libKPim6AkonadiCore.so.*.*
%ghost %{_libdir}/libKPim6AkonadiCore.so.6
%attr(755,root,root) %{_libdir}/libKPim6AkonadiPrivate.so.*.*
%ghost %{_libdir}/libKPim6AkonadiPrivate.so.6
%attr(755,root,root) %{_libdir}/libKPim6AkonadiWidgets.so.*.*
%ghost %{_libdir}/libKPim6AkonadiWidgets.so.6
%attr(755,root,root) %{_libdir}/libKPim6AkonadiXml.so.*.*
%ghost %{_libdir}/libKPim6AkonadiXml.so.6
%attr(755,root,root) %{_libdir}/qt6/plugins/designer/akonadi6widgets.so
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/akonadi/akonadi_test_searchplugin.so
%{_datadir}/kf6/akonadi/akonadi-xml.xsd
%{_datadir}/kf6/akonadi/kcfg2dbus.xsl
%{_datadir}/kf6/akonadi_knut_resource/knut-template.xml
%{_datadir}/qlogging-categories6/akonadi.categories
%{_datadir}/qlogging-categories6/akonadi.renamecategories

# TODO subpackage
%{_datadir}/kdevappwizard/templates/akonadiresource.tar.bz2
%{_datadir}/kdevappwizard/templates/akonadiserializer.tar.bz2

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/KPim6
%{_includedir}/KPim6/Akonadi
%{_includedir}/KPim6/AkonadiAgentBase
%{_includedir}/KPim6/AkonadiCore
%{_includedir}/KPim6/AkonadiWidgets
%{_includedir}/KPim6/AkonadiXml
%{_libdir}/cmake/KPim6Akonadi
%{_libdir}/libKPim6AkonadiAgentBase.so
%{_libdir}/libKPim6AkonadiCore.so
%{_libdir}/libKPim6AkonadiPrivate.so
%{_libdir}/libKPim6AkonadiWidgets.so
%{_libdir}/libKPim6AkonadiXml.so


%files apparmor
%defattr(644,root,root,755)
/etc/apparmor.d/mariadbd_akonadi
/etc/apparmor.d/mysqld_akonadi
/etc/apparmor.d/postgresql_akonadi
/etc/apparmor.d%{_prefix}.bin.akonadiserver

