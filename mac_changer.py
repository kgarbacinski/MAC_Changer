import subprocess
import argparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_argument("-m", "--mac", dest="mac_address", help="New MAC address")

    options  = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    if not options.mac_address:
        parser.error("[-] Please specify a MAC address, use --help for more info.")
    return options

def get_current_mac_address(interface):
    ipa_result = subprocess.check_output(["ip", "link", "show", interface]).decode()
    mac_address_regex_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ipa_result)
    if mac_address_regex_search:
        return mac_address_regex_search.group(0)
    else:
        print("[-] Could not read MAC address")

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for", interface, "to:", new_mac)

    subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "down"])
    subprocess.call(["sudo", "ip", "link", "set", interface, "address", new_mac])
    subprocess.call(["sudo", "ip", "link", "set", interface, "up"])

options = get_arguments()
current_mac_address = get_current_mac_address(options.interface)
print("Current MAC Adress:", str(current_mac_address))
change_mac(options.interface, str(options.mac_adress))
current_mac_address = get_current_mac_address(options.interface)
if current_mac_address == options.mac_address:
    print("[+] MAC Address has been changed successfully. New MAC Adress:", current_mac_address)
else:
    print("[-] Could not change MAC Address")
