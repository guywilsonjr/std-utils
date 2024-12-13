from pytest_benchmark.fixture import BenchmarkFixture
from std_utils.pseudofs import cache
from utils import get_benchmark_data


def test_get_all_cpu_info(benchmark: BenchmarkFixture):
    benchmark_data = get_benchmark_data(cache.get_all_cpu_info)
    benchmark(**benchmark_data)







