%undefine _debugsource_packages

Name:		nqp
Version:	2024.10
Release:	1
Summary:	Not Quite Perl (6)

Group:		Development/Perl
License:	Artistic 2.0 and ISC and WTFPL
URL:		https://github.com/perl6/nqp
Source0:	https://github.com/Raku/nqp/releases/download/%{version}/nqp-%{version}.tar.gz

BuildRequires:	readline-devel gmp-devel icu-devel
BuildRequires:	perl(Test::Harness)
BuildRequires:	pkgconfig(moar)
BuildRequires:	perl-devel

%description
This is "Not Quite Perl" -- a compiler for quickly generating PIR routines
from Perl6-like code. The key feature of NQP is that it's
designed to be a very small compiler (as compared with, say, perl6
or Rakudo) and is focused on being a high-level way to create
compilers and libraries for virtual machines (such as the Parrot
Virtual Machine). Unlike a full-fledged implementation of Perl 6,
NQP strives to have as small a run-time footprint as it can, while
still providing a Perl 6 object model and regular expression engine
for the virtual machine.


%prep
%autosetup -p1

%build
# FIXME js backend seems to require a different version of v8
# FIXME jvm backend fails to "make install" because of lacking DESTDIR support
%{__perl} Configure.pl --backends moar --prefix %{_prefix}
CFLAGS="$RPM_OPT_FLAGS -fPIC" make

%install
%make_install

%check
make test

%files
%{_bindir}/nqp
%{_bindir}/nqp-m
%{_datadir}/nqp/lib/*
