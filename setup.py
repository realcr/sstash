from setuptools import setup

# Based on
# https://python-packaging.readthedocs.io/en/latest/minimal.html

def readme():
    with open('README.md','r') as fr:
        return fr.read()


setup(name='sstash',
        version='0.1',
        description='A simple on-disk secure stash for secrets',
        long_description=readme(),
        classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5',
            'Topic :: Security',
        ],
        keywords='sstash secure stash secret on-disk',
        url='https://github.com/realcr/sstash',
        author='real',
        author_email='realcr@gmail.com',
        license='MIT',
        packages=['sstash'],
        install_requires=[
            'jsonschema',
            'PyNaCl',
        ],
        setup_requires=['pytest-runner'],
        tests_require=['pytest'],
        include_package_data=True,
        zip_safe=False)
