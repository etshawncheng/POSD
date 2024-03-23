from enum import Enum
from pathlib import Path
from typing import List, Self


class Command(Enum):
    Load_logic_circuit_file = 1
    Simulation = 2
    Display_truth_table = 3
    Exit = 4


class TextUI:

    def __init__(self) -> None:
        self.MENU = """
        1. Load logic circuit file
        2. Simulation
        3. Display truth table
        4. Exit
        Command:
        """
        self.logicSimulator: LogicSimulator = LogicSimulator()

    def displayMenu(self):
        pass

    def processCommand(self):
        while True:
            # try read command
            command: Command = int(input(self.MENU))
            if command == Command.Load_logic_circuit_file:
                filePath = Path(input("Please key in a file path: "))
                # verify path
                if filePath.exists():
                    with open(filePath, "r") as lcf:
                        # verify lcf
                        if self.logicSimulator.load(lcf):
                            print(f"Circuit: {len(self.logicSimulator.iPins)} input pins, \
                                    {len(self.logicSimulator.oPins)} output pins and \
                                        {len(self.logicSimulator.circuit)} gates")
                            continue
                self.logicSimulator = None
                print("File not found or file format error!!")
                continue
            if len(self.logicSimulator.iPins) == 0:
                print("Please load an lcf file, before using this operation.")
                continue
            if command == Command.Simulation:
                pins = []
                for i in range(1, len(self.logicSimulator.iPins)+1):
                    pin = int(
                        input(f"Please key in the value of input pin {i}: ")
                    )
                    while pin != 0 or pin != 1:
                        print("The value of input pin must be 0/1")
                    pins.append(pin)
                print("Simulation Result:")
                print(self.logicSimulator.getSimulitaionResult())
            elif command == Command.Display_truth_table:
                print("Truth table:")
                print(self.logicSimulator.getTruthTable())
            elif command == Command.Exit:
                print("Goodbye, thanks for using LS.")
                break
            else:
                # Invalid Command
                pass


class LogicSimulator:
    def __init__(self) -> None:
        self.circuit: List[Device] = []
        self.iPins: List[Device] = []
        self.oPins: List[Device] = []

    def getSimulitaionResult(self) -> str:
        return

    def getTruthTable(self) -> str:
        return

    def load(self, lcf: str) -> bool:
        try:
            lines = lcf.split("\n")
            pinCount = int(lines[0])
            for _ in range(pinCount):
                self.iPins.append(Device(DeviceType.iPin))
            gateCount = int(lines[1])
            gatesInfos = [lines[2 + i].split(" ") for i in range(gateCount)]
            deviceFactory = DeviceFactory()
            # init circuit
            for info in gatesInfos:
                gateType = int(info[0])
                self.circuit.append(deviceFactory.generateDevice(gateType))
            for gate, info in zip(self.circuit, gatesInfos):
                for device in info[1:-1]:
                    if device[0] == "-":  # pin
                        deviceID = int(device[1:])
                        gate.addInputPin(self.iPins[deviceID-1])
                    else:  # gate
                        deviceID = int(device[:device.find(",")])
                        gate.addInputPin(self.circuit[deviceID-1])
            return True
        except Exception as e:
            return False


class DeviceType(Enum):
    oPin = 1
    iPin = 2
    gateNot = 3
    gateAND = 4
    gateOR = 5


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
        self.output = self.iPins[0].getOutput()
        self.output = self.output ^ self.output
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
        if deviceType == DeviceType.gateORND:
            return GateOR()
        if deviceType == DeviceType.iPin:
            return IPin()
        if deviceType == DeviceType.oPin:
            return OPin()
        raise ValueError


def testing():
    ui = TextUI()
    ui.displayMenu()
    ui.processCommand()


if __name__ == "__main__":
    testing()
