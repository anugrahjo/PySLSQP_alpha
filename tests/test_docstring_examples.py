'''
This file contains tests for the examples within docstrings.
'''
import os
import sys
here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(here, '../pyslsqp'))  # Add the pyslsqp directory to the Python path
import doctest

# def test_main():
#     import main
#     failures, _ = doctest.testmod(main)
#     assert failures == 0, 'One or more doctests failed in main.py'

# import pytest

# @pytest.mark.visualize
# def test_visualize():
#     import visualize
#     failures, _ = doctest.testmod(visualize)
#     assert failures == 0, 'One or more doctests failed in visualize.py'


# def test_save_and_load():
#     import save_and_load
#     failures, _ = doctest.testmod(save_and_load)
#     assert failures == 0, 'One or more doctests failed in save_and_load.py'

# if __name__ == '__main__':
#     test_main()
#     test_visualize()
#     test_save_and_load()