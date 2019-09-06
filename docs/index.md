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

Notice how imprecise and hand-wavy that analysis was? 
