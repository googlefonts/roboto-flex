#!/bin/bash

for d in fonts/repos/*; do
    if [ -d $d ]; then
	pushd $d
	git pull
	popd
    fi
done

python3 make-webfonts.py
