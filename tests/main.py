import unittest

loader = unittest.TestLoader()
suite = unittest.TestSuite()


import pages_page_tests
import pages_registry_tests
import mycms_misc_tests
import mycms_model_tests
import mycms_serializers_tests
import pages_api_tests
import pages_serializer_tests


suite.addTests(loader.loadTestsFromModule(pages_page_tests))
suite.addTests(loader.loadTestsFromModule(pages_registry_tests))
suite.addTests(loader.loadTestsFromModule(pages_api_tests))
suite.addTests(loader.loadTestsFromModule(mycms_misc_tests))
suite.addTests(loader.loadTestsFromModule(mycms_model_tests))
suite.addTests(loader.loadTestsFromModule(mycms_serializers_tests))
suite.addTests(loader.loadTestsFromModule(pages_serializer_tests))

runner = unittest.TextTestRunner(verbosity=1)
result = runner.run(suite)