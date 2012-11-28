#!/bin/bash
MOZ_SPS_REPORT_DATE=$(date)
rm -rf reports
mkdir -p "reports/$MOZ_SPS_REPORT_DATE"
python generateJSONData.py > "reports/$MOZ_SPS_REPORT_DATE/data.json"
