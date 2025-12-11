#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeappsver	25.12.0
%define		kfver		5.53.0
%define		qtver		5.15.2
%define		kaname		akonadi
Summary:	Akonadi - The PIM Storage Service
Summary(pl.UTF-8):	Akonadi - usługa przechowywania danych PIM
Name:		ka6-%{kaname}
Version:	25.12.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	ae4e30c61ad28a00c709a9145c2cf3ed
URL:		https://kde.org/
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
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-akonadi < 24
Conflicts:	akonadi-libs >= 1.0.0
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
Obsoletes:	ka5-akonadi-devel < 24

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%package apparmor
Summary:	Files for apparmor
Summary(pl.UTF-8):	Pliki dla apparmor
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description apparmor
Files for apparmor.

%description apparmor -l pl.UTF-8
Pliki dla apparmor.

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

#install -d $RPM_BUILD_ROOT%{_libdir}/qt6/plugins/pim5/kontact
#install -d $RPM_BUILD_ROOT%{_libdir}/qt6/plugins/pim5/kcms

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/akonadiagentconfigdialog
%attr(755,root,root) %{_bindir}/akonadi2xml
%attr(755,root,root) %{_bindir}/akonadi_agent_launcher
%attr(755,root,root) %{_bindir}/akonadi_agent_server
%attr(755,root,root) %{_bindir}/akonadi_control
%attr(755,root,root) %{_bindir}/akonadi_knut_resource
%attr(755,root,root) %{_bindir}/akonadi_rds
%attr(755,root,root) %{_bindir}/akonadictl
%attr(755,root,root) %{_bindir}/akonadiselftest
%attr(755,root,root) %{_bindir}/akonadiserver
%attr(755,root,root) %{_bindir}/akonaditest
%attr(755,root,root) %{_bindir}/asapcat
%attr(755,root,root) %{_bindir}/akonadi-db-migrator
%{_libdir}/libKPim6AkonadiAgentBase.so.*.*.*
%ghost %{_libdir}/libKPim6AkonadiAgentBase.so.6
%{_libdir}/libKPim6AkonadiCore.so.*.*.*
%ghost %{_libdir}/libKPim6AkonadiCore.so.6
%{_libdir}/libKPim6AkonadiPrivate.so.*.*.*
%ghost %{_libdir}/libKPim6AkonadiPrivate.so.6
%{_libdir}/libKPim6AkonadiWidgets.so.*.*.*
%ghost %{_libdir}/libKPim6AkonadiWidgets.so.6
%ghost %{_libdir}/libKPim6AkonadiAgentWidgetBase.so.6
%{_libdir}/libKPim6AkonadiAgentWidgetBase.so.*.*
%{_libdir}/libKPim6AkonadiXml.so.*.*.*
%ghost %{_libdir}/libKPim6AkonadiXml.so.6
%{_libdir}/qt6/plugins/designer/akonadi6widgets.so
%dir %{_libdir}/qt6/plugins/pim6
%dir %{_libdir}/qt6/plugins/pim6/akonadi
%{_libdir}/qt6/plugins/pim6/akonadi/akonadi_test_searchplugin.so
%dir %{_libdir}/qt6/plugins/pim6/akonadi/config
%{_libdir}/qt6/plugins/pim6/akonadi/config/knutconfig.so
%dir %{_libdir}/qt6/qml/org/kde/akonadi
%{_libdir}/qt6/qml/org/kde/akonadi/AgentConfigurationForm.qml
%{_libdir}/qt6/qml/org/kde/akonadi/CollectionChooserPage.qml
%{_libdir}/qt6/qml/org/kde/akonadi/CollectionComboBox.qml
%{_libdir}/qt6/qml/org/kde/akonadi/FormCollectionComboBox.qml
%{_libdir}/qt6/qml/org/kde/akonadi/TagManagerPage.qml
%{_libdir}/qt6/qml/org/kde/akonadi/akonadi_quick_plugin.qmltypes
%{_libdir}/qt6/qml/org/kde/akonadi/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/akonadi/libakonadi_quick_plugin.so
%{_libdir}/qt6/qml/org/kde/akonadi/qmldir
%dir /etc/xdg/akonadi
/etc/xdg/akonadi/mysql-global-mobile.conf
/etc/xdg/akonadi/mysql-global.conf
%{_desktopdir}/org.kde.akonadi.configdialog.desktop
%dir %{_datadir}/akonadi
%dir %{_datadir}/akonadi/agents
%{_datadir}/akonadi/agents/knutresource.desktop
%{_datadir}/config.kcfg/resourcebase.kcfg
%{_datadir}/dbus-1/interfaces/org.freedesktop.Akonadi.*.xml
%{_datadir}/dbus-1/services/org.freedesktop.Akonadi.Control.service
%dir %{_datadir}/kf6/akonadi
%{_datadir}/kf6/akonadi/akonadi-xml.xsd
%{_datadir}/kf6/akonadi/kcfg2dbus.xsl
%dir %{_datadir}/kf6/akonadi_knut_resource
%{_datadir}/kf6/akonadi_knut_resource/knut-template.xml
%{_datadir}/mime/packages/akonadi-mime.xml
%{_datadir}/qlogging-categories6/akonadi.categories
%{_datadir}/qlogging-categories6/akonadi.renamecategories
%{_iconsdir}/hicolor/128x128/apps/akonadi.png
%{_iconsdir}/hicolor/16x16/apps/akonadi.png
%{_iconsdir}/hicolor/22x22/apps/akonadi.png
%{_iconsdir}/hicolor/256x256/apps/akonadi.png
%{_iconsdir}/hicolor/32x32/apps/akonadi.png
%{_iconsdir}/hicolor/48x48/apps/akonadi.png
%{_iconsdir}/hicolor/64x64/apps/akonadi.png
%{_iconsdir}/hicolor/scalable/apps/akonadi.svgz

# TODO subpackage
%{_datadir}/kdevappwizard/templates/akonadiresource.tar.bz2
%{_datadir}/kdevappwizard/templates/akonadiserializer.tar.bz2

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKPim6AkonadiAgentBase.so
%{_libdir}/libKPim6AkonadiCore.so
%{_libdir}/libKPim6AkonadiPrivate.so
%{_libdir}/libKPim6AkonadiWidgets.so
%{_libdir}/libKPim6AkonadiAgentWidgetBase.so
%{_libdir}/libKPim6AkonadiXml.so
%dir %{_includedir}/KPim6
%{_includedir}/KPim6/Akonadi
%{_includedir}/KPim6/AkonadiAgentBase
%{_includedir}/KPim6/AkonadiCore
%{_includedir}/KPim6/AkonadiWidgets
%{_includedir}/KPim6/AkonadiAgentWidgetBase
%{_includedir}/KPim6/AkonadiXml
%{_libdir}/cmake/KPim6Akonadi

%files apparmor
%defattr(644,root,root,755)
/etc/apparmor.d/mariadbd_akonadi
/etc/apparmor.d/mysqld_akonadi
/etc/apparmor.d/postgresql_akonadi
/etc/apparmor.d%{_prefix}.bin.akonadiserver
