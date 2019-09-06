# Password basics (aka "How to Think About Passwords")

The goal of this article is to discuss what are generally considered good and bad practices for choosing and managing passwords. If you're already familiar with these ideas and are simply looking for a strong password generation tool, you might look at my [password generation tool](https://github.com/allisonk2277/passwords) that supports a variety of common password formats.

## Best practices, the short version

1. Strong passwords must be chosen randomly. There are no exceptions to this rule.
2. Password strength is described in terms of *entropy*, which is a measure of the number of possible passwords that could have been chosen.
3. Without sacrificing entropy, choose passwords that are easier to remember.
4. As of this writing, ~80 bits of entropy is a pretty reasonable choice for password entropy. This is approximately 16 alphanumeric characters, or 6 words from the large words list, or 8 words from the short words list.
5. Use a password manager. Memorize one really strong password as your master password, and let the password manager handle the rest.
6. Don't reuse passwords. This is trivial to do if you use a password manager.

Everything else below is a more detailed discussion about the above points.

## Choose passwords randomly

This is the most fundamental idea with creating strong passwords. A general principle when discussing security is that a system that is *proven* to be secure can be trusted; unproven systems are inherently untrustworthy. Proving a system is secure requires a precise definition of:

  * What you know
  * What the attacker knows
  * What the attacker is capable of
  
Let's discuss.

### What is entropy?

Entropy is a measure of how much your attacker has to guess in order to crack your password. We usually discuss this in terms of the number of possible passwords that you could have chosen, with the units being the base-2 log of that number. That is, "80 bits of entropy" means you chose a password at random (each choice having the same probability of being chosen) from 2^80 = 1.2 * 10^24 possible choices. 

If your password has N bits of entropy, then we generally expect the attacker to guess your password after 1/2 * 2^N = 2^(N - 1) guesses (if they went through each possible choice, then half the time they would guess your password before the halfway point and half the time they would guess your password after the halfway point).

### Schemes that do not work

* Passwords based on personal information, preferences, history, etc.
* Passwords based on phrases you have seen before (in a book, in conversation, etc).
* Passwords based on one or more foreign languages.
* Passwords that do predictable transformations to word(s).
* etc.

These don't work because a large part of its security comes from hiding *how* you came up with the password. For example, if your password scheme is:

1. Choose an English word.
2. Capitalize the first and last letter.
3. Replace all the 'e's with '3's.
4. Add the zip code you were born in to the end.

Only step 1 meaningfully adds real entropy to your password. The rest of the steps rely on your attacker not knowing your procedure, and these are all fairly common "tricks" that add at most a couple extra bits of entropy.

Notice how imprecise and hand-wavy that analysis was, and that much of its entropy relies on the attacker not knowing what you actually did. This kind of scheme is difficult to reason about - how many possible words did you actually consider during step 1? How should you account for what the attacker may or may not know about you? etc. In general, debating if these schemes are secure comes down to squabbling over a few bits of entropy, which is not a large margin of safety either way.

This comic sums it up pretty well: https://xkcd.com/936/

### What resources does the attacker have?

The most valuable resources we *must* assume the attacker has are the vast dumps of previously cracked passwords. In our threat model, we can safely say:

1. At least hundreds of millions of passwords have been compromised in one way or another. While it's certainly true that websites that properly salt and hash their passwords are difficult to crack, it only takes a few websites to do something improper (passwords in plaintext, passwords *encrypted* rather than *hashed* and likely with a single sitewide key that's the only thing the attacker needs to crack in order to decrypt everything, passwords hashed with broken algorithms, passwords from sites that invent their own crypto, and the list goes on) in order for attackers to have a huge database of cracked passwords. 
2. Attackers learn what common (and uncommon) password schemes are using these databases, and customize password cracking software to target those patterns first. They will try all common substitutions, transformations, etc. you can think of when cracking your password.
3. If a password you reuse is in these databases, then all other accounts that reuse are instantly compromised.

There are a few other things we should try to defend against (it's better to assume that the attacker has many resources, and defend against them all, instead of defending against a weaker threat model). 

* A common objection is that websites will rate limit the number of login attempts. This is true, but we have to assume that the attacker has stolen your password data and is cracking it offline, rather than online (I disagree with the XKCD comic I linked above on this point). Again, we want to defend against the strongest possible threat model.
* If the attacker is cracking it offline, let's be generous and say the attacker has a billion computers at their disposal, and each machine can attempt a billion guesses per second. These are wild overestimates, of course, but we want a large margin of safety to account for future advances in computing.
