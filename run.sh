#!/bin/bash

for spider in $(scrapy list)
do
    # put all the data in separate files to make it easier to trace
    # data back to the spider
    scrapy crawl $spider -o data/$spider.csv -t csv
done

# dedupe and merge

# should generate a single header (if not, we have inconsistent data)
head -n 1 -q data/*.csv | sort -u > alldata.csv
tail -q -n +2 data/*.csv | sort -u >> data.csv
