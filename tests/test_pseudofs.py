import asyncio
import logging

from std_utils.pseudofs import cache

def test_cache():
    logging.info(cache.get_cpu_list())
    logging.info(asyncio.run(cache.get_cache_cpu_info('cpu0')))