from setuptools import setup, find_packages

setup(
    name='sparrow_django_common',
    version='0.0.3',
    author="hg",
    description='Including a variety of common middleware',
    license='MIT License',
    url='https://github.com/hanguangbaihuo/sparrow_django_common.git',
    packages=find_packages(),
    install_requires=[
        'requests>=2.12.1',
        'python-consul>=1.1.0'
    ]
)
