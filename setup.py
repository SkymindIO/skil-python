from setuptools import setup
from setuptools import find_packages

setup(
    name='skil',
    version='0.1',
    packages=find_packages(),
    install_requires=['skil_client', 'requests'],
    extras_require={
        'tests': ['pytest', 'pytest-pep8', 'pytest-cov']
    },
    include_package_data=True,
    license='Apache',
    description='Deploy your Python models with SKIL',
    url='https://github.com/deeplearning4j/pyskil',
    entry_points={
        'console_scripts': [
            'skil=skil.cli:handle'
        ]
    },
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
