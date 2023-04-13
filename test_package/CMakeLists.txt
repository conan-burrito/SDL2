cmake_minimum_required(VERSION 3.6)
project(PackageTest)

find_package(SDL2 REQUIRED CONFIG)

if(ANDROID)
    # On Android we don't use executables, we use shared libraries instead
    add_library(example SHARED example.cpp)
else()
    add_executable(example example.cpp)
endif()

target_link_libraries(example SDL2::SDL2main)

set_target_properties(example PROPERTIES OUTPUT_NAME "test")
