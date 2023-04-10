from glue_helper_lib import arguments, logging
from demo_lib import show
import dataclasses

logger = logging.Logger("demo-logger", logging.LogLevel.DEBUG, None)


@dataclasses.dataclass
class DemoArguments(arguments.Arguments):
    demo_argument: str


args = DemoArguments.from_glue_arguments()
logger.info("demo arguments: %s", args)

demo_lib_works = show.show_demo_lib_works()
logger.info(demo_lib_works)
