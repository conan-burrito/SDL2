cmake_minimum_required(VERSION 3.6)

project(cross_test LANGUAGES CXX VERSION 0.0.1)

find_package(SDL2 REQUIRED CONFIG)

################################################################################
## Setup platform-specific flags
if(IOS)
    set(CMAKE_XCODE_ATTRIBUTE_DEVELOPMENT_TEAM $ENV{XCODE_ATTRIBUTE_DEVELOPMENT_TEAM})
    set(MACOSX_BUNDLE_GUI_IDENTIFIER $ENV{MACOSX_BUNDLE_GUI_IDENTIFIER})
    set(CMAKE_XCODE_ATTRIBUTE_CODE_SIGN_IDENTITY $ENV{XCODE_ATTRIBUTE_CODE_SIGN_IDENTITY})

    enable_language(Swift)
    enable_language(OBJC)

    set(STORYBOARDS
        apple/storyboards/LaunchScreen.storyboard
    )

    set(ASSETS
        ${CMAKE_CURRENT_LIST_DIR}/apple/assets/Default.xcassets
    )
endif()

##
## Create the main build target - our game. Its either a shared library (on Android)
## or an executable with some platform-specific properties
##
if(IOS OR APPLE)
    add_executable(game MACOSX_BUNDLE)
elseif(ANDROID)
    add_library(game SHARED)
else()
    add_executable(game)
endif()

target_sources(game PRIVATE
    src/main.cpp
)

set_target_properties(game
    PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED YES
        CXX_EXTENSIONS NO
)

target_include_directories(game PUBLIC ${CMAKE_CURRENT_LIST_DIR}/include)
target_link_libraries(game PUBLIC
    SDL2::SDL2main
)

if(IOS OR APPLE)
    target_sources(game PRIVATE ${STORYBOARDS} ${ASSETS})

    set_target_properties(game PROPERTIES
        RESOURCE "${STORYBOARDS};${ASSETS}"
        MACOSX_BUNDLE_INFO_PLIST "${CMAKE_CURRENT_LIST_DIR}/apple/plist.in"
        MACOSX_BUNDLE_SHORT_VERSION_STRING ${CMAKE_PROJECT_VERSION}
        MACOSX_BUNDLE_BUNDLE_VERSION ${CMAKE_PROJECT_VERSION}
    )
endif()
