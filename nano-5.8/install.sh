#!/bin/bash

# Spark declared variables:
loc="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Actual install
cp -r $loc/fs/* /
