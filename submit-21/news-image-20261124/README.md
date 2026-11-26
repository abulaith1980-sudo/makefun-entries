# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/abulaith1980-sudo/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/abulaith1980-sudo/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A pure-stdlib Python program that draws one newspaper-style image summing up Tuesday 24 November 2026's world news: Huawei's US jury conviction, four tankers hit by mines in the Strait of Hormuz, the drone strike on Riyadh's PIF tower, Ukraine's drone strikes on Russian ships, the Cartagena supermarket hostage siege, and China's Shenzhou 24 launch carrying Pakistan's first astronaut — plus the day's other headlines in a footer strip.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024x1024 PNG, under 1 MiB). It is fully deterministic — two runs write identical bytes — and uses no network and no external files: the image is drawn procedurally with a built-in 5x7 bitmap font.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
