import argparse
import json
import sys

from . import encoders
from . import reader


def new_arg_parser():
    choices = sorted(encoders.JSON_ENCODERS)

    parser = argparse.ArgumentParser()
    parser.add_argument('--bytes', choices=choices, default='utf-8')
    parser.add_argument('source')

    return parser


def main(argv, outfile):
    args = new_arg_parser().parse_args(argv[1:])
    encoder = encoders.JSON_ENCODERS[args.bytes]

    for key, props in reader.find_records(args.source):
        props['_key'] = key
        json.dump(props, outfile, cls=encoder)
        outfile.write('\n')
