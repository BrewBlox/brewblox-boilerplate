from setuptools import find_packages, setup

setup(
    name='YOUR-PROJECT',
    version='0.1',
    long_description=open('README.md').read(),
    url='YOUR_REPOSITORY',
    author='YOUR NAME',
    author_email='YOU@PROVIDER.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Hardware',
    ],
    keywords='brewing brewpi brewblox embedded plugin service',
    packages=find_packages(exclude=['test', 'docker']),
    install_requires=[
        'brewblox-service~=0.14.0'
    ],
    python_requires='>=3.7',
    extras_require={'dev': ['pipenv']}
)
