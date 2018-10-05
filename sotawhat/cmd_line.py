import os
import argparse
import warnings
from sotawhat import sotawhat


def main():
    parser = argparse.ArgumentParser('Query arxiv-sanity to obtain most recent sota papers.')

    parser.add_argument('query', type=str,
                        help='Keyword to query')

    parser.add_argument('-c', '--count', type=int, default=5,
                        help='Number of results to display')

    parser.add_argument('-e', '--exact', action='store_true', dest='exact',
                        help='Assume query is exact, with no spelling mistakes')
    parser.set_defaults(exact=False)

    args = parser.parse_args()

    if 'nt' in os.name:
        try:
            import win_unicode_console
            win_unicode_console.enable()
        except ImportError:
            warnings.warn('On Windows, encoding errors may arise when displaying the data.\n'
                          'If such errors occur, please install `win_unicode_consolde` via \n'
                          'the command `pip install win-unicode-console`.')

    sotawhat.main(args)
