import asyncio
import logging
from typing import Coroutine

from _pytest.mark import ParameterSet

from std_utils.pseudofs import cache
import pytest
from pytest_benchmark.plugin import benchmark



@pytest.mark.parametrize(('async_func',), ((cache.get_all_cpu_info,),))
@pytest.mark.benchmark
def test_async_func(benchmark, async_func: Coroutine):
    @benchmark
    def sync_test_func():
        return asyncio.run(async_func())

    assert sync_test_func

