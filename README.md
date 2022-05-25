# uscis-case-status-action

## Introduction

This [GitHub Action](https://docs.github.com/en/actions) is used to
check the case status in [uscis](https://egov.uscis.gov/casestatus/landing.do).

## Workflow demo

Create `.github/workflows/uscis.yml` with demo config as：

```yaml
name: USCIS Case Status Check Action

on:
  schedule:
    # This crontab makes this action scheduled for 20:00 each day
    - cron:  '0 20 * * *'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out
        uses: actions/checkout@v2
      - name: USCIS Action
        uses: Bluefissure/uscis-case-status-action@latest
        id: script
        continue-on-error: true
        with:
          receipt_number: ${{ secrets.RECEIPT_NUMBER }}
      - name: Output status.txt
        run: cat status.txt
      - name: Commit files
        continue-on-error: true
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "Case Status Check Action"
          git add ./status.txt
          git commit -m "${{ steps.script.outputs.status }}"
      - name: Push changes
        continue-on-error: true
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch: ${{ github.ref }}
      - name: Test status is not changed
        uses: pr-mpt/actions-assert@v3
        with:
          assertion: npm://@assertions/is-equal:v1
          actual: "${{ steps.script.outputs.status_changed }}"
          expected: false
```

The `${{ secrets.RECEIPT_NUMBER }}` is the receipt number of your case, you need to manually add by:

![](https://static.zkqiang.cn/images/20200118171056.png-slim)


## Arguments


| Arg | Required | Hint |
| --- | --- | --- |
| receipt_number | Yes | The receipt number of the case. |