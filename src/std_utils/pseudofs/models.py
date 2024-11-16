from decimal import Decimal
from enum import StrEnum
from fractions import Fraction
from numbers import Integral
from typing import ClassVar

from pydantic import BaseModel, Field, field_validator


class TestMeasurement(BaseModel):
    value: float
    unit: str

class Measurement(BaseModel):
    value: Fraction = Field(json_schema_extra={
        'properties': {
            'value': {'title': 'Value', 'type': 'number'},
            'unit': {'title': 'Unit', 'type': 'string'}
        },
        'required': ['value', 'unit'],
        'title': 'TestMeasurement',
        'type': 'object'
    })
    unit: str


class MemoryUnit(StrEnum):
    BIT = "bit"
    BYTE = "byte"
    KB = "kb"
    KIB = "kib"
    MB = "mb"
    MIB = "mib"
    GB = "gb"
    GIB = "gib"
    TB = "tb"
    TIB = "tib"
    PB = "pb"
    PIB = "pib"


class MemoryMeasurement(Measurement):
    unit: MemoryUnit
    value: Fraction = Field(ge=0)
    units_to_bits: ClassVar[dict[MemoryUnit, int]] = Field(
        frozen=True,
        default={
            MemoryUnit.BIT: 1,
            MemoryUnit.BYTE: 8,
            MemoryUnit.KB: 8 * 10 ** 3,
            MemoryUnit.KIB: 8 * 2 ** 10,
            MemoryUnit.MB: 8 * 10 ** 6,
            MemoryUnit.MIB: 8 * 2 ** 20,
            MemoryUnit.GB: 8 * 10 ** 9,
            MemoryUnit.GIB: 8 * 2 ** 30,
            MemoryUnit.TB: 8 * 10 ** 12,
            MemoryUnit.TIB: 8 * 2 ** 40,
            MemoryUnit.PB: 8 * 10 ** 15,
            MemoryUnit.PIB: 8 * 2 ** 50,
        })

    @classmethod
    def get_bits(cls, value: Fraction, units: MemoryUnit) -> Fraction:
        return value * cls.units_to_bits[units]


    @field_validator('value')
    @classmethod
    def value_validator(cls, value: Fraction) -> Fraction:
        if cls.get_bits(value, cls.unit).is_integer():
            raise ValueError("Memory size must be non-negative")



    def convert(self, to_unit: MemoryUnit) -> 'MemoryMeasurement':
        """
        Convert memory sizes between different units.

        Parameters:
            value (float): The memory size to convert.
            from_unit (MemoryUnit): The unit of the input value (e.g., MemoryUnit.BIT, MemoryUnit.BYTE, etc.).
            to_unit (MemoryUnit): The unit to convert to (e.g., MemoryUnit.BIT, MemoryUnit.BYTE, etc.).

        Returns:
            float: The converted value.
        """

        # Define conversion factors for base-10 and base-2 units


        # Convert the input value to bits
        value_in_bits: Integral = self.value * self.units_to_bits[self.unit]

        # Convert the value from bits to the target unit
        converted_value = value_in_bits / self.units_to_bits[to_unit]

        return MemoryMeasurement(value=converted_value, unit=to_unit)

class CPUInfoInputModel(BaseModel):
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


class CPUInfoAddressSizes(BaseModel):
    '''Address sizes in bits'''
    physical: int
    virtual: int


class CPUInfoOutputModel(BaseModel):
    address_sizes: CPUInfoAddressSizes
    apicid: int
    bogomips: Decimal
    bugs: tuple[str]
    cache_alignment: int
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