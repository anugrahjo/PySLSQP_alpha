
from pyslsqp import optimize

def test_simple_example():
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

def test_complex_example():
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


if __name__ == '__main__':
    test_simple_example()
    test_complex_example()
