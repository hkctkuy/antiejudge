# Usage

## extracter.py

    usage: extracter.py [-h] [-f] raw [out]

    Extract and save tests inputs and answers

    positional arguments:
      raw          Target file from which need to extract tests
      out          Path to resulting dir with tests (default: tests)

    options:
      -h, --help   show this help message and exit
      -f, --force  if out dir exists it will be recreated (default: False)

    Resulting test dir tree:
    tests
    ├── answers
    │   ├── test1
    │   └── test2
    └── inputs
        ├── test1
        └── test2

    NOTE: input and answer for one test is the same

    Written by Ilya "hkctkuy" Yegorov, 2024

## tester.py

    usage: tester.py [-h] [--tests DIR [DIR ...]] [--abort-on-fail | --no-abort-on-fail] [-t SEC]
                     target {stdin,snippet}

    Test given python program

    positional arguments:
      target                               Tested python program path
      {stdin,snippet}                      Test mode

    options:
      -h, --help                           show this help message and exit
      --tests DIR [DIR ...]                Paths to dirs with tests (default: ['tests'])
      --abort-on-fail, --no-abort-on-fail  Abort testing if some test fails (default: True)
      -t SEC, --timeout SEC                Timeout in sec (default: None)

    Use stdin mode for program getting input from stdin
    Use snippet mode for testing functions, classes and others

    Each test dir tree:
    tests
    ├── answers
    │   ├── test1
    │   └── test2
    └── inputs
        ├── test1
        └── test2

    NOTE: input and answer for one test should be the same

    NOTE: for python target use shebang (#!/bin/env python3 or etc)
    Read more: https://en.wikipedia.org/wiki/Shebang_(Unix)

    Written by Ilya "hkctkuy" Yegorov, 2024
