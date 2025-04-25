import psutil
import datetime
from tabulate import tabulate

# gets process ID, name, username and established remote connections
def get_processes():
    procs = []
    for p in psutil.process_iter():
        with p.oneshot():
            pid = p.pid
            if pid == 0:
                continue
            name = p.name()
            try:
                create_time = datetime.datetime.fromtimestamp(p.create_time())
            except OSError:
                create_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            status = p.status()
            try:
                user = p.username()
            except psutil.AccessDenied:
                user = "N/A"
            conns = p.net_connections()
            if conns:
                conns = conns[0][4]
            else:
                conns = ""

            
        procs.append({
            "pid" : pid,
            "name" : name,
            "create_time": create_time,
            "status": status,
            "user": user,
            "connections": conns
        })
    return procs

# prints process-list as table in console
def print_procs(processes: list[dict]):
    print(tabulate(processes, headers="keys", tablefmt="github"))

print_procs(get_processes())