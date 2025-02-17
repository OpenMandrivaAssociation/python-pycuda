%define module	pycuda

# CUDA version used to build the package:
%define cuda_ver 7.5

# NVIDIA driver version required by CUDA:
%define driver_ver 352.39

# Since x11-driver-video-nvidia-current doesn't explicitly provide
# this, it shouldn't be included in the requires list:
%if %{_use_internal_dependency_generator}
%define	__noautoreq libcuda.*
%else
%define _requires_exceptions libcuda.*
%endif

Summary:	Python wrapper for NVIDIA's CUDA API

Name:		python-%{module}
Version:	2015.1.3
Release:	1
Source0:        http://pypi.python.org/packages/source/p/%{module}/%{module}-%{version}.tar.gz
Source100:	python-pycuda.rpmlintrc
License:	MIT
Group:		Development/Python
Url:		https://mathema.tician.de/software/pycuda
Requires:	nvidia-cuda-toolkit >= %{cuda_ver}
Requires:	nvidia-current-cuda-opencl >= %{driver_ver}
Requires:	nvidia >= %{driver_ver}
Requires:	python-mako
Requires:	python-pytools >= 2011.2
Requires:	python-decorator >= 3.2.0
Requires:	python-pytest >= 2
BuildRequires:	python-setuptools >= 0.6c9
BuildRequires:	nvidia-cuda-toolkit-devel >= %{cuda_ver}
BuildRequires:	nvidia-devel >= %{driver_ver}
BuildRequires:	python-numpy-devel >= 1.0.4
BuildRequires:	boost-devel
BuildRequires:	python-sphinx
BuildRequires:	python-devel
ExclusiveArch:	x86_64

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

%__python ./configure.py --cudadrv-lib-dir=/usr/lib/nvidia-current,/usr/lib64/nvidia-current \
--boost-inc-dir=/usr/include/,/usr/include/boost \
--boost-lib-dir=/usr/lib,/usr/lib64 --boost-python-libname=boost_python --boost-thread-libname=boost_thread
%__python setup.py build

make -C doc PAPER=letter html
find -name .buildinfo | xargs rm -f

%install
PYTHONDONTWRITEBYTECODE= %__python setup.py install --root=%{buildroot}

%clean

%files
%doc doc/build/html/ examples/ README.rst
%{py_platsitedir}/pycuda*

