%global debug_package %{nil}

Name:           nunit
Version:        2.6.4
Release:        2
Summary:        Unit test framework for CLI
License:        MIT with advertising
Group:          Development/C
Url:            http://www.nunit.org/
Source0:        https://github.com/nunit/nunit/archive/%{name}v2-%{version}.tar.gz
Source1:        nunit.pc
Source2:        nunit-gui.sh
Source3:        nunit-console.sh
Source4:        nunit.desktop
BuildRequires:  mono-devel libgdiplus-devel desktop-file-utils
Provides:       mono-nunit = 4.0.2-5
Obsoletes:      mono-nunit < 4.0.2-6
Obsoletes:      nunit-runner

%description
NUnit is a unit testing framework for all .NET languages. It serves the
same purpose as JUnit does in the Java world. It supports test
categories, testing for exceptions and writing test results in plain
text or XML.

NUnit targets the CLI (Common Language Infrastructure) and supports Mono and
the Microsoft .NET Framework.

%package gui
Summary:        Tools for run NUnit test
Requires:       %{name} = %{version}-%{release}

%description gui
Desktop application for run NUnit test

%package doc
Summary:        Documentation package for NUnit
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for NUnit

%package        devel
Summary:        Development files for NUnit
Group:          Development/C
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Provides:       mono-nunit-devel = 4.0.2-5
Obsoletes:      mono-nunit-devel < 4.0.2-6

%description devel
Development files for %{name}.

%prep
%setup -qn nunitv2-%{version}

%build

# fix compile with Mono4
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

%{?exp_env}
%{?env_options}
xbuild /property:Configuration=Debug ./src/NUnitCore/core/nunit.core.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitCore/interfaces/nunit.core.interfaces.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitFramework/framework/nunit.framework.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitMocks/mocks/nunit.mocks.csproj
xbuild /property:Configuration=Debug ./src/ClientUtilities/util/nunit.util.dll.csproj
xbuild /property:Configuration=Debug ./src/ConsoleRunner/nunit-console/nunit-console.csproj
xbuild /property:Configuration=Debug ./src/ConsoleRunner/nunit-console-exe/nunit-console.exe.csproj
xbuild /property:Configuration=Debug ./src/GuiRunner/nunit-gui/nunit-gui.csproj
xbuild /property:Configuration=Debug ./src/GuiComponents/UiKit/nunit.uikit.dll.csproj
xbuild /property:Configuration=Debug ./src/GuiException/UiException/nunit.uiexception.dll.csproj
xbuild /property:Configuration=Debug ./src/GuiRunner/nunit-gui-exe/nunit-gui.exe.csproj

%install
%{?env_options}
%{__mkdir_p} %{buildroot}%{_prefix}/lib/mono/nunit
%{__mkdir_p} %{buildroot}%{_libdir}/pkgconfig
%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{__mkdir_p} %{buildroot}%{_datadir}/icons/NUnit
%{__install} -m0644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/
%{__install} -m0755 %{SOURCE2} %{buildroot}%{_bindir}/`basename -s .sh %{SOURCE2}`26
%{__install} -m0755 %{SOURCE3} %{buildroot}%{_bindir}/`basename -s .sh %{SOURCE3}`26
%{__install} -m0644 src/ConsoleRunner/nunit-console-exe/App.config %{buildroot}%{_prefix}/lib/mono/nunit/nunit-console.exe.config
%{__install} -m0644 src/GuiRunner/nunit-gui-exe/App.config %{buildroot}%{_prefix}/lib/mono/nunit/nunit.exe.config
find %{_builddir}/%{?buildsubdir}/bin -name \*.dll -exec %{__install} \-m0755 "{}" "%{buildroot}%{_prefix}/lib/mono/nunit/" \;
find %{_builddir}/%{?buildsubdir}/bin -name \*.exe -exec %{__install} \-m0755 "{}" "%{buildroot}%{_prefix}/lib/mono/nunit/" \;
for i in nunit-console-runner.dll nunit.core.dll nunit.core.interfaces.dll nunit.framework.dll nunit.mocks.dll nunit.util.dll ; do
    gacutil -i %{buildroot}%{_prefix}/lib/mono/nunit/$i -package nunit -root %{buildroot}%{_prefix}/lib/mono/../
done
desktop-file-install --dir=%{buildroot}/%{_datadir}/applications %{SOURCE4}
cp src/GuiRunner/nunit-gui-exe/App.ico %{buildroot}/%{_datadir}/icons/NUnit/nunit.ico

%files
%doc license.txt
%{_bindir}/nunit-console*
%{_prefix}/lib/mono/nunit/nunit-console.exe*
%{_prefix}/lib/mono/gac/nunit*
%{_prefix}/lib/mono/nunit/*.dll

%files gui
%{_bindir}/nunit-gui*
%{_prefix}/lib/mono/nunit/nunit.exe*
%{_datadir}/applications/nunit.desktop
%{_datadir}/icons/NUnit

%files doc
%doc doc/license.html
%doc doc/*

%files devel
%{_libdir}/pkgconfig/nunit.pc

%post gui
/bin/touch --no-create %{_datadir}/icons/NUnit &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun gui
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/NUnit &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/NUnit &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans gui
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/NUnit &>/dev/null || :

