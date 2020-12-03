import os
 
import setuptools
 
setuptools.setup(
    name='NVpower',
    version='0.0.1',
    keywords='power',
    description='A tool for measure NVidia power.',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    author='wildkid1024',      
    author_email='wildkid1024@163.com',  

    install_requires=[
         'nvidia-ml-py3',
    ],
 
    url='https://github.com/wildkid1024/NVpower', 
    packages=setuptools.find_packages(),
    license='MIT',
    entry_points={
        'console_scripts': [
            'NVpower = NVpower.main:main'
        ]
    }
)