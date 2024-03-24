from enum import Enum
import sys
from typing import List, Self


class LogicSimulator:
    def __init__(self) -> None:
        self.circuit: List[Device] = []
        self.iPins: List[Device] = []
        self.oPins: List[Device] = []

    def getSimulitaionResult(self) -> str:
        result = self.getHeader()
        iPins = [str(iPin.output) for iPin in self.iPins]
        oPins = [str(oPin.getOutput()) for oPin in self.oPins]
        result += " ".join(iPins) + " | " + " ".join(oPins)
        return result

    def getTruthTable(self) -> str:
        def generateInputs(count: int) -> List[List[int]]:
            assert count > 0
            preInputs: List[List[int]] = [[]]
            nextInputs: List[List[int]] = []
            while count > 0:
                for inputs in preInputs:
                    nextInputs.append([0] + inputs)
                for inputs in preInputs:
                    nextInputs.append([1] + inputs)
                preInputs = nextInputs
                nextInputs = []
                count -= 1
            return preInputs
        truthTable = self.getHeader()
        for i in generateInputs(len(self.iPins)):
            # init ipin
            for iPin, v in zip(self.iPins, i):
                iPin.output = v
            iPins = [str(iPin.output) for iPin in self.iPins]
            oPins = [str(oPin.getOutput()) for oPin in self.oPins]
            truthTable += " ".join(iPins) + " | " + " ".join(oPins) + "\n"
        return truthTable[:-1]

    def load(self, lcf: str) -> bool:
        try:
            lines = lcf.split("\n")
            pinCount = int(lines[0])
            for _ in range(pinCount):
                self.iPins.append(IPin())
            deviceFactory = DeviceFactory()
            gateCount = int(lines[1])
            gateHasOGates = [False]*gateCount
            gatesInfos = [lines[2 + i].split(" ") for i in range(gateCount)]
            # init circuit
            for info in gatesInfos:
                gateType = DeviceType(int(info[0]))
                self.circuit.append(deviceFactory.generateDevice(gateType))
            for gate, info in zip(self.circuit, gatesInfos):
                for device in info[1:-1]:
                    if device[0] == "-":  # pin
                        deviceID = int(device[1:])
                        gate.addInputPin(self.iPins[deviceID-1])
                    else:  # gate
                        deviceID = int(device[:device.find(".")])
                        gateHasOGates[deviceID-1] = True
                        gate.addInputPin(self.circuit[deviceID-1])
            assert gateHasOGates.index(False) >= 0
            gateToOPin = self.circuit[gateHasOGates.index(False)]
            self.oPins.append(OPin())
            self.oPins[-1].addInputPin(gateToOPin)
            return True
        except Exception as e:
            sys.stdout.write(f"{e}\n")
            return False

    def getHeader(self) -> str:
        iPinCount = len(self.iPins)
        oPinCount = len(self.oPins)
        header = f"{'i '*iPinCount}| o\n"
        iPinIDs = [str(i) for i in range(1, iPinCount+1)]
        oPinIDs = [str(i) for i in range(1, oPinCount+1)]
        header += " ".join(iPinIDs) + " | " + " ".join(oPinIDs) + "\n"
        header += "-"*(iPinCount << 1) + "+" + \
            "-"*(oPinCount << 1) + "\n"
        return header


class DeviceType(Enum):
    gateAND = 1
    gateOR = 2
    gateNot = 3
    iPin = 4
    oPin = 5


class Device:
    def __init__(self) -> None:
        self.iPins: List[Device] = []
        self.output: int = 0

    def addInputPin(self, device: Self) -> None:
        self.iPins.append(device)

    def getOutput(self) -> int:
        return self.output


class OPin(Device):
    def __init__(self) -> None:
        super().__init__()

    def getOutput(self) -> int:
        return self.iPins[0].getOutput()


class IPin(Device):
    def __init__(self) -> None:
        super().__init__()


class GateNot(Device):
    def __init__(self) -> None:
        super().__init__()

    def getOutput(self) -> int:
        self.output = 1 - self.iPins[0].getOutput()
        return self.output


class GateAND(Device):
    def __init__(self) -> None:
        super().__init__()

    def getOutput(self) -> int:
        self.output = 1
        for pin in self.iPins:
            if pin.getOutput() == 0:
                self.output = 0
                break
        return self.output


class GateOR(Device):
    def __init__(self) -> None:
        super().__init__()

    def getOutput(self) -> int:
        self.output = 0
        for pin in self.iPins:
            if pin.getOutput() == 1:
                self.output = 1
                break
        return self.output


class DeviceFactory:
    def __init__(self) -> None:
        pass

    def generateDevice(self, deviceType: DeviceType) -> Device:
        if deviceType == DeviceType.gateAND:
            return GateAND()
        if deviceType == DeviceType.gateNot:
            return GateNot()
        if deviceType == DeviceType.gateOR:
            return GateOR()
        if deviceType == DeviceType.iPin:
            return IPin()
        if deviceType == DeviceType.oPin:
            return OPin()
        raise ValueError
