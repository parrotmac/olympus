import argparse
import serial
from serial.tools import list_ports
import pprint
import time
import random
import sys
from collections import defaultdict
from socketIO_client import SocketIO, LoggingNamespace

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port')
parser.add_argument('-b', '--baud', default=115200)
parser.add_argument('-d', '--demo', dest='demo', action='store_true')
args = parser.parse_args()



if args.demo:
    with SocketIO('localhost', 3003, LoggingNamespace) as socketIO:

        longest_line = 0

        while(True):

            can_id = str( hex( random.randint(0, 20) ) )
            msg_data = "%s %s" % (" ".join([hex(ord(val)).replace("0x", "") for val in can_id]), str(hex(random.randint(0, 1)).replace('0x', '').zfill(2) ))
            # msg_data = "%sDEADBEEF" % str(hex(random.randint(0, 1)))

            current_line = "\rSimulated transmit: %s %s" % (can_id, msg_data)

            current_line_len = len(current_line)
            if current_line_len > longest_line:
                longest_line = current_line_len
                
            sys.stdout.write("%s%s" % (current_line, " " * (longest_line - current_line_len) ))

            socketIO.emit('vehicle-report', {
                "sender_id": can_id,
                "value": msg_data
            })
            time.sleep(0.05)


if not args.port:
    print("Please specify a serial port with --port or use --demo mode")
    print("A list of available ports is provided below")
    for com_port in list_ports.comports():
        print(com_port)
    exit(-1)


conn = serial.Serial(args.port, args.baud)

can_display = {}

pp = pprint.PrettyPrinter(indent=4)

last_25_data = None

interesting_can_ids = [
    # "20",
    # "22",
    "23",
    "25",
    "30",
    # "38",
    # "39",
    # "3A",
    # "3B",
    # "3E",
    # "60",
    # "87",
    # "B0",
    # "B1",
    # "B3",
    # "B4",
    # "C9",
    # "120",
    # "230",
    # "244",
    # "262",
    # "348",
    # "34F",
    # "3C8",
    # "3C9",
    # "3CA",
    # "3CB",
    # "3CD",
    # "3CF",
    # "423",
    # "4C1",
    # "4C3",
    # "4C6",
    # "4C7",
    # "4C8",
    # "4CE",
    # "4D0",
    # "4D1",
    # "520",
    # "521",
    # "526",
    # "527",
    # "528",
    # "529",
    # "52C",
    # "540",
    # "553",
    # "554",
    # "56D",
    "57F",
    # "591",
    # "5A4",
    # "5B2",
    # "5B6",
    # "5C8",
    # "5CC",
    # "5D4",
    # "5EC",
    # "5ED",
    # "5F8",
    # "602",
    # "C00"
]

with SocketIO('localhost', 3003, LoggingNamespace) as socketIO:
    while (True):
        if conn.in_waiting:
            can_msg = conn.readline().decode('ascii').strip()
            if ":" in can_msg:
                msg_parts = can_msg.split(":")
                can_id = msg_parts[0]
                msg_data = msg_parts[1]
                can_display[can_id] = msg_data

                # if can_id in interesting_can_ids:

                print(can_msg)

                socketIO.emit('vehicle-report', {
                    "sender_id": can_id,
                    "value": msg_data
                })

                    # if msg_data != last_25_data:
                    #     print("%s\t%d" % (msg_data, int(msg_data[0:3], 16)))
                    #     last_25_data = msg_data
        
                # print(json.dumps(can_display))



                # pp.pprint(can_display)
