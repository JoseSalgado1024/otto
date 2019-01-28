"""
Simple key generation
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
DEFAULT_RECORDS_AMOUNT = 10
DEFAULT_RECORDS_LENGTH = 16


def binomial_coefficient(n: int, k: int) -> int:
    n_fac = math.factorial(n)
    k_fac = math.factorial(k)
    n_minus_k_fac = math.factorial(n - k)
    return round(n_fac/(k_fac*n_minus_k_fac))


def _default_dictionary(use_uppercase=True, use_numbers=True, use_special_chars=True):
    _dict = CHARS_DICTIONARY
    _dict += CHARS_DICTIONARY.upper() if use_uppercase else ''
    _dict += NUMBERS_DICTIONARY if use_numbers else ''
    _dict += SPECIAL_CHARS_DICTIONARY if use_special_chars else ''
    return _dict


# Scrip arguments
script_arguments = [
    {
        'flag': '--dictionary,-d',
        'help': 'Dictionary elements.',
        'default': 'undefined',
        'action': '',
        'type': str
    },
    {
        'flag': '--amount,-a',
        'help': 'Amount of records.',
        'default': DEFAULT_RECORDS_AMOUNT,
        'action': '',
        'type': int
    },
    {
        'flag': '--length,-l',
        'help': 'Records length.',
        'default': DEFAULT_RECORDS_LENGTH,
        'action': '',
        'type': int
    },
    {
        'flag': '--randomize,-r',
        'help': 'Generation method, if -r or --randomize is present,'
                'random generation selected else, permutations method selected.',
        'default': None,
        'type': bool,
        'action': 'store_true'
    },
    {
        'flag': '--uppercase,-u',
        'help': 'Use upper case.',
        'default': None,
        'action': 'store_true',
        'type': bool
    },
    {
        'flag': '--numbers,-n',
        'help': 'Use add to dictionary numbers chars.',
        'default': None,
        'action': 'store_true',
        'type': bool
    }
]


def generate_by_random(**kwargs):
    """Generates key randomly"""

    _dictionary = kwargs.get('dictionary')
    _length = kwargs.get('length')
    _amount = kwargs.get('amount')

    if any(x is None for x in [_dictionary, _length, _amount]):
        raise KeyError('Random Dict generator: missing required argument.')

    generated_keys = []
    for i in range(kwargs.get('amount')):
        while True:
            nk = ''
            while len(nk) < _length:
                nk += _dictionary[randint(0, len(_dictionary)-1)]
            if nk not in generated_keys:
                generated_keys.append(nk)
                break
    return generated_keys


def generate_by_combinations(**kwargs):
    _dictionary = kwargs.get('dictionary')
    _length = kwargs.get('length')
    _amount = kwargs.get('amount')

    if any(x is None for x in [_dictionary, _length, _amount]):
        raise KeyError('Combination Dict generator: missing required argument.')

    generated_key = list(combinations(_dictionary, _length))
    return [''.join(generated_key[i]) for i in range(_amount-1)]


RECORD_GENERATION_METHODS = {
    'combinations': generate_by_combinations,
    'randomize': generate_by_random
}


def prepare_chars_dictionary(_dictionary, **kwargs):
    """
    Convert a str to list char.

    Args:
        - char_dict: str(strict)

    Return:
        - char list.
    """
    if not isinstance(_dictionary, str) or len(_dictionary) == 0 or _dictionary == 'undefined':
        # Build default dict
        _dictionary = _default_dictionary(use_numbers=kwargs.get('use_numbers', True),
                                          use_uppercase=kwargs.get('use_uppercase', True),
                                          use_special_chars=kwargs.get('use_special_chars', False))
    return [x for x in _dictionary]


if __name__ == '__main__':
    """Main"""
    parser = argparse.ArgumentParser(description="Char dictionary generator", allow_abbrev=True)
    # KeyGen Ags
    for args in script_arguments:
        # add scripts arguments
        parser.add_argument(*args.get('flag').split(','),
                            help=args.get('help'),
                            type=args.get('type'),
                            default=args.get('default'))
    arguments = parser.parse_args()
    dictionary = prepare_chars_dictionary(_dictionary=arguments.dictionary,
                                          use_uppercase=arguments.uppercase,
                                          use_numbers=arguments.numbers)
    method = 'randomize' if arguments.randomize else 'combinations'
    try:
        if arguments.amount > binomial_coefficient(len(dictionary), arguments.length):
            raise IndexError(f'With provided dictionary it is impossible generate {arguments.amount} keys.')
        records = RECORD_GENERATION_METHODS[method](dictionary=dictionary,
                                                    length=arguments.length,
                                                    amount=arguments.amount)
        for record in records:
            sys.stdout.write(f'{record}\n')
    except MemoryError:
        print('You do not have enough memory for do this table.')
    except ValueError:
        print(f'Record length({arguments.length}) can\'t be greater than dictionary length({len(dictionary)}).')
