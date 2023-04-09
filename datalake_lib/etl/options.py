import enum
import typing


class DatalakeFormat(enum.Enum):
    HUDI = "hudi"
    DELTA = "delta"
    ICEBERG = "iceberg"
