# Python implementation of the EFX allocation algorithm
This repository contains code that is a Python implementation of the algorithm in the paper[1]. EFX is a concept of fair allocation. Despite the signficance of the notion, the efficient computation of an EFX allocation for indivisible items remains an open problem.

## What is EFX
EFX, introduced recently by [2] and [3], is an additive relaxation of envy-freeness. Here an agent may envy another agent but only by the value of the least desirable good in the other agent's bundle. While this added flexibility of EFX takes care of extreme pathological cases like the one mentioned above (2 agents, 1 good), this notion is not well understood yet. Despite the active interest in it, it is not known whether EFX allocations always exist, even for 4 agents with additive valuation functions.1 We consider the problem of showing the existence of EFX allocations to be one of the most intriguing currently open questions in fair division.

## Algorithms that now include
This repository gives code to efficiently compute EFX allocations in two cases. 
1. The algorithm "match&freeze" is a polynomial-time algorithm for producing EFX allocations for general 2-value instance. 
2. The algorithm "modified round robin" is suitable for instances where the values of the agents lie in an interval such that the ratio between the maximum and the minimum value is at most 2.(Classify the cases in this way because is because the paper had proved that the difficulty of computing EFX allocations also depends on the ratio between the maximum and the minimum value)

## Reference
```
[1] Georgios Amanatidis et al. “Maximum Nash Welfare and Other Stories About EFX” arXiv: Computer Science and Game Theory(2020): n. pag.
[2] Laurent Gourvès et al. “Near fairness in matroids” European Conference on Artificial Intelligence(2014): n. pag.
[3] Caragiannis, Ioannis, et al. "The unreasonable fairness of maximum Nash welfare." ACM Transactions on Economics and Computation (TEAC) 7.3 (2019): 1-32.
