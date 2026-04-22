from setuptools import setup
import os
from glob import glob

package_name = 'eagle_nav'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        # Install marker file in the package index
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        # Include our package.xml file
        ('share/' + package_name, ['package.xml']),
        # Include launch files if you create them later
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Prabesh Pathak',
    maintainer_email='eagleauv@usm.edu', # Update with your actual email
    description='Navigation and mission control framework for EagleAUV',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # format: 'executable_name = package_name.file_name:main_function'
            'pilot = eagle_nav.sub_pilot:main',
            'mission = eagle_nav.mission_manager:main',
        ],
    },
)
