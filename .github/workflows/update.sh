name: update_dags

on:
  push:
    branches:
      - '*'
    tags:
      - v*
  pull_request:

  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set webhook deployment master-isi
        if: endsWith(github.ref, '/master')
        run: |
          curl -f -H "webhook:${KEY}" https://webhook.node1.mint.isi.edu/hooks/ui
        env:
          KEY: ${{ secrets.WEBHOOK_PASSWORD }}