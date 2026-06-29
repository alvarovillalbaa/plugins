#!/usr/bin/env python3
"""Calculate required sample size for a two-proportion A/B test.

Uses the normal-approximation formula for comparing two proportions with a
given baseline rate, minimum detectable effect (absolute), power, and alpha.
Dependency-free (math only).

Usage:
    python calculate_sample_size.py --baseline 0.04 --mde 0.008
    python calculate_sample_size.py --baseline 0.04 --mde 0.008 --power 0.8 --alpha 0.05 --traffic 9000
"""
import argparse
import math


def z(p):
    # Inverse normal CDF (Acklam approximation), good to ~1e-9.
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p <= phigh:
        q = p - 0.5
        r = q*q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
               (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    q = math.sqrt(-2 * math.log(1 - p))
    return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
            ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--baseline", type=float, required=True, help="Baseline rate, e.g. 0.04")
    ap.add_argument("--mde", type=float, required=True, help="Absolute min detectable effect, e.g. 0.008")
    ap.add_argument("--power", type=float, default=0.8)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--traffic", type=float, default=0, help="Visitors/week to estimate duration")
    args = ap.parse_args()

    p1 = args.baseline
    p2 = args.baseline + args.mde
    z_alpha = z(1 - args.alpha / 2)
    z_beta = z(args.power)
    pbar = (p1 + p2) / 2
    n = ((z_alpha * math.sqrt(2 * pbar * (1 - pbar)) +
          z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2) / (args.mde ** 2)
    n = math.ceil(n)

    print(f"Baseline:            {p1:.4f}")
    print(f"Target (baseline+MDE): {p2:.4f}")
    print(f"Power / alpha:       {args.power} / {args.alpha}")
    print(f"Required per arm:    {n:,}")
    print(f"Required total:      {2*n:,}")
    if args.traffic > 0:
        weeks = (2 * n) / args.traffic
        print(f"Est. duration:       {weeks:.1f} weeks at {int(args.traffic):,} visitors/week")


if __name__ == "__main__":
    main()
