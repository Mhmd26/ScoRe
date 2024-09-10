import os
import subprocess

def run_command(command, retry_count=0):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True)
        print("✅✅✅✅") 
        return result.stdout
    except subprocess.CalledProcessError as e:
        if "Network is unreachable" in e.stderr and retry_count < 5:
            print("🔄🛜🛜🔄 Retry due to an internet connection issue...")
            return run_command(command, retry_count + 1)
        else:
            print("❌❌❌❌ Failed to execute command:", e)
            return None

run_command("termux-setup-storage")

if not os.path.exists("/data/data/com.termux/files/usr/bin/telethon"):
    run_command("yes | pkg update && pkg upgrade")
    run_command("pip install telethon")

if not os.path.exists("/data/data/com.termux/files/usr/bin/git"):
    run_command("yes | pkg install git")

if not os.path.exists("/data/data/com.termux/files/usr/bin/ninja"):
    run_command("yes | pkg install ninja")

if not os.path.exists("/data/data/com.termux/files/usr/bin/psql"):
    run_command("yes | pkg install postgresql")


if os.path.exists("/data/data/com.termux/files/usr/bin/psql"):
    os.system("pg_ctl -D $PREFIX/var/lib/postgresql stop")
    os.system("yes | pkg uninstall postgresql")
    os.system("rm -rf $PREFIX/var/lib/postgresql")


if not os.path.exists("/data/data/com.termux/files/usr/bin/psql"):
    run_command("yes | pkg install postgresql")


# ********************************************************
# *                    Dev FINAL                                *
# *            I am the best always and ever                    *
# ********************************************************

run_command("mkdir -p $PREFIX/var/lib/postgresql")

run_command("initdb $PREFIX/var/lib/postgresql")

run_command("pg_ctl -D $PREFIX/var/lib/postgresql start")

run_command("createuser --superuser postgres")

run_command('psql -U postgres -d postgres -c "ALTER USER postgres WITH PASSWORD \'final111\';"')

run_command('psql -U postgres -d postgres -c "CREATE DATABASE finalv OWNER postgres;"')

run_command("pg_ctl -D $PREFIX/var/lib/postgresql status")

if os.path.exists("/sdcard/ScoRe"):
    run_command("cp -rf /sdcard/ScoRe ~")

if not os.path.exists("/data/data/com.termux/files/usr/bin/proot-distro"):
    run_command("yes | pkg install proot-distro") 
    run_command("proot-distro install debian")

run_command("proot-distro login debian")

