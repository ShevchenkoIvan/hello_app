# #
# # Thanks https://github.com/obi-wan-shinobi/Stress-test
# #
# from multiprocessing import Process, active_children, Pipe
# import os
# import signal
# import sys
# import time
# import psutil
#
# DEFAULT_TIME = 60
# TOTAL_CPU = psutil.cpu_count(logical=True)
# DEFAULT_MEMORY = (psutil.virtual_memory().total >> 20) * 1000
# PERCENT = 100
# GIGA = 2 ** 30
# MEGA = 2 ** 20
#
#
# def loop(conn, affinity, check):
#     """
#     Function to stress cores to run at 100%
#
#     Arguments:
#         conn    : child connection which is an object of Pipe()
#         affinity: list of cores to assign affinity for the process
#         check   : conditional flag to enable real time calibration
#     """
#     proc = psutil.Process()
#     proc_info = proc.pid
#     msg = "Process ID: " + str(proc_info) + " CPU: " + str(
#         affinity[0])  # Create a message string of PID and core number
#     conn.send(msg)  # Send message to parent
#     conn.close()
#     proc.cpu_affinity(affinity)  # Assigns a core to process
#     while True:
#         '''
#         Conditional check for calibration
#         '''
#         if (check and psutil.cpu_percent() > PERCENT):
#             time.sleep(0.05)  # Change the time for finetuning
#         1 * 1
#
#
# def last_core_loop(conn, affinity, percent):
#     """
#     Function to stress the last core at fractional percentage.
#     e.g. core 5 at 45% Usage
#
#     Arguments:
#         conn    : child connection which is an object of Pipe()
#         affinity: list of cores to assign affinity for the process
#         percent   : fractional percentage to run the core at
#     """
#     proc = psutil.Process()
#     proc_info = proc.pid
#     msg = "Process ID: " + str(proc_info) + " CPU: " + str(
#         affinity[0])  # Create a message string of PID and core number
#     conn.send(msg)  # Send message to parent
#     conn.close()
#     proc.cpu_affinity(affinity)  # Assigns a core to process
#     while True:
#         '''
#         Conditional check for core calibration
#         '''
#         if (psutil.cpu_percent(percpu=True)[affinity[0]] > percent):
#             time.sleep(0.1)  # Change the time for finetuning
#         1 * 1
#
#
# # signal.signal(signal.SIGINT, sigint_handler)
#
#
# def pmem():
#     """
#     Function to display memory statistics
#     """
#     virtual_mem = psutil.virtual_memory()
#     tot = virtual_mem.total
#     avail = virtual_mem.available
#     percent = virtual_mem.percent
#     used = virtual_mem.used
#     free = virtual_mem.free
#     tot, avail, used, free = tot / GIGA, avail / GIGA, used / GIGA, free / GIGA
#     print("---------------------------------------")
#     print("Memory Stats: total = %s GB \navail = %s GB \nused = %s GB \nfree = %s GB \npercent = %s"
#           % (tot, avail, used, free, percent))
#
#
# def alloc_max_str(memory):
#     """
#     Function to load memory by assigning string of requested size
#
#     Arguments:
#         memory: amount of memory to be utilized in MB
#     Returns:
#         a : String of size 'memory'
#     """
#     i = 0
#     a = ''
#     while True:
#         try:
#             a = ' ' * (i * 256 * MEGA)
#             if (psutil.virtual_memory().used >> 20) > memory:
#                 break
#             del a
#         except MemoryError:
#             break
#         i += 1
#     return a
#
#
# def memory_stress(memory, exec_time):
#     """
#     Function to stress memory and display memory Stats
#
#     Arguments:
#         memory: amount of memory to be utilized in MB
#         exec_time: time for which the system is supposed to keep the object
#
#     Returns:
#         a : String of size 'memory'
#     """
#     pmem()
#     a = alloc_max_str(memory)
#     pmem()
#     print("Memory Filled:")
#     print("Waiting for %d sec" % exec_time)
#     return a
#
#
# def _main():
#     """
#     Function to stress CPU and Memory
#     """
#     exec_time = DEFAULT_TIME
#     proc_num = TOTAL_CPU
#     memory = DEFAULT_MEMORY
#
#     procs = []
#     conns = []
#     print("CPU and Memory Stress in progress:")
#
#     '''
#     Memory Stress call:
#     '''
#
#     # a = memory_stress(memory, exec_time)
#
#     '''
#     CPU Stress logic:
#     '''
#
#     print("Stressing %f cores:" % proc_num)
#     actual_cores = int(proc_num)
#     last_core_usage = round((proc_num - actual_cores), 2) * 100
#     proc_num = actual_cores
#
#     # Run the required cores at 100% except one
#     for i in range(proc_num - 1):
#         parent_conn, child_conn = Pipe()
#         p = Process(target=loop, args=(child_conn, [i], False))
#         p.start()
#         procs.append(p)
#         conns.append(parent_conn)
#
#     # Run the last core out of the required cores to balance total output by actively calibrating realtime usage
#     parent_conn, child_conn = Pipe()
#     p = Process(target=loop, args=(child_conn, [proc_num - 1], True))
#     p.start()
#     procs.append(p)
#     conns.append(parent_conn)
#
#     # If CPU usage is not 100%, run the fractional part of the last core
#     if proc_num != TOTAL_CPU:
#         last_core = proc_num
#         parent_conn, child_conn = Pipe()
#         p = Process(target=last_core_loop, args=(child_conn, [last_core], last_core_usage))
#         p.start()
#         procs.append(p)
#         conns.append(parent_conn)
#
#     # Print PID and core messages sent by the children
#     for conn in conns:
#         try:
#             print(conn.recv())
#         except EOFError:
#             continue
#
#     # Carry out the execution for exec_time
#     time.sleep(exec_time)
#
#     # delete memory load
#     # del a
#
#     # Terminate child processes
#     for p in procs:
#         p.terminate()
