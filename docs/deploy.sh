#!/bin/bash
python autogen.py
mkdocs build
cp -r img site
cp -r img sources
mkdocs gh-deploy