#!/bin/bash

echo "Running all tests..."

# Run Python tests
echo "Running Python tests..."
python -m pytest tests/ -v

# Run Android tests if available
if [ -d "mobile/android" ]; then
    echo "Running Android tests..."
    cd mobile/android
    ./gradlew test
    cd ../..
fi

# Run iOS tests if available
if [ -d "mobile/ios" ]; then
    echo "Running iOS tests..."
    cd mobile/ios
    xcodebuild test -workspace ARMIntelligence.xcworkspace -scheme ARMIntelligence -destination 'platform=iOS Simulator,name=iPhone 14'
    cd ../..
fi

echo "All tests complete!"
