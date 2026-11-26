# Token Radar

The best token launch radar: a sealed snapshot of every protocol DefiLlama
tracks, ranked by what each pre-token protocol's launch would be worth.

## What it does

The program reads the sealed snapshot (`/input/snapshot.json`), scores every
pre-token protocol with the **radar-2** model, and writes a ranked board,
a static dashboard and a dossier to `/output`.

- **Board** — `board.json` ranks all 198 launch candidates in the snapshot:
  the 40 on the house watchlist plus every other pre-token protocol that
  passes the watchlist's own test at any TVL — no token recorded, and not a
  wrapped, staked or bridged product of one that trades (no WBTC, no Binance
  staked ETH: those are tokens that already exist, not launches still to
  come). Strongest implied value first. Each row carries its implied value
  and a seven-step farm plan with costs and times.
- **Dashboard** — `dashboard/` is a static page (no network, no framework)
  that renders the board, a live-token view of the protocols that already
  trade, and a methodology view. It is sortable, searchable, and filterable
  by category, chain and watchlist, with a detail view per protocol that
  shows the model's full breakdown and the farm plan.
- **Dossier** — `dossier.json` is the summary the judge reads.

## The model (radar-2)

Implied value follows only from the snapshot's own figures, never from a
hand-written list of names:

```
peer     = median market-cap / TVL of the live-token protocols in the same
           category (at least 3 peers), else the global median, clamped [0.05, 1.00]
base     = tvl_usd x peer
growth   = clamp(change_7d, -40, 150) per cent
growthM  = 1 + (growth / 100) x 0.6
maturity = 0.7 + min(age_days, 1095) / 1095 x 0.3   (age unknown: 365 days)
breadth  = 1 + 0.04 x ln(chain count)
implied  = max(1, round(base x growthM x maturity x breadth))
```

TVL says how much value a protocol already secures; the peer multiple says
what the market pays for that kind of value; growth says where it is heading;
maturity says how long it has run with no token (pent-up launch value); and
breadth says how widely it is distributed.

## Farm plans

Each protocol gets seven steps derived from its own record — category,
chains, TVL and age: a fresh wallet, the category's action with capital sized
to TVL ($50–$250), a weekly qualifying action, a second chain or feature, a
hold of 30–60 days, claim safety, and an exit with a log and the category's
main risk. Every step names its cost and time.

## Run it

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts --input ../input/snapshot.json
```

Node 22, standard library only, no network. The program runs deterministically
and refuses a board that would fail the gate (missing watchlist slugs, ranks
out of order, or a farm step outside 20–600 characters).

## Entry

- Competition: **token-radar-01** on make.fun — "Build the best token launch radar"
- Program: `main.ts` (Node 22), model in `lib/model.ts`, vendored board library in `vendor/makefun-board.ts`
- Screenshots: `screenshots/` — the board, a protocol detail view, and a filtered view

## Dashboard exports and keyboard shortcuts

The dashboard adds no buttons, so the board looks exactly as the
screenshots show. A reader who wants the filtered board out of the page
uses the keyboard while the focus is on the page itself (never while
typing in a field):

- `e` — download the filtered board as `token-radar-board.csv`: rank,
  name, category, chains, TVL, seven-day change, age, peer multiple,
  implied value and watchlist, one row per protocol, in the current
  sort order.
- `j` — download the same filtered board as `token-radar-board.json`.
- `s` — copy a one-line summary of the top five rows of the filtered
  board, with each row's rank, name and implied value.
- `c` — copy a link to the current filtered view (the state already
  lives in the query string, so the link reopens the same view).
- `w` — toggle the watchlist-only filter.
- `/` — focus the search box.
- `1`, `2`, `3` — board, live-token and methodology tabs.

Exports always follow the filters and sort on screen: search, category,
chain, watchlist and the sort column all apply before the file is made.
