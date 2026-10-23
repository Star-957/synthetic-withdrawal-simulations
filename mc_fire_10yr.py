#!/usr/bin/env python3
# Synthetic dimensionless demonstration. All balances are abstract units, not personal money.
# No ages, residence, holdings or personal plan are represented. Assumptions are not advice.
# Historical Gaussian-IID engine; no model validation or safe-withdrawal guarantee.
# Ten synthetic periods: phaseA withdrawals, phaseB no withdrawals, phaseC withdrawals.
import random, math, statistics
N=30000; INFL=0.02; START=1.0; ONE=0.02; UNI=0.04; RET=0.03

def draw_gauss(m,sd): return random.gauss(m,sd)
def draw_t(m,sd,df=5):
    # Student-t (fat tails) scaled to target sd. var(t_df)=df/(df-2); scale to sd.
    z=random.gauss(0,1); chi2=sum(random.gauss(0,1)**2 for _ in range(df))
    t=z/math.sqrt(chi2/df)            # standard t_df
    return m + sd*math.sqrt((df-2)/df)*t

def run10(mean,sd,sampler):
    surv=0; bal10=[]
    for _ in range(N):
        bal=START-ONE; ok=True
        for y in range(10):
            ia=(1+INFL)**y
            w = UNI*ia if y<=3 else (0.0 if y<=5 else RET*ia)
            bal-=w
            if bal<=0: ok=False; bal=0; break
            r=sampler(mean,sd)
            if y>5 and r>0: r*=0.85       # light tax drag in retirement yrs
            bal*=(1+r)
            # A terminal loss is ruin too; unleveraged balances cannot go below zero.
            if bal<=0: ok=False; bal=0; break
        surv+=ok; bal10.append(bal)
    bal10.sort()
    return surv/N*100, statistics.median(bal10), bal10[int(0.25*N)], bal10[int(0.10*N)]


def main():
    random.seed(12345)
    print("=== Synthetic ten-period unit-balance demonstration ===")
    for sampler,sname in [(draw_gauss,"Gaussian"),(draw_t,"Student-t df=5")]:
        for label,(m,sd) in {"Example A":(0.09,0.18),"Example B":(0.09,0.28),"Example C":(0.06,0.10)}.items():
            s,med,p25,p10=run10(m,sd,sampler)
            print(f"{sname}/{label}: survival {s:.1f}%; median {med:.3f}; p25 {p25:.3f}; p10 {p10:.3f} abstract units")


if __name__ == "__main__":
    main()
