from os import path
from setuptools import setup

__version__ = "0.2.0"

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here, "LICENSE"), encoding="utf-8") as f:
    license_ = f.read()

# get the dependencies and installs
install_requires = ["attrs"]

# --
postgres_reqs = ["sqlalchemy", "psycopg2-binary"]
dynamodb_reqs = ["boto3"]
mongo_reqs = ["pymongo"]
redis_reqs = ["redis"]
dev_reqs = ["pytest", "pytest-cov", "black", "flake8"]

nosql_reqs = dynamodb_reqs + mongo_reqs + redis_reqs
all_reqs = dynamodb_reqs + mongo_reqs + redis_reqs + postgres_reqs

extras_require = dict(
        dev=all_reqs + dev_reqs,
        postgres=postgres_reqs,
        dynamodb=dynamodb_reqs,
        mongo=mongo_reqs,
        redis=redis_reqs,
        nosql=nosql_reqs,
        all=all_reqs,
)
# dependency_links = [
#     x.strip().replace('git+', '') for x in reqs if x.startswith('git+')]

setup(
    name="dsdb",
    version=__version__,
    description="One-line database manager for Data Science workloads.",
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    url="https://github.com/buildnn/dsdb",
    license=license_,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
    ],
    packages=["dsdb"],
    keywords="",
    # include_package_data=True,
    author="Giacomo Barone, Buildnn",
    install_requires=install_requires,
    extras_require=extras_require,
    # dependency_links=dependency_links,
    author_email="giacomo.barone@buildnn.com",
)
