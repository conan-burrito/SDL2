from conan import ConanFile
from conan.tools.files import copy
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout

import os


class Recipe(ConanFile):
    name = 'cross-test'
    version = '0.0.1'

    description = 'Simple SDL2 game recipe'
    settings = 'os', 'arch', 'compiler', 'build_type'

    requires = [
        'sdl2/2.26.4@conan-burrito/stable'
    ]

    def layout(self):
        build_folder = 'build'
        if self.settings.os == 'Android':
            # Use different install path for android
            build_folder = os.path.join('android', 'app', 'build', 'conan')

        cmake_layout(self, build_folder=build_folder)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

        cmake_deps = CMakeDeps(self)
        cmake_deps.generate()

        if self.settings.os == 'Android':
            self._import_java_sources()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def _import_java_sources(self):
        script_path = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(script_path, 'android', 'app', 'src', 'main', 'generated', 'java')
        if not os.path.exists(target):
            os.makedirs(target)

        for dep in self.dependencies.values():
            extra_sources = dep.cpp_info.get_property("extra_sources")
            if extra_sources is None:
                continue

            source = os.path.join(extra_sources, 'java')
            copy(self, pattern='*.java', dst=target, src=source)
