import sys

from setuptools import find_packages, setup
from setuptools_rust import RustExtension, Binding

with open("README.md", mode="r") as f:
    long_description = f.read()

version_range_max = max(sys.version_info[1], 12) + 1
python_min_version = (3, 11, 0)

setup(
    name="keywords",
    version="1.0.0",
    author="akitenkrad",
    author_email="akitenkrad@gmail.com",
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    rust_extensions=[
        RustExtension(
            "keywords._lib",
            path="Cargo.toml",
            binding=Binding.PyO3,
        )
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
    + ["Programming Language :: Python :: 3.{}".format(i) for i in range(python_min_version[1], version_range_max)],
    long_description=long_description,
)
