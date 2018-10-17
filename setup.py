from setuptools import setup
from setuptools import find_packages

setup(
    name='skil',
    version='0.2',
    packages=find_packages(),
    install_requires=['skil_client', 'requests'],
    extras_require={
        'tests': ['pytest', 'pytest-pep8', 'pytest-cov', 'mock']
    },
    include_package_data=True,
    license='Apache',
    description='Deploy your Python models with SKIL',
    long_description='Deploy your Python models with SKIL',
    author='Max Pumperla',
    author_email='max@skymind.io',
    url='https://github.com/SkymindIO/skil-python',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
)
