"""
Simple key generation.
"""
from itertools import combinations
from random import randint
import argparse
import math
import sys


# Basics
NUMBERS_DICTIONARY = '0123456789'
SPECIAL_CHARS_DICTIONARY = '.+-*/\\|°¬!"#$&/()=?¡¨*[]{}´+,.;:-_<>@'
CHARS_DICTIONARY = 'abcdefghijklmnñopqrstuvwxyz'
DEFAULT_KEYS_AMOUNT = 10
DEFAULT_KEYS_LENGTH = 16


def binomial_coefficient(n: int, k: int) -> int:
    """Calculate Binomial coefficient"""
    n_fac = math.factorial(n)
    k_fac = math.factorial(k)
    n_minus_k_fac = math.factorial(n - k)
    return round(n_fac/(k_fac*n_minus_k_fac))


def _default_dictionary(use_uppercase=True, use_numbers=True, use_special_chars=True):
    """
    Build a dictionary by default.

    Args:
        - use_uppercase: Include upper cases in dictionary.
            - Type: bool
            - Default: True.

        - use_numbers: Include numbers in default dictionary
            - Type: bool
            - Default: True.

        - use_special_chars: Include specials characters in default dictionary.
            - Type: bool
            - Default: True.
    """
    _dict = CHARS_DICTIONARY
    _dict += CHARS_DICTIONARY.upper() if use_uppercase else ''
    _dict += NUMBERS_DICTIONARY if use_numbers else ''
    _dict += SPECIAL_CHARS_DICTIONARY if use_special_chars else ''
    return _dict


def generate_by_random(**kwargs):
    """Generates keys randomly"""
    _dictionary_ = kwargs.get('dictionary')
    if any(x is None for x in [_dictionary_, kwargs.get('length'), kwargs.get('amount')]):
        raise KeyError('Random Dict generator: missing required argument.')

    generated_keys = []
    for i in range(kwargs.get('amount')):
        while True:
            nk = ''
            while len(nk) < kwargs.get('length'):
                nk += _dictionary_[randint(0, len(_dictionary_)-1)]
            if nk not in generated_keys:
                generated_keys.append(nk)
                sys.stdout.write(f'{nk}\n')
                break


def generate_by_combinations(**kwargs):
    """Generates Keys using itertools.combinations."""
    _dictionary_ = kwargs.get('dictionary')

    if any(x is None for x in [_dictionary_, kwargs.get('length'), kwargs.get('amount')]):
        raise KeyError('Combination Dict generator: missing required argument.')

    for idx, key in enumerate(combinations(_dictionary_, kwargs.get('length'))):
        if idx > kwargs.get('amount'):
            break
        sys.stdout.write(''.join(list(key)) + '\n')


RECORD_GENERATION_METHODS = {
    'combinations': generate_by_combinations,
    'randomize': generate_by_random
}


def prepare_chars_dictionary(_dictionary_, **kwargs):
    """
    Convert a str to list char.

    Args:
        - char_dict: str(strict)

    Return:
        - char list.
    """
    if not isinstance(_dictionary_, str) or len(_dictionary_) == 0 or _dictionary_ == 'undefined':
        # Build default dict
        _dictionary_ = _default_dictionary(use_numbers=kwargs.get('use_numbers', True),
                                           use_uppercase=kwargs.get('use_uppercase', True),
                                           use_special_chars=kwargs.get('use_special_chars', False))
    else:
        if kwargs.get('use_uppercase') is True:
            _dictionary_ += _dictionary_.upper()
    return [x for x in _dictionary_]


if __name__ == '__main__':
    """Main"""
    parser = argparse.ArgumentParser(description="Char dictionary generator", allow_abbrev=True)

    # KeyGen Ags setup
    parser.add_argument('--dictionary', '-d', help='Dictionary elements.', default='undefined', type=str)
    parser.add_argument('--amount', '-a', help='Amount of keys.', default=DEFAULT_KEYS_AMOUNT, type=str)
    parser.add_argument('--length', '-l', help='Keys length', default=DEFAULT_KEYS_LENGTH, type=int)
    parser.add_argument('--uppercase', '-u', help='Use upper case', action='store_true')
    parser.add_argument('--numbers', '-n', help='Use add to dictionary numbers chars.', action='store_true')
    parser.add_argument('--randomize', '-r', action='store_true', default=False,
                        help='Generation method, if -r or --randomize is present'
                             'random generation selected else, permutations method selected.')

    arguments = parser.parse_args()

    # Get Args
    _dictionary = arguments.dictionary
    _uppercase = arguments.uppercase
    _numbers = arguments.numbers
    _amount = int(arguments.amount)
    _length = int(arguments.length)

    # Pepare Chars Dictionary
    dictionary = prepare_chars_dictionary(_dictionary_=_dictionary,
                                          use_uppercase=_uppercase,
                                          use_numbers=_numbers)
    method = 'randomize' if arguments.randomize else 'combinations'
    try:
        if int(_amount) > binomial_coefficient(len(dictionary), _length):
            raise IndexError(f'With provided dictionary it is impossible generate {_amount} keys.')
        RECORD_GENERATION_METHODS[method](dictionary=dictionary, length=_length, amount=_amount)
    except MemoryError:
        print('You do not have enough memory for do this table.')
    except ValueError:
        print(f'Record length({_length}) can\'t be greater than dictionary length({len(dictionary)}).')
