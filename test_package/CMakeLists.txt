cmake_minimum_required(VERSION 3.6)
project(PackageTest)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(ANDROID)
    # On Android we don't use executables, we use shared libraries instead
    add_library(example SHARED example.cpp)
else()
    add_executable(example example.cpp)
endif()
target_link_libraries(example ${CONAN_LIBS})
set_target_properties(example PROPERTIES OUTPUT_NAME "test")
