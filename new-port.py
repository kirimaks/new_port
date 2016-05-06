#!/usr/bin/env python3

import os
import re
import time

class WatchPorts:
    def __init__(self):
        self.patt = r"[ \w]* (\d+.\d+.\d+.\d+:\d{2,})"
        self.ports = self.get_ports()

    def get_ports(self):
        buff = []

        shell_out = os.popen("netstat -lpnt4 2> /dev/null")

        for line in shell_out.read().split("\n"):
            out = re.match(self.patt, line)
            if out:
                buff.append(out.group(1))

        return buff

    @property
    def cur_ports(self):
        return self.ports

    def main(self):
        while True:
            buff = self.get_ports()
            diff = set(buff) - set(self.ports)
            if len(diff) > 0:
                self.display_ports(diff)

            self.ports = buff
            time.sleep(2)

    def display_ports(self, ports):
        for i in ports:
            addr, port = i.split(":")
            os.system("notify-send 'New port: {}' 'Listen on:<i>{}</i>'".format(port, addr))

wp = WatchPorts()
wp.main()
