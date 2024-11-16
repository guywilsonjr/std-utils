import logging
from std_utils.benchmark.benchmark import benchmark, BenchMarkCallType, BenchmarkInput, ParamatersInstance, StarmapInstance
from std_utils.std_collections.sequence import linux_seq

logging.basicConfig(level=logging.INFO)


def test_seq_benchmark():
    arg_inputs = ((1,), (10,), (100,), (1000,))
    param_data = tuple(map(lambda args: ParamatersInstance(args=args), arg_inputs[:1]))
    starmap_data = StarmapInstance(callable=linux_seq, param_data=param_data)

    benchmark_input = BenchmarkInput(
        name="test_linux_seq",
        call_type=BenchMarkCallType.ARGS,
        iterations=5,
        starmap_data=starmap_data
    )
    output = benchmark(benchmark_input)
    logging.info(output.print())
    logging.info(output.name)


    starmap_data = StarmapInstance(callable=range, param_data=param_data)

    benchmark_input = BenchmarkInput(
        name="test_range",
        call_type=BenchMarkCallType.ARGS,
        iterations=5,
        starmap_data=starmap_data
    )
    output = benchmark(benchmark_input)
    logging.info(output.print())
    logging.info(output.name)