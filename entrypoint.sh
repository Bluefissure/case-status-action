#!/bin/bash

if [ -z "$INPUT_RECEIPT_NUMBER" ]; then
  echo '::error::Required Receipt Number 2'
  exit 1
fi

echo "Running case checker"
python main.py --receipt-number "$INPUT_RECEIPT_NUMBER"
