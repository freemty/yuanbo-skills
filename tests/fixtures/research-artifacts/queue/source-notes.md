# Queue Sources and Derivations

## Source Q1

Supplied synthetic fixture: `../fixtures.md`, section Q1. No external literature or measurements.

## Assumptions A1

The deck instantiates stationary M/M/1 as independent Poisson arrivals, independent identically distributed exponential service times, one work-conserving server, first-come first-served service, an unbounded waiting room, and lambda < mu. Rates are fixed over time. The FCFS and unbounded-room details are explicit modeling choices for the teaching example. All sensitivity rows retain these assumptions and fix mu = 10 jobs/s.

## Calculation D1

The supplied expected system-time formula gives W = 1/(10-6) = 0.25 s. Exponential service at rate mu = 10 jobs/s has mean S = 1/mu = 0.10 s. Since system time is waiting time plus service time, the mean waiting time is Wq = W-S = 0.15 s. Utilization rho = lambda/mu = 0.60.

## Calculation D2

All entries are evaluations of the supplied formula, not observations.

| Arrival rate (jobs/s) | Utilization | System time (s) | Waiting time (s) |
| --- | --- | --- | --- |
| 2 | 0.20 | 0.125 | 0.025 |
| 6 | 0.60 | 0.250 | 0.150 |
| 8 | 0.80 | 0.500 | 0.400 |
| 9 | 0.90 | 1.000 | 0.900 |

## Derivation D3

Wq = 1/(mu-lambda) - 1/mu = lambda/[mu(mu-lambda)]. With mu fixed and 0 <= lambda < mu, its derivative with respect to lambda is 1/(mu-lambda)^2 > 0. As lambda approaches mu from below, Wq tends to infinity. This stationary finite-mean formula is inapplicable at lambda >= mu. The mechanism explanation is that random arrivals/service can create a backlog and less mean spare capacity leaves less room to clear it. This intuition is not presented as a separate empirical finding.

The slides discuss means only. They do not establish tail latency, a deployment-specific utilization target, or an observed serving result. The supplied stationary formula itself is assumed, not proved in the five-minute talk.
