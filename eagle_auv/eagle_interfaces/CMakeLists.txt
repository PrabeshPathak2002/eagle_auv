cmake_minimum_required(VERSION 3.8)
project(eagle_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# This generates the message headers
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Detection.msg"
)

ament_package()