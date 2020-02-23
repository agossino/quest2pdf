#!/usr/bin/env python
import configparser
import argparse
import logging
import logging.config
import json
import pathlib
from typing import Dict, Any, List
from _version import __version__

logName = "quest2pdf." + __name__
logger = logging.getLogger(logName)


def param_parser(args: List[str] = None) -> Dict[str, Any]:
    """Arguments from command line have precedence over the ones
    coming from configuration file.
    """
    default_delimiter = ","
    delimiters_translator = {
        "colon": ":",
        "comma": ",",
        "dash": "-",
        "exclamation": "!",
        "period": ".",
        "semicolon": ";",
        "space": " ",
        "tab": "\t",
    }
    parser = cli_parser()
    cli_args = vars(parser.parse_args(args))

    start_logger(pathlib.Path(cli_args["log_configuration_file"]))

    default_values = get_default(parser)

    cli_chosen: Dict[str, Any] = {}
    for key, value in cli_args.items():
        if value != parser.get_default(key):
            cli_chosen[key] = value

    # configuration file comes from cli, if set, or the default one
    config_file = cli_chosen.get(
        "app_configuration_file", cli_args["app_configuration_file"]
    )

    # cli chosen values override configuration file values
    result = default_values
    result.update(conf_file_parser(config_file))
    result.update({"app_configuration_file": config_file})
    result.update(cli_chosen)

    result["delimiter"] = delimiters_translator.get(
        result["delimiter"], default_delimiter
    )

    return result


def cli_parser():
    description = (
        "Provide a PDF file from a text file: "
        + "this represents an exam, made of question with multiple answers."
    )
    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "input",
        type=str,
        nargs="?",
        help="input text file with questions and answers.",
        default="questions.csv",
    )
    parser.add_argument(
        "-n", "--number", type=int, nargs="?", help="number of output files.", default=1
    )
    parser.add_argument(
        "-e",
        "--exam",
        help="file name prefix; date and time till ms, is appended.",
        type=str,
        default="Exam",
    )
    parser.add_argument(
        "-c",
        "--correction",
        help="correction file prefix; date and time till ms, is appended.",
        type=str,
        default="Correction",
    )
    parser.add_argument(
        "-f",
        "--app_configuration_file",
        help="application configuration file.",
        default="conf.ini",
    )
    parser.add_argument(
        "-l",
        "--log_configuration_file",
        help="log configuration file.",
        default="loggingConf.json",
    )
    parser.add_argument(
        "-s",
        "--shuffle",
        help="if set, question sequence will be shuffled.",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        "--page_heading",
        help="page heading; if not set, file name is provided.",
        nargs="?",
        const=True,
        default=False,
    )
    parser.add_argument("-E", "--encoding", help="character encoding.", default="utf-8")
    parser.add_argument(
        "-d",
        "--delimiter",
        choices=[
            "exclamation",
            "dash",
            "period",
            "space",
            "comma",
            "semicolon",
            "colon",
            "tab",
        ],
        help="delimiter for comma separated value input file.",
        default="comma",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="show current version.",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    return parser


def start_logger(file_name: pathlib.Path) -> None:
    script_path: pathlib.Path = pathlib.Path(__file__).resolve().parent
    home_path: pathlib.Path = pathlib.Path.home()

    for file in (
        file_name,
        script_path.joinpath(file_name),
        home_path.joinpath(file_name),
    ):
        result = try_log_conf_file(file)
        if result is True:
            return

    logger.warning("configuration file not found: default configuration will be used.")


def try_log_conf_file(file_path: pathlib.Path) -> bool:
    """It tries to open a log configuration file.
    filePath: filePath
    return: boolean (True is succeed, False otherwise)
    """
    global logger

    try:
        with file_path.open() as f:
            logger_conf = json.load(f)
            logging.config.dictConfig(logger_conf)
            logger = logging.getLogger(__name__)
            logger.debug("logger started from " + str(pathlib.Path.cwd()))
            logger.info(str(file_path) + " found")
            return True
    except FileNotFoundError as e:
        msg = str(file_path) + " not found"
        logger.info(msg + str(e))
        return False


def get_default(parser: argparse.ArgumentParser) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    args: Dict[str, Any] = vars(parser.parse_args())
    for key, value in args.items():
        result[key] = parser.get_default(key)
    return result


def conf_file_parser(file_name):
    scriptPath = pathlib.Path(__file__).resolve().parent
    homePath = pathlib.Path.home()

    for file in (
        file_name,
        scriptPath.joinpath(file_name),
        homePath.joinpath(file_name),
    ):
        output = try_conf_file(file)
        if output is not None:
            return output

    msg = "configuration file not found in . " + str(scriptPath) + str(homePath)
    logger.critical(msg)
    raise FileNotFoundError(msg)


def try_conf_file(filePath):
    output = {}
    config = configparser.ConfigParser()
    filePath = str(filePath)

    try:
        with open(filePath, "r") as f:
            config.read_file(f)
            logger.info(filePath + " found")
            for key, value in config["Default"].items():
                output[key] = value
    except FileNotFoundError as e:
        msg = filePath + " not found"
        logger.info(msg + str(e))
        return None

    return output
