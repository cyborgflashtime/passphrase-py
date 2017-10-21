"""Passphrase: Generates cryptographically secure passphrases and passwords

Passphrases are built by picking from a word list using cryptographically
secure random number generator. Passwords are built from printable characters.
"""

from os.path import isfile
from string import digits, ascii_letters, punctuation
from .secrets import randchoice, randhex, randbetween
from .calc import entropy_bits as calc_entropy_bits
from .calc import entropy_bits_nrange as calc_entropy_bits_nrange
from .calc import password_len_needed as calc_password_len_needed
from .calc import words_amount_needed as calc_words_amount_needed
from .settings import MIN_NUM, MAX_NUM, ENTROPY_BITS_MIN

__author__ = "HacKan"
__license__ = "GNU GPL 3.0+"
__version__ = "0.4.3"


class Passphrase():
    """Generates cryptographically secure passphrases and passwords.

    Attributes:
        wordlist: A list of words to be consumed by the passphrase generator.
        amount_w: Amount of words to be generated by the passphrase generator.
        amount_n: Amount of numbers to be generated by the passphrase
                  generator.
        randnum_min: Minimum value for the random number in the passphrase.
        randnum_max: Maximum value for the random number in the passphrase.
        passwordlen: Length of the password.
        last_result: The last generated passphrase or password.
    """

    _passwordlen = 12    # For EFF Large Wordlist
    _amount_n = 0
    _amount_w = 6        # For EFF Large Wordlist
    last_result = []
    _randnum_min = MIN_NUM
    _randnum_max = MAX_NUM
    _entropy_bits_req = ENTROPY_BITS_MIN
    _wordlist = []
    _wordlist_entropy_bits = 0
    _external_wordlist = False
    _separator = ' '

    @property
    def entropy_bits_req(self):
        return self._entropy_bits_req

    @entropy_bits_req.setter
    def entropy_bits_req(self, entropybits: float) -> None:
        if not isinstance(entropybits, (int, float)):
            raise TypeError('entropy_bits_req can only be int or float')
        if entropybits < 0:
            raise ValueError('entropy_bits_req should be greater than 0')
        self._entropy_bits_req = float(entropybits)

    @property
    def randnum_min(self):
        return self._randnum_min

    @randnum_min.setter
    def randnum_min(self, randnum: int) -> None:
        if not isinstance(randnum, int):
            raise TypeError('randnum_min can only be int')
        if randnum < 0:
            raise ValueError('randnum_min should be greater than 0')
        self._randnum_min = randnum

    @property
    def randnum_max(self):
        return self._randnum_max

    @randnum_max.setter
    def randnum_max(self, randnum: int) -> None:
        if not isinstance(randnum, int):
            raise TypeError('randnum_max can only be int')
        if randnum < 0:
            raise ValueError('randnum_max should be greater than 0')
        self._randnum_max = randnum

    @property
    def amount_w(self):
        return self._amount_w

    @amount_w.setter
    def amount_w(self, amount: int) -> None:
        if not isinstance(amount, int):
            raise TypeError('amount_w can only be int')
        if amount < 0:
            raise ValueError('amount_w should be greater than 0')
        self._amount_w = amount

    @property
    def amount_n(self):
        return self._amount_n

    @amount_n.setter
    def amount_n(self, amount: int) -> None:
        if not isinstance(amount, int):
            raise TypeError('amount_n can only be int')
        if amount < 0:
            raise ValueError('amount_n should be greater than 0')
        self._amount_n = amount

    @property
    def passwordlen(self):
        return self._passwordlen

    @passwordlen.setter
    def passwordlen(self, length: int) -> None:
        if not isinstance(length, int):
            raise TypeError('passwordlen can only be int')
        if length < 0:
            raise ValueError('passwordlen should be greater than 0')
        self._passwordlen = length

    @property
    def separator(self):
        return self._separator

    @separator.setter
    def separator(self, sep: str) -> None:
        if not isinstance(sep, str):
            raise TypeError('separator can only be string')
        self._separator = sep

    @property
    def wordlist(self):
        return self._wordlist

    @wordlist.setter
    def wordlist(self, words: list) -> None:
        if not isinstance(words, (list, tuple)):
            raise TypeError('wordlist can only be list or tuple')
        self._wordlist = list(words)
        self._external_wordlist = True

    def __init__(self,
                 inputfile: str = None,
                 is_diceware: bool = False) -> None:
        if inputfile is not None:
            self.import_words_from_file(inputfile, is_diceware)
        else:
            # Read default wordlist
            from json import loads as json_loads
            from pkg_resources import resource_string

            wordlist = json_loads(resource_string(
                'passphrase',
                'wordlist.json'
            ).decode('utf-8'))
            self._wordlist = wordlist['wordlist']
            self._wordlist_entropy_bits = wordlist['entropy_bits']
            self._external_wordlist = False

    def __str__(self) -> str:
        if self.last_result is None:
            return ''

        separator_len = len(self.separator)
        rm_last_separator = -separator_len if separator_len > 0 else None
        return "".join(
            '{}{}'.format(w, self.separator) for w in map(
                str,
                self.last_result
            )
        )[:rm_last_separator:]

    @staticmethod
    def entropy_bits(lst: list) -> float:
        """Calculate the entropy of a wordlist or a numerical range.

        Keyword arguments:
        lst -- A wordlist or a numerical range as a list: (minimum, maximum)

        Returns: float
        """
        size = len(lst)
        if (size == 2 and
                isinstance(lst[0], (int, float)) is True and
                isinstance(lst[1], (int, float)) is True):
            return calc_entropy_bits_nrange(lst[0], lst[1])

        return calc_entropy_bits(lst)

    @staticmethod
    def _read_words_from_wordfile(inputfile: str) -> list:
        if isfile(inputfile) is False:
            raise FileNotFoundError('Input file does not exists: '
                                    '{}'.format(inputfile))

        return [
            word.strip() for word in open(inputfile, mode='rt')
        ]

    @staticmethod
    def _read_words_from_diceware(inputfile: str) -> list:
        if isfile(inputfile) is False:
            raise FileNotFoundError('Input file does not exists: '
                                    '{}'.format(inputfile))

        return [
            word.split()[1] for word in open(inputfile, mode='rt')
        ]

    def import_words_from_file(self,
                               inputfile: str,
                               is_diceware: bool) -> None:
        if is_diceware is True:
            self.wordlist = self._read_words_from_diceware(inputfile)
        else:
            self.wordlist = self._read_words_from_wordfile(inputfile)

    def password_len_needed(self) -> int:
        return calc_password_len_needed(self.entropy_bits_req)

    def words_amount_needed(self) -> int:
        # Thanks to @julianor for this tip to calculate default amount of
        # entropy: minbitlen/log2(len(wordlist)).
        # I set the minimum entropy bits and calculate the amount of words
        # needed, cosidering the entropy of the wordlist.
        # Then: entropy_w * amount_w + entropy_n * amount_n >= ENTROPY_BITS_MIN
        entropy_n = self.entropy_bits((self.randnum_min, self.randnum_max))

        # The entropy for EFF Large Wordlist is ~12.9, no need to calculate
        if self._external_wordlist is False:
            entropy_w = self._wordlist_entropy_bits
        else:
            entropy_w = self.entropy_bits(self._wordlist)

        return calc_words_amount_needed(
            self.entropy_bits_req,
            entropy_w,
            entropy_n,
            self.amount_n
        )

    def generate(self) -> list:
        """Generates a list of words randomly chosen from a wordlist."""

        if len(self.wordlist) < 1:
            raise ValueError('wordlist can\'t be empty')

        passphrase = []
        for _ in range(0, self.amount_w):
            passphrase.append(randchoice(self.wordlist))

        for _ in range(0, self.amount_n):
            passphrase.append(randbetween(MIN_NUM, MAX_NUM))

        self.last_result = passphrase
        return passphrase

    def generate_password(self) -> list:
        """Generates a list of random characters."""

        characters = list(digits + ascii_letters + punctuation)
        password = []
        for _ in range(0, self.passwordlen):
            password.append(randchoice(characters))

        self.last_result = password
        return password
