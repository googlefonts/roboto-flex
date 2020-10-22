#!/bin/bash

# open terminal, type: sh build.sh
# this version requires newer fonttools to use --output-dir command


printf "Build fonts…\n"

# cd source_roboto || exit


if ! python "build-roboto.py"
    then
        printf "Unable to run pyhon script.  Build canceled." 1>&2
        exit 1
fi








printf "\nBuild complete"