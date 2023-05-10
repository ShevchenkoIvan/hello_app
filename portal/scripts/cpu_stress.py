#
# Thanks https://github.com/obi-wan-shinobi/Stress-test
#
from multiprocessing import Process, Pipe

import time
import psutil

DEFAULT_TIME = 60
TOTAL_CPU = psutil.cpu_count(logical=True)
PERCENT = 100


def loop(conn, affinity, check):
    """
    Function to stress cores to run at 100%

    Arguments:
        conn    : child connection which is an object of Pipe()
        affinity: list of cores to assign affinity for the process
        check   : conditional flag to enable real time calibration
    """
    proc = psutil.Process()
    proc_info = proc.pid
    msg = "Process ID: " + str(proc_info) + " CPU: " + str(
        affinity[0])  # Create a message string of PID and core number
    conn.send(msg)  # Send message to parent
    conn.close()
    proc.cpu_affinity(affinity)  # Assigns a core to process
    while True:
        '''
        Conditional check for calibration
        '''
        if check and psutil.cpu_percent() > PERCENT:
            time.sleep(0.05)  # Change the time for finetuning
        1 * 1


def last_core_loop(conn, affinity, percent):
    """
    Function to stress the last core at fractional percentage.
    e.g. core 5 at 45% Usage

    Arguments:
        conn    : child connection which is an object of Pipe()
        affinity: list of cores to assign affinity for the process
        percent   : fractional percentage to run the core at
    """
    proc = psutil.Process()
    proc_info = proc.pid
    msg = "Process ID: " + str(proc_info) + " CPU: " + str(
        affinity[0])  # Create a message string of PID and core number
    conn.send(msg)  # Send message to parent
    conn.close()
    proc.cpu_affinity(affinity)  # Assigns a core to process
    while True:
        '''
        Conditional check for core calibration
        '''
        if psutil.cpu_percent(percpu=True)[affinity[0]] > percent:
            time.sleep(0.1)  # Change the time for finetuning
        1 * 1


def main():
    """
    Function to stress CPU
    """
    exec_time = DEFAULT_TIME
    proc_num = TOTAL_CPU

    procs = []
    conns = []
    print("CPU Stress in progress:")

    '''
    CPU Stress logic:
    '''

    print("Stressing %f cores:" % proc_num)
    actual_cores = int(proc_num)
    last_core_usage = round((proc_num - actual_cores), 2) * 100
    proc_num = actual_cores

    # Run the required cores at 100% except one
    for i in range(proc_num - 1):
        parent_conn, child_conn = Pipe()
        p = Process(target=loop, args=(child_conn, [i], False))
        p.start()
        procs.append(p)
        conns.append(parent_conn)

    # Run the last core out of the required cores to balance total output by actively calibrating realtime usage
    parent_conn, child_conn = Pipe()
    p = Process(target=loop, args=(child_conn, [proc_num - 1], True))
    p.start()
    procs.append(p)
    conns.append(parent_conn)

    # If CPU usage is not 100%, run the fractional part of the last core
    if proc_num != TOTAL_CPU:
        last_core = proc_num
        parent_conn, child_conn = Pipe()
        p = Process(target=last_core_loop, args=(child_conn, [last_core], last_core_usage))
        p.start()
        procs.append(p)
        conns.append(parent_conn)

    # Print PID and core messages sent by the children
    for conn in conns:
        try:
            print(conn.recv())
        except EOFError:
            continue

    # Carry out the execution for exec_time
    time.sleep(exec_time)

    # Terminate child processes
    for p in procs:
        p.terminate()
