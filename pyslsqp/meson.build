slsqp_source = custom_target('_slsqpmodule.c',
  input : ['slsqp.pyf'],
  output : ['_slsqpmodule.c'],
  command : [py, '-m', 'numpy.f2py', '@INPUT@', '--lower', '--build-dir', 'pyslsqp/']
)

py.extension_module('_slsqp',
  ['slsqp_optmz.f', slsqp_source],
  incdir_f2py / 'fortranobject.c',
  include_directories: inc_np,
  dependencies : py_dep,
  subdir : 'pyslsqp/',
  install : true
)