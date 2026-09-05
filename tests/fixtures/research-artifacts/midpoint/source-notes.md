# Midpoint Sources and Proof

## Source T1

Supplied synthetic fixture: `../fixtures.md`, section T1. No external paper, figure, or attribution.

## Definitions A1 and Statement T2

Let d be a positive integer. Let a,b be fixed vectors in R^d. Minimize F(x) = ||x-a||^2 + ||x-b||^2 over all x in R^d, using the ordinary Euclidean norm and equal weights. Define m = (a+b)/2. The unique global minimizer is m and the minimum is ||a-b||^2/2. No distinctness assumption on a and b is needed.

## Proof D1: Recenter

Define y = x-m and v = (b-a)/2. Then a = m-v, b = m+v, x-a = y+v, and x-b = y-v.

## Proof D2: Expand

By the Euclidean inner-product identity,

`||y+v||^2 = ||y||^2 + 2<y,v> + ||v||^2`

and

`||y-v||^2 = ||y||^2 - 2<y,v> + ||v||^2`.

Adding gives F(x) = 2||y||^2 + 2||v||^2 = 2||x-m||^2 + ||a-b||^2/2, which proves the supplied identity.

## Proof D3: Optimize

F(m) = ||a-b||^2/2. Hence F(x)-F(m) = 2||x-m||^2 >= 0 for every x. Equality holds if and only if x=m by positive definiteness of the Euclidean norm. This establishes global optimality and uniqueness, including a=b.

## Example E1

For a=0,b=2 in R, m=1 and F(x)=x^2+(x-2)^2=2(x-1)^2+2. At x=0,0.5,1,1.5,2 the objective equals 4,2.5,2,2.5,4, respectively. The table illustrates but does not prove the general theorem.

## Scope S1

Equal weights, an unconstrained vector domain, and squared Euclidean distance are the stated setting. Removing the square already removes uniqueness: for every x in [0,2], |x|+|x-2|=2, the global minimum by the triangle inequality. An arbitrary metric space need not define vector addition or division by two, and need not satisfy the supplied inner-product identity. The deck does not assert a midpoint theorem for arbitrary metrics. It also does not claim that squared Euclidean geometry is the only possible setting with any related center theorem.
