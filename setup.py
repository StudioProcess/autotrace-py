from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

def glob(pattern, dir='.'):
    '''glob relative to the specified directory'''
    import os
    from glob import glob
    cwd = os.getcwd()
    os.chdir( os.path.join(cwd, dir) )
    res = glob(pattern, recursive=True)
    os.chdir(cwd)
    return res

setup(
    name='autotrace-py', # required
    version='0.3.0',  # required
    description='Python interface for Autotrace',
    url='https://github.com/StudioProcess/autotrace-py',
    author='Martin Grödl',
    author_email='martin@process.studio',
    packages=['autotrace'], # required
    package_data={ 'autotrace': glob('lib/**/*', 'autotrace') }, # inlcude lib files
    install_requires=requirements,
    platforms=['MacOS, Linux'],
)
