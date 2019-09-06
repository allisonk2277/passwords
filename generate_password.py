#!/usr/bin/env python3
"""Script for generating a secure password interactively.

See README.md for details.

Usage:
  python generate_password.py <flags>
"""

from absl import app
from absl import flags
from absl import logging
import os.path
import re
import secrets
import string
import sys

FLAGS = flags.FLAGS
flags.DEFINE_integer("entropy", 128, "Number of bits")
flags.DEFINE_bool("use_user_entropy", True, "Use user provided entropy.")
flags.DEFINE_bool("use_system_entropy", True, "Use system provided entropy.")
flags.DEFINE_string("user_source", "coin", "Source of user entropy.")
flags.DEFINE_string("mode", "charset", "How to generate password.")
flags.DEFINE_string("charset", "alphanumeric", "Charset to use.")
flags.DEFINE_string("wordlist", "eff_large", "Wordlist to use.")
flags.DEFINE_bool("verbose", True, "Print intermediate steps.")

def GetEntities():
  """Returns a string or list with the desired entities."""
  if FLAGS.mode == "charset":
    return GetCharset()
  elif FLAGS.mode == "wordlist":
    return GetWordlist()
  else:
    logging.fatal("Invalid --mode.")

def GetCharset():
  """Returns the charset as a string."""
  charset = None
  if FLAGS.charset == "alphanumeric":
    charset = string.ascii_lowercase + string.digits
  elif FLAGS.charset == "alphanumeric_full":
    charset = string.ascii_letters + string.digits
  elif FLAGS.charset == "letters":
    charset = string.ascii_lowercase
  elif FLAGS.charset == "digits":
    charset = string.digits
  elif FLAGS.charset == "hex":
    charset = string.digits + "abcdef"
  elif FLAGS.charset.startswith("custom="):
    charset = FLAGS.charset[len("custom="):]
  else:
    logging.fatal("Invalid --charset.")
  assert charset is not None
  if FLAGS.verbose:
    print("Using charset: {}".format(charset))
  return charset

def GetWordlist():
  """Loads the wordlist as a list of strings."""
  wordlist_file = GetWordlistFile()
  if FLAGS.verbose:
    print("Loading words from: {}".format(wordlist_file))
  words = []
  with open(wordlist_file, "r") as f:
    for line in f:
      line = line.strip()
      # Check if list is in the format of the EFF word lists, since they're made for diceware.
      # Otherwise expect 1 line = 1 word.
      m = re.match(r'[1-6]+\s+(\w+)', line)
      if m is not None:
        words.append(m.group(1))
      else:
        words.append(line)
  return words

def GetWordlistFile():
  """Returns the path to the wordlist file."""
  parent_dir = os.path.dirname(os.path.realpath(__file__))
  if FLAGS.wordlist == "eff_large":
    return os.path.join(parent_dir, "wordlists/eff_large_wordlist.txt")
  elif FLAGS.wordlist == "eff_short":
    return os.path.join(parent_dir, "wordlists/eff_short_wordlist_1.txt")
  elif FLAGS.wordlist == "eff_short_v2":
    return os.path.join(parent_dir, "wordlists/eff_short_wordlist_2_0.txt")
  elif FLAGS.wordlist.startswith("custom="):
    return FLAGS.wordlist[len("custom="):]
  else:
    logging.fatal("Invalid --wordlist.")

def GetCoinFlip(bit_num):
  """Returns a single random bit generated by the user."""
  while True:
    value = input("Flip a coin (h/t) [{}/{}]: ".format(bit_num,
                                                       FLAGS.entropy)).upper()
    if value == "H":
      return [0]
    elif value == "T":
      return [1]
    else:
      print("Invalid value. Must be 'h' or 't'.")

def GetDiceRoll(bit_num):
  """Returns 1 or 2 bits from a dice roll.

  1-4 = 2 bits
  5-6 = 1 bit
  """
  while True:
    value = input("Roll a dice (1-6) [{}/{}]: ".format(bit_num, FLAGS.entropy))
    if value == "1":
      return [0, 0]
    elif value == "2":
      return [0, 1]
    elif value == "3":
      return [1, 0]
    elif value == "4":
      return [1, 1]
    elif value == "5":
      return [0]
    elif value == "6":
      return [1]
    else:
      print("Invalid value. Must be an integer in range [1, 6].")

def GetUserEntropyOnce(bit_num):
  if FLAGS.user_source == "coin":
    return GetCoinFlip(bit_num)
  elif FLAGS.user_source == "dice":
    return GetDiceRoll(bit_num)
  else:
    logging.fatal("Invalid --user_source.")

def GetUserBits(n):
  """Returns an integer with the desired number of random bits."""
  x = 0
  bits_collected = 0
  while bits_collected < n:
    new_bits = GetUserEntropyOnce(bits_collected + 1)
    # It's possible to collect too many bits on the last roll. Truncate if
    # this happens.
    if bits_collected + len(new_bits) > n:
      new_bits = new_bits[:n - bits_collected - len(new_bits)]
    for bit in new_bits:
      x <<= 1
      x |= bit
      bits_collected += 1
  assert bits_collected == n
  if FLAGS.verbose:
    print("Done collecting entropy!")
  return x

def NumToBase(x, base):
  """Converts the number to the requested base.

  Returns an array of integers intended to be read left to right.

  Example:
    NumToBase(32, 2) -> [1, 0, 0, 0, 0, 0]
    NumToBase(0x20, 10) -> [3, 2]
  """
  # Right to left order.
  digits = []
  while x > 0:
    digits.append(x % base)
    x //= base
  if len(digits) == 0:
    digits.append(0)
  # Reverse the digits so they are left to right.
  return digits[::-1]

def NumToBitString(x):
  """Converts x into a bit string. Left pads to the entropy length."""
  bs = NumToBase(x, 2)
  if len(bs) < FLAGS.entropy:
    bs = [0] * (FLAGS.entropy - len(bs)) + bs
  return "".join(map(str, bs))

def GetEntropy():
  """Returns an integer containing all the requested entropy."""
  entropy = 0
  if not FLAGS.use_user_entropy and not FLAGS.use_system_entropy:
    logging.fatal("No entropy source! Must enable --use_user_entropy \
        and/or --use_system_entropy.")
  if FLAGS.use_user_entropy:
    user_bits = GetUserBits(FLAGS.entropy)
    if FLAGS.verbose:
      print("User generated entropy:   {}".format(NumToBitString(user_bits)))
      print("                          {}".format(hex(user_bits)))
    entropy ^= user_bits
  if FLAGS.use_system_entropy:
    system_bits = secrets.randbits(FLAGS.entropy)
    if FLAGS.verbose:
      print("System generated entropy: {}".format(NumToBitString(system_bits)))
      print("                          {}".format(hex(system_bits)))
    entropy ^= system_bits
  # Print combined bits if it provides any additional insight.
  if FLAGS.use_user_entropy and FLAGS.use_system_entropy and FLAGS.verbose:
    # Just so indent matches above...
    if True:
      print("Combined entropy:         {}".format(NumToBitString(entropy)))
      print("                          {}".format(hex(entropy)))
  return entropy

def main(argv):
  if FLAGS.entropy <= 0:
    logging.fatal("Invalid --entropy.")
  if FLAGS.verbose:
    print("Generating password with {} bits of entropy.".format(FLAGS.entropy))

  entities = GetEntities()
  entropy = GetEntropy()
  offsets = NumToBase(entropy, len(entities))
  parts = [entities[i] for i in offsets]

  if FLAGS.mode == "wordlist":
    pwd = " ".join(parts)
  else:
    pwd = "".join(parts)

  if FLAGS.verbose:
    print("")
    print("Offsets: {}".format(" ".join(map(str, offsets))))
    print("Generated password: {}".format(pwd))
  else:
    print(pwd)

if __name__ == "__main__":
  app.run(main)