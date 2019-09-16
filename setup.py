#+
# Distutils script to install python_pixman. Invoke from the command line
# in this directory as follows:
#
#     python3 setup.py build
#     sudo python3 setup.py install
#
# Written by Lawrence D'Oliveiro <ldo@geek-central.gen.nz>.
#-

import distutils.core

distutils.core.setup \
  (
    name = "Pixman",
    version = "0.3",
    description = "language bindings for the Pixman graphics library, for Python 3.2 or later",
    author = "Lawrence D'Oliveiro",
    author_email = "ldo@geek-central.gen.nz",
    url = "https://github.com/ldo/python_pixman",
    py_modules = ["pixman"],
  )
