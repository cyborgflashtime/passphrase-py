Passphrase
==========

**Passphrase** is a tool to generate **cryptographically secure**
passphrases and passwords. A passphrase is a list of words usually
separated by a blank space. This tool acts like a
`diceware <http://world.std.com/~reinhold/diceware.html>`__ generator
(more info in `EFF's website <https://www.eff.org/es/dice>`__).

Its security is based on Python's
`os.urandom <https://docs.python.org/3/library/os.html#os.urandom>`__ to
get cryptographically secure random bits to make an integer number. It
also makes use of the `EFF's Large
Wordlist <https://www.eff.org/es/document/passphrase-wordlists>`__ as
words reference for passphrases.

A secure passphrase must be of at least 6 words, but 7 is better, and
maybe you can add a random number to the list. If you need a password,
make it bigger than 8 characters (`NIST's latest
recommendation <https://nakedsecurity.sophos.com/2016/08/18/nists-new-password-rules-what-you-need-to-know/>`__),
and prefer more than 12 (I recommend 16 or more). Passwords are
comprised of digits, upper and lower case letters and punctuation
symbols - more specifically: ``ascii_letters``, ``digits`` and
``punctuation`` from
`Lib/string <https://docs.python.org/3.6/library/string.html#string-constants>`__
-.

Those settings mentioned are specifically for the EFF's Large Wordlist.
If you specify a different wordlist, the minimum amount of words for a
passphrase to be secure changes: for shorter lists, the amount
increases. The minimum secure amount of words (for a passphrase) or
characters (for a password) are calculated by **Passphrase** and a
warning is shown if the chosen number is too low (when used as a
script), by calculating the list's entropy.

Requirements
------------

-  **Python 3.2+**
-  NumPy 1.13+ [optional] for faster entropy computation
-  Flake8 [optional] for linting

| Passphrase gets plenty of benefits from NumPy if you use an external
  wordlist, because it computes the entropy of it, but it works fine
  without it.
| For the sake of security, you might want to avoid using any external
  library. It's possible to entirely disable the use of NumPy by setting
  ``TRY_NUMPY = False`` in `settings.py <passphrase/settings.py>`__.

How to use it
-------------

**Passphrase** can be used as a *package* in other apps, or as a
*stand-alone script*.

In any case, just download the files, preferrably fom the `latest
release <https://github.com/HacKanCuBa/passphrase-py/releases/latest>`__
- releases are always signed -.

As a package
~~~~~~~~~~~~

Once downloaded and verified, use ``setup.py`` to install (I let you
decide whether to use virtualenv or not): ``./setup.py install``. You
can also do ``make package-install`` with the same outcome. Run it with
``sudo`` or elevated privileges to install it system-wide.

Examples of use
^^^^^^^^^^^^^^^

A good example is how `I implemented it <passphrase/__main__.py>`__.

.. code:: python

    from passphrase.passphrase import Passphrase

    passphrase = Passphrase('/tmp/mi_own_wordlist.txt')

    # WARNING: entropy and good default values ARE NOT automatically calculated!
    # Generic 6 words default is being used here, which could be bad if the
    # wordlist is too short!
    passphrase.generate()
    # >>> ['shop', 'jolt', 'spoof', 'cupid', 'pouch', 'dose']

    passphrase.words_amount_needed()
    # >>> 8

    passphrase.amount_w = passphrase.words_amount_needed()
    passphrase.generate()
    # >>> ['grub', 'mummy', 'woozy', 'whole', 'ritzy', 'sift', 'train', 'radar']

    # Change the wordlist (note than no other parameter is changed!)
    passphrase.import_words_from_file('/tmp/some_other_wordlist.txt', False)
    passphrase.generate()
    # >>> ['vexingly', 'skedaddle', 'gilled', 'desolate', 'cartoon', 'frail', 'brute', 'filled']

As a script
~~~~~~~~~~~

Once downloaded and verified, you can install it with
``setup.py install`` but I recommend you do ``make install`` for
system-wide installation or ``make altinstall`` for user-wide
installation, as it will create a single executable zip file plus
install the man page.

Examples of use
^^^^^^^^^^^^^^^

Check the `man page <man/passphrase.md>`__ for more information.

Generate a passphrase of 6 words (default settings)
'''''''''''''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase
    trophy affiliate clobber vivacious aspect thickness

Generate a passphrase of 6 words and a number (minimum recommended)
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase -w 6 -n 1
    jasmine identity chemo suave clerk copartner 853727

Generate a password of 16 characters (minimum recommended)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase -p 16
    E`31nDL0^$oYu5='

Use an external wordlist to generate a passphrase
'''''''''''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase -i eff_short_wordlist_1_1column.txt
    wimp broke dash pasta zebra viral outer clasp
    :~$ passphrase -d -i eff_short_wordlist_1.txt 
    mouse trend coach stain shut rhyme baggy scale

Save the output to a file
'''''''''''''''''''''''''

::

    :~$ passphrase -o pass.txt
    :~$ passphrase > pass.txt

Generate a passphrase and use it with GPG
'''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase -o pass.txt | gpg --symmetric --batch --passphrase-fd 0 somefile.txt
    :~$ sha256sum somefile.txt
    589ed823e9a84c56feb95ac58e7cf384626b9cbf4fda2a907bc36e103de1bad2  somefile.txt
    :~$ cat pass.txt | gpg --decrypt --batch --passphrase-fd 0 somefile.txt.gpg | sha256sum -
    gpg: AES256 encrypted data
    gpg: encrypted with 1 passphrase
    589ed823e9a84c56feb95ac58e7cf384626b9cbf4fda2a907bc36e103de1bad2  -

Generate a passphrase avoiding `shoulder surfing <https://en.wikipedia.org/wiki/Shoulder_surfing_(computer_security)>`__
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

::

    :~$ passphrase -q -o pass.txt

Is this really secure?
----------------------

First of all, we will say that a password or passphrase generator
algorithm is secure if its output is *trully* random. To achieve that,
**Passphrase** relies entirely on ``os.urandom``. The whole program is
quite big, but most of it is just the menues and the word list. The
generator algorithms are very short and simple (simplified code with
type-checking removed):

.. code:: python

    ## Random number generation from os.urandom
    # passphrase > secrets.py
    def getrandbits(nbits: int) -> int:
        """Generates an int with nbits random bits."""

        nbytes = (nbits + 7) // 8                       # bits / 8 and rounded up
        num = int.from_bytes(_urandom(nbytes), 'big')
        return num >> (nbytes * 8 - nbits)              # trim excess bits

    def randbelow(num: int) -> int:
        """Return a random int in the range [0,num)."""

        nbits = num.bit_length()      # don't use (n-1) here because n can be 1
        randnum = getrandbits(nbits)  # 0 <= randnum < 2**nbits
        while randnum >= num:
            randnum = getrandbits(nbits)
        return randnum


    ## Passphrase or password generation using the random number as index of a list
    # passphrase > passphrase.py
    def generate(self) -> list:
        """Generates a list of words randomly chosen from a wordlist"""

        passphrase = []
        for _ in range(0, self.amount_w):
            index = randbelow(len(self.wordlist))
            passphrase.append(self.wordlist[index])

        for _ in range(0, self.amount_n):
            num = randbelow(self.randnum_max - self.randnum_min + 1) + self.randnum_min
            passphrase.append(num)

        return passphrase

    def generate_password(self) -> list:
        """Generates a list of random characters"""

        characters = list(digits + ascii_letters + punctuation)
        password = []
        for _ in range(0, self.passwordlen):
            index = randbelow(len(characters))
            password.append(characters[index])

        return password

The whole magic is done by
```randbelow()`` <passphrase/secrets.py#L24>`__, that returns a random
natural number lower than the given value, that is then used as index
for the word or character list. ``randbelow()`` uses
```getrandbits()`` <passphrase/secrets.py#L12>`__ which in turn uses
``os.urandom`` at the back. ``os.urandom`` always provides an interface
to the OS's cryptographically secure random generator. And both
``randbelow()`` and ``getrandbits()`` where copyied from Python's
Lib/random, but trimmed down so that they don't allow anything fishy.
This also makes **Passphrase** independent from unnecessary libraries
and potential vulnerabilities.

The algorithms are very straight forward, easy to understand and verify.
*Boring crypto is the best crypto*.

Attack surface
~~~~~~~~~~~~~~

Let's analyze some possible attack scenarios and its mitigations. If you
want to add something or you see a mistake, please write an
`issue <https://github.com/HacKanCuBa/passphrase-py/issues>`__.

Attacker is root
^^^^^^^^^^^^^^^^

TL;DR: **game over**.

An attacker that is *root* can do whatever it wants, so it's out of the
scope of this analysis.

Attacker can modify source code or wordlist
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If it can modify the source code somehow, or the default
`wordlist <passphrase/wordlist.json>`__, it's also game over since a
software that succesfully checks itself doesn't exist yet. However, it
could be mitigated by placing the files under the ownership of some
privileged user (*root*).

Attacker can modify external libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| **Passphrase** doesn't require any external library, but if NumPy
  exists, it will use it. Let's assume the attacker has full control
  over this library, which is used to improve entropy calculations.
| The attacker could alter it so that the resulting entropy calculation
  is bigger than it should, so that Passphrase will recommend (or use)
  shorter passphrases or passwords. This attack would only be possible
  if Passphrase is being use as a script with default parameters or as a
  module in a script with entropy-based calculated parameters. In that
  scenario, the attack succeeds in reducing the difficulty in
  bruteforcing the passphrase/password by making Passphrase generate
  very short passphrases/passwords. However, using Passphrase like that
  is not the best practice: the user should realize that
  passphrases/passwords are too short, and should avoid using default
  parameters (as a general rule of thumb, always set what you want and
  expect).
| Either way, this can be mitigated by setting ``TRY_NUMPY = False`` in
  `settings.py <passphrase/settings.py>`__.

License
-------

**Passphrase** is made by `HacKan <https://hackan.net>`__ under GNU GPL
v3.0+. You are free to use, share, modify and share modifications under
the terms of that `license <LICENSE>`__.

::

    Copyright (C) 2017 HacKan (https://hackan.net)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.