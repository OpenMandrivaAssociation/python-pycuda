%define module	pycuda
%define name	python-%{module}
%define version	0.94
%define rel	rc0
%define release %mkrel 0.%{rel}

# NVIDIA driver version required by CUDA:
%define driver_ver 195.0

# Since x11-driver-video-nvidia-current doesn't explicitly provide
# this, it shouldn't be included in the requires list:
%define _requires_exceptions libcuda.*

Summary:	Python wrapper for NVIDIA's CUDA API
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:        http://pypi.python.org/packages/source/p/%{module}/%{module}-%{version}rc.tar.gz
Patch0:		no-distribute.patch
License:	MIT
Group:		Development/Python
Url:		http://mathema.tician.de/software/pycuda
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	nvidia-cuda-toolkit >= 3.0
Requires:	nvidia >= %{driver_ver}
Requires:	python-pytools >= 8
BuildRequires:	python-setuptools >= 0.6c9
BuildRequires:	nvidia-cuda-toolkit-devel >= 3.0
BuildRequires:	nvidia-devel >= %{driver_ver}
BuildRequires:	python-numpy-devel >= 1.0.4
BuildRequires:	boost-devel
BuildRequires:	python-sphinx
%py_requires -d

%description
PyCuda lets you access Nvidia's CUDA parallel computation API from
Python. Several wrappers of the CUDA API already exist - so what's so
special about PyCuda?

* Object cleanup tied to lifetime of objects. This idiom, often called
  RAII in C++, makes it much easier to write correct, leak- and
  crash-free code. PyCuda knows about dependencies, too, so (for
  example) it won't detach from a context before all memory allocated
  in it is also freed.
* Convenience. Abstractions like pycuda.driver.SourceModule and
  pycuda.gpuarray.GPUArray make CUDA programming even more convenient
  than with Nvidia's C-based runtime.
* Completeness. PyCuda puts the full power of CUDA's driver API at
  your disposal, if you wish.
* Automatic Error Checking. All CUDA errors are automatically
  translated into Python exceptions.
* Speed. PyCuda's base layer is written in C++, so all the niceties
  above are virtually free.
* Helpful Documentation.

%prep
%setup -q -n %{module}-%{version}rc
%patch0 -p0

%build
find -name .gitignore | xargs rm -f

./configure.py --cudadrv-lib-dir=/usr/lib/nvidia-current,/usr/lib64/nvidia-current \
--boost-inc-dir=/usr/include/,/usr/include/boost \
--boost-lib-dir=/usr/lib,/usr/lib64 --boost-python-libname=boost_python --boost-thread-libname=boost_thread
%__python setup.py build

make -C doc PAPER=letter html
find -name .buildinfo | xargs rm -f

%install
%__rm -rf %{buildroot}
%__python setup.py install --root=%{buildroot} --record=FILE_LIST

%clean
%__rm -rf %{buildroot}

%files -f FILE_LIST
%defattr(-,root,root)
%doc doc/build/html/ examples/ README

