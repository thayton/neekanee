#!/bin/sh


for f in `find . -name "*.py"`; do
  if grep -n 'from pdftohtml' $f > /dev/null 2>&1; then
    cat $f | sed -E -e 's/from jobscraper/from neekanee.jobscrapers.jobscraper/' \
                    -e '/from location import parse_location/D' \
                    -e 's/from pdftohtml/from neekanee.txtextract.pdftohtml/' \
                    -e 's/from soupify/from neekanee.htmlparse.soupify/' > $f.cpy
    mv $f.cpy $f
  fi
done
