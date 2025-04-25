import psutil
import datetime
from tabulate import tabulate

# gets process ID, name, username and established remote connections
def get_processes():
    procs: list[dict] = []
    for p in psutil.process_iter():
        with p.oneshot():
            pid: int = p.pid
            if pid == 0:
                continue
            name: str = p.name()
            try:
                create_time: datetime = datetime.datetime.fromtimestamp(p.create_time())
            except OSError:
                create_time: datetime = datetime.datetime.fromtimestamp(psutil.boot_time())
            status = p.status()
            try:
                user: str = p.username()
            except psutil.AccessDenied:
                user: str = "N/A"
            conns: list = p.net_connections()
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

if __name__ == "__main__":
    print_procs(get_processes())