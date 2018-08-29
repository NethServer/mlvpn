%define mlvpn_commit a06369fe7cb3395a13dca188fdb7b12b8edf1388
%define git_short %(echo "%{mlvpn_commit}" | cut -c1-8)

Name:              mlvpn
Version:           2.3.1.%{git_short}
Release:           1%{?dist}
Summary:           MLVPN fork
URL:               https://github.com/markfoodyburton/MLVPN
Source0:           https://github.com/markfoodyburton/MLVPN/archive/%{mlvpn_commit}.tar.gz
Patch100:          mlvpn-systemd.patch
Patch101:          mlvpn.conf.in.diff
Patch102:          mlvpn.inid.d-sysconfig.patch 
License:           GPLv2
BuildRequires:     systemd-devel
BuildRequires:     libsodium-devel >= 1.0
BuildRequires:     libev-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libpcap-devel
%{?systemd_requires}
BuildRequires:     systemd
BuildRequires:     systemd-units
Requires:          libsodium >= 1.0
Requires:          iproute
Requires(pre):     /usr/sbin/useradd
Requires(post):    systemd-sysv
Requires(post):    systemd-units
Requires(preun):   systemd-units
Requires(postun):  systemd-units

%description
MLVPN will do its best to achieve the following tasks:
Bond your internet links to increase bandwidth (unlimited)
Secure your internet connection by actively monitoring your links and removing the faulty ones, without loosing your TCP connections.
Secure your internet connection to the aggregation server using strong cryptography.
Scriptable automation and monitoring.

%prep
%setup -n MLVPN-%{mlvpn_commit}
%patch100 -p0
%patch101 -p1
%patch102 -p1

%build
./autogen.sh
%configure \
    --docdir=%{_pkgdocdir} \
%{__make}

%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT
mkdir -p -m 0750 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp doc/examples/mlvpn_updown.sh doc/examples/mlvpn.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -m 0710 -p $RPM_BUILD_ROOT%{_rundir}/mlvpn

install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -p -m 0644 doc/examples/systemd/mlvpn.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

%{__install} -d -m 0755 %{buildroot}/%{_datadir}/%{name}/

%clean
rm -rf %{buildroot}

%pre
getent group mlvpn &>/dev/null || groupadd -r mlvpn
getent passwd mlvpn &>/dev/null || \
    /usr/sbin/useradd -r -g mlvpn -s /sbin/nologin -c MLVPN \
        -d %{_rundir}/mlvpn mlvpn


%files
%{_pkgdocdir}
%{_mandir}/man1/%{name}.1*
%{_mandir}/man5/%{name}*.5*
%{_sbindir}/%{name}
%{_unitdir}/%{name}@.service
%{_unitdir}/%{name}.service
/usr/lib/systemd/system-generators/%{name}-generator
%{_tmpfilesdir}/%{name}.conf
%config %dir %{_sysconfdir}/%{name}/
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/mlvpn.conf
%attr(700,root,root) %config(noreplace) %{_sysconfdir}/%{name}/mlvpn_updown.sh
%attr(0775,root,mlvpn) %{_rundir}/mlvpn
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/mlvpn


%changelog
* Wed Aug 29 2018 Giacomo Sanchietti - 2.3.1-a06369fe
- Build of markfoodyburton fork, commit: a06369fe7cb3395a13dca188fdb7b12b8edf1388
- Based on a work of Luigi Iotti <luigi@iotti.biz>
