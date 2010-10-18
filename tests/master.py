#!/usr/bin/env python
import unittest

from coq_proofweb import Test_CP

if __name__ == '__main__':
  suite = unittest.TestSuite()
  suite.addTests([Test_CP.get_suite()])
  unittest.TextTestRunner(verbosity = 2).run(suite)
