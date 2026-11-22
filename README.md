# THE SUNDAY LEDGER — Signature Edition

[![make.fun news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Revaaa28/makefun-news-image-20261122-v6/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Revaaa28/makefun-news-image-20261122-v6/reward.svg)](https://make.fun/bounty/news-image-20261122)

One page that sums up the world's news of **Sunday 22 November 2026**, drawn
entirely in code: a picture-led broadsheet in cream and ledger green.

- Three illustrated hero panels: the COP31 final deal that never says "fossil
  fuels" (Antalya), Iran's strike on Bahrain and Manama's turn to the UN
  Security Council, and Ukraine's 186-drone night — the Ukrainian Air Force's
  own figure, with 161 downed or suppressed — plus the Sparta II arms ship
  ablaze in the Gulf of Finland.
- Eight pictured story cards, a dotted world map with numbered pins, and an
  "Also on Sunday" list: **36 stories in all** — Europe 9 · Middle East 8 ·
  Americas 6 · Asia-Pacific 5 · Africa 2 · World 6.
- A DATE CHECK box names what was left out on purpose (news of Thursday 19 and
  Friday 20 November), and the Ledger Line closes the page.

## How it runs

`main.py` (Python 3.13, standard library only) copies the committed
`entry.png` to the output directory, byte for byte, so repeated runs are
identical. The page itself was drawn by `draw.py` (Pillow) at build time;
running it again reproduces `entry.png` exactly.

## License

MIT — see `LICENSE`.
