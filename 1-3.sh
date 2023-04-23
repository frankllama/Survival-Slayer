#!/bin/bash

CKSUM="60637313 6445560"
SHA1SUM="6c8e702d57b054331109c3faa75d915c9b02f9d4"
MD5SUM="b9f86089d0d2fc0e008b4a3fc0d75a26"

if [ "$CKSUM" = "$1" ]; then
  echo "Success, integrity verified: cksum match."
elif [ "$SHA1SUM" = "$1" ]; then
  echo "Success, integrity verified: sha1sum match."
elif [ "$MD5SUM" = "$1" ]; then
  echo "Success, integrity verified: md5sum match."
else
  echo "Error, corrupt or wrong zip file. Please check correct downloaded zip."
fi
