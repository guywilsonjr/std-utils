import asyncio
import logging
from typing import Coroutine
from std_utils.pseudofs import cache
import pytest
from pytest_benchmark.plugin import benchmark




@pytest.mark.benchmark
def test_cache(benchmark):

    @benchmark
    def run():
        return asyncio.run(cache.get_all_cpu_info())

    assert run

