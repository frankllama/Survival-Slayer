#!/bin/bash

echo "Checking dependencies..."

if command -V python3 >/dev/null 2>&1 ; then
    echo "python3 found"
    echo "version: $(python3 -V)"
else
    echo "python3 not found"
fi

if command -V pip >/dev/null 2>&1 ; then
    echo "pip found"
    echo "version: $(pip -V)"
else
    echo "pip not found. Use: apt install python3-pip"
fi

if pip show pygame &>/dev/null; then
    echo "pygame found"
    echo "version: $(pip show pygame)"
else
    echo "pygame not found. Use: python3 -m pip install -U pygame --user"
fi

CKSUM="2030573888 6684332"
SHA1SUM="a77093d7910936419a7630f7ce20dd8100ae71f4"
MD5SUM="11b323eae5527cbbeb2bd327b689b45d"

if [ "$CKSUM" = "$1" ]; then
  echo "Success, integrity verified: cksum match."
elif [ "$SHA1SUM" = "$1" ]; then
  echo "Success, integrity verified: sha1sum match."
elif [ "$MD5SUM" = "$1" ]; then
  echo "Success, integrity verified: md5sum match."
else
  echo "Error, corrupt or wrong zip file. Please check correct downloaded zip."
fi
