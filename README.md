# Case Status Action

## Introduction

This [GitHub Action](https://docs.github.com/en/actions) is used to
check the case status in [uscis](https://egov.uscis.gov/casestatus/landing.do).

## Workflow demo

Create `.github/workflows/uscis.yml` with demo config as：

```yaml
name: Case Status Check Action

on:
  schedule:
    # This crontab makes this action scheduled for 23:00 UTC each day
    - cron:  '0 23 * * *'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out this repo
        uses: actions/checkout@v2
      - name: USCIS Action
        uses: Bluefissure/case-status-action@v0.1.4
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

The `${{ secrets.RECEIPT_NUMBER }}` is the receipt number of your case, you need to manually add it in:

![secrets.RECEIPT_NUMBER](https://vip1.loli.io/2022/05/26/C8XgA1j2eKbBpav.png)


## Arguments


| Arg | Required | Hint |
| --- | --- | --- |
| receipt_number | Yes | The receipt number of the case. |


## Notifications

The action will fail if the status of your case is changed, and a fail notification will be sent by github.
The current status will be kept in `status.txt` of your project root.

There're also two outputs of this action so you can use them with other github actions to send customized notifications 
(such as slack webhook):

- `outputs.status`: The current case status.
- `outputs.status_changed`: Whether the new case status is different than the one in `status.txt`.
