from configparser import ConfigParser
from .logger import set_logger
from .paths import Paths

cp: ConfigParser = ConfigParser()
cp.read("config/config.ini")

paths: Paths = Paths.from_config(__file__, cp)

set_logger(paths.LOGS_DIR)
set_logger(paths.LOGS_DIR)