from conans import ConanFile, CMake, tools
import os
import sys


class Recipe(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()


    def test(self):
        if tools.cross_building(self.settings):
            return

        self.run(os.path.join('bin', 'test'), run_environment=True)
