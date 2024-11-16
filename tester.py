#!/bin/env python3.11

import argparse
import filecmp
import glob
import os
import shutil
import subprocess
import sys
import textwrap

from enum import StrEnum

MAX_HELP_POSITION = 100

REL_INPUTS_PATH = 'inputs'
REL_ANSWERS_PATH = 'answers'

SNIP_RUNNER = 'tmp_snippet_runner.py'
OUT = 'tmp_out.out'


class Mode(StrEnum):
    Stdin = 'stdin'
    Snippet = 'snippet'


class CustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter
):
    def __init__(self, *args, **kwargs):
        if 'max_help_position' not in kwargs:
            kwargs['max_help_position'] = MAX_HELP_POSITION
        super().__init__(*args, **kwargs)


parser = argparse.ArgumentParser(
    description=textwrap.dedent('''
        Test given python program
    '''),
    epilog=textwrap.dedent(f'''
        Each test dir tree:
        tests
        ├── {REL_ANSWERS_PATH}
        │   ├── test1
        │   └── test2
        └── {REL_INPUTS_PATH}
            ├── test1
            └── test2
        NOTE: input and answer for one test should be the same

        Use stdin mode for program getting input from stdin
        Use snippet mode for testing functions, classes and others
        Made by Ilya "hkctkuy" Yegorov
    '''),
    formatter_class=CustomFormatter
)
parser.add_argument(
    'target',
    help='Tested python program path'
)
parser.add_argument(
    'mode', type=Mode, choices=Mode,
    help='Test mode'
)
parser.add_argument(
    '--tests', dest='dirs', metavar='DIR',
    action='extend', nargs='+', default=['tests'],
    help='Paths to dirs with tests'
)
parser.add_argument(
    '--abort-on-error', dest='abort',
    action=argparse.BooleanOptionalAction,
    default=True,
    help='''
        Abort testing if some test fails
    '''
)
parser.add_argument(
    '-t', '--timeout', metavar='SEC',
    type=int, default=None,
    help='Timeout in sec'
)


def extract(test_dir):
    inputs = os.path.join(test_dir, REL_INPUTS_PATH)
    answers = os.path.join(test_dir, REL_ANSWERS_PATH)
    if (
        not os.path.exists(inputs)
        or not os.path.isdir(inputs)
    ):
        print('Bed test inputs path:', inputs, file=sys.stderr)
        return None, None
    if (
        not os.path.exists(inputs)
        or not os.path.isdir(inputs)
    ):
        print('Bed test answers path:', answers, file=sys.stderr)
        return None, None
    inputs = glob.glob(os.path.join(inputs, '**/*'), recursive=True)
    answers = glob.glob(os.path.join(answers, '**/*'), recursive=True)
    inputs.sort()
    answers.sort()
    return inputs, answers


def append(src, dest):
    with open(src, 'r') as src, open(dest, 'a+') as dest:
        dest.write(src.read())


def run_test(target, inp, ans, mode, timeout):
    runner = target
    stdin = inp
    if mode == Mode.Snippet:
        shutil.copy(target, SNIP_RUNNER)
        append(inp, SNIP_RUNNER)
        runner = SNIP_RUNNER
        stdin = None
    else:
        stdin = open(inp, 'r')

    cmd = ['python3', runner]
    try:
        with open(OUT, 'w+') as out:
            subprocess.run(cmd, stdin=stdin, stdout=out, timeout=timeout)
    except subprocess.TimeoutExpired:
        print('TIMEOUT!', file=sys.stderr)
        return False
    return filecmp.cmp(OUT, ans, shallow=False)


def cleanup():
    try:
        os.remove(OUT)
        os.remove(SNIP_RUNNER)
    except OSError:
        pass


def main(args):
    dirs = set(args.dirs)
    for test_dir in dirs:
        inputs, answers = extract(test_dir)
        if not inputs or not answers:
            continue
        for (inp, ans) in zip(inputs, answers):
            if os.path.basename(inp) != os.path.basename(ans):
                print('Missing test:', inp, file=sys.stderr)
                continue
            status = run_test(args.target, inp, ans, args.mode, args.timeout)
            if status:
                print('OK')
            else:
                print('FAILED:', inp, ans)
                if args.abort:
                    sys.exit(1)
    else:
        cleanup()


if __name__ == '__main__':
    main(parser.parse_args())
