import os
import subprocess
import time

def install_package(package):
    """Installs a package using apt-get with retries."""
    for attempt in range(10):  
        result = subprocess.run(["sudo", "apt", "install", "-y", package], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Installed {package} successfully. (✅✅✅)")
            return
        else:
            print(f"Failed to install {package} (attempt {attempt + 1}/10): {result.stderr}")
            if "Temporary failure resolving" in result.stderr or "Could not resolve host" in result.stderr:  
                print("( ❌ 🛜🛜🛜❌ ) Retrying due to potential internet issue...")
            elif attempt < 9:  
                print("Retrying...")


install_package("curl")
install_package("build-essential")
install_package("sudo")
install_package("python3.10")
install_package("ninja-build")
install_package("python3-telethon")


subprocess.run(["sudo", "apt", "update"])
subprocess.run(["sudo", "apt", "upgrade", "-y"])


install_package("python3.11-venv")



install_package("curl")
install_package("git")
install_package("libffi-dev")
install_package("libjpeg-dev")
install_package("libwebp-dev")
install_package("python3-lxml")
install_package("python3-psycopg2")
install_package("libpq-dev")
install_package("libcurl4-openssl-dev")
install_package("libxml2-dev")
install_package("libxslt1-dev")
install_package("python3-pip")
install_package("python3-sqlalchemy")
install_package("openssl")
install_package("wget")
install_package("python3")
install_package("python3-dev")
install_package("libreadline-dev")
install_package("libyaml-dev")
install_package("gcc")
install_package("zlib1g")
install_package("ffmpeg")
install_package("libssl-dev")
install_package("libgconf-2-4")
install_package("libxi6")
install_package("unzip")
install_package("libopus0")
install_package("libopus-dev")
install_package("libmagickwand-dev")
install_package("pv")
install_package("tree")
install_package("mediainfo")

if os.path.exists("/data/data/com.termux/files/home/ScoR"):
    os.chdir(os.path.expanduser("~"))
    result = subprocess.run(["cp", "-r", "/data/data/com.termux/files/home/ScoR", "."], capture_output=True, text=True)
    if result.returncode == 0:
        print("Copied ScoR directory successfully. (✅✅✅)")
        time.sleep(10)  
        if os.path.exists(os.path.expanduser("~/ScoR")):
            os.chdir(os.path.expanduser("~/ScoR"))

            
            pip_upgrade_result = subprocess.run(["pip3", "install", "--upgrade", "pip"], capture_output=True, text=True)
            if pip_upgrade_result.returncode == 0:
                print("Upgraded pip successfully. (✅✅✅)")
            else:
                print(f"Failed to upgrade pip: {pip_upgrade_result.stderr} (❌❌❌)")
                if "Could not resolve host" in pip_upgrade_result.stderr:
                    print("( ❌ 🛜🛜🛜❌ ) Check your internet connection.")

            

        else:
            print("Failed to access ScoR directory after 5 seconds delay. (❌❌❌)")
    else:
        print(f"Failed to copy ScoR directory: {result.stderr} (❌❌❌)")
else:
    print("Error: ScoR directory not found in Termux home. (❌❌❌)")

if os.path.exists(os.path.expanduser("~/ScoR")):
    os.chdir(os.path.expanduser("~/ScoR"))
else:
    print("Error: ScoR directory not found. (❌❌❌)")
    exit(1)

for command in [
    ["pip3", "install", "Telethon"],
    ["pip3", "install", "-r", "requirements.txt"],
    ["pip3", "install", "--upgrade", "psycopg2-binary"],
    ["pip3", "install", "heroku3"],
    ["pip3", "install", "psycopg2"]
]:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Command '{command}' executed successfully. (✅✅✅)")
    else:
        
        if "Could not resolve host" in result.stderr:
            print(f"Command '{command}' failed: ( ❌ 🛜🛜🛜❌ ) Check your internet connection.")
        else:
            print(f"Command '{command}' failed: {result.stderr} (❌❌❌)")
