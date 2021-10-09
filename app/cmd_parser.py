import sys
from config import *


class Arg:
    def __init__(self, arg_name: str, value: str = None):
        self.__arg_name = arg_name
        self.__value = value

    def get_arg_name(self) -> str:
        return self.__arg_name

    def get_value(self) -> str:
        return self.__value


class CommandLineParser:
    @staticmethod
    def parse() -> list:
        args = sys.argv[1:]

        results = []

        if len(args) > 0:
            for arg in args:
                if arg == SAVE_MAP:
                    print("Saving map")
                    results.append(Arg(SAVE_MAP))
                if arg == AUTO_MODE:
                    print("Auto mode")
                    results.append(Arg(AUTO_MODE))
                elif arg.find(LOAD_MAP, 0, len(LOAD_MAP)-1):
                    cmd = arg.split("=")
                    if len(cmd) == 2:
                        # print(cmd)
                        map_name = cmd[1]
                        print(f"Loading map: {map_name}")
                        results.append(Arg(LOAD_MAP, map_name))
                    else:
                        raise Exception(f"Incorrect name of map: {cmd}!")
                else:
                    raise Exception(f"Unknown arg {arg}")
            # print(args)

        return results
