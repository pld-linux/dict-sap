Summary:	sap - English-Polish and vice versa dictionary for dictd
Summary(pl):	sap - s³ownik angielsko-polski i odwrotnie dla dictd
Name:		dict-sap
Version:	0.1b_0.1
Release:	3
License:	GPL
Group:		Applications/Dictionaries
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	7d53db1c78a0662d1ebb10b0912caa9a
URL:		http://www.dict.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dictzip
BuildRequires:	%{_bindir}/perl
Requires:	dictd
Requires:	%{_sysconfdir}/dictd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains sap - English-Polish and Polish-English
dictionary version 0.1b, formatted for use by the DICT server.

%description -l pl
Ten pakiet zawiera sap - s³ownik angielsko-polski i polsko-angielski
sformatowane do u¿ycia z serwerem s³ownika dictd.

%prep
%setup -q

%build
%{__autoconf}
cp -f %{_datadir}/automake/install-sh .
cp -f %{_datadir}/automake/config.sub .
%configure
%{__make} db

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/dictd,%{_sysconfdir}/dictd,%{_bindir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

for dictname in sap_en-pl sap_pl-en; do
	dictprefix=%{_datadir}/dictd/$dictname
	echo "# sap dictionary, part $dictname
database $dictname {
	data  \"$dictprefix.dict.dz\"
	index \"$dictprefix.index\"
}" > $RPM_BUILD_ROOT%{_sysconfdir}/dictd/$dictname.dictconf
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2
fi

%postun
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2 || true
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dictd/sap_*.dictconf
%attr(755,root,root) %{_bindir}/sapdict
%{_datadir}/dictd/sap_*
