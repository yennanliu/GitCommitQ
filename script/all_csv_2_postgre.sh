#!/bin/sh
#################################################################
# SCRIPTS DUMP ALL CSV TO MYSQL    
#################################################################
python script/csv_2_postgre.py data/commit_sample.csv  git_raw_data
