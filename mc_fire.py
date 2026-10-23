#!/usr/bin/env python3
# Synthetic dimensionless demonstration. All balances are abstract units, not personal money.
# No ages, residence, holdings or personal plan are represented. Assumptions are not advice.
# Historical Gaussian-IID engine; no model validation or safe-withdrawal guarantee.
import random, statistics
N=20000; INFL=0.02; TAX_DRAG=0.15

def run(start, onetime, uni_exp, ret_exp, work_yrs, horizon, mean, sd):
    surv=0; ends=[]
    for _ in range(N):
        bal=start-onetime; ok=True
        for y in range(horizon):
            ia=(1+INFL)**y
            w = uni_exp*ia if y<=3 else (0.0 if y<=3+work_yrs else ret_exp*ia)
            bal-=w                       # START-of-year withdrawal (conservative)
            if bal<=0: ok=False; bal=0; break
            r=random.gauss(mean,sd)
            if y>3+work_yrs and r>0: r*=(1-TAX_DRAG)
            bal*=(1+r)
            # A terminal loss is ruin too; unleveraged balances cannot go below zero.
            if bal<=0: ok=False; bal=0; break
        surv+=ok; ends.append(bal)
    ends.sort()
    se=(surv/N*(1-surv/N)/N)**0.5*100
    return surv/N*100, se, statistics.median(ends), ends[int(0.10*N)]


def main():
    random.seed(12345)
    print(f"Synthetic unit-balance demo, N={N}; start-of-period withdrawals.")
    for horizon in (30,60):
        print(f"=== Synthetic horizon {horizon} periods ===")
        for label,(m,sd) in {"Example A":(0.09,0.18),"Example B":(0.09,0.28),"Example C":(0.06,0.10)}.items():
            s,se,med,p10=run(1.0,0.02,0.04,0.03,2,horizon,m,sd)
            print(f"{label}: survival {s:.1f}% +/- {se:.1f}; median {med:.3f} units; p10 {p10:.3f} units")
        lo,hi=1.0,5.0
        for _ in range(20):
            mid=(lo+hi)/2
            if run(mid,0.02,0.04,0.03,2,horizon,0.09,0.18)[0]<85: lo=mid
            else: hi=mid
        print(f"Conditional model threshold at85%: {(lo+hi)/2:.3f} units; not a safety guarantee")


if __name__ == "__main__":
    main()
