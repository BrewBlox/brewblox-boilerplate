from setuptools import find_packages, setup

project_name = 'YOUR-PACKAGE'
package_name = 'YOUR_PACKAGE'

setup(
    name=project_name,
    version='0.1',
    long_description=open('README.md').read(),
    url='YOUR_REPOSITORY',
    author='YOUR NAME',
    author_email='YOU@PROVIDER.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Hardware',
    ],
    keywords='brewing brewpi brewblox embedded plugin service',
    packages=find_packages(exclude=['test']),
    install_requires=[
        'brewblox-service~=0.11.0'
    ],
    python_requires='>=3.6',
    extras_require={'dev': ['tox', 'pipenv']}
)
