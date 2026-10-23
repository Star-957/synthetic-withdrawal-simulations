# Monte Carlo Withdrawal Simulations in Python

Small, inspectable **synthetic unit-balance experiments** for studying withdrawal order, random returns and simulation edge cases. Standard-library Python; no market data, accounts, currencies or personal financial plans.

This is educational numerical code, **not financial advice, a validated retirement model or a safe-withdrawal calculator**. Example return assumptions are invented inputs, not forecasts.

## What's here

| Program | Experiment |
|---|---|
| `mc_fire.py` | Gaussian independent-return paths, phased withdrawals and an illustrative threshold search |
| `mc_fire_10yr.py` | Ten abstract periods with Gaussian or Student-t samples |
| `mc_fire_grid.py` | Synthetic balance/horizon grid and conditional threshold searches |
| `test_simulations.py` | Deterministic regression checks, including terminal-period ruin |

The historical `fire` filenames are retained for traceability; examples represent abstract units, not an individual's FIRE plan. A balance of `1.0` means one arbitrary unit. Periods need not represent years; legacy variable names remain in the small kernels.

## Quick check

```sh
python -B -m unittest -v test_simulations.py
```

Four test methods exercise 15 deterministic subcases across the three programs. Imports are checked for no printed output and no reseeding of the global random generator. Tests use only eight paths per case and do not call the CLI simulations.

To run an example deliberately:

```sh
python mc_fire_10yr.py
```

The demonstration CLIs use 20,000 or 30,000 paths; grid/threshold examples can be CPU-intensive. Importing a module does not run them.

## Changes made for this source release

- Replaced personal inputs, profile details and display strings with fabricated dimensionless examples.
- Moved simulation loops and random seeding behind a `main()` guard.
- Fixed a terminal-period accounting bug: zero/negative balances after the final return must count as ruin and are clamped to zero for this unleveraged toy model.
- Added regression tests. Six terminal-loss subcases failed before the fix and passed afterwards; original source and pre-fix copies remain preserved locally.

## What the checks do not establish

No empirical calibration, historical backtest, tax-law implementation, investment recommendation, full simulation run or independent financial validation was performed. Gaussian/Student-t draws are independent and can produce returns below −100%; clamping prevents negative balances but does not make the distribution realistic. Withdrawal timing, inflation and tax-drag factors are simplified assumptions.

The search loops reuse fresh random samples at each trial: their output is noisy and should not be read as an exact minimum, a confidence bound or a safety guarantee. Inputs are not a hardened public API: invalid path counts, horizons or distribution parameters are outside these examples' tested contract.

## Provenance and reuse

An isolated publication copy of owner-authorized project code, with synthetic inputs and a fresh source commit. No personal records, raw chats, credentials, third-party assets or original Git history are included. Dependency implementations are not bundled. No new blanket license is granted; request permission before redistribution where a license is required.
