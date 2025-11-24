from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

MASIVOS_EGRESOS_DIR = Path("MASIVO EGRESOS")
MASIVOS_INGRESOS_DIR = Path("MASIVOS INGRESOS")
EGR_PEN_DIR = MASIVOS_EGRESOS_DIR / "SOLES"
EGR_USD_DIR = MASIVOS_EGRESOS_DIR / "DOLARES"
# ING_PEN_DIR = MASIVOS_INGRESOS_DIR / "SOLES"
# ING_USD_DIR = MASIVOS_INGRESOS_DIR / "DOLARES"


@dataclass
class Paths:
    """Class to store paths such as bot's root, config, src directories, etc."""

    ROOT: Path
    DOT_DATA: Path
    CONFIG_DIR: Path
    PROJECT_DIR: Path
    LOGS_DIR: Path
    INPUT_DIR: Path
    OUTPUT_DIR: Path
    TEMP_DIR: Path
    SIG_PATH: Path

    @classmethod
    def from_config(cls, bot_path: str, cp: ConfigParser) -> "Paths":
        """
        Create Paths object from bot's root path and ConfigParser object.

        Parameters:
            bot_path (str): It's the path where __init__.py is called.
            cp (ConfigParser): A ConfigParser object to read the configuration file

        Returns:
            Paths: A instance of Paths.
        """
        parents: Sequence[Path] = Path(bot_path).parents
        root: Path = parents[2]
        config_dir: Path = root / "config"
        project_dir: Path = parents[0]
        dot_data: Path = root / ".data"
        logs_dir: Path = dot_data / "logs"
        input_dir: Path = Path(
            cp.get("PATHS", "INPUT_PATH", fallback=dot_data / "input")
        )
        output_dir: Path = Path(
            cp.get("PATHS", "OUTPUT_PATH", fallback=dot_data / "output")
        )
        temp_dir: Path = Path(root / ".temp")
        sig_path: Path = Path(cp["PATHS"]["APP_PATH"])

        for path in (logs_dir, dot_data):
            path.mkdir(parents=True, exist_ok=True)

        return cls(
            ROOT=root,
            PROJECT_DIR=project_dir,
            CONFIG_DIR=config_dir,
            DOT_DATA=dot_data,
            LOGS_DIR=logs_dir,
            INPUT_DIR=input_dir,
            OUTPUT_DIR=output_dir,
            TEMP_DIR=temp_dir,
            SIG_PATH=sig_path,
        )
