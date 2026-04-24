Name:           downtimed
Version:        1.0
Release:        1%{?dist}
Summary:        Downtime Monitoring Daemon
Source0:        https://github.com/snabb/downtimed/archive/version-%{version}/%{name}-%{version}.tar.gz
Source1:        downtimed.service
URL:            https://github.com/snabb/downtimed
License:        BSD-3-Clause
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
%if 0%{?rhel} == 7
BuildRequires:  systemd
%else
BuildRequires:  systemd-rpm-macros
%endif
%{?systemd_requires}

%description
downtimed is a program that monitors operating system downtime, uptime,
shutdowns, and crashes and records any findings either to the system log or to
a separately specified log file. At OS startup it logs information about
previous downtime. It then periodically updates a time stamp file on the disk,
which is used to determine the approximate time when the system was last up and
running. During a graceful system shutdown, it records a time stamp in another
file.

%prep
%setup -q -n %{name}-version-%{version}

%build
%configure
%make_build

%install
%make_install

mkdir -p %{buildroot}/%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}/downtimed.service
install -d %{buildroot}%{_sharedstatedir}/downtimed
touch %{buildroot}%{_sharedstatedir}/downtimed/downtimedb

%post
%systemd_post %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%preun
%systemd_preun %{name}.service

%files
%license LICENSE
%doc NEWS README
%{_bindir}/downtime*
%{_sbindir}/downtime*
%{_unitdir}/downtimed.service
%{_mandir}/man1/downtime*.1*
%{_mandir}/man8/downtime*.8*
%ghost %{_sharedstatedir}/downtimed/downtimedb
%dir %{_sharedstatedir}/downtimed

%changelog
* Fri Apr 24 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.0-1
- Modernize spec for EL10
- Remove deprecated BuildRoot, Group, %clean, %defattr
- Use systemd-rpm-macros
- Use downloadable GitHub Source0 URL

* Wed Feb 14 2018 Casjays Developments <admin@build.casjaysdev.pro> - 0.4
- Rebuild for CentOS 7
