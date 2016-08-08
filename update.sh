#!/bin/bash

echo "downloading payroll data ..."
fab download_payroll_data

echo ""
echo ""
echo "parsing payroll data ..."
fab parse_payroll_data

echo ""
echo ""
echo "aggregating payroll data ..."
fab aggregate_payroll_data


read -n1 -p "Do you want to push data to the production database? [y,n]" killfill
case $killfill in
  y|Y)
    echo ""
    echo ""
    echo "ok, killing and filling ..."
    # upload ish here
  ;; 
  n|N)
    echo ""
    echo ""
    echo "k bye" exit 1
  ;;
esac
