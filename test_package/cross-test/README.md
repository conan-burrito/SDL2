## Building for Android

1. Open the Android project
2. Execute the `app:conanInstallAll` Gradle task to install the libraries (including application one)
3. Build and run the application


## Building for macOS

Requires no additional actions:

```shell
conan build . -b missing
open build/Release/game.app
```

## Building for iOS

### Signing

Requires a valid bundle GUI identifier and a signing identity.
The development team value can be found by opening the `Keychain Access.app`, selecting the `login` keychain and navigating
into `Certificates` section. There you can find your `development` or `distribution` certificate. e.g.:
`Apple Development: John Doe (2347GVV3KC)`. Double-click on it and copy the value under `Organisational Unit`


Here is an example:

```shell
export MACOSX_BUNDLE_GUI_IDENTIFIER="cross-build.yoba.de"
export XCODE_ATTRIBUTE_DEVELOPMENT_TEAM="2347GVV3KC"
export XCODE_ATTRIBUTE_CODE_SIGN_IDENTITY="iPhone Developer"
```


### Building

You can now build the application:

```shell
mkdir build
cd build
conan build .. -pr:h ../profiles/ios/armv8 -pr:b default  -b missing -s build_type=Debug
conan build .. -pr:h ../profiles/ios/armv8 -pr:b default  -b missing -s build_type=Release
```

**NOTE:** Use the `../profiles/ios/x86_64` profile if you want to use an emulator instead of real phone.

And open it in the XCode to play around:

```shell
open cross_test.xcodeproj
```
