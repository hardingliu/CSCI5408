#!/bin/sh
python3 tweet_extracter.py && python3 sentiment_analysis.py && python3 import_into_elasticsearch.py
