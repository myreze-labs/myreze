#!/usr/bin/env python
"""
Example of visualizing data in Three.js.
"""

from myreze.data import MyrezeDataPackage
from myreze.viz import ThreeJSRenderer


def main():
    # Create a sample data package
    data_package = MyrezeDataPackage()

    # Visualize with Three.js
    renderer = ThreeJSRenderer()
    print("Visualizing with Three.js:", renderer)


if __name__ == "__main__":
    main()
