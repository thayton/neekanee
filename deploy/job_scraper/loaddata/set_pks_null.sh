#!/bin/sh

if [ $# -ne 1 ]; then
  echo "usage: $0 <file>"
  exit 1
fi

cp -f $1 $1.bak
cat $1 | sed -E "s/\"pk\": [0-9]+/\"pk\": null/g" > $1.$$
mv -f $1.$$ $1