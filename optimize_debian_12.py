import os
import shutil
import subprocess
from datetime import datetime

# Function to run shell commands with error handling
def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {command}")
        print(f"Error: {e.stderr.decode().strip()}")
        return False
    return True

# Function to back up a file if it exists
def backup_file(filepath):
    if os.path.exists(filepath):
        backup_dir = "/opt/debian_optim_backup"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filepath = os.path.join(backup_dir, f"{os.path.basename(filepath)}.{timestamp}.bak")
        try:
            shutil.copy(filepath, backup_filepath)
            print(f"Backup of {filepath} created at {backup_filepath}.")
        except Exception as e:
            print(f"Failed to backup {filepath}: {e}")
    else:
        print(f"No backup needed: {filepath} does not exist.")

# Function to restore a file from a backup
def restore_file(filepath):
    backup_dir = "/opt/debian_optim_backup"
    backup_files = [f for f in os.listdir(backup_dir) if f.startswith(os.path.basename(filepath))]
    if backup_files:
        latest_backup = max(backup_files)
        backup_filepath = os.path.join(backup_dir, latest_backup)
        try:
            shutil.copy(backup_filepath, filepath)
            print(f"Restored {filepath} from {backup_filepath}.")
        except Exception as e:
            print(f"Failed to restore {filepath}: {e}")
    else:
        print(f"No backup found for {filepath}.")

# Function to modify the GRUB configuration
def configure_grub():
    grub_file = "/etc/default/grub"
    backup_file(grub_file)
    
    try:
        with open(grub_file, 'r+') as f:
            content = f.read()
            # Preserve the 'resume=UUID' line and replace 'quiet splash' with 'default'
            content = content.replace('quiet splash', 'default')
            f.seek(0)
            f.write(content)
            f.truncate()
        print("GRUB configuration updated.")
        run_command("update-grub")
    except Exception as e:
        print(f"Failed to update GRUB configuration: {e}")

# Function to configure swappiness
def configure_swappiness():
    swappiness_file = "/etc/sysctl.d/99-swappiness.conf"
    backup_file(swappiness_file)

    try:
        with open(swappiness_file, 'w') as f:
            f.write("vm.swappiness=10\n")
        print("Swappiness configured.")
        run_command("sysctl -p")
    except Exception as e:
        print(f"Failed to configure swappiness: {e}")

# Function to check and install the latest firmware and GPU drivers
def install_firmware_and_drivers():
    print("Checking for and installing the latest firmware...")
    run_command("apt update && apt install firmware-linux-nonfree firmware-misc-nonfree -y")

    print("Checking for and installing the latest GPU drivers...")
    run_command("apt install xserver-xorg-video-intel -y")

# Function to optimize the system
def optimize_system():
    # 1. Ensure system is up-to-date
    print("Updating the system...")
    run_command("apt update && apt upgrade -y")

    # 2. Install Preload for faster application loading
    print("Installing Preload...")
    run_command("apt install preload -y")

    # 3. Install cpufrequtils and configure CPU governor
    print("Configuring CPU governor...")
    if not run_command("apt install cpufrequtils -y"):
        print("Skipping CPU governor configuration due to failed installation.")
    else:
        run_command("cpufreq-set -r -g performance")

    # 4. Ensure correct Wi-Fi driver is used
    print("Ensuring correct Wi-Fi driver is used...")
    run_command("apt install firmware-iwlwifi -y")
    run_command("modprobe -r iwlwifi && modprobe iwlwifi")

    # Disable Wi-Fi power management
    print("Disabling Wi-Fi power management...")
    wifi_powersave_file = '/etc/NetworkManager/conf.d/default-wifi-powersave-on.conf'
    backup_file(wifi_powersave_file)

    try:
        with open(wifi_powersave_file, 'w') as f:
            f.write("[connection]\nwifi.powersave = 2\n")
        print("Wi-Fi power management disabled.")
    except Exception as e:
        print(f"Failed to disable Wi-Fi power management: {e}")

    print("Restarting NetworkManager...")
    run_command("systemctl restart NetworkManager")

    # 5. Configure swappiness
    configure_swappiness()

    # 6. Configure GRUB
    configure_grub()

    # 7. Install the latest firmware and GPU drivers
    install_firmware_and_drivers()

    # 8. Prompt user for reboot
    reboot = input("Optimization complete. Do you want to reboot now? (y/n): ").strip().lower()
    if reboot == 'y':
        run_command("reboot")
    else:
        print("Reboot skipped. Please reboot manually to apply changes.")

# Main function
def main():
    choice = input("Would you like to (b)ackup current settings, (r)estore from backup, or (o)ptimize the system? (b/r/o): ").strip().lower()

    if choice == 'b':
        print("Backing up current settings...")
        backup_file("/etc/default/grub")
        backup_file("/etc/sysctl.d/99-swappiness.conf")
        backup_file("/etc/NetworkManager/conf.d/default-wifi-powersave-on.conf")
        print("Backup complete.")
    elif choice == 'r':
        print("Restoring from backup...")
        restore_file("/etc/default/grub")
        restore_file("/etc/sysctl.d/99-swappiness.conf")
        restore_file("/etc/NetworkManager/conf.d/default-wifi-powersave-on.conf")
        print("Restore complete.")
    elif choice == 'o':
        optimize_system()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
