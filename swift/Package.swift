// swift-tools-version: 5.9

import PackageDescription

let package = Package(
    name: "CornTest",
    targets: [
        .target(
            name: "CornTest",
            path: "Sources/CornTest"
        ),
        .testTarget(
            name: "CornTestTests",
            dependencies: ["CornTest"],
            path: "Tests/CornTestTests"
        ),
    ]
)
