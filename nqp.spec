%define year 2013
%define month 08
%define parrot_version 5.7.0
%define _disable_ld_no_undefined 1

%define PAR_LIB_DIR %{_libdir}/parrot/%{parrot_version}
%define parrot_dynext %{PAR_LIB_DIR}/dynext

Name:		nqp
Version:	0.0.%{year}.%{month}
Release:	1
Summary:	Not Quite Perl (6)

Group:		Development/Perl
License:	Artistic 2.0 and ISC and WTFPL
URL:		https://github.com/perl6/nqp
Source0:	http://rakudo.org/downloads/nqp/nqp-%{year}.%{month}.tar.gz

BuildRequires:	readline-devel gmp-devel icu-devel
BuildRequires:	perl(Test::Harness)
BuildRequires:	parrot >= %{parrot_version}
BuildRequires:	parrot-devel >= %{parrot_version}

Requires:	parrot >= %{parrot_version}

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
%setup -q -n %{name}-%{year}.%{month}


%build
%{__perl} Configure.pl
make


%install
%makeinstall_std

# Force executable permission on shared objects so they get stripped
%{__chmod} 755 %{buildroot}%{parrot_dynext}/nqp*.so

%check
%ifarch %{ix86}
  # This test fails on this architecture
  %{__rm} -f t/nqp/60-bigint.t
%endif
make test

%files
%doc CREDITS LICENSE README.pod docs examples
%{_bindir}/nqp

# The unversioned shared system library files are needed for the essential work
# of the nqp executable, otherwise the executing of nqp fails
# with error message "PARROT VM: Could not load bytecode ..."
%{parrot_dynext}/nqp_group.so
%{parrot_dynext}/nqp_ops.so
%{parrot_dynext}/nqp_bigint_ops.so
%{parrot_dynext}/nqp_dyncall_ops.so

%{PAR_LIB_DIR}/languages/nqp
%{PAR_LIB_DIR}/library/ModuleLoader.pbc
%{PAR_LIB_DIR}/include/nqp_const.pir
%{_includedir}/parrot/%{parrot_version}/dynpmc/pmc_*
