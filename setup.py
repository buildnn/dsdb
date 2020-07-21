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
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    reqs = f.read().split("\n")

with open(path.join(here, 'requirements-postgres.txt'), encoding='utf-8') as f:
    postgres_reqs = f.read().split('\n')

with open(path.join(here, 'requirements-dynamodb.txt'), encoding='utf-8') as f:
    dynamodb_reqs = f.read().split('\n')

with open(path.join(here, 'requirements-mongo.txt'), encoding='utf-8') as f:
    mongo_reqs = f.read().split('\n')

with open(path.join(here, 'requirements-redis.txt'), encoding='utf-8') as f:
    redis_reqs = f.read().split('\n')

with open(path.join(here, 'requirements-dev.txt'), encoding='utf-8') as f:
    dev_reqs = f.read().split('\n')

nosql_reqs = dynamodb_reqs + mongo_reqs + redis_reqs
all_reqs = dynamodb_reqs + mongo_reqs + redis_reqs + postgres_reqs

install_requires = [x.strip() for x in reqs if "git+" not in x]
# dependency_links = [
#     x.strip().replace('git+', '') for x in reqs if x.startswith('git+')]

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
    extras_require={
        'dev': all_reqs + dev_reqs,
        'postgres': postgres_reqs,
        'dynamodb': dynamodb_reqs,
        'mongo': mongo_reqs,
        'redis': redis_reqs,
        'nosql': nosql_reqs,
        'all': all_reqs,
    },
    # dependency_links=dependency_links,
    author_email="giacomo.barone@buildnn.com",
)
