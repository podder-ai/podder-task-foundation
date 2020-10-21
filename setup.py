from podder_task_foundation import __version__ as version
from setuptools import find_packages, setup

setup(
    name='podder-task-foundation',
    version=version,
    packages=find_packages(exclude=["tests.*"]),
    author="podder-ai",
    url='https://podder.ai/',
    install_requires=install_requires,
)
