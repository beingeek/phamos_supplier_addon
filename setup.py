from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in phamos_supplier_addon/__init__.py
from phamos_supplier_addon import __version__ as version

setup(
	name="phamos_supplier_addon",
	version=version,
	description="Phamos Supplier Addon",
	author="phamos GmbH",
	author_email="furqan.asghar@phamos.eu",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
