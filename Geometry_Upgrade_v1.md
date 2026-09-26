# Geometry upgrade v1 — exact lattice volume and the geometry of independent columns

26 September 2026 · Mathematical extension and correction note

**The useful upgrade is to retain the coefficient matrix alongside the monomial polygon.** That gives exact rank, exact volume, and a geometry of independent column sets. It also exposes several errors in the supplied transcript.

Scope: the later Coppersmith / Boneh–Durfee / Herrmann–May material in `Pasted markdown(20260926-034418).md`. This is a standalone companion, not a complete audit of its group-theory, NFS, or post-quantum sections. The proofs below establish the stated algebraic and geometric claims; they do not establish a new RSA attack bound.

## 1. Fix the equation before changing its geometry

From

\[
ed=1+k\varphi(N),\qquad A=N+1,
\]

use

\[
f(x,y)=1+Ax+xy,\qquad (x_0,y_0)=(k,-p-q).
\]

Then \(f(x_0,y_0)=ed\), hence \(f(x_0,y_0)\equiv0\pmod e\).

The transcript instead repeatedly pairs this same root with \(x(A+y)-1\). At that root the value is \(ed-2\), which generally fails the congruence. A minus-one convention is possible with a corresponding change to the root, but the stated pair is inconsistent.

For \(u=1+xy\), the consistent linearization is

\[
\widetilde f(x,u)=Ax+u.
\]

Even if retaining the transcript's minus-one polynomial, substitution would produce \(Ax+u-2\), not its written \(Ax+u-1\).

## 2. Substitution preserves rank on the ring actually named

The transcript asserts that

\[
\pi:\mathbb Z[x,u]\longrightarrow\mathbb Z[x,y],\qquad
x\mapsto x,\quad u\mapsto1+xy
\]

has kernel directions that explain lost lattice rank. **This map is injective.**

Proof: write a nonzero polynomial as

\[
P(x,u)=\sum_{j=0}^{d}a_j(x)u^j,\qquad a_d(x)\ne0.
\]

The coefficient of \(y^d\) in \(P(x,1+xy)\) is \(a_d(x)x^d\ne0\). Thus \(\pi(P)\ne0\). Every finite independent family in this domain stays independent after substitution.

A different map does have the intended relation as its kernel:

\[
\widetilde\pi:\mathbb Z[x,y,u]\to\mathbb Z[x,y],\qquad
\ker\widetilde\pi=(u-1-xy).
\]

Division by the monic polynomial \(u-1-xy\), treating \(u\) as the variable, proves this statement. Domain choice matters.

Neither statement says substitution preserves Euclidean coefficient lengths. The single polynomial \(u\) becomes \(1+xy\), with scaled coefficient norm \(\sqrt{1+X^2Y^2}\). Injectivity and preservation of lengths are separate properties.

Also, sharing a leading monomial does not establish dependence: \(x+y\) and \(x-y\) both lead with \(x\), yet their coefficient determinant is \(-2\). Dropping rows requires a module calculation, not a visual collision test.

## 3. What the cited paper actually corrects

Kalam, Karmakar and Sarkar's 2025 paper identifies a floor-function approximation in the original Herrmann–May asymptotic analysis. The lower limit involves \(\lfloor m/t\rfloor j\). Replacing it by \(mj/t\) changes the leading-order region when \(t/m\) is fixed. Their Remark 1 explicitly identifies this issue; it does not attribute the discrepancy to a kernel of \(\mathbb Z[x,u]\to\mathbb Z[x,y]\).

The paper reports approximately \(0.292256\) for the original construction and \(1-1/\sqrt2\approx0.292893\) for its refined construction. These concern their specific shift families. The full strip below is a different family.

Source: [Kalam–Karmakar–Sarkar, Scientific Reports 15, 28544 (2025), especially Remark 1](https://www.nature.com/articles/s41598-025-10019-9.pdf).

The difference between the displayed bounds is approximately \(0.000637\), not the transcript's \(0.000541\).

## 4. An exact determinant for the full strip in the attachment

Let \(m\ge1\), \(t\ge0\), and use the complete families

\[
g_{i,k}=x^if^ke^{m-k},\quad 0\le k\le m,\quad0\le i\le m-k,
\]

\[
h_{j,k}=y^jf^ke^{m-k},\quad1\le j\le t,\quad0\le k\le m.
\]

Use the coefficient embedding of \(h(xX,yY)\), with positive integer scales \(X,Y\). Every row evaluates to a multiple of \(e^m\) at the specified modular root.

Order monomials first by increasing power of \(x\), then by increasing power of \(y\). The pivots are respectively

\[
x^{i+k}y^k,\qquad x^ky^{k+j}.
\]

They are distinct and cover the entire support. Every other term precedes its pivot. Thus the matrix is square and triangular after the corresponding row ordering. The diagonal products in this particular construction are genuine determinants.

Writing \(n\) for its rank,

\[
n=\frac{(m+1)(m+2)}2+t(m+1),
\]

\[
a=c=\frac{m(m+1)(m+2)}3+\frac{tm(m+1)}2,
\]

\[
b=\frac{m(m+1)(m+2)}6+
\frac{(m+1)t(t+1)}2+\frac{tm(m+1)}2,
\]

we obtain

\[
\boxed{\operatorname{vol}(L)=X^aY^be^c.}
\]

Here \(a,b,c\) are exponent totals, not the polynomial parameter \(A=N+1\). The final transcript's closed forms for these totals are correct. Earlier passages use an incorrect leading term for \(c\).

For the asymptotic model \(X=N^\delta\), \(Y=N^{1/2}\), \(\log_N e\to1\), put \(t/m\to\tau\). Ignoring reduction penalties at this stage gives

\[
\delta < F(\tau)=\frac{1+3\tau-3\tau^2}{4+6\tau}.
\]

Differentiation gives

\[
F'(\tau)=\frac{6-24\tau-18\tau^2}{(4+6\tau)^2},
\]

so

\[
\boxed{\tau_* =\frac{\sqrt7-2}{3}=0.215250437\ldots,\qquad
F(\tau_*)=\frac76-\frac{\sqrt7}{3}=0.284749563\ldots.}
\]

At \(t=0\), the asymptotic limit is \(1/4\). Therefore the transcript's attribution of \(0.284749\) to the x-only block and \(0.292893\) to this entire full strip is wrong. The displayed strip achieves the former after optimization. Recovering the latter requires a different construction and its own verified determinant.

For exact finite parameters, the volume-only ceiling under the idealized \(e=N\) scaling is

\[
\delta_{\max}=\frac{mn-b/2-c}{a}.
\]

| \(m\) | \(t\) | Exact rank \(n\) | Volume-only \(\delta_{\max}\) |
|---:|---:|---:|---:|
| 4 | 1 | 20 | 0.250000 |
| 8 | 3 | 72 | 0.250000 |
| 12 | 4 | 143 | 0.262500 |
| 16 | 6 | 255 | 0.260417 |
| 20 | 8 | 399 | 0.258824 |
| 22 | 8 | 460 | 0.265152 |

These ranks correct the attachment's table for its stated full-strip formula. They must not be substituted for ranks of other shift constructions.

## 5. Restore the missing rank factors in the finite-size test

For a rank-\(r\) lattice embedded in \(s\) monomial coordinates, the standard LLL first-vector bound at Lovász parameter \(3/4\) is

\[
\|b_1\|\le2^{(r-1)/4}\operatorname{vol}(L)^{1/r}.
\]

Within the declared root box, Cauchy–Schwarz gives the sufficient Howgrave–Graham threshold \(\|b_1\|<e^m/\sqrt{s}\). Thus

\[
\boxed{
\log_N\operatorname{vol}(L)
<rm\log_Ne-
\frac{r(r-1)}4\log_N2-
\frac r2\log_Ns.
}
\]

For the square strip, \(r=s=n\). The transcript writes a total determinant logarithm on the left but penalties appropriate to the normalized logarithm on the right, omitting a factor of \(n\) in both penalties.

At \((m,t)=(20,8)\), \(\delta=0.285\), and the idealized scales \(\log_Ne=1\), \(\log_NY=1/2\):

\[
\delta a+b/2+c=8104.6>7980=mn.
\]

It already fails the volume-only condition by \(124.6\). If \(\log_2N=1000\), the correct additional penalty is approximately \(41.424229\). For an actual modulus, use its actual logarithm, the actual public exponent, and root bounds including their constants.

Failure of this sufficient inequality does not prove recovery impossible. Passing it guarantees the stated length conclusion, not that two output polynomials determine the desired root.

## 6. The extension: volume geometry from independent column sets

Let \(C\in\mathbb Z^{r\times s}\) contain an actual integer basis of the polynomial coefficient lattice, with full row rank. Let column \(j\) correspond to \(x^{\alpha_j}y^{\beta_j}\), and define

\[
D=\operatorname{diag}(X^{\alpha_j}Y^{\beta_j}),\qquad B=CD.
\]

The general volume is

\[
\boxed{\operatorname{vol}(L)^2=\det(BB^{\mathsf T}).}
\]

Cauchy–Binet expands it into

\[
\boxed{
\operatorname{vol}(L)^2=
\sum_{\substack{J\subseteq\{1,\ldots,s\}\\|J|=r}}
\det(C_J)^2\,
X^{2\sum_{j\in J}\alpha_j}
Y^{2\sum_{j\in J}\beta_j}.
}
\]

Only independent column sets contribute. This identity remains valid for rectangular matrices. A single minor is generally only one contribution; it is not the full volume.

A minimal check uses

\[
C=\begin{pmatrix}1&1&0\\0&1&1\end{pmatrix},\qquad
D=\operatorname{diag}(1,2,3).
\]

Then

\[
BB^{\mathsf T}=\begin{pmatrix}5&4\\4&13\end{pmatrix},\qquad
\operatorname{vol}(L)^2=65-16=49.
\]

The three squared maximal minors contribute \(4+9+36=49\). Keeping just one misses part of the geometry.

For the geometric interpretation, set \(z=(\log X,\log Y)\), and for each nonzero minor define

\[
v_J=\left(\sum_{j\in J}\alpha_j,\sum_{j\in J}\beta_j\right).
\]

Then

\[
\log\operatorname{vol}(L)
=\frac12\log\sum_{J:\det C_J\ne0}
\exp\left(2\log|\det C_J|+2v_J\cdot z\right).
\]

This is an exact log-sum-exp formula. With coefficient matrix \(C\) held fixed, its gradient and Hessian are

\[
\nabla_z\log\operatorname{vol}(L)=\mathbb E_w[v_J],\qquad
\nabla_z^2\log\operatorname{vol}(L)=2\operatorname{Cov}_w(v_J)\succeq0,
\]

where \(w_J\) is the normalized positive contribution of minor \(J\).

**The barycentre idea survives, with a precise object:** a weighted barycentre of exponent sums over independent column sets. The convex hull of the \(v_J\) controls which terms dominate as the scaling changes. Coefficients determine the weights; linear dependence determines which points exist. This is standard Cauchy–Binet and convexity applied to the attachment's setting, not a claim of a new theorem in the literature.

A polygon of individual monomials alone cannot supply this information. If coefficients also vary with \(N\), their growth must be retained; the fixed-\(C\) convexity statement must not silently be applied while changing \(C\).

## 7. Rules for a reproducible next construction

1. State the polynomial, modulus, root convention, and root box.
2. State the polynomial ring and any quotient relation explicitly.
3. Construct the exact integer coefficient module. Distinguish number of rows, rank, and number of monomial columns.
4. Obtain an integer lattice basis without silently changing the module. An arbitrary rationally independent subset can change the lattice: rows \([2]\) and \([3]\) generate \(\mathbb Z\), while retaining only \([2]\) gives \(2\mathbb Z\).
5. Use a proved square triangular determinant or the Gram determinant of the actual basis.
6. Apply the rank-correct length inequality; evaluate the actual returned vectors as well.
7. Check whether the resulting polynomial equations isolate candidates, then substitute candidates into the original equations.

A nonzero resultant alone is not a complete root-recovery certificate. Two independent coefficient vectors can still represent polynomials with a common factor. Rank, shortness, and usefulness for elimination are separate checks.

## Verification performed

The included Python program uses only the standard library. It independently expands the full-strip polynomials for 30 parameter pairs, computes their exact integer determinants, and compares them with the closed form. It also checks the \((20,8)\) arithmetic, the optimum, the rectangular Gram identity, and the equal-leading-monomial counterexample.

All these checks passed. No cryptographic-size lattice reduction or key recovery was run. The paper's refined implementation and the rest of the attachment were not audited here.

## Reproducible verification code

Copy the following into a Python file and run it with Python 3.

```python
from math import comb, sqrt, log2
from fractions import Fraction

def determinant(matrix):
    a = [list(map(int, row)) for row in matrix]
    n = len(a)
    if n == 0:
        return 1
    sign, previous = 1, 1
    for k in range(n-1):
        if a[k][k] == 0:
            pivot = next(i for i in range(k+1, n) if a[i][k])
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                numerator = a[i][j]*pivot-a[i][k]*a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator//previous
            a[i][k] = 0
        previous = pivot
    return sign*a[-1][-1]

def sums_closed(m, t):
    n = (m+1)*(m+2)//2+t*(m+1)
    a = m*(m+1)*(m+2)//3+t*m*(m+1)//2
    b = m*(m+1)*(m+2)//6+(m+1)*t*(t+1)//2+t*m*(m+1)//2
    return n, a, b, a

def indices(m, t):
    return ([(i, 0, k) for k in range(m+1) for i in range(m-k+1)]
            + [(0, j, k) for j in range(1, t+1) for k in range(m+1)])

def matrix(m, t, A=22, e=101, X=2, Y=3):
    rows = []
    for i, j, k in indices(m, t):
        row = {}
        # Expand x^i y^j (1+A*x+x*y)^k e^(m-k).
        for a in range(k+1):
            for b in range(k-a+1):
                exponent = (i+a+b, j+b)
                c = comb(k, a)*comb(k-a, b)*A**a*e**(m-k)
                row[exponent] = row.get(exponent, 0)+c
        rows.append(row)
    support = sorted(set().union(*(row.keys() for row in rows)))
    B = [[row.get((a,b),0)*X**a*Y**b for a,b in support] for row in rows]
    return B, support

checks = 0
for m in range(1, 6):
    for t in range(0, 6):
        n, a, b, c = sums_closed(m,t)
        brute = [(i+k,j+k,m-k) for i,j,k in indices(m,t)]
        assert (n,a,b,c) == (len(brute), *(sum(v[z] for v in brute) for z in range(3)))
        B, support = matrix(m,t)
        assert len(B) == len(support) == n
        assert abs(determinant(B)) == 2**a*3**b*101**c
        checks += 1
print(f'PASS: {checks} expanded matrices; exact determinants and exponent sums')

n,a,b,c = sums_closed(20,8)
assert (n,a,b,c) == (399,4760,3976,4760)
lhs = Fraction(285,1000)*a+Fraction(1,2)*b+c
assert lhs == Fraction(81046,10)
assert Fraction(20*n,1)-lhs == Fraction(-623,5)
print('PASS: m=20, t=8: n=399; lhs=8104.6; ceiling=7980; deficit=124.6')

tau = (sqrt(7)-2)/3
bound = (1+3*tau-3*tau*tau)/(4+6*tau)
assert abs(bound-(7/6-sqrt(7)/3)) < 1e-14
print(f'PASS: optimum tau={tau:.12f}; full-strip bound={bound:.12f}')
penalty = n*(n-1)/(4*1000)+n*log2(n)/(2*1000)
print(f'At log2(N)=1000, the square-matrix LLL/HG log_N penalty is {penalty:.6f}')

# Cauchy-Binet for C=[[1,1,0],[0,1,1]], D=diag(1,2,3).
B = [[1,2,0],[0,2,3]]
G = [[sum(x*y for x,y in zip(r,s)) for s in B] for r in B]
assert determinant(G) == 49 == 4+9+36
print('PASS: rectangular Gram determinant = sum of squared maximal minors = 49')

# Equal leading monomials need not mean dependent coefficient rows.
assert determinant([[1,1],[1,-1]]) == -2
print('PASS: x+y and x-y share leading x but remain independent')
```
