from setuptools import find_packages, setup
from pathlib import Path


pwd = Path(__file__).parent.resolve()

long_description = ''
with open(f"{pwd}/README.md", "r") as f:
    long_description = f.read()

setup(
    name='netbox_ip_monitor',
    version='0.1.1',
    description='Visual representation of IP addresses',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url='https://github.com/Future998/netbox-ip-monitor',
    author='Alexander Burmatov',
    author_email='burmatov202002@gmail.com',
    license='Apache 2.0',
    keywords='netbox ip monitor plugin',
    install_requires=[],
    packages=find_packages(),
    package_data={
        "netbox_ip_monitor": [
            "templates/netbox_ip_monitor/*",
        ]
    },
    include_package_data=True,
    zip_safe=False,
)