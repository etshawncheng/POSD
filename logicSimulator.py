import sys
from typing import List

from device import Device, DeviceFactory, DeviceType, IPin, OPin


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
            if len(lines) < 2:
                raise ValueError
            pinCount = int(lines[0])
            if pinCount <= 0:
                raise ValueError
            for _ in range(pinCount):
                self.iPins.append(IPin())
            deviceFactory = DeviceFactory()
            gateCount = int(lines[1])
            if gateCount < 0:
                raise ValueError
            gatesInfos = [lines[2 + i].split(" ") for i in range(gateCount)]
            if gateCount != len(gatesInfos):
                raise ValueError
            # to determine output gate
            gateHasOGates = [False]*gateCount
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
            sys.stderr.write(f"{e}\n"
                             "LCF:\n"
                             f"{lcf}\n")
            return False

    def getHeader(self) -> str:
        iPinCount = len(self.iPins)
        oPinCount = len(self.oPins)  # 1
        header = f"{'i ' * iPinCount}|{' o' * oPinCount}\n"
        iPinIDs = [str(i) for i in range(1, iPinCount+1)]
        header += " ".join(iPinIDs) + " | " + " ".join(oPinIDs) + "\n"
        oPinIDs = [str(i) for i in range(1, oPinCount+1)]
        header += f"{'-' * (iPinCount << 1)}+{'-' * (oPinCount << 1)}\n"
        return header
