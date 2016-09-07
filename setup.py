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
        keywords='sstash secure stash secret on-disk',
        url='https://github.com/realcr/secure_stash',
        author='real',
        author_email='realcr@gmail.com',
        license='MIT',
        packages=['secure_stash'],
        install_requires=[
            'jsonschema',
            'PyNaCl',
        ],
        tests_require=[
            'pytest',
        ],
        zip_safe=False)
