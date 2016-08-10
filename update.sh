#!/bin/bash

echo "downloading payroll data ..."
fab download_payroll_data

echo ""
echo ""
echo "parsing payroll data ..."
fab parse_payroll_data

# if the missing-*.txt files not present, continue



# else echo "deal with missing data, then continue" exit 1


echo ""
echo ""
echo "aggregating payroll data ..."
fab aggregate_payroll_data

echo "~done~"
