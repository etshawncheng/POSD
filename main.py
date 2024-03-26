import unittest
import textUI
import logicSimulator
import device


class TestDeviceOutput(unittest.TestCase):
    def testIPin(self):
        for i in range(2):
            with self.subTest(msg=str(i)):
                pin = device.IPin(i)
                self.assertEqual(pin.getOutput(), i)

    def testGateAND(self):
        gate = device.GateAND()
        for pin in [device.IPin(1)]*3:
            gate.addInputPin(pin)
        with self.subTest(msg=str(gate.iPins)):
            self.assertEqual(gate.getOutput(), 1)
        for i in range(3):
            gate.iPins = [device.IPin(0), device.IPin(0), device.IPin(0)]
            gate.iPins[i].output = 1
            with self.subTest(msg=str(gate.iPins)):
                self.assertEqual(gate.getOutput(), 0)

    def testGateNOT(self):
        gate = device.GateNot()
        gate.addInputPin(device.IPin(0))
        with self.subTest(msg=str(gate.iPins)):
            self.assertEqual(gate.getOutput(), 1)
        gate.iPins = [device.IPin(1)]
        with self.subTest(msg=str(gate.iPins)):
            self.assertEqual(gate.getOutput(), 0)

    def testGateOR(self):
        gate = device.GateOR()
        for pin in [device.IPin(0)]*3:
            gate.addInputPin(pin)
        with self.subTest(msg=str(gate.iPins)):
            self.assertEqual(gate.getOutput(), 0)
        for i in range(3):
            gate.iPins = [device.IPin(1), device.IPin(1), device.IPin(1)]
            gate.iPins[i].output = 0
            with self.subTest(msg=str(gate.iPins)):
                self.assertEqual(gate.getOutput(), 1)

    def testOPin(self):
        oPin = device.OPin()
        oPin.addInputPin(device.IPin(0))
        with self.subTest(msg=str(oPin.iPins)):
            self.assertEqual(oPin.getOutput(), 0)
        oPin.iPins = [device.IPin(1)]
        with self.subTest(msg=str(oPin.iPins)):
            self.assertEqual(oPin.getOutput(), 1)


class TestLogicSimulator(unittest.TestCase):
    def setUp(self):
        self.logicSimulator = logicSimulator.LogicSimulator()

    def testIsLcfFormat(self):
        # file1
        lcf = "3\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg=lcf):
            self.assertTrue(self.logicSimulator.isLcfFormat(lcf))
        # file1 with newline
        lcf = "3\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0\n"
        with self.subTest(msg=lcf):
            self.assertTrue(self.logicSimulator.isLcfFormat(lcf))
        # only one gateinfo
        lcf = "3\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"
        with self.subTest(msg=lcf):
            self.assertTrue(self.logicSimulator.isLcfFormat(lcf))
        # zero device amount
        lcf = "0\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"
        with self.subTest(msg=lcf):
            self.assertTrue(self.logicSimulator.isLcfFormat(lcf))
        # negative device amount
        lcf = "-1\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg=lcf):
            self.assertFalse(self.logicSimulator.isLcfFormat(lcf))
        # no gateinfo
        lcf = "3\n"\
            "1\n"
        with self.subTest(msg=lcf):
            self.assertFalse(self.logicSimulator.isLcfFormat(lcf))
        # invalid gatetype
        lcf = "3\n"\
            "3\n"\
            "4 -1 2.1 3.1 0\n"
        with self.subTest(msg=lcf):
            self.assertFalse(self.logicSimulator.isLcfFormat(lcf))
        # gateinfo no zero ending
        lcf = "3\n"\
            "3\n"\
            "1 -1 2.1 3.1\n"
        with self.subTest(msg=lcf):
            self.assertFalse(self.logicSimulator.isLcfFormat(lcf))

    def testGenerateInputs(self):
        for i in range(1, 4):
            with self.subTest(msg=str(i)):
                self.assertEqual(
                    len(self.logicSimulator.generateInputs(i)), 1 << i)

    def testLoad(self):
        # file1
        lcf = "3\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg=lcf):
            self.assertTrue(logicSimulator.LogicSimulator().load(lcf))
        # no ipin
        lcf = "0\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg=lcf):
            self.assertFalse(logicSimulator.LogicSimulator().load(lcf))
        # no gate
        lcf = "1\n"\
            "0\n"\
            "1 -1 2.1 3.1 0\n"
        with self.subTest(msg=lcf):
            self.assertFalse(logicSimulator.LogicSimulator().load(lcf))
        # gate amount not match
        lcf = "3\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"\
            "3 -2 0\n"
        with self.subTest(msg=lcf):
            self.assertFalse(logicSimulator.LogicSimulator().load(lcf))
        # invalid device type
        lcf = "3\n"\
            "3\n"\
            "4 -1 2.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg=lcf):
            self.assertFalse(logicSimulator.LogicSimulator().load(lcf))
        # no output device
        lcf = "3\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"\
            "3 -2 1.1 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg=lcf):
            self.assertFalse(logicSimulator.LogicSimulator().load(lcf))


#     def testGetHeader(self):
#         pass


# class TestTextUI(unittest.TestCase):
#     def testDisplayMenu(self):
#         pass

#     def testProcessCommand(self):
#         pass


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDeviceOutput))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestLogicSimulator))
    unittest.TextTestRunner(verbosity=3).run(suite)
