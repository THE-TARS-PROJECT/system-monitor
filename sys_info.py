import psutil
from os import listdir
from time import strftime, gmtime, time

def get_sys_info() -> dict:
    mem = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    swap = psutil.swap_memory().percent
    uptime = time() - psutil.boot_time()

    return {
        "cpu": cpu,
        "mem": mem,
        "swap": swap,
        "uptime": str(strftime("%H:%M:%S", gmtime(uptime)))
    }

def convert_size_units(value: int):
    mb = value/1024
    if mb >= 1024:
        return f"{round(mb/1024, 3)} GB"
    else:
        return f"{round(mb, 3)} MB"
    

def get_processes(uid) -> list:
    processes_raw = listdir('/proc')
    pids = [pid for pid in processes_raw if pid.isdigit()]
    processes = []

    for pid in pids:
        try:
            with open(f'/proc/{pid}/status') as pid_info:
                data = pid_info.readlines()

                name, mem_str, proc_uid = None, None, None

                for line in data:
                    if line.startswith("Uid:"):
                        proc_uid = line.split(":", 1)[1].strip().split()[0]  # Real UID
                    elif line.startswith("Name:"):
                        name = line.split(":", 1)[1].strip()
                    elif line.startswith("VmRSS:"):
                        mem_str = line.split(":", 1)[1].strip().split()[0]

                if proc_uid and int(proc_uid) == uid and name and mem_str:
                    processes.append({
                        "name": name,
                        "pid": pid,
                        "mem": convert_size_units(int(mem_str))
                    })

        except FileNotFoundError:
            continue

    return processes


