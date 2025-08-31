---
file_format: mystnb
kernelspec:
  name: python3
---

# GSoC 2025 with Optimagic: Adding More Optimizer Interfaces to Optimagic
---

## Intro

``` python
import optimagic as om
```

This is a blog for the Google Summer of Code 2024 project, entitled ['Adding More Optimizer Interfaces to Optimagic'](https://summerofcode.withgoogle.com/programs/2024/projects/), under the [NumFOCUS](https://numfocus.org/) organization, on the [Optimagic Project](https://estimagic.org/), which is supported by NumFOCUS.

## Why would I do this
Math reading is a skill. I just need a reason to and I got it.


## Optimagic: One Interface, Many Optimizers
This gives the ability to try out any optimizer currently in optimagic using the same interface. Just change the algorithm, no need to worry about the backend. optimagic will handle it.
# What to do
Our focus was on quality over quantity. My mentor guided me and said that even if we are able to wrap a few optimizers less, it is fine as long as they are complete and accurate.

## PyTrees
PyTrees are what makes optimagic very versatile in its input.

## Harmonizing names, API, everything..
Optimagic harmonizes paramters names across optimizers. like all stopping criteria start with `stopping_maxiter`meaning maximum number of iterations, all convergencce criteria start with `convergence_ftol_rel` meaning relative function tolerance.

## Code Contributions
While the primary objective was adding more optimizers to optimagic a number of additional changes. These changes are outlined below in order.

## Optimizers from Nevergrad[(Merged)](https://github.com/optimagic-dev/optimagic/pull/591)

### Why Nevergrad?
Nevergrad provides a rich collection of derivative-free optimization algorithms. By integrating these into Optimagic, users can now experiment with cutting-edge techniques using the same API.

### Covariance Matrix Adaptation Evolution Strategy
CMAES had many controlling parameters. I had to look through all of them to determine which were the ones having most influence on the adaption process.

### OnePlusOne Evolution Strategy
This is variant of the CMAES where (mu, lambda) is (1,1).

### Random Search


### Sampling Search

### Differential Evolution


### Bayesian Optimization
This is a wrapper over the `bayes_optim` package.

### Estimation of Distribution Algorithm

### Test-Based Population Sampling Adaptaion

### Estimation of Multivariate Normal Algorithm (EMNA)

When I dont find the papers, I dig deep, deep into the code.
### NGOPT Optimizers
Nevergrad has many meta optmizers which switch between different optimizers with budgets depending on the function landscape and history.

### META Optimizers
Nevergrad has many meta optmizers which combine and derivative free global optimizers and then taker over by derivate based local optimizers to find the solution 

### Example usage of Meta Optimizer

```python
import optimagic as om
om.minimize(
    fun = lambda x: x@x,
    params = om.Bounds(lower = np.full(3,-5), upper = np.full(3,5))
    algorithm = om.algos.nevergrad_meta(optimizer= "BFGSCMAPlus")
            )
```

### Adding `needs_bounds` and `supports_infinite_bounds` fields in the AlgoInfo [(Merged)](https://github.com/optimagic-dev/optimagic/pull/610)

While all global optimizers run with bounds, optimizers from nevergrad can run without bounds where bounds are implicitly derived from a normal distribution whose standard deviation can be set.
This was raised in an issue.
This entailed reading up and understanding which algorithms could run without bounds and which supported infinite bounds. Obviously, local algorithms run unbounded and global ones require bounds to run.
Hence, we introduced two new fields in the AlgoInfo class, namely `needs_bounds` and `supports_infinite_bounds`.
Also added a guide on how to use it for filtering the algorithms more finely.

```python
from optimagic.algorithms import AVAILABLE_ALGORITHMS

algos_with_bounds_support = [
    algo
    for name, algo in AVAILABLE_ALGORITHMS.items()
    if algo.algo_info.supports_bounds
]
my_selection = [
    algo for algo in algos_with_bounds_support if algo.algo_info.needs_bounds
]
my_selection[0:3]
```

```python
my_selection2 = [
    algo
    for algo in algos_with_bounds_support
    if algo.algo_info.supports_infinite_bounds
]
my_selection2[0:3]
```

## Migrate nevergrad optimizers to new documentation style [(Open)](https://github.com/optimagic-dev/optimagic/pull/632)
Before, documentation lived in algorithms.md and optimizers in optimizers.py.
Then, nevergrad optimizers were migrated to Optimagic’s new documentation style, where optimizers are documented in the class docstrings and parameters in the parameter docstrings.

## Wrap Local Optimizers from Gradient Free Optimizers [(Open)](https://github.com/optimagic-dev/optimagic/pull/624)
These optimizers, the search space is defined discrete for this optimization package. This means translating bounds into a discrete search space for the algorithm to run. Most of these are given to helper functions.
Also, added documentation for each optimizer and tests to make sure nothing breaks.

A challenge here was that these are global optimizers and were unable to passs tests because of their low accuracy and due to the limitation of the search space. 

These are all local algorithms.

### Hill Climbing

### Stochastic Hill Climbing

### Simulated Annealing

### Repulsing Hill Climbing

### Downhill Simplex Optimization

### Simulated Annealing

### Powell's Method


## Wrap Population Based Optimizers from Gradient Free Optimizers [(Open)](https://github.com/optimagic-dev/optimagic/pull/636)

### Particle Swarm Optimization
This is a global optimizer.

### Spiral Optimization

### Genetic Algorithm

### Evolution Strategy

### Differential Evolution

### Rework `test_many_algorithms`
Anyway, we had to refactor tests so we also introduced tests based on algorthm needs bounds and supports infinite bounds. And in a new manner which is dynamic that can be fetched for the test case. Also , we introduced a new dictionary for agotihm that had specific precision requirements for our tests.

### New Example in class SphereExampleInternalOptimizationProblemWithConverter
Pytrees is what makes optimagic very versatile in its input. It can take any input. Previosly, a test object was missing for this, so I
Introduced a new example in the `internal_optimization_problem.py` which could be used for testing with PyTrees. which has converter functions dealing with dictionary inoputs.

```python
import numpy as np
from optimagic.optimization.internal_optimization_problem import SphereExampleInternalOptimizationProblemWithConverter
from optimagic.typing import AggregationLevel
problem = SphereExampleInternalOptimizationProblemWithConverter(solver_type=AggregationLevel.LEAST_SQUARES)
problem.converter.params_to_internal({"x0":2,"x1":3})
problem.converter.derivative_to_internal(
    {
    "x0":{
         "x0":2,
         "x1":3,
        },
   "x1":{
       "x0":2,
       "x1":3
       }
    },
    [2,])
```

## Add L-BFGS optimizer from pyensmallen [(Open)](https://github.com/optimagic-dev/optimagic/pull/566)

ensmallen is a very fast library in C++ for cheap objective functions. This has been pending because of development from the pyensmallen repo.
A challenge here was that the author of this repo was inactive and hence we had trouble with communication. But once a dependeant Pr is merged , this will also be complete.

## What does this mean
By wrapping these optimizers, Optimagic now provides users with an even broader toolkit for local optimization

## Future Work

### Wrap Grid Search and SMBO Based Optimizers from Gradient Free Optimizers
I will be wrazpping Grid Search and other optimizers like
Bayesian Optimization
Tree Structured Parzen Estimators

### Maintenance

Support for nonlinear constraints with optimizers from Nevergrad

Support for nonlinear constraints with optimizers from Gradient Free Optimizers

## Acknowledgements

I would like to express my gratitude to the following individuals and institutions for their support and contributions:

Firstly I would like to my mentors of the GSOC project, for their kind welcome to the community and receptivity to new ideas, as well as for fostering a generally constructive and engaging atmosphere for discussion.
[Janos Gabler](https://janosg.github.io/) and [Tim Mensinger](https://janosg.github.io/) for aware of the possibilty of a GSOC project.

Furthermore, I would be remiss if I did not acknowledge the contributions of all community members who provided assistance through comments and feedback on various pull requests.

In conclusion, I would like to express my gratitude to the Google Summer of Code program for providing me with the opportunity and financial support, which enabled me to pursue my academic interests and enhance my technical abilities with minimal constraints.