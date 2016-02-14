import psutil
from constants import *

class Stats(object):
    STATS_UPDATE_INTERVAL=5

    def __init__(self):
        self.engine_stats=[]

    def _get_cpu_stats(self):
        cpu_stats={}

        cpu_stats[TOTAL_CPU_USAGE]=psutil.cpu_percent()
        cpu_stats[PER_CPU_USAGE]=psutil.cpu_percent(percpu=True)
        
        return cpu_stats

    def _get_mem_stats(self):
        mem=psutil.virtual_memory()

        mem_stats={}
        mem_stats[TOTAL_MEM]=mem.total
        mem_stats[AVAIL_MEM]=mem.available
        mem_stats[MEMORY_USAGE]=mem.percent
        mem_stats[USED_MEM]=mem.used
        mem_stats[FREE_MEM]=mem.free

        return mem_stats

    def _get_disk_stats(self):
        disk_stats=[]

        for partition in psutil.disk_partitions():
            disk=psutil.disk_usage(partition.mountpoint)
            disk_stats.append({TOTAL_DISK:disk.total,
                                USED_DISK:disk.used,
                                FREE_DISK:disk.free,
                                DISK_USAGE:disk.percent})

        return disk_stats

    def get(self):
        stats={}

        stats[CPU_STATS]=self._get_cpu_stats()
        stats[MEMORY_STATS]=self._get_mem_stats()
        stats[DISK_STATS]=self._get_disk_stats()
        stats[ENGINE_STATS]=self.engine_stats

        return stats

    def add_engine(self,engine):
        for node in self.engine_stats:
            if node[ENGINE_NAME]==engine:
                return

        self.engine_stats.append({ENGINE_NAME:engine,ENGINE_STAT:ENGINE_STAT_RUNNING})

