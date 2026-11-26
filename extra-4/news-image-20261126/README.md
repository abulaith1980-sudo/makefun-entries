# News image — 26 November 2026

A program that draws one image summing up Thursday 26 November 2026's
world news: a newspaper front page with the day's lead stories, a tariff
bar chart, and a short "also today" strip.

Run it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

It writes `entry.png` (1024x1024 PNG). Run it twice and the two files are
byte-identical. Standard library only, no network.

License: MIT.
