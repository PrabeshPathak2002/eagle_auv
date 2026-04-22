from setuptools import find_packages, setup

package_name = 'eagle_vision'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='eagleauv',
    maintainer_email='eagleauv@todo.todo',
    description='Vision package for EagleAUV',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'yolo_node = eagle_vision.yolo_node:main',
        ],
    },
)
