import asyncio
import os
import typing

import aiofile




sysfs_cpu_dir = '/sys/devices/system/cpu'
l1_cache_dir = 'index0'
l2_cache_dir = 'index1'
l3_cache_dir = 'index2'
l4_cache_dir = 'index3'
cache_dirs = (l1_cache_dir, l2_cache_dir, l3_cache_dir, l4_cache_dir)

cache_info_files = (
    'id',
    'level',
    'type',
    'size',
    'coherency_line_size',
    'number_of_sets',
    'ways_of_associativity',
    'shared_cpu_list',
    'shared_cpu_map',
)


class CPUCacheLevelInfo(typing.NamedTuple):
    id: str
    level: int
    type: str
    size: str
    coherency_line_size: str
    number_of_sets: str
    ways_of_associativity: str
    shared_cpu_list: str
    shared_cpu_map: str


def is_cpu_dir(dir_name: str) -> bool:
    return dir_name.startswith('cpu') and dir_name[-1].isnumeric()


def get_cpu_list():
    cpu_list = tuple(filter(is_cpu_dir, os.listdir(sysfs_cpu_dir)))
    return cpu_list


async def read_data_from_file(file_path: str):
    async with aiofile.async_open(file_path, 'r') as afp:
        return (await afp.read()).rstrip()


async def get_cache_cpu_level_info(cache_dir: str):
    coros = (read_data_from_file(f'{cache_dir}/{file}') for file in cache_info_files)
    return tuple(await asyncio.gather(*coros))


def construct_cpu_cache_level_data(data: tuple[str, str, str, str, str, str, str, str, str]):
    cpu_id = int(data[0])
    cache_level = int(data[1])
    cache_type = data[2]
    total_cache_size = int(data[3][:-1])
    cache_line_size = int(data[4])
    number_of_sets = int(data[5])
    ways_of_associativity = int(data[6])
    shared_cpu_list_str = data[7]
    shared_cpu_start, shared_cpu_end = map(int, shared_cpu_list_str.split('-'))
    shared_cpu_list = tuple(range(shared_cpu_start, shared_cpu_end + 1))
    shared_cpu_map = int(data[8])
    return CPUCacheLevelInfo(
        cpu_id,
        cache_level,
        cache_type,
        total_cache_size,
        cache_line_size,
        number_of_sets,
        ways_of_associativity,
        shared_cpu_list,
        shared_cpu_map
    )


async def get_cache_cpu_info(cpu_name: str):
    full_cache_dirs = tuple('/'.join((sysfs_cpu_dir, cpu_name,'cache', cache_dir)) for cache_dir in cache_dirs)
    test_dir = full_cache_dirs[0]
    print(test_dir)
    data = await get_cache_cpu_level_info(test_dir)
    return construct_cpu_cache_level_data(data)

print(get_cpu_list())
print(asyncio.run(get_cache_cpu_info('cpu0')))
