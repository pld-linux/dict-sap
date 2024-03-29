Summary:	sap - English-Polish and vice versa dictionary for dictd
Summary(pl.UTF-8):	sap - słownik angielsko-polski i odwrotnie dla dictd
Name:		dict-sap
Version:	0.1b_0.1
Release:	5
License:	GPL
Group:		Applications/Dictionaries
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	7d53db1c78a0662d1ebb10b0912caa9a
Patch0:		%{name}-gcc.patch
URL:		http://www.dict.org/
BuildRequires:	%{_bindir}/perl
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dictzip
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	%{_sysconfdir}/dictd
Requires:	dict
Requires:	dictd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains sap - English-Polish and Polish-English
dictionary version 0.1b, formatted for use by the DICT server.

%description -l pl.UTF-8
Ten pakiet zawiera sap - słownik angielsko-polski i polsko-angielski
sformatowane do użycia z serwerem słownika dictd.

%prep
%setup -q
%patch0 -p1

%build
%{__autoconf}
cp -f /usr/share/automake/install-sh .
cp -f /usr/share/automake/config.sub .
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
%service -q dictd restart

%postun
if [ "$1" = 0 ]; then
	%service -q dictd restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dictd/sap_*.dictconf
%attr(755,root,root) %{_bindir}/sapdict
%{_datadir}/dictd/sap_*
