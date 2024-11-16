import typing



cpuinfo_keys = (
'address_sizes', 'apicid', 'bogomips', 'bugs', 'cache_alignment', 'cache_size',
'clflush_size', 'core_id', 'cpu_MHz', 'cpu_cores', 'cpu_family', 'cpuid_level',
'flags', 'fpu', 'fpu_exception', 'initial_apicid', 'microcode', 'model',
'model_name', 'physical_id', 'power_management', 'processor', 'siblings',
'stepping', 'vendor_id', 'vmx_flags', 'wp')


class CPUInfoType(typing.NamedTuple):
    address_sizes: str
    apicid: str
    bogomips: str
    bugs: str
    cache_alignment: str
    cache_size: str
    clflush_size: str
    core_id: str
    cpu_MHz: str
    cpu_cores: str
    cpu_family: int
    cpuid_level: str
    flags: str
    fpu: str
    fpu_exception: str
    initial_apicid: str
    microcode: str
    model: str
    model_name: str
    physical_id: str
    power_management: str
    processor: str
    siblings: str
    stepping: str
    vendor_id: str
    vmx_flags: str
    wp: str
