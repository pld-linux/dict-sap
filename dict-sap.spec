Summary:	sap - English-Polish and vice versa dictionary for dictd
Name:		dict-sap
Version:	0.1b_0.1
Release:	1
License:	GPL
Group:		Applications/Dictionaries
Group(pl):	Aplikacje/S³owniki
Source:		%{name}-%{version}.tar.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	/usr/bin/dictzip
BuildRequires:	/usr/bin/perl
Requires:	dictd
Requires:	%{_sysconfdir}/dictd
BuildArch:	noarch

%description 
This package contains sap - English-Polish and Polish-English
dictionary version 0.1b, formatted for use by the DICT server.

%prep
%setup -q

%build
%configure 
%{__make} db 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/dictd/,%{_bindir},%{_sysconfdir}/dictd}
%{__make} install DESTDIR=$RPM_BUILD_ROOT

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

%postun
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2 || true
fi

%post
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dictd/*.dictconf
%attr(755,root,root) %{_bindir}/sapdict
%{_datadir}/dictd/sap_*
