import unittest
import textUI
import logicSimulator
import device


class TestDeviceOutput(unittest.TestCase):
    def testIPin(self):
        pin = device.IPin(0)
        self.assertEqual(pin.getOutput(), 0)
        pin = device.IPin(1)
        self.assertEqual(pin.getOutput(), 1)

    def testGateAND(self):
        gate = device.GateAND()
        for pin in [device.IPin(1)]*3:
            gate.addInputPin(pin)
        self.assertEqual(gate.getOutput(), 1)
        for i in range(3):
            gate.iPins = [device.IPin(0), device.IPin(0), device.IPin(0)]
            gate.iPins[i].output = 1
            self.assertEqual(gate.getOutput(), 0)

    def testGateNOT(self):
        gate = device.GateNot()
        gate.addInputPin(device.IPin(0))
        self.assertEqual(gate.getOutput(), 1)
        gate.iPins = [device.IPin(1)]
        self.assertEqual(gate.getOutput(), 0)

    def testGateOR(self):
        gate = device.GateOR()
        for pin in [device.IPin(0)]*3:
            gate.addInputPin(pin)
        self.assertEqual(gate.getOutput(), 0)
        for i in range(3):
            gate.iPins = [device.IPin(1), device.IPin(1), device.IPin(1)]
            gate.iPins[i].output = 0
            self.assertEqual(gate.getOutput(), 1)

    def testOPin(self):
        oPin = device.OPin()
        oPin.addInputPin(device.IPin(0))
        self.assertEqual(oPin.getOutput(), 0)
        oPin.iPins = [device.IPin(1)]
        self.assertEqual(oPin.getOutput(), 1)

class TestLogicSimulatorCommand(unittest.TestCase):
    def testLoad(self):
        pass
    def testGetHeader(self):
        pass

class TestTextUI(unittest.TestCase):
    def testDisplayMenu(self):
        pass
    def testProcessCommand(self):
        pass
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDeviceOutput))
    # suite.addTest(unittest.makeSuite(TestLogicSimulatorCommand))
    unittest.TextTestRunner().run(suite)
