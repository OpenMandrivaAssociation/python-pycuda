%define module	pycuda
%define name	python-%{module}
%define version	2011.1.1
%define release %mkrel 1

# CUDA version used to build the package:
%define cuda_ver 3.2

# NVIDIA driver version required by CUDA:
%define driver_ver 260.19.26

# Since x11-driver-video-nvidia-current doesn't explicitly provide
# this, it shouldn't be included in the requires list:
%define _requires_exceptions libcuda.*

Summary:	Python wrapper for NVIDIA's CUDA API
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:        http://pypi.python.org/packages/source/p/%{module}/%{module}-%{version}.tar.gz
License:	MIT
Group:		Development/Python
Url:		http://mathema.tician.de/software/pycuda
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	nvidia-cuda-toolkit >= %{cuda_ver}
Requires:	nvidia-current-cuda-opencl >= %{driver_ver}
Requires:	nvidia >= %{driver_ver}
Requires:	python-pytools >= 2011.2
Requires:	python-decorator >= 3.2.0
BuildRequires:	python-setuptools >= 0.6c9
BuildRequires:	nvidia-cuda-toolkit-devel >= %{cuda_ver}
BuildRequires:	nvidia-devel >= %{driver_ver}
BuildRequires:	python-numpy-devel >= 1.0.4
BuildRequires:	boost-devel
BuildRequires:	python-sphinx
%if %mdkversion < 201100
BuildRequires:	python-virtualenv
%endif
BuildRequires:	python-devel

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
%setup -q -n %{module}-%{version}

%build
find -name .gitignore | xargs rm -f

# Use virtualenv to build/install on Mandriva < 2011.0 because
# pycuda-0.94rc requires distribute rather than setuptools and
# Mandriva < 2011.0 uses the latter:
%if %mdkversion < 201100
virtualenv --distribute CUDA
./CUDA/bin/python ./configure.py --cudadrv-lib-dir=/usr/lib/nvidia-current,/usr/lib64/nvidia-current \
--boost-inc-dir=/usr/include/,/usr/include/boost \
--boost-lib-dir=/usr/lib,/usr/lib64 --boost-python-libname=boost_python --boost-thread-libname=boost_thread
./CUDA/bin/python setup.py build
%else
%__python ./configure.py --cudadrv-lib-dir=/usr/lib/nvidia-current,/usr/lib64/nvidia-current \
--boost-inc-dir=/usr/include/,/usr/include/boost \
--boost-lib-dir=/usr/lib,/usr/lib64 --boost-python-libname=boost_python --boost-thread-libname=boost_thread
%__python setup.py build
%endif

make -C doc PAPER=letter html
find -name .buildinfo | xargs rm -f

%install
%__rm -rf %{buildroot}

%if %mdkversion < 201100
PYTHONDONTWRITEBYTECODE= ./CUDA/bin/python setup.py install --root=tmp/
PYCUDAROOT=`find tmp/ -name pycuda-%{version}`
echo $PYCUDAROOT
%__install -d -m 755 %{buildroot}/usr
mv -f $PYCUDAROOT/CUDA/* %{buildroot}/usr/
%else
PYTHONDONTWRITEBYTECODE= %__python setup.py install --root=%{buildroot}
%endif

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/build/html/ examples/ README
%_includedir/pycuda/*
%py_platsitedir/pycuda*

