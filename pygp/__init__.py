__author__= 'ananta narayanan'

import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import argparse, sys
from .parser import Parser

def main():

    cli = argparse.ArgumentParser(description="Gateway dataset Experiment")

    arg_parse = cli

    arg_parse.add_argument('-d', '--dest', type=str, help="stores the processed file to destination")
    arg_parse.add_argument('-p', '--parse', type=str, help="parses the dataset")
    arg_parse.add_argument('-ds', '--dataset', type=str, help="locate dataset")
    arg_parse.add_argument('-f', '--file', type=str, help="name of the file to be stored")

    if len(sys.argv) == 1:
        cli.print_help()
        return

    args = cli.parse_args()

    dataset = args.dataset if args.dataset else None

    if args.parse:
        p = Parser(dataset=dataset)
        if args.dest:
            p.generate_path(args.dest, filename=args.file)

