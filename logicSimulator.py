from re import fullmatch
from typing import List

from device import Device, DeviceFactory, DeviceType, IPin, OPin


class LogicSimulator:
    def __init__(self) -> None:
        self.circuit: List[Device] = []
        self.iPins: List[Device] = []
        self.oPins: List[Device] = []
        pin = r"-([0-9])*?"  # 3
        gate = r"([0-9])*?.([0-9])*?"  # 3
        gateinfo = r"[1-3]" + rf"( ({pin}|{gate}))+?" + " 0"  # 1 -1 2.1 0
        self.LCF_FORMAT = r"([0-9])*?\n" * 2 + \
            rf"({gateinfo}\n)*?{gateinfo}(\n)?"

    def getSimulitaionResult(self) -> str:
        result = self.getHeader()
        iPins = [str(iPin.output) for iPin in self.iPins]
        oPins = [str(oPin.getOutput()) for oPin in self.oPins]
        result += " ".join(iPins) + " | " + " ".join(oPins)
        return result

    def getTruthTable(self) -> str:
        truthTable = self.getHeader()
        for values in self.generateInputs(len(self.iPins)):
            # init ipin
            for iPin, v in zip(self.iPins, values):
                iPin.output = v
            iPins = [str(iPin.output) for iPin in self.iPins]
            oPins = [str(oPin.getOutput()) for oPin in self.oPins]
            truthTable += " ".join(iPins) + " | " + " ".join(oPins) + "\n"
        return truthTable[:-1]

    def load(self, lcf: str) -> bool:
        if not self.isLcfFormat(lcf):
            return False
        lines = lcf.split("\n")
        if lines[-1] == "":
            lines.pop()
        pinCount = int(lines[0])
        if not (0 < pinCount <= 16):
            return False
        gateCount = int(lines[1])
        if not (0 < gateCount <= 1000):
            return False
        if gateCount + 2 != len(lines):
            return False
        for _ in range(pinCount):
            self.iPins.append(IPin())
        deviceFactory = DeviceFactory()
        gatesInfos = [lines[2 + i].split(" ") for i in range(gateCount)]
        # for determining output gate
        gateHasOGates = [False]*gateCount
        # init circuit
        for info in gatesInfos:
            gateType = DeviceType(int(info[0]))
            self.circuit.append(deviceFactory.generateDevice(gateType))
        for gate, info in zip(self.circuit, gatesInfos):
            for device in info[1:-1]:
                if device[0] == "-":  # pin
                    deviceID = int(device[1:])
                    if not (0 < deviceID <= len(self.iPins)):
                        return False
                    gate.addInputPin(self.iPins[deviceID-1])
                else:  # gate
                    deviceID = int(device[:device.find(".")])
                    if not (0 < deviceID <= len(self.circuit)):
                        return False
                    gateHasOGates[deviceID-1] = True
                    gate.addInputPin(self.circuit[deviceID-1])
        oGateIdxes = [i for (i, hasOGates) in enumerate(
            gateHasOGates) if not hasOGates]
        if len(oGateIdxes) == 0:
            return False
        for i in oGateIdxes:
            gateToOPin = self.circuit[i]
            self.oPins.append(OPin())
            self.oPins[-1].addInputPin(gateToOPin)
        return True

    def isLcfFormat(self, lcf: str) -> bool:
        return fullmatch(self.LCF_FORMAT, lcf) != None

    def generateInputs(self, count: int) -> List[List[int]]:
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

    def getHeader(self) -> str:
        iPinCount = len(self.iPins)
        oPinCount = len(self.oPins)
        header = f"{'i ' * iPinCount}|{' o' * oPinCount}\n"
        iPinIDs = [str(i) for i in range(1, iPinCount+1)]
        header += " ".join(iPinIDs) + " | " + " ".join(oPinIDs) + "\n"
        oPinIDs = [str(i) for i in range(1, oPinCount+1)]
        header += f"{'-' * (iPinCount << 1)}+{'-' * (oPinCount << 1)}\n"
        return header
