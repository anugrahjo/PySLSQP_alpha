# PySLSQP

<!---
[![Python](https://img.shields.io/pypi/pyversions/py_slsqp)](https://img.shields.io/pypi/pyversions/py_slsqp)
[![Pypi](https://img.shields.io/pypi/v/py_slsqp)](https://pypi.org/project/py_slsqp/)
[![Coveralls Badge][13]][14]
[![PyPI version][10]][11]
[![PyPI Monthly Downloads][12]][11]
-->

[![GitHub Actions Test Badge](https://github.com/LSDOlab/py_slsqp/actions/workflows/actions.yml/badge.svg)](https://github.com/py_slsqp/py_slsqp/actions)
[![Forks](https://img.shields.io/github/forks/LSDOlab/py_slsqp.svg)](https://github.com/LSDOlab/py_slsqp/network)
[![Issues](https://img.shields.io/github/issues/LSDOlab/py_slsqp.svg)](https://github.com/LSDOlab/py_slsqp/issues)

The SLSQP algorithm is designed to solve nonlinear programming (NLP) problems.
PySLSQP is a Python package that wraps the original SLSQP algorithm written in Fortran.
While the Fortran code is sourced from `scipy.optimize.minimize`, 
PySLSQP significantly extends its functionality 
by offering new features for further analysis of optimization problems, 
thereby significantly improving the utility of the original algorithm.
The prebuilt packages for various system architectures are available on PyPI for download, 
thus avoiding the need for the user to compile the Fortran sources.


Some of the additional features provided by PySLSQP include:

- **Data Saving**: PySLSQP allows you to save optimization data during the optimization process. 
  This can be useful for analyzing the progress of the optimization, for post-processing purposes, 
  or for warm/hot restart of the optimization.

- **Warm/Hot Starting**: PySLSQP supports warm/hot starting, enabling users to initialize the optimization 
  algorithm with a previously saved solution. This can be particularly useful when you want to restart an 
  optimization from a previous solution or continue the optimization that was terminated
  for various reasons.

- **Live Visualization**: PySLSQP provides the capability to visualize the optimization progress in real-time,
  enabling users to monitor the convergence via the optimality and feasibility measures.
  This also helps the users understand how the objective function, constraints, and design variables 
  are changing during the optimization.

- **Scaling**: PySLSQP allows you to independently scale the objective function, constraints, and design variables, 
  separate from their original definitions.
  Scaling can help improve the convergence behavior of the optimization algorithm and make it more robust.

- **More Internal Optimization Variables**: PySLSQP provides access to additional internal optimization variables,
  like optimality, feasibility, Lagrange multipliers, etc. which can be useful for advanced analysis 
  of your problem. The original callback function in `scipy.optimize.minimize` only returned the optimization
  variable iterates.

These additional features make PySLSQP a powerful tool for solving constrained optimization problems in Python.
In addition, PySLSQP also supports the estimation of gradients using first-order finite differencing, 
as in the Scipy version. 

## Dependencies
Before installing PySLSQP, make sure you have the dependencies installed.
Numpy is the minimum requirement for using PySLSQP. 
[numpy](https://numpy.org/install/) can be installed from PyPI with
```sh
pip install numpy
```
Additionally, if you need to save optimization data and visualize different variables during the optimization,
install `h5py` and `matplotlib` respectively.
All the dependencies can be installed at once with 
```sh
pip install numpy h5py matplotlib
```

## Installation

To install the latest release of PySLSQP on PyPI, run on the terminal or command line
```sh
pip install pyslsqp
```

To install the latest commit from the main branch, run
```sh
pip install git+https://github.com/LSDOlab/PySLSQP.git@main
```

To upgrade PySLSQP from an older version to the latest released version on PyPI, run
```sh
pip install --upgrade pyslsqp
```

To uninstall PySLSQP, run
```sh
pip uninstall pyslsqp
```

## Testing
To test if the package works correctly and as intended, install `pytest` using
```sh
pip install pytest
```

and run the following line on the terminal from the project root directory:
```sh
pytest
```

## Usage
Most features of the PySLSQP package can be accessed through the `pyslsqp` function.
However, there are some additional utility functions that are available to load various information 
from the saved data files.
Here is a small optimization example that minimizes `x^4 + y^4`.
```python
import numpy as np
from pyslsqp import pyslsqp

# `v` represents the vector of optimization variables
def objective(v):
    # the objective function
    return v[0]**4 + v[1]**4

x0 = np.array([1., 1.])
# pyslsqp returns a dictionary that contains the reults from optimization
results = pyslsqp(x0, obj=objective)
print(results)
```
Note that we did not provide the gradient for the objective function above.
In the absence of user-provided gradients, `pyslsqp` estimates the gradients
using first-order finite differencing.
However, it is always more efficient for the user to provide the exact gradients
as will be shown in the next example.

The above example does not have any constraints or variable bounds. 
Now, let's look at a slightly more complex example that minimizes `x^4 + y^4` 
subject to the constraints `x+y=1` and `3x+2y>=1`, and the bounds `x>=0.4` and `y<=0.6`.

```python
import numpy as np
from pyslsqp import pyslsqp

# `v` represents the vector of optimization variables
def objective(v):
    # the objective function
    return v[0]**4 + v[1]**4

def gradient(v):
    # the gradient of the objective function
    return np.array([4*v[0]**3, 4*v[1]**3])

def constraints(v):
    # the constraint functions formulated as c_eq(x) = 0, c_ineq(x) >= 0
    return  np.array([v[0] + v[1] - 1, 3*v[0] + 2*v[1] - 1])

def jacobian(v):
    # the jacobian of the constraint functions
    return np.array([[1, 1], [3, 2]])

# lower bounds on the optimization variables
x_lower = np.array([0.4, -np.inf])
# upper bounds on the optimization variables
x_upper = np.array([np.inf, 0.6])
# number of equality constraints (at the beginning of the constraint vector)
num_eqcon = 1

x0 = np.array([2,3])
# pyslsqp returns a dictionary that contains the reults from optimization
results = pyslsqp(x0, obj=objective, grad=gradient, con=constraints, jac=jacobian, meq=num_eqcon, xl=x_lower, xu=x_upper)
print(results)
```

## Documentation
For API reference and more details on installation and usage, visit the [documentation](https://pyslsqp.readthedocs.io/).

## Citation
If you use PySLSQP in your work, please use the following reference for citation:

```
@Misc{pyslsqp,
author = "Anugrah Jo Joshy",
title = "PySLSQP",
howpublished = "\url{https://github.com/anugrahjo/PySLSQP}",
year = "2024",
}
```

## Bugs, feature requests, questions
Please use the [GitHub issue tracker](https://github.com/anugrahjo/PySLSQP/issues) for reporting bugs, requesting new features, or any other questions.

## Contributing
We always welcome contributions to PySLSQP. 
Please refer the [`CONTRIBUTING.md`](https://github.com/anugrahjo/PySLSQP_alpha/blob/main/CONTRIBUTING.md) 
file for guidelines on how to contribute.

## License
This project is licensed under the terms of the **BSD license**.
