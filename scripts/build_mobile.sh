#!/bin/bash

echo "Building ARM Adaptive Intelligence mobile applications..."

# Build Android
if [ -d "mobile/android" ]; then
    echo "Building Android application..."
    cd mobile/android
    ./gradlew assembleRelease
    echo "Android APK built: mobile/android/app/build/outputs/apk/release/app-release.apk"
    cd ../..
fi

# Build iOS
if [ -d "mobile/ios" ]; then
    echo "Building iOS application..."
    cd mobile/ios
    pod install
    xcodebuild -workspace ARMIntelligence.xcworkspace \
               -scheme ARMIntelligence \
               -configuration Release \
               -archivePath build/ARMIntelligence.xcarchive \
               archive
    echo "iOS archive built: mobile/ios/build/ARMIntelligence.xcarchive"
    cd ../..
fi

echo "Mobile builds complete!"
