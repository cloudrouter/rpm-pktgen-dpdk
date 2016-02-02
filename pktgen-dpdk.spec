Name:		pktgen-dpdk
Version:	2.9.8
Release:	1%{?dist}
Summary:	Traffic generator utilizing DPDK

Group:		Applications/Internet
License:	BSD
URL:		http://dpdk.org/browse/apps/pktgen-dpdk/refs/
Source0:	http://dpdk.org/browse/apps/pktgen-dpdk/snapshot/pktgen-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:	dpdk-devel >= 1.8.0
BuildRequires:	libpcap-devel zlib-devel
BuildConflicts: lua-devel

# The tarball contains two bundled 'n hacked up Lua versions, sigh.
# There are at least two additions to upstream: lua_shell and lua-socket
# so a simple rm -rf of the directory wont cut it. Needs to be
# unbundled or exception requested.
# This is the one that gets built and statically linked in the binary:
Provides:	bundled(lua) = 5.3.0

%description
%{summary}

%prep
%setup -q -n pktgen-%{version}

%build
unset RTE_SDK
unset RTE_TARGET
. /etc/profile.d/dpdk-sdk-%{_arch}.sh

# Hack up Lua library path to our private libdir
lua="lua-5.3.0"
sed -ie 's:/usr/local:%{_libdir}:g' lib/${lua}/src/luaconf.h
sed -ie 's:share/lua/.*:/%{name}/":g' lib/${lua}/src/luaconf.h
sed -ie 's:lib/lua/.*:/%{name}/":g' lib/${lua}/src/luaconf.h

# Doesn't build with the default -Werror, sigh...
export EXTRA_CFLAGS="%{optflags} -Wno-error"

# Parallel build doesn't work
# Work around DPDK makefiles, we're not building shared libraries here
# make V=1 %{?_smp_mflags}
make V=1 CONFIG_RTE_BUILD_SHARED_LIB=n

%install
# No working "install" target, lets do it manually (sigh)
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/%{name}
. /etc/profile.d/dpdk-sdk-%{_arch}.sh
install -m 755 app/app/${RTE_TARGET}/pktgen %{buildroot}%{_bindir}/pktgen
for f in Pktgen.lua PktgenGUI.lua; do
   install -m 644 ${f} %{buildroot}%{_libdir}/%{name}/${f}
done

%files
%license LICENSE Pktgen_3rdPartyNotices_v1.0.pdf
%doc README.md
%doc pcap themes doit.sh test
%{_bindir}/pktgen
%{_libdir}/%{name}

%changelog
* Mon Feb 01 2016 Jay Turner <jkt@iix.net> - 2.9.8-1
- Update to 2.9.8
- Initial build for CloudRouter Project

* Wed Dec 16 2015 Panu Matilainen <pmatilai@redhat.com> - 2.9.7-1
- Update to 2.9.7
- Build conflicts with lua-devel, sigh

* Mon Sep 28 2015 Panu Matilainen <pmatilai@redhat.com> - 2.9.2-2
- Rebuild for dpdk changes
- Buildrequires zlib-devel (static linking brokenness carried over
  to shared libraries, sigh)

* Mon Sep 28 2015 Panu Matilainen <pmatilai@redhat.com> - 2.9.2-1
- Update to 2.9.2
- Drop bogus fuse-devel buildreq

* Fri Mar 27 2015 Panu Matilainen <pmatilai@redhat.com> - 2.8.4-1
- Update to 2.8.4

* Mon Mar 02 2015 Panu Matilainen <pmatilai@redhat.com> - 2.8.3-1
- Update to 2.8.3
- Use rpm optflags for building

* Fri Feb 27 2015 Panu Matilainen <pmatilai@redhat.com> - 2.8.0-6
- Rebuild

* Tue Feb 17 2015 Panu Matilainen <pmatilai@redhat.com> - 2.8.0-5
- Add some missing Lua bits and pieces
- Workaround DPDK linking madness by buildrequiring fuse-devel

* Thu Feb 05 2015 Panu Matilainen <pmatilai@redhat.com> - 2.8.0-4
- Another rebuild for versioning change

* Thu Feb 05 2015 Panu Matilainen <pmatilai@redhat.com> - 2.8.0-3
- Another rebuild for versioning change

* Tue Feb 03 2015 Panu Matilainen <pmatilai@redhat.com> - 2.8.0-2
- Rebuild with library versioned dpdk
- Ensure RTE_SDK from dpdk-devel gets used

* Fri Jan 30 2015 Panu Matilainen <pmatilai@redhat.com> - 2.8.0-1
- Initial packaging

