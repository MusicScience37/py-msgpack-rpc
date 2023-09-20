#!/bin/bash

set -e

cd $(dirname $0)

./update_apidoc.sh

poetry run sphinx-autobuild source build --port 7612
