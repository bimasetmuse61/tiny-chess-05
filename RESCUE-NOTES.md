# tiny-chess-05 — rescue notes for tiny-chess-01

## Why tiny-chess-03 scored Elo 0 (diagnosis, reproduced)

Not a protocol bug: tc03 speaks the HTTP protocol correctly. It is a
speed collapse. tc03 burns its full 90,001-node cap on essentially
every move; measured on this VM: 7.7–9.0 s per move (~11k nodes/s —
make-move copies the whole board into an undo stack per node, the
TT key is a freshly built 64-tuple hashed per node, eval loops all
64 squares per leaf). A practice trial is 16 games with a 3,600 s
total wall (house thinking included) and a 10,000 ms per-move
limit; a trial that exhausts the wall scores 0 on every column.
tc03's own thinking alone projects to ~5,800 s (8 s × ~45 own
moves × 16 games), so the trial dies and the grade is exactly 0.
Secondary defects: no en passant, positional eval only for
pawns/knights, no repetition awareness.

## How tc05 fixes it

Same protocol, ~3x cheaper nodes (compact 64-square board, copy
unmake, tight eval), hard node budget (80,000/move) enforced by an
exception that discards the partial iteration — best move always
from the last completed depth. Full rules: castling, en passant
(incl. pin legality), promotions. Eval mirrors the house engine's
published formulas (piece values, pawn advancement, N/B
centrality, rook terms, king MG/EG tables blended by material,
bishop pair). Quiescence with in-check evasions, MVV-LVA +
promotion ordering, one killer per depth. Driver hardened: any
exception re-fetches state and keeps playing; one process plays
all 16 games. Deterministic: node budgets only, no wall clock.

## Evidence (kit practice trial-0, real env server, this VM)

- Perft, all exact: startpos 20/400/8902; Kiwipete 48/2039/97862;
  EP-pin 14/191/2812/43238; promo/castling 6/264/9467; pos5
  44/1486/62379.
- Protocol: full 16-game trial in one process, 740 server calls,
  0 illegal moves, 0 timeouts, max think 3,687 ms (limit 10,000).
  Finds mate-in-1 (Scholar's Qxf7#).
- Trial-0 score: 2W/3D/11L = 3.5 points → performance Elo 1,040
  (beat depth-2, mated depth-3 as Black, drew depth-3, depth-4).
  Other builds on the same trial: TT+weak eval 705 and 871; no-TT
  full eval at 50k nodes ~1,040–1,087 (13 games, interrupted);
  check-extension variant 3.5 pts in 10 games (interrupted).

## Honest floor judgment

Practice floor is 1,154. Best measured build is ~1,040 on
trial-0 — likely BELOW the floor by ~100 Elo, though a 16-game
sample carries ±~100 Elo of variance and the graded trial is a
fresh draw. Certain: tc05 can never repeat tc03's zero — it
answers every move legally in ≤3.7 s.
