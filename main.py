from io import StringIO
from pathlib import Path
import unittest
from unittest.mock import patch

from textUI import Command, TextUI
from logicSimulator import LogicSimulator
from device import GateAND, GateNot, GateOR, IPin, OPin

_PATH = Path(__file__).parent.resolve()


class TestDeviceOutput(unittest.TestCase):
    def testIPin(self):
        for i in range(2):
            with self.subTest(msg=f"iPin input: {i}"):
                pin = IPin(i)
                self.assertEqual(pin.getOutput(), i)

    def testGateAND(self):
        gate = GateAND()
        for pin in [IPin(1)]*3:
            gate.addInputPin(pin)
        with self.subTest(msg=f"ipins: {[ipin.output for ipin in gate.iPins]}"):
            self.assertEqual(gate.getOutput(), 1)
        for i in range(3):
            gate.iPins = [IPin(0), IPin(0), IPin(0)]
            gate.iPins[i].output = 1
            with self.subTest(msg=f"ipins: {[ipin.output for ipin in gate.iPins]}"):
                self.assertEqual(gate.getOutput(), 0)

    def testGateNOT(self):
        gate = GateNot()
        gate.addInputPin(IPin(0))
        with self.subTest(msg=f"ipins: {[ipin.output for ipin in gate.iPins]}"):
            self.assertEqual(gate.getOutput(), 1)
        gate.iPins = [IPin(1)]
        with self.subTest(msg=f"ipins: {[ipin.output for ipin in gate.iPins]}"):
            self.assertEqual(gate.getOutput(), 0)

    def testGateOR(self):
        gate = GateOR()
        for pin in [IPin(0)]*3:
            gate.addInputPin(pin)
        with self.subTest(msg=f"ipins: {[ipin.output for ipin in gate.iPins]}"):
            self.assertEqual(gate.getOutput(), 0)
        for i in range(3):
            gate.iPins = [IPin(1), IPin(1), IPin(1)]
            gate.iPins[i].output = 0
            with self.subTest(msg=f"ipins: {[ipin.output for ipin in gate.iPins]}"):
                self.assertEqual(gate.getOutput(), 1)

    def testOPin(self):
        oPin = OPin()
        oPin.addInputPin(IPin(0))
        with self.subTest(msg=f"ipin input: {oPin.iPins[0].output}"):
            self.assertEqual(oPin.getOutput(), 0)
        oPin.iPins = [IPin(1)]
        with self.subTest(msg=str(oPin.iPins)):
            self.assertEqual(oPin.getOutput(), 1)


class TestLogicSimulator(unittest.TestCase):
    def setUp(self):
        self.logicSimulator = LogicSimulator()

    def testIsLcfFormat(self):
        lcf = "3\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg="file1"):
            self.assertTrue(self.logicSimulator.isLcfFormat(lcf))
        lcf = "3\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0\n"
        with self.subTest(msg="file1 with newline"):
            self.assertTrue(self.logicSimulator.isLcfFormat(lcf))
        lcf = "3\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"
        with self.subTest(msg="only one gateinfo"):
            self.assertTrue(self.logicSimulator.isLcfFormat(lcf))
        lcf = "0\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"
        with self.subTest(msg="zero device amount"):
            self.assertTrue(self.logicSimulator.isLcfFormat(lcf))
        lcf = "-1\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg="negative device amount"):
            self.assertFalse(self.logicSimulator.isLcfFormat(lcf))
        lcf = "3\n"\
            "1\n"
        with self.subTest(msg="no gateinfo"):
            self.assertFalse(self.logicSimulator.isLcfFormat(lcf))
        lcf = "3\n"\
            "3\n"\
            "4 -1 2.1 3.1 0\n"
        with self.subTest(msg="invalid gatetype"):
            self.assertFalse(self.logicSimulator.isLcfFormat(lcf))
        lcf = "3\n"\
            "3\n"\
            "1 -1 2.1 3.1\n"
        with self.subTest(msg="gateinfo no zero ending"):
            self.assertFalse(self.logicSimulator.isLcfFormat(lcf))

    def testGenerateInputs(self):
        for count, pinValues in enumerate(self.logicSimulator.generateInputs(4)):
            num = 0
            for i, v in enumerate(reversed(pinValues)):
                num += v << i
            self.assertEqual(num, count)

    def testLoad(self):
        lcf = "3\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg="file1"):
            self.assertTrue(LogicSimulator().load(lcf))
        lcf = "0\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg="no ipin"):
            self.assertFalse(LogicSimulator().load(lcf))
        lcf = "17\n"\
            "1\n"\
            "1 -1 2.1 3.1 0\n"
        with self.subTest(msg="too many ipin"):
            self.assertFalse(LogicSimulator().load(lcf))
        lcf = "1\n"\
            "0\n"\
            "1 -1 2.1 3.1 0\n"
        with self.subTest(msg="no gate"):
            self.assertFalse(LogicSimulator().load(lcf))
        lcf = "1\n"\
            "1001\n"\
            "1 -1 2.1 3.1 0\n"
        with self.subTest(msg="too many gate"):
            self.assertFalse(LogicSimulator().load(lcf))
        lcf = "3\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"\
            "3 -2 0\n"
        with self.subTest(msg="gate amount not match"):
            self.assertFalse(LogicSimulator().load(lcf))
        lcf = "3\n"\
            "3\n"\
            "1 -1 2.1 3.1 0\n"\
            "3 -2 1.1 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg="no output device"):
            self.assertFalse(LogicSimulator().load(lcf))
        lcf = "3\n"\
            "3\n"\
            "1 -1 4.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg="igateid too big"):
            self.assertFalse(LogicSimulator().load(lcf))
        lcf = "3\n"\
            "3\n"\
            "1 -1 0.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg="igateid cannot be zero"):
            self.assertFalse(LogicSimulator().load(lcf))
        lcf = "3\n"\
            "3\n"\
            "1 -0 2.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg="ipinid cannot be zero"):
            self.assertFalse(LogicSimulator().load(lcf))
        lcf = "3\n"\
            "3\n"\
            "1 -4 2.1 3.1 0\n"\
            "3 -2 0\n"\
            "2 2.1 -3 0"
        with self.subTest(msg="igateid too big"):
            self.assertFalse(LogicSimulator().load(lcf))

    def testGetHeader(self):
        self.logicSimulator.iPins = [IPin()]*3
        self.logicSimulator.oPins = [OPin()]*3
        header = "i i i | o o o\n"\
            "1 2 3 | 1 2 3\n"\
            "------+------"
        self.assertEqual(self.logicSimulator.getHeader(), header)

    def testTruthTable(self):
        self.logicSimulator.iPins = [IPin() for _ in range(2)]
        for ipin in self.logicSimulator.iPins:
            self.logicSimulator.oPins.append(OPin())
            self.logicSimulator.oPins[-1].addInputPin(ipin)
        result = "i i | o o\n"\
            "1 2 | 1 2\n"\
            "----+----\n"\
            "0 0 | 0 0\n"\
            "0 1 | 0 1\n"\
            "1 0 | 1 0\n"\
            "1 1 | 1 1"
        self.assertEqual(self.logicSimulator.getTruthTable(), result)

    @patch("logicSimulator.LogicSimulator.getHeader", new=lambda _: "i i i | o o o\n"
           "1 2 3 | 1 2 3\n"
           "------+------")
    @patch("logicSimulator.LogicSimulator.getPinResult", new=lambda _: "0 1 0 | 0 1 0")
    def testSimulationResult(self):
        result = "i i i | o o o\n"\
            "1 2 3 | 1 2 3\n"\
            "------+------\n"\
            "0 1 0 | 0 1 0"
        self.assertEqual(self.logicSimulator.getSimulitaionResult(), result)

    def testGetPinResult(self):
        for iPin, oPin in [(IPin(), OPin()) for _ in range(3)]:
            self.logicSimulator.iPins.append(iPin)
            self.logicSimulator.oPins.append(oPin)
            oPin.addInputPin(iPin)
        self.logicSimulator.iPins[1].output = 1
        result = "0 1 0 | 0 1 0"
        self.assertEqual(self.logicSimulator.getPinResult(), result)

    def testSimulateOutput(self):
        for iPin, oPin in [(IPin(), OPin()) for _ in range(3)]:
            self.logicSimulator.iPins.append(iPin)
            self.logicSimulator.oPins.append(oPin)
            oPin.addInputPin(iPin)
        self.logicSimulator.iPins[1].output = 1
        self.assertEqual(self.logicSimulator.getSimulateOutput(), [0, 1, 0])


class TestTextUI(unittest.TestCase):
    def setUp(self) -> None:
        self.textUI = TextUI()

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.stdin", new=open(
        _PATH.joinpath("example.txt"), "r"))
    def testDisplayMenu(self, stdout: StringIO):
        with open(_PATH.joinpath("expected.txt"), "r") as expectedFile:
            self.textUI.displayMenu()
            expected = expectedFile.read()
            self.assertEqual(stdout.getvalue(), expected)

    def testProcessCommand(self):
        with self.subTest(msg="Invalid Command"):
            self.textUI.processCommand(5)
            self.assertRaises(ValueError)
        with patch("sys.stdout.write", new=lambda _: None
                   ), self.subTest(msg="fail to exit"):
            self.textUI.processCommand(Command.Exit)
            self.assertTrue(self.textUI.exit)
        with (patch("sys.stdin.readline",
                    new=lambda: str(_PATH.joinpath("file1.lcf"))),
              patch("sys.stdout", new=StringIO()) as stdout,
              self.subTest(msg="read lcf")):
            self.textUI.processCommand(Command.Load_logic_circuit_file)
            output = stdout.getvalue()
            self.assertEqual(output[output.find(": ")+2:],
                             f"Circuit: {len(self.textUI.logicSimulator.iPins)} input pins, "
                             f"{len(self.textUI.logicSimulator.oPins)} output pins and "
                             f"{len(self.textUI.logicSimulator.circuit)} gates\n")


if __name__ == "__main__":
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TestDeviceOutput))
    suite.addTest(loader.loadTestsFromTestCase(TestLogicSimulator))
    suite.addTest(loader.loadTestsFromTestCase(TestTextUI))
    unittest.TextTestRunner(verbosity=3).run(suite)
