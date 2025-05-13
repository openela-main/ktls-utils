%global forgeurl https://github.com/oracle/ktls-utils
%global baseversion 0.11

Name:           ktls-utils
Version:        %{baseversion}
Release:        3%{?dist}
Summary:        TLS handshake agent for kernel sockets

%forgemeta

License:        GPL-2.0-only AND (GPL-2.0-only OR BSD-3-Clause)
URL:            %{forgeurl}

# FIXME: is this a bug in the tagging scheme or forgesource macro?
Source0:        %{forgeurl}/releases/download/%{name}-%{baseversion}/%{name}-%{baseversion}.tar.gz

#
# RHEL-9.6
#
Patch001: ktls-utils-0.11-nvme-default-keyring.patch
Patch002: ktls-utils-0.11-tlshd-Pass-ETIMEDOUT-from-gnutls-to-kernel.patch

BuildRequires:  bash systemd-rpm-macros
BuildRequires:  gcc make coreutils
BuildRequires:  pkgconfig(gnutls) >= 3.3.0
BuildRequires:  autoconf >= 2.69
BuildRequires:  automake
BuildRequires:  pkgconfig(libkeyutils)
BuildRequires:  pkgconfig(glib-2.0) >= 2.6
BuildRequires:  pkgconfig(libnl-3.0) >= 3.1

%description
In-kernel TLS consumers need a mechanism to perform TLS handshakes
on a connected socket to negotiate TLS session parameters that can
then be programmed into the kernel's TLS record protocol engine.

This package of software provides a TLS handshake user agent that
listens for kernel requests and then materializes a user space
socket endpoint on which to perform these handshakes. The resulting
negotiated session parameters are passed back to the kernel via
standard kTLS socket options.

%prep
%setup -q -n %{name}-%{baseversion}
%autopatch -p1

%build
./autogen.sh
%configure --with-systemd
%make_build

%install
%make_install

%files
%config(noreplace) %{_sysconfdir}/tlshd.conf
%{_sbindir}/tlshd
%{_mandir}/man5/tlshd.conf.5.gz
%{_mandir}/man8/tlshd.8.gz
%{_unitdir}/tlshd.service
%license COPYING
%doc README.md
%doc SECURITY.md

%post
%systemd_post tlshd.service

%preun
%systemd_preun tlshd.service

%postun
%systemd_postun_with_restart tlshd.service

%changelog
* Mon Mar 03 2025 Scott Mayhew <smayhew@redhat.com> 0.11-3
- tlshd: Pass ETIMEDOUT from gnutls to kernel

* Wed Feb 12 2025 Scott Mayhew <smayhew@redhat.com> 0.11-2
- Bump release to satisfy the errata automation

* Tue Feb 04 2025 Steve Dickson <steved@redhat.com> 0.11-1
- tlshd: link .nvme default keyring into the session (RHEL-71505)

* Mon Jun 17 2024 Steve Dickson <steved@redhat.com> 0.11-0
- Release ktls-utils 0.11 (RHEL-39442)

* Thu Feb 29 2024 Steve Dickson <steved@redhat.com> 0.10-0
- Initial package
- Upstream contributions by:
    - Chuck Lever <chuck.lever@oracle.com>
    - Hannes Reinecke <hare@suse.de>
    - Jeff Layton <jlayton@kernel.org>
    - Benjamin Coddington <bcodding@redhat.com>
    - David Härdeman <david@hardeman.nu>
    - Tigran Mkrtchyan <tigran.mkrtchyan@desy.de>
    - Moritz "WanzenBug" Wanzenböck <moritz.wanzenboeck@linbit.com>
