#!/bin/sh 

cd $(dirname $0)

echo "Unit testing..."
echo "Checking the cli..."
python tests/unit/test_cli.py -b
echo "Checking the scraper..."
python tests/unit/test_scraper.py -b

echo "End-to-end test..."
python src/scraper.py
echo "Done testing!"
echo "Check your downloads folder for the scraped test images."
