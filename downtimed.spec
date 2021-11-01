Name:           downtimed
Version:        1.0
Release:        0.2%{?dist}
Summary:        Downtime Monitoring Daemon
# http://dist.epipe.com/downtimed/downtimed-%{version}.tar.gz
Source:         downtimed-%{version}.tar.gz
Source1:        downtimed.service
URL:            http://dist.epipe.com/downtimed/
Group:          System/Monitoring
License:        BSD3c
BuildRoot:      %{_tmppath}/build-%{name}-%{version}
BuildRequires:  gcc make glibc-devel
BuildRequires:  autoconf automake libtool systemd
BuildRequires:  systemd-units
BuildRequires:  autoconf, automake, libtool
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
downtimed is a program that monitors operating system downtime, uptime,
shutdowns, and crashes and records any findings either to the system log or to
a separately specified log file. At OS startup it logs information about
previous downtime. It then periodically updates a time stamp file on the disk,
which is used to determine the approximate time when the system was last up and
running. During a graceful system shutdown, it records a time stamp in another
file.

%prep
%setup -q

%build
%configure
%__make %{?jobs:-j%{jobs}}

%install
%__rm -rf "$RPM_BUILD_ROOT"
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
%__install -d "$RPM_BUILD_ROOT%_sharedstatedir/downtimed"
cp -Rfv "%{SOURCE1}" "$RPM_BUILD_ROOT/%{_unitdir}/downtimed.service"
touch "$RPM_BUILD_ROOT%_sharedstatedir/downtimed/downtimedb"
%__install -d "$RPM_BUILD_ROOT%{_sbindir}"


%clean
%__rm -rf "$RPM_BUILD_ROOT"

%post
/sbin/ldconfig
%systemd_post %{name}.service
systemctl enable %{name}.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%preun
/sbin/ldconfig
%systemd_preun %{name}.service

%files
%defattr(-,root,root)
#%doc LICENSE NEWS README
%_bindir/downtime*
%_sbindir/downtime*
%{_unitdir}/downtimed.service
%_mandir/man1/downtime*.1.gz
%_mandir/man8/downtime*.8.gz
%_sharedstatedir/downtimed/downtimedb
%dir %_sharedstatedir/downtimed

%changelog
* Wed Feb 14 2018 Casjays Developments <admin@build.casjaysdev.com> - 0.4
- Rebuild for CentOS 7

