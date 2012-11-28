#!/bin/bash
#MOZ_SPS_REPORT_DATE=$(date)
MOZ_SPS_REPORT_DATE=TEST
rm -rf reports
mkdir -p "reports/$MOZ_SPS_REPORT_DATE"
mkdir -p "reports/$MOZ_SPS_REPORT_DATE/js"
python src/generateJSONData.py > "reports/$MOZ_SPS_REPORT_DATE/js/data.json"
cp html/report.html "reports/$MOZ_SPS_REPORT_DATE/report.html"
cp -r js "reports/$MOZ_SPS_REPORT_DATE/"
cp -r css "reports/$MOZ_SPS_REPORT_DATE/"
