from setuptools import setup
from setuptools import find_packages

setup(
    name='skil',
    version='0.2.7',
    packages=find_packages(),
    install_requires=['skil_client>=1.2.1', 'requests', 'numpy', 'tensorflow', 'keras', 'opencv-python', 'six'],
    extras_require={
        'tests': ['pytest', 'pytest-pep8', 'pytest-cov', 'mock']
    },
    include_package_data=True,
    license='Apache',
    description='Train, deploy and manage your Python models with SKIL',
    long_description='Train, deploy and manage your Python models with SKIL',
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
