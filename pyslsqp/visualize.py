import warnings
import numpy as np
import time

try:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

except ImportError:
    warnings.warn("matplotlib not found, plotting disabled.")
    plt = None

class Visualizer:

    def __init__(self, visualize_vars, summary_filename):
        '''
        Initialize the visualizer with the variables to visualize. 
        The variables should be a list of strings, where each string is the name of a variable to visualize. 
        The variables can be any of the following:
            - 'objective'       : the objective function value
            - 'optimality'      : the optimality condition
            - 'feasibility'     : the feasibility condition
            - 'x[i]'            : the ith variable value
            - 'constraints[i]'  : the ith constraint value
            - 'jacobian[i,j]'   : the (i,j) element of the Jacobian matrix
            - 'gradient[i]'     : the ith gradient value
            - 'multipliers[i]'  : the ith Lagrange multiplier value

        Creates an interactive plot with the specified variables on the y-axis and the iteration number on the x-axis.
        The plots are stacked vertically in the order they are specified in the list.
        The plot is updated with the latest values of the variables after each iteration.
        '''

        v_start = time.time()
        if plt is None:
            raise ImportError("matplotlib not found, cannot visualize.")
        self.visualize_vars = visualize_vars
        plt.ion()
        lines_dict = {}
        var_dict = {}
        n_plots = len(visualize_vars)
        self.fig, self.axs = plt.subplots(n_plots, figsize=(10, 3*n_plots))
        self.fig.suptitle(f'SLSQP Optimization [{summary_filename}]')
        for ax, var in zip(self.axs, visualize_vars):
            # ax.set_title(var)
            # ax.set_xlabel('Iteration')
            ax.set_ylabel(var)
            var_dict[var] = []
            if var in ['optimality', 'feasibility']:
                lines_dict[var], = ax.semilogy([], [], label=var)
            else:
                lines_dict[var], = ax.plot([], [], label=var)
            ax.legend()
        self.lines_dict = lines_dict
        self.var_dict = var_dict

        self.vis_time = time.time() - v_start
        self.wait_time = 0.0

    def update_plot(self, out_dict):
        '''
        Update the plot with the latest values of the variables.
        Appends the values of scalar iterates after each iteration in the var_dict attribute before updating the plot.
        The out_dict should be a dictionary containing the following
        keys:
            - 'majiter'     : the number of major iterations
            - 'objective'   : the objective function value
            - 'optimality'  : the optimality condition
            - 'feasibility' : the feasibility condition
            - 'x'           : the variable values
            - 'constraints' : the constraint values
            - 'jacobian'    : the Jacobian matrix
            - 'gradient'    : the gradient values
            - 'multipliers' : the Lagrange multiplier values
        '''

        v_start = time.time()
        x_data = np.arange(out_dict['majiter']+1)
        for k, var in enumerate(self.visualize_vars):
            if var in ['objective', 'optimality', 'feasibility']:
                self.var_dict[var].append(out_dict[var]*1.0) # *1.0 is necessary so that the value is not a reference
            elif var.startswith('jacobian['):
                idx1, idx2 = map(int, var[9:-1].split(','))
                self.var_dict[var].append(out_dict[var.split('[')[0]][idx1, idx2])
            else:
                if var.startswith('x['):
                    idx = int(var[2:-1])
                elif var.startswith('constraints['):
                    idx = int(var[12:-1])
                elif var.startswith('gradient['):
                    idx = int(var[9:-1])
                elif var.startswith('multipliers['):
                    idx = int(var[12:-1])
                self.var_dict[var].append(out_dict[var.split('[')[0]][idx])
            
            self.lines_dict[var].set_data(x_data, self.var_dict[var])
                
            # Rescale the plot
            self.axs[k].relim()
            self.axs[k].autoscale_view()

        # time.sleep(0.5)

        # Redraw the plot
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        self.vis_time += time.time() - v_start

    def keep_plot(self):
        '''
        Keep the plot open after the optimization is completed.
        '''
        w_start = time.time()
        plt.ioff()
        plt.show()
        self.wait_time += time.time() - w_start



def visualize(savefilename, visualize_vars, itr_start=0, itr_end=-1, major_only=False):
    '''
    Visualize different scalar variables using the saved data in a file.

    The variables to visualize should be a list of strings, where each string is the name of a variable to visualize. 
    The variables can be any of the following:
    
        - 'objective'       : the objective function value
        - 'optimality'      : the optimality condition
        - 'feasibility'     : the feasibility condition
        - 'x[i]'            : the ith variable value
        - 'constraints[i]'  : the ith constraint value
        - 'jacobian[i,j]'   : the (i,j) element of the Jacobian matrix
        - 'gradient[i]'     : the ith gradient value
        - 'multipliers[i]'  : the ith Lagrange multiplier value

    Creates a plot with the specified variables on the y-axis and the iteration number on the x-axis.
    The plots are stacked vertically in the order they are specified in the list.

    Parameters
    ----------
    savefilename : str
        Path to the saved file.
    visualize_vars : str or list of str
        List of variables to visualize.
    itr_start : int, default=0
        Starting iteration to visualize.
        Negative indices are allowed with -1 representing the last iteration
        and -2 representing the second last iteration and so on.
    itr_end : int, default=-1
        Ending iteration to visualize.
        Negative indices are allowed with -1 representing the last iteration
        and -2 representing the second last iteration and so on.
    major_only : bool, default=False
        If True, only major iterations are visualized.
        If False, all iterations are visualized irrespective of major or line search iterations.
    '''

    v_start = time.time()
    if plt is None:
        raise ImportError("matplotlib not found, cannot visualize.")
    from pyslsqp.postprocessing import load_variables
    if isinstance(visualize_vars, str):
        visualize_vars = [visualize_vars]
    var_dict = load_variables(savefilename, visualize_vars, itr_start=itr_start, itr_end=itr_end, major_only=major_only)
    
    x_data = np.arange(len(var_dict[visualize_vars[0]]))
    n_plots = len(visualize_vars)
    fig, axs = plt.subplots(n_plots, figsize=(10, 3*n_plots))
    fig.suptitle(f'SLSQP Optimization [{savefilename}]')
    for ax, var in zip(axs, visualize_vars):
        # ax.set_title(var)
        # ax.set_xlabel('Iteration')
        ax.set_ylabel(var)
        if var in ['optimality', 'feasibility']:
            ax.semilogy(x_data, var_dict[var], label=var)
        else:
            ax.plot(x_data, var_dict[var], label=var)

        ax.legend()

    plt.show()
    vis_time = time.time() - v_start