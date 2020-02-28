from os import path
from setuptools import setup

__version__ = "0.1.2"

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here, "LICENSE"), encoding="utf-8") as f:
    license_ = f.read()

# get the dependencies and installs
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]
# dependency_links = [
#     x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name="dsdb",
    version=__version__,
    description="Quick and real database peristence for Data Scientists.",
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    url="https://github.com/buildnn/dsdb",
    license=license_,
    classifiers=[
        "Development Status :: 2 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    packages=["dsdb"],
    keywords="",
    # include_package_data=True,
    author="Giacomo Barone, Buildnn",
    install_requires=install_requires,
    # dependency_links=dependency_links,
    author_email="giacomo.barone@buildnn.com",
)

