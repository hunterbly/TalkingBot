import os
import os.path as op
import unittest

__all__ = [
    op.splitext(f)[0]  # remove .py extension
    for f in os.listdir(BASE_DIR)  # list contents of current dir
    if not f.startswith('_') and
    ((op.isfile(op.join(BASE_DIR, f)) and f.endswith('.py')) or
     (op.isdir(op.join(BASE_DIR, f)) and op.isfile(op.join(BASE_DIR, f, '__init__.py'))))
]

from . import *  # to make `scripts.script1` work after `import script`
