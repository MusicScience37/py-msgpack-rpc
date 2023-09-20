#!/bin/bash

set -e

cd $(dirname $0)

# For options, see https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html.
sphinx-apidoc -H "API Reference" -f -q -o ./source/api ../py_msgpack_rpc
