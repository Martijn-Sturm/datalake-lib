import enum


class DatalakeFormat(enum.Enum):
    HUDI = "hudi"
    DELTA = "delta"
    ICEBERG = "iceberg"


class WorkerType(enum.Enum):
    G_1X = "G.1X"
    G_2X = "G.2X"


class JobType(enum.Enum):
    GLUE_ETL = "glueetl"
    PYTHON_SHELL = "pythonshell"


class ExecutionClass(enum.Enum):
    STANDARD = "STANDARD"
    FLEX = "FLEX"
