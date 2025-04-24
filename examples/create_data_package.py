#!/usr/bin/env python
"""
Example of creating a Myreze data package.
"""

from myreze.data import MyrezeDataPackage


def main():
    # Create a sample data package
    data_package = MyrezeDataPackage()
    print("Created data package:", data_package)


if __name__ == "__main__":
    main()
