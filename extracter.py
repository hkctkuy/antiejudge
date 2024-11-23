#!/bin/env python3.11

import argparse
import os
import re
import sys
import shutil
import textwrap

# Alias
REL_INPUTS_PATH = 'inputs'
REL_ANSWERS_PATH = 'answers'
BASENAME = 'test'

# Main regex
number = r'====== Тест #(?P<number>\d+) =======\n'
inp = r'''--- Входные данные: размер \d+ ---
(?P<input>(?:.*\n)*?)
--- Результат работы:( файл слишком велик,|) размер \d+ ---
'''
ans = r'''--- Правильный ответ:( файл слишком велик,|) размер \d+ ---
(?P<answer>(?:.*\n)*?)
--- Поток ошибок: размер \d+ ---
'''
pattern = r'%s%s(?:.*\n)*?%s' % (number, inp, ans)
regex = re.compile(pattern)


class CustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter
):
    pass


parser = argparse.ArgumentParser(
    description=textwrap.dedent('''
        Extract and save tests inputs and answers
    '''),
    epilog=textwrap.dedent(f'''
        Resulting test dir tree:
        tests
        ├── {REL_ANSWERS_PATH}
        │   ├── test1
        │   └── test2
        └── {REL_INPUTS_PATH}
            ├── test1
            └── test2

        NOTE: input and answer for one test is the same

        Written by Ilya "hkctkuy" Yegorov, 2024
    '''),
    formatter_class=CustomFormatter
)
parser.add_argument(
    'raw', default='raw', type=argparse.FileType(),
    help='Target file from which need to extract tests'
)
parser.add_argument(
    'out', type=str, nargs='?', default='tests',
    help='Path to resulting dir with tests'
)
parser.add_argument(
    '-f', '--force', action='store_true',
    help='if out dir exists it will be recreated'
)


def main(args):
    out = args.out
    inputs = os.path.join(out, REL_INPUTS_PATH)
    answers = os.path.join(out, REL_ANSWERS_PATH)
    if os.path.exists(out):
        if not args.force:
            print('Out dir already exists:', out, file=sys.stderr)
            sys.exit(1)
        else:
            shutil.rmtree(out)

    os.makedirs(out)
    os.makedirs(inputs)
    os.makedirs(answers)

    content = args.raw.read()

    for m in regex.finditer(content):
        name = BASENAME + m['number']

        inp = os.path.join(inputs, name)
        with open(inp, 'w+') as f:
            f.write(m['input'])

        ans = os.path.join(answers, name)
        with open(ans, 'w+') as f:
            f.write(m['answer'])
    return


if __name__ == '__main__':
    main(parser.parse_args())
