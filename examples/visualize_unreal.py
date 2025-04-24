#!/usr/bin/env python
"""
Example of visualizing data in Unreal Engine.
"""

from myreze.data import MyrezeDataPackage
from myreze.viz import UnrealRenderer


def main():
    # Create a sample data package
    data_package = MyrezeDataPackage()

    # Visualize with Unreal Engine
    renderer = UnrealRenderer()
    print("Visualizing with Unreal Engine:", renderer)


if __name__ == "__main__":
    main()
