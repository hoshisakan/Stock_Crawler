import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from argparse import ArgumentParser
from instance.config import Initialization as Init
from module.log_generate import Loggings
# from pathlib import Path


logger = Loggings()

class ArgumentConfig():
    @staticmethod
    def run():
        parser = ArgumentParser()
        parser.add_argument("-t", "--task", help="stock ticker and country list", type=str)
        parser.add_argument("-o", "--output", help="stock info output path", type=str)
        args = parser.parse_args()

        if args.task and args.output:
            Init.stock_info_list_path = args.task
            Init.output_path = args.output
        else:
            logger.error(f"argument task and output is required.")
            os._exit(0)