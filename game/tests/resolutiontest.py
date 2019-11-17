import unittest
import main

class TestResolutionFunctions(unittest.TestCase):
    def test_getLargestFittingResolution_baseResolution(self):
        result = main.getLargestFittingResolution((320, 240), (320, 240))
        self.assertEqual((320,240), result)

    def test_getLargestFittingResolution_largerResolutionAvailable(self):
        result = main.getLargestFittingResolution((320, 240), (640, 480))
        self.assertEqual((640,480), result)

    def test_getLargestFittingResolution_largerResolutionDifferentRatio(self):
        result = main.getLargestFittingResolution((320, 240), (1152, 864))
        self.assertEqual((960,720), result)

    def test_isMultipleOfBaseResolution_sameResolution(self):
        result = main.isMultipleOfBaseResolution((320, 240), (320, 240))
        self.assertTrue(result)

    def test_isMultipleOfBaseResolution_doubleResolution(self):
        result = main.isMultipleOfBaseResolution((320, 240), (640, 480))
        self.assertTrue(result)

    def test_isMultipleOfBaseResolution_different(self):
        result = main.isMultipleOfBaseResolution((320, 240), (1152, 864))
        self.assertFalse(result)

    def test_getFittingDisplaySize(self):
        result = main.getFittingDisplaySize((320, 240), [(640, 480), (720, 480)])
        self.assertEqual((640, 480), result)