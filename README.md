# debian-aspire-optimization-script
Optimizes a Debian 12 installation on an Aspire ES 15 (ES1-533-C55P) 
Summary of Key Updates:

    Backup and Restore:
        Added restore_file() function for restoring files from backups.
        The script checks for the existence of files before attempting to back them up.

    Error Handling:
        Improved error handling with clear messages when a command fails or a file cannot be backed up or restored.

    CPUGovernor Installation:
        The script now installs cpufrequtils if it’s not already installed and proceeds with CPU governor configuration.

    GRUB Configuration:
        The resume=UUID line in the GRUB configuration is preserved, and quiet splash is replaced with default.

    Swappiness Configuration:
        The script checks for and backs up existing swappiness configurations before applying new settings.

    Wi-Fi Power Management:
        If the Wi-Fi power management configuration file doesn’t exist, the script creates it and writes the required settings.

This updated script should now handle most scenarios robustly and provide comprehensive system optimization while maintaining a backup of existing configurations.

    Firmware and GPU Drivers:
        The install_firmware_and_drivers() function is added to check for and install the latest firmware and GPU drivers (firmware-linux-nonfree, firmware-misc-nonfree, and xserver-xorg-video-intel).

    Optimized Workflow:
        The optimize_system() function now includes a step to install the latest firmware and GPU drivers, ensuring that your hardware is fully supported and optimized.

Testing the Updated Script:

    Backup: Run the script and select the backup option to verify it correctly backs up existing files.
    Restore: Test the restore functionality to ensure it correctly restores from backups.
    Optimize: Select the optimize option to apply all system optimizations, including the installation of the latest firmware and GPU drivers, ensuring no steps are skipped and no errors occur.

This script should now comprehensively optimize your Debian 12 system on the Aspire ES 15 (ES1-533-C55P) laptop while maintaining a backup of existing configurations.
