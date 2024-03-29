from enum import Enum
from typing import List, Self


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
        self.output = self.iPins[0].getOutput()
        return self.output


class IPin(Device):
    def __init__(self, value: int = 0) -> None:
        super().__init__()
        self.output = value


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
