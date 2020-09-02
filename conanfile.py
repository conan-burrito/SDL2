from conans import tools, ConanFile, CMake
from conans.errors import ConanException

import os


class Recipe(ConanFile):
    name = 'SDL2'
    description = 'Simple DirectMedia Layer is a cross-platform development library designed to provide ' \
                  'low level access to audio, keyboard, mouse, joystick, and graphics hardware via ' \
                  'OpenGL and Direct3D'
    homepage = 'http://www.libsdl.org'
    license = 'Zlib (https://www.zlib.net/zlib_license.html)'
    url = 'https://github.com/conan-burrito/SDL2'

    settings = 'os', 'arch', 'compiler', 'build_type'
    options = {
        'shared': [True, False],
        'fPIC': [True, False],
    }
    default_options = {'shared': False, 'fPIC': True}
    build_policy = 'missing'

    generators = 'cmake'
    exports_sources = ['patches/*']

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        # It's a C project - remove irrelevant settings
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

        if self.settings.os == 'Android':
            self.requires('cpu-features/0.4.1@conan-burrito/stable')

        if self.settings.os == 'watchOS':
            raise ConanException('watchOS is currently not supported')

    @property
    def source_subfolder(self):
        return os.path.join(self.source_folder, 'src')

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("{}-{}".format(self.name, self.version), 'src')
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)

    def build(self):
        cmake = CMake(self)
        if self.settings.os in ['iOS', 'Macos', 'tvOS']:
            unsupported_features = ['FSEEKO64', 'ITOA', '_LTOA', '_STRLWR', '_STRREV', '_STRUPR', '_UI64TOA', '_UITOA',
                                    '_ULTOA', '_I64TOA']
            for feature in unsupported_features:
                cmake.definitions['HAVE_%s' % feature] = 'FALSE'

        if self.settings.os in ['Android']:
            cmake.definitions['VIDEO_VULKAN'] = 'FALSE'

        cmake.definitions['SDL_SHARED_ENABLED_BY_DEFAULT'] = 'ON' if self.options.shared else 'OFF'
        cmake.definitions['SDL_STATIC_ENABLED_BY_DEFAULT'] = 'OFF' if self.options.shared else 'ON'
        cmake.definitions['SDL_CMAKE_DEBUG_POSTFIX'] = ''

        if not self.options.shared and self.options.get_safe('fPIC'):
            cmake.definitions['SDL_STATIC_PIC'] = 'ON'

        cmake.configure(source_folder='src')
        cmake.build()
        cmake.install()

    def package(self):
        # Extract the License/s from the header to a file
        with tools.chdir(self.source_subfolder):
            tmp = tools.load(os.path.join(self.source_subfolder, 'include', 'SDL.h'))
            license_contents = tmp[2:tmp.find("*/", 1)]
            tools.save("LICENSE", license_contents)

        # Copy the license files
        self.copy("LICENSE", src=self.source_subfolder, dst="licenses")

        # Binaries are bound to the build OS
        tools.rmdir(os.path.join(self.package_folder, 'bin'))

        if self.settings.os == 'Android':
            java_target = os.path.join(self.package_folder, 'share', 'java')
            self.copy('*.java',
                      src=os.path.join(self.source_subfolder, 'android-project', 'app', 'src', 'main', 'java'),
                      dst=java_target, keep_path=True)

            key_name = 'shared' if self.options.shared else 'static'
            for patch in self.conan_data["package_patches"][self.version][key_name]:
                tools.patch(**patch, base_path=java_target)

    def package_info(self):
        self.cpp_info.libs.append('SDL2')
        self.cpp_info.libs.append('SDL2main')

        self.cpp_info.names["cmake_find_package"] = "SDL2"
        self.cpp_info.names["cmake_find_package_multi"] = "SDL2"

        if self.settings.os == 'Macos':
            self.cpp_info.libs.append("iconv")
            self.cpp_info.frameworks.extend(['AudioToolbox', 'CoreAudio', 'CoreGraphics', 'CoreFoundation',
                                             'CoreVideo', 'QuartzCore', 'Metal', 'Cocoa', 'Carbon', 'Foundation',
                                             'CoreServices', 'ApplicationServices', 'AppKit', 'IOKit', 'ForceFeedback'])

        elif self.settings.os in ['iOS', 'tvOS']:
            self.cpp_info.libs.append("iconv")
            self.cpp_info.frameworks.extend(['AudioToolbox', 'AVFoundation', 'CoreAudio', 'CoreGraphics',
                                             'Foundation', 'GameController', 'Metal', 'OpenGLES', 'QuartzCore', 'UIKit',
                                             'CoreBluetooth'])
            if self.settings.os == 'iOS':
                self.cpp_info.frameworks.append('CoreMotion')

        elif self.settings.os == 'Android':
            self.cpp_info.libs.extend([
                'dl',
                'GLESv1_CM',
                'GLESv2',
                'log',
                'android',
                'hidapi'
            ])

        elif self.settings.os == 'Windows':
            self.cpp_info.libs.extend(['imm32', 'version', 'winmm', 'Setupapi'])

        elif self.settings.os == 'Linux':
            self.cpp_info.libs.extend(['dl', 'm', 'pthread'])
