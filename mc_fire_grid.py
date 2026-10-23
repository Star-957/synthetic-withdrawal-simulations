#!/usr/bin/env python3
# Synthetic dimensionless demonstration. All balances are abstract units, not personal money.
# No ages, residence, holdings or personal plan are represented. Assumptions are not advice.
# Historical Gaussian-IID engine; no model validation or safe-withdrawal guarantee.
import random, statistics
N=20000; INFL=0.02; TAX_DRAG=0.15

def run(start, onetime, uni_exp, ret_exp, work_yrs, horizon, mean, sd):
    surv = 0; ends = []
    for _ in range(N):
        bal = start - onetime; ok = True
        for y in range(horizon):
            ia = (1 + INFL) ** y
            w = uni_exp * ia if y <= 3 else (0.0 if y <= 3 + work_yrs else ret_exp * ia)
            bal -= w                        # START-of-year withdrawal (conservative)
            if bal <= 0: ok = False; bal = 0; break
            r = random.gauss(mean, sd)
            if y > 3 + work_yrs and r > 0: r *= (1 - TAX_DRAG)
            bal *= (1 + r)
            # A terminal loss is ruin too; unleveraged balances cannot go below zero.
            if bal <= 0: ok = False; bal = 0; break
        surv += ok; ends.append(bal)
    ends.sort()
    return surv / N * 100, statistics.median(ends), ends[int(0.10 * N)]

PORTS={"Example A":(0.09,0.18),"Example B":(0.09,0.28),"Example C":(0.06,0.10),"Example D":(0.07,0.14)}
PRINCIPALS=[1.0,1.2,1.5]
ONETIME=0.02; UNI=0.04; RET=0.03; WORK=2

def main():
    random.seed(12345)
    print("Synthetic grid: abstract unit balances; no personal holdings or currency amounts.")
    for horizon in (10,20,30):
        print(f"Horizon {horizon} periods")
        for label,(m,sd) in PORTS.items():
            cells=[run(start,ONETIME,UNI,RET,WORK,horizon,m,sd)[0] for start in PRINCIPALS]
            print(label, cells)
    for horizon in (20,30):
        for label,(m,sd) in PORTS.items():
            lo,hi=0.5,5.0
            for _ in range(22):
                mid=(lo+hi)/2
                if run(mid,ONETIME,UNI,RET,WORK,horizon,m,sd)[0]<85: lo=mid
                else: hi=mid
            print(f"{label}, horizon {horizon}: conditional threshold {(lo+hi)/2:.3f} units")
    for label,(m,sd) in PORTS.items():
        lo,hi=0.0,0.1
        for _ in range(24):
            mid=(lo+hi)/2
            if run(1.0,ONETIME,UNI,mid,WORK,30,m,sd)[0]>=85: lo=mid
            else: hi=mid
        print(f"{label}: conditional period withdrawal {(lo+hi)/2:.5f} units; not a guarantee")


if __name__ == "__main__":
    main()
