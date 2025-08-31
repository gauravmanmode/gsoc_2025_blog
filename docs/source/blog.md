# GSoC 2025 with Optimagic: Adding More Optimizer Interfaces to Optimagic
---

# Intro 📝

This is my final report and blog post for my Google Summer of Code 2025 project, titled ['Adding More Optimizer Interfaces to Optimagic'](https://summerofcode.withgoogle.com/programs/2025/projects/j9i3Vx5T), under the [NumFOCUS](https://numfocus.org/) organization, working on the [Optimagic Project](https://estimagic.org/), supported by NumFOCUS.

## Motivation
I am a graduate student in Mathematics. I love topology, and also worked on numerical methods during my dissertation. Working with optimagic gave me the perfect opportunity to dive into optimization techniques. While my coursework covered boring topics, working on Optimagic introduced me to state-of-the-art algorithms used in real-world applications.

## Why Optimization Needs a Little Magic
Optimization is challenging because real-world problems are complex. Functions can be non-linear, non-differentiable, or have multiple optima, making it tough to pinpoint the best solution. For instance, in machine learning, black-box functions where only inputs and outputs are known can be noisy, high-dimensional, or feature steep valleys and flat plateaus, which challenge most algorithms. Some problems require finding global optima, while others need local solutions, and choosing the wrong algorithm can lead to poor results. No single algorithm solves every optimization problem. Depending on the problem’s characteristics, one algorithm may outperform another.

Moreover, switching between algorithms often involves rewriting code between libraries, which is frustrating for researchers and developers focused on solving their problems.

Optimagic addresses these challenges by offering a unified interface for a wide range of optimizers, from gradient-based to derivative-free. Users can switch algorithms seamlessly without modifying their code.

# 🪄 Optimagic: A Unified Interface to Optimizers 
Optimagic allows users to experiment with any supported optimizer using a consistent interface similar to that of scipy's. Simply change the algorithm, and optimagic handles the rest. Featuring, 

### Flexibility at its core.
[PyTrees](https://optimagic.readthedocs.io/en/latest/development/ep-01-pytrees.html) enable Optimagic to handle a wide variety of input formats, making it highly flexible.

### Consistency is the key
Optimagic standardizes parameter names across optimizers. For example, all stopping criteria start with `stopping_maxiter` (maximum number of iterations), and all convergence criteria begin with `convergence_ftol_rel` (relative function tolerance).

# Code Contributions 💻
The primary objective was to add more optimizers to Optimagic, also some additional changes were done. These are detailed below.

## Optimizers from Nevergrad [(Merged)](https://github.com/optimagic-dev/optimagic/pull/591)
This was a pretty big PR and I worked on this from Week 1 to Week 4.

### Why Nevergrad?
Nevergrad offers a robust set of derivative-free optimization algorithms. Integrating these into Optimagic would allows users to leverage cutting-edge methods through a same API. In machine learning and AI, black-box functions—where only inputs and outputs are known, and the internal workings are non-differentiable and non-convex benefit greatly from derivative-free methods, which effectively explore the function landscape to find optima.

- **Covariance Matrix Adaptation Evolution Strategy (CMA-ES)**  
  CMA-ES has many parameters, and I analyzed them to identify those most critical to its adaptation process.

- **OnePlusOne Evolution Strategy**  
  This is a simplified variant of CMA-ES where \((\mu, \lambda) = (1, 1)\), meaning one parent generates one offspring per iteration.

- **Random Search**  
  A one-shot method for sampling the search space which serves as the baseline.

- **Sampling Search**  
  Improved over Random Search.

- **Differential Evolution**  
  A population-based method for global optimization.

- **Bayesian Optimization**  
  A wrapper around the `bayes_optim` package.

- **Estimation of Distribution Algorithm (EDA)**  
  A probabilistic method for adaptive sampling.

- **Test-Based Population Sampling Adaptation**  
  An algorithm for continuous noisy optimization.

- **Estimation of Multivariate Normal Algorithm (EMNA)**  
  A probabilistic method for adaptive sampling. When papers were unavailable, I delved deeply into the code to understand its mechanics.

- **NGOPT Optimizers**  
   NGOpt (Nevergrad Optimizer) is the optimizer selection wizard of Nevergrad. Nevergrad’s meta-optimizers dynamically switch between algorithms based on the function landscape and optimization history.

- **META Optimizers**  
  These combine derivative-free global optimizers with derivative-based local optimizers to refine solutions.

```{note}
We skipped SPSA from Nevergrad due to failing tests and lack of tunable parameters. I also excluded optimizers like ConfSplit, as their functionality can be achieved through multiple optimization runs.
```

### Example usage 

```python
import optimagic as om
om.minimize(
    fun=lambda x: x@x,
    params=om.Bounds(lower=np.full(3,-5), upper=np.full(3,5)),
    algorithm=om.algos.nevergrad_meta(optimizer="BFGSCMAPlus")
)
```

## Adding `needs_bounds` and `supports_infinite_bounds` fields in the AlgoInfo [(Merged)](https://github.com/optimagic-dev/optimagic/pull/610)
During Week 5 and Week 6 I worked on this PR.

While global optimizers typically require bounds, optimizers from Nevergrad can operate without bounds by which in case sample from a normal distribution with given standard deviation. This was a open issue . Local algorithms often run unbounded, while global ones need bounds.I researched which algorithms could run without bounds and which supported infinite bounds. As a result, we added two new fields to the AlgoInfo class: `needs_bounds` and `supports_infinite_bounds`.
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
```

```python
my_selection2 = [
    algo
    for algo in algos_with_bounds_support
    if algo.algo_info.supports_infinite_bounds
]
```

## Migrate Nevergrad optimizers to new documentation style [(Open)](https://github.com/optimagic-dev/optimagic/pull/632)
Previously, documentation was stored in `algorithms.md` and optimizers in `optimizers.py`. I migrated Nevergrad optimizers to Optimagic’s new documentation style, embedding details in class docstrings and parameter docstrings to follow the new style. With this, I also cleaned up any remaining work and linked issues.

## Wrap Local Optimizers from Gradient-Free Optimizers [(Open)](https://github.com/optimagic-dev/optimagic/pull/624)
After discussing with my mentor, we decided to wrap optimizers from this library and worked on this and following PR during Week 7 to Week 11.

These optimizers work on a discrete search space, requiring bounds to be translated into a grid, used helper functions for this process. I also added documentation and tests to ensure reliability.

A challenge was that these global optimizers struggled to pass tests due to low accuracy and search space limitations.

These are all local algorithms:

- **Hill Climbing**  
  A local optimization method that iteratively moves to better neighboring solutions.

- **Stochastic Hill Climbing**  
  A variant of hill climbing that incorporates randomness to escape local optima.

- **Simulated Annealing**  
  A probabilistic technique that mimics the cooling process to find global optima, though used here for local optimization.

- **Repulsing Hill Climbing**  
  A variation of hill climbing that avoids revisiting solutions.

- **Downhill Simplex Optimization**  
  A derivative-free method using a simplex to navigate the search space.

- **Powell's Method**  
  A local optimization technique using conjugate directions. 

I am very thankful to the developer of Gradient-Free Optimizers for patiently helping me understand the workings and clarify any doubts which I had.  
  [No improvement even after many iterations with some algorithms](https://github.com/SimonBlanke/Gradient-Free-Optimizers/issues/84)

## Wrap Population-Based Optimizers from Gradient-Free Optimizers [(Open)](https://github.com/optimagic-dev/optimagic/pull/636)
Thanks to the exposed converter, population-based algorithms can now be initialized with a initial population.
The following algorithms are now available in optimagic.

- **Particle Swarm Optimization**  
  This is a population-based method inspired by the social behavior of flocks.

- **Spiral Optimization**  
  A global method that searches the space in a spiral pattern.

- **Genetic Algorithm**  
  A population-based method using principles of natural selection.

- **Evolution Strategy**  
  A population-based method c that evolves a population of solutions.

- **Differential Evolution**  
  A population-based method for global optimization, also implemented in Nevergrad.

### Rework `test_many_algorithms`
We refactored the test suite to include dynamic tests for `needs_bounds` and `supports_infinite_bounds`. We also introduced a dictionary to specify precision requirements for certain algorithms.

### New Example in class SphereExampleInternalOptimizationProblemWithConverter
PyTrees enable Optimagic to handle diverse inputs. Previously, a test object for PyTrees was missing, so I added an example in `internal_optimization_problem.py` to support testing with dictionary inputs via converter functions.

Example snippet

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

ensmallen is a fast C++ library for efficient objective functions. This is pending due to inactivity in the pyensmallen repository . Once a dependent PR is merged, this will be completed.  
[Cleaned Report callback PR](https://github.com/apoorvalal/pyensmallen/pull/17)

## Issues raised by me:
- [Improve handling of internal nonlinear_constraints](https://github.com/optimagic-dev/optimagic/issues/606)
- [Improper docs build of How to guide - How to specify params bug](https://github.com/optimagic-dev/optimagic/issues/628)
- [bayesian_optimization](https://github.com/facebookresearch/nevergrad/issues/1701)
- [Unable to retrieve loss for Parametrized CMA](https://github.com/facebookresearch/nevergrad/issues/1697)

## What does this mean
By integrating these optimizers, Optimagic now offers a more comprehensive toolkit for tackling optimization challenges.

## Future Work

### Wrap Grid Search and SMBO-Based Optimizers from Gradient-Free Optimizers
I plan to wrap Grid Search and other optimizers, including:
- Bayesian Optimization
- Tree-Structured Parzen Estimators
- Forest Optimization

### Maintenance 🛠️
- Support for nonlinear constraints with optimizers from Nevergrad
- Document particular portfolio and meta optimizers in `nevergrad_meta` and `nevergrad_ngopt` which are not documented sufficiently in 
the nevergrad documentation but which can be sourced through other papers.
- Support for nonlinear constraints with optimizers from Gradient-Free Optimizers

## Acknowledgements
I am deeply grateful to the following individuals and institutions for their support:

Firstly, I thank my GSoC mentors [Janos Gabler](https://github.com/janosg) and [Tim Mensinger](https://github.com/timmens) for their warm welcome, openness to new ideas, and fostering a constructive and engaging discussion environment.

I also appreciate the contributions of community members who provided valuable feedback and comments on my pull requests.

Finally, I express my gratitude to the Google Summer of Code program for providing the opportunity and financial support, enabling me to pursue my academic interests and enhance my technical skills with minimal constraints.