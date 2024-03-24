from enum import Enum
from pathlib import Path
import sys
from typing import Optional
from logicSimulator import LogicSimulator


class Command(Enum):
    Load_logic_circuit_file = 1
    Simulation = 2
    Display_truth_table = 3
    Exit = 4


class TextUI:

    def __init__(self) -> None:
        self.MENU = "1. Load logic circuit file\n"\
                    "2. Simulation\n"\
                    "3. Display truth table\n"\
                    "4. Exit\n"\
                    "Command:"
        self.logicSimulator: Optional[LogicSimulator] = None

    def displayMenu(self) -> None:
        while True:
            # try read command
            sys.stdout.write(self.MENU)
            command = Command(int(sys.stdin.readline().rstrip()))
            self.processCommand(command)
            sys.stdout.write("\n")

    def processCommand(self, command: Command) -> None:
        if command == Command.Exit:
            sys.stdout.write("Goodbye, thanks for using LS.\n")
            exit()
        if command == Command.Load_logic_circuit_file:
            sys.stdout.write("Please key in a file path: ")
            filePath = Path(sys.stdin.readline().rstrip())
            # verify path
            if filePath.exists():
                with open(filePath, "r") as lcf:
                    # verify lcf
                    logicSimulator = LogicSimulator()
                    if logicSimulator.load(lcf.read()):
                        self.logicSimulator = logicSimulator
                        sys.stdout.write(
                            f"Circuit: {len(self.logicSimulator.iPins)} input pins, "
                            f"{len(self.logicSimulator.oPins)} output pins and "
                            f"{len(self.logicSimulator.circuit)} gates\n")
                        return
            sys.stdout.write("File not found or file format error!!\n")
        elif not self.logicSimulator:
            sys.stdout.write(
                "Please load an lcf file, before using this operation.\n")
        elif command == Command.Simulation:
            for i in range(len(self.logicSimulator.iPins)):
                sys.stdout.write(
                    f"Please key in the value of input pin {i+1}: ")
                pin = int(sys.stdin.readline().rstrip())
                while pin != 0 and pin != 1:
                    sys.stdout.write("The value of input pin must be 0/1\n"
                                     f"Please key in the value of input pin {i+1}: ")
                    pin = int(sys.stdin.readline().rstrip())
                self.logicSimulator.iPins[i].output = pin
            sys.stdout.write("Simulation Result:\n" +
                             self.logicSimulator.getSimulitaionResult() + "\n")
        elif command == Command.Display_truth_table:
            sys.stdout.write("Truth table:\n" +
                             self.logicSimulator.getTruthTable() + "\n")
        else:
            raise ValueError


def testing(testCasePath: str, resultPath: str):
    try:
        sys.stdin = open(testCasePath, "r")
        sys.stdout = open(resultPath, "w")
        ui = TextUI()
        ui.displayMenu()
    except Exception as e:
        sys.stdout.write(f"{e}\n")
    finally:
        sys.stdin.close()
        sys.stdout.close()


if __name__ == "__main__":
    testing(r"C:\VS_Workplace\POSD\testcase.txt",
            r"C:\VS_Workplace\POSD\result.txt")
