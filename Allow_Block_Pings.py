import subprocess
import ctypes
import sys

# Admin verification function --> Need Admin rights to modify Firewall
def check_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()

# Reset entire firewall function --> Deletes all custom rules made by user
def reset_firewall():
    print("\nResetting Firewall to DEFAULT settings..")
    reset_cmd = "netsh advfirewall reset"   # Reset -command for CMD
    subprocess.run(reset_cmd, shell=True)   # Run in CMD
    print("Firewall has been reset!\nAll custom rules are deleted.")

# Adding ping rule function --> Can add or remove specific ping rules
def ping_rules(rule_name, scope, action):
    delete_cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'  # Delete specific rule name -command for CMD
    subprocess.run(delete_cmd, shell=True)   # Run in CMD

    if action == 'off':
        print(f"Rule '{rule_name}' has been removed.\nPings are now BLOCKED!")
        return

    # If action 'on', add new rule
    print(f"Enabling rule: '{rule_name}'...")
    
    base_cmd = f'netsh advfirewall firewall add rule name="{rule_name}" protocol=icmpv4 dir=in action=allow'    # New rule -command for CMD
    if scope == 'LocalSubnet':
        cmd = f'{base_cmd} remoteip=LocalSubnet'    # Add scope command --> Rule applies only to Local Subnet
    else:
        cmd = base_cmd      # No scope needed --> Rule applies to ALL
    subprocess.run(cmd, shell=True)     # Run in CMD
    
    print(f"Rule '{rule_name}' is active!")

# User menu function --> Main interface for user interaction
def show_menu():
    while True:
        print("**** FIREWALL PING MANAGER ****")
        print("1. Reset Firewall (Factory SETTINGS)")
        print("2. Allow LOCALHOST Pings (LOCAL)")
        print("3. Allow ALL Pings (GLOBAL)")
        print("4. Exit")
        print("********************************")
        
        # Get user choice
        choice = input("Select an option (1-4): ")

        if choice == '1':
            input("\nBy choosing this option, ALL custom firewall rules will be REMOVED and the firewall will be reset to DEFAULT settings.\n\nPress Enter to CONTINUE or CTRL+C to CANCEL...")
            reset_firewall()    # Call Reset Function
            input("\nPress Enter to return to menu...\n")

        elif choice == '2':
            print("\n**** MANAGE LOCAL PINGS ****")
            sub_choice = input("'1' to ALLOW\n'2' to BLOCK: ")
            if sub_choice == '1':
                ping_rules("Allow_Ping_LOCAL", "LocalSubnet", "on")   # Allow Local Subnet Pings
            elif sub_choice == '2':
                ping_rules("Allow_Ping_LOCAL", "LocalSubnet", "off")  # Block Local Subnet Pings
            else:
                print("Invalid choice.")
            input("\nPress Enter to return to menu...\n")

        elif choice == '3':
            print("\n**** MANAGE GLOBAL PINGS ****")
            sub_choice = input("'1' to ALLOW\n'2' to BLOCK: ")
            if sub_choice == '1':
                ping_rules("Allow_Ping_GLOBAL", "any", "on")  # Allow All Pings
            elif sub_choice == '2':
                ping_rules("Allow_Ping_GLOBAL", "any", "off") # Block All Pings
            else:
                print("Invalid choice.")
            input("\nPress Enter to return to menu...\n")

        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid selection. Please try again.")

# Main initialization
if __name__ == "__main__":
    if not check_admin():    # Check for Admin privileges
        print("Requesting Admin privileges...")
        
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)    # Relaunch script with Admin rights
        if result <= 32:    # If user declines Admin request
            print("\nERROR!!!\n--> You must run this program as Administrator!\nProgram will now exit.")
    
    else:
        show_menu()