#!/usr/bin/env python3

__author__ = "Suka Wirawan"
__version__= "1.0.0"

from flaskr import create_app

server = create_app()

if __name__ == "__main__":
    server