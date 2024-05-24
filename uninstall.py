import os
import subprocess

def remove_from_crontab(script_path):
    try:
        # Read current crontab into memory
        current_cron = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True).stdout
        # Filter out the line containing the script path
        updated_cron = ''.join(line for line in current_cron.splitlines(True) if script_path not in line)
        with open("mycron", "w") as file:
            file.write(updated_cron)
        # Update the crontab
        subprocess.run(["crontab", "mycron"], check=True)
        print("ui_server.py removed from crontab.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update crontab: {e}")
    finally:
        if os.path.exists("mycron"):
            os.remove("mycron")

def remove_from_systemd():
    service_name = "uiserver.service"
    service_path = f"/etc/systemd/system/{service_name}"
    try:
        subprocess.run(["sudo", "systemctl", "stop", service_name], check=True)
        subprocess.run(["sudo", "systemctl", "disable", service_name], check=True)
        subprocess.run(["sudo", "rm", service_path], check=True)
        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
        print(f"{service_name} service removed and system daemon reloaded.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to remove systemd service: {e}")

def get_script_path():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, "ui_server.py")

def main():
    script_path = get_script_path()
    print("Uninstall ui_server.py from system startup.")
    print("1: Remove from crontab")
    print("2: Remove from systemd service")
    choice = input("Choose an option (1 or 2): ")

    if choice == '1':
        remove_from_crontab(script_path)
    elif choice == '2':
        remove_from_systemd()
    else:
        print("Invalid option selected. Exiting.")

if __name__ == "__main__":
    main()
