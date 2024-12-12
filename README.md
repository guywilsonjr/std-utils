# std-utils
Standard Python Utils

## Benchmark reports
Benchmark reports are stored in [.reports/benchmarks](.reports/benchmarks)

### Reading CProfile data

- ncalls: Total number of calls to the function. If there are two numbers, that means the function recursed and the
  first is the total number of calls and the second is the number of primitive (non-recursive) calls.
- tottime: total time spent in the given function (excluding time made in calls to sub-functions)
- percall: tottime divided by ncalls
- cumtime: is the cumulative time spent in this and all subfunctions (from invocation till exit). This figure is
  accurate even for recursive functions.
- percall: cumtime divided by primitive calls