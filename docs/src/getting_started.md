# Getting started
This page provides instructions for installing your package 
and running a minimal example.

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
Most features of the PySLSQP package can be accessed through the `optimize` function.
However, there are some additional utility functions that are available to load various information 
from the saved data files.
Here is a small optimization example that minimizes `x^4 + y^4`.
```python
import numpy as np
from pyslsqp import optimize

# `v` represents the vector of optimization variables
def objective(v):
    # the objective function
    return v[0]**4 + v[1]**4

x0 = np.array([1., 1.])
# optimize returns a dictionary that contains the reults from optimization
results = optimize(x0, obj=objective)
print(results)
```
Note that we did not provide the gradient for the objective function above.
In the absence of user-provided gradients, `optimize` estimates the gradients
using first-order finite differencing.
However, it is always more efficient for the user to provide the exact gradients
as will be shown in the next example.

The above example does not have any constraints or variable bounds. 
Now, let's look at a slightly more complex example that minimizes `x^4 + y^4` 
subject to the constraints `x+y=1` and `3x+2y>=1`, and the bounds `x>=0.4` and `y<=0.6`.

```python
import numpy as np
from pyslsqp import optimize

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
# optimize returns a dictionary that contains the reults from optimization
results = optimize(x0, obj=objective, grad=gradient, con=constraints, jac=jacobian, meq=num_eqcon, xl=x_lower, xu=x_upper)
print(results)
```
