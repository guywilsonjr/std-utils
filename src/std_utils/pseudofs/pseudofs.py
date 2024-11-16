from pydantic import BaseModel


cacheinfo = '/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'

cpuinfo = '/proc/cpuinfo'



def read_cpuinfo():
    with open(cpuinfo) as f:
        return f.read()


def get_cpu_info_dict():
    cpu_data = read_cpuinfo()
    split_data = tuple(tuple(data.strip() for data in line.strip().split(':')) for line in cpu_data.splitlines() if line)
    return {tup[0]: tup[1] for tup in split_data}


