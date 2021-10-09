#!/usr/bin/python3
from app import App
from app.cmd_parser import CommandLineParser

if __name__ == '__main__':
    args = CommandLineParser.parse()
    app = App(args)
    app.run()
