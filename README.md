# Strong password generator

Generate passwords with user-provided entropy. Supports generating passwords with random characters as well as [diceware style word lists](https://xkcd.com/936/). Can also generate passwords without user input.

You can find a short article about the basics of securing your accounts [here](https://allisonk2277.github.io/passwords/).

## Requirements

* Python 3.6+
* Absl (`pip install absl-py`)

## Usage

```sh
./generate_password.py <flags>
```

By default, the password generator will:

* Generate a password with 128 bits of entropy.
* Combine the user-provided entropy with 128 bits of system-provided entropy (see below).
* Use the charset [a-z0-9].

## Flags

Flag | Type | Description
-----|------|------------
entropy | int | Number of bits of entropy desired. Default is 128.
use_user_entropy | bool | If enabled, collect entropy from user. Enabled by default.
use_system_entropy | bool | If enabled, user-provided bits are XORed with system-provided bits. It is well-known that XORing uncorrelated randomness sources generally increases the quality of randomness over either source by itself, and is at minimum no worse than the better of the two sources (so long as the sources are uncorrelated). This helps protect against possible bias in any single randomness source; no conventional method for generating randomness is perfect. See [RFC 4086](https://tools.ietf.org/html/rfc4086#section-5) for a more detailed discussion. Enabled by default.
user_source | string | May be 'coin' or 'dice'. Default is 'coin'.
mode | string | May be 'charset' or 'wordlist'. If 'charset', chooses characters from a string. If 'wordlist', chooses words from a file containing a list of words. Default is 'charset'.
charset | string | If `--mode=charset`, this customizes which characters are used; see below. Default is 'alphanumeric'.
wordlist | string | If `--mode=wordlist`, this customizes which wordlist is used; see below. Default is 'eff_large'.
verbose | bool | Enabled by default.

### Available charsets

Name | Description
-----|------------
alphanumeric | [a-z0-9]
alphanumeric_full | [a-zA-Z0-9]
letters | [a-z]
digits | [0-9]
hex | [0-9a-f]
custom | You may use `--charset=custom=<some string>` to provide your own string to sample from.

The default is [a-z0-9]; each character provides 5.17 bits of entropy. I prefer this over alphanumeric_full because I found that having to memorize the capitalization of each letter was much harder than memorizing a couple more characters.

### Available wordlists

We use the wordlists published by the EFF [here](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases). These lists have been carefully curated to make it easier to remember; details in the article linked.

Name | Description
-----|------------
eff_large | Large word list, containing 7776 words.
eff_short | Short word list, containing 1296 words.
eff_short_v2 | Another short word list, additionally designed such that each word has a unique 3-letter prefix and an edit distance of at least 3 from any other word in the list.
custom | You may use `--wordlist=custom=<path to file>` to use a custom word list.

The default is eff_large.

## Examples

Use all defaults (128 bits, [a-z0-9] charset, flip a coin):

```sh
./generate_password.py
```

Roll dice, 64 bits of entropy, only use user input, use EFF large wordlist:

```sh
./generate_password.py \
  --entropy=64 \
  --user_source=dice \
  --nouse_system_entropy \
  --mode=wordlist \
  --wordlist=eff_large
```

Generate a password without user input, 256 bits of entropy, extended charset, only print result:

```sh
./generate_password.py \
  --entropy=256 \
  --nouse_user_entropy \
  --mode=charset \
  --charset=alphanumeric_full \
  --noverbose
```

Print available flags:

```sh
./generate_password.py --help
```

## How a password is generated

We generate a password by choosing from a set of N entities repeatedly until we have as many bits of entropy as desired. The entities we choose may be characters from a string or a word list (in the spirit of diceware passphrases).

Let E be the number of bits desired (the entropy) and N the size of the entity list we choose from.

1. Generate an integer X with E random bits, using user-provided entropy (and system-provided entropy, if enabled).
2. Convert X into base N as a sequence of integers in the range [0, N).
3. Use this list to index into the list of entities to construct the password.

### Collecting entropy

* If flipping a coin, heads -> 0 and tails -> 1.
* If rolling dice, 1-4 generate 2 bits of entropy and 5-6 generate 1 bit of entropy.
  * 1 -> 00, 2 -> 01, 3 -> 10, 4 -> 11, 5 -> 0, 6 -> 1.
