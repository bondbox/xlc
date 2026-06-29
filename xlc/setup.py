# coding=utf-8

import os
import tarfile
from urllib.parse import urljoin
import sys

from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install

sys.path.append(os.path.dirname(__file__))

from xlc.attribute import __project_desc__
from xlc.attribute import __package_name__
from xlc.attribute import __project_home__
from xlc.attribute import __version__

__urlcode__ = __project_home__
__urldocs__ = __project_home__
__urlbugs__ = urljoin(__project_home__, "issues")


def all_requirements():
    def read_requirements(path: str):
        with open(path, "r", encoding="utf-8") as rhdl:
            return rhdl.read().splitlines()

    requirements = read_requirements("requirements.txt")
    return requirements


class CustomInstallCommand(install):
    """Customized setuptools install command"""

    def run(self):
        install.run(self)  # Run the standard installation
        self.unpack_tar_files()  # Unpack all .tar files after installation

    def unpack_tar_files(self):
        install_lib = self.install_lib
        assert isinstance(install_lib, str)
        package_dir = os.path.join(install_lib, "xlc", "database")
        for filename in os.listdir(package_dir):
            if filename.endswith(".tar.xz"):
                tar_path = os.path.join(package_dir, filename)
                with tarfile.open(tar_path, "r:xz") as tar:
                    tar.extractall(path=tar_path[:-7])
                os.remove(tar_path)


setup(
    version=__version__,
    packages=find_packages(include=["xlc*"], exclude=["xlc.unittest"]),
    package_data={"xlc.database": ["langmark.toml", "langtags.toml", "*.tar.xz"]},  # noqa:E501
    install_requires=all_requirements(),
    cmdclass={
        "install": CustomInstallCommand,
    }
)
