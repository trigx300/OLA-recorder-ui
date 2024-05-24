import os
import subprocess

# Get the full path of ui_server.py assuming it's in the same directory as this script
current_dir = os.path.dirname(os.path.realpath(__file__))
script_path = os.path.join(current_dir, "ui_server.py")

def add_to_crontab():
    job = f"@reboot /usr/bin/python3 {script_path}\n"
    with open("mycron", "a+") as file:
        file.write(job)
    subprocess.run(["crontab", "mycron"])
    os.remove("mycron")
    print("ui_server.py added to crontab.")

def add_to_systemd():
    service_content = f"""[Unit]
Description=UI Server Script Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 {script_path}

[Install]
WantedBy=multi-user.target
"""
    service_name = "uiserver.service"
    with open(f"/etc/systemd/system/{service_name}", "w") as file:
        file.write(service_content)
    subprocess.run(["sudo", "systemctl", "daemon-reload"])
    subprocess.run(["sudo", "systemctl", "enable", service_name])
    subprocess.run(["sudo", "systemctl", "start", service_name])
    print(f"ui_server.py added as a service: {service_name}")

def main():
    method = input("Choose method to run ui_server.py on boot (crontab/systemd): ").lower()

    if method == "crontab":
        add_to_crontab()
    elif method == "systemd":
        add_to_systemd()
    else:
        print("Invalid method chosen. Exiting.")

if __name__ == "__main__":
    main()
