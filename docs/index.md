# Password basics (aka "How to Think About Passwords")

The goal of this article is to discuss what are generally considered good and bad practices for choosing and managing passwords, aimed at a general audience. If you're already familiar with these ideas and are simply looking for a strong password generation tool, you might look at my [password generation script](https://github.com/allisonk2277/passwords) that supports common strong password formats.

There are already many articles out there that talk about what you should or shouldn't do with passwords. Some are well written and give sound advice; others may give actively harmful advice. I hope to use this article to present a more rigorous approach to thinking about your computer security, without assuming more than a minimal mathematical background. If anything is unclear, I'm always happy to answer questions or discuss ideas!

## Recommended best practices, in short

1. Strong passwords must be chosen randomly. There are no exceptions to this rule. If there's a single idea I hope is a takeaway from this article, it's that your Clever Password Scheme&trade; is likely broken.
2. Without sacrificing entropy, choose passwords that are easier to remember.
3. As of this writing, ~80 bits of entropy is a reasonable choice for password entropy (more is better, of course). This is approximately 16 alphanumeric characters, or 6 words from the large words list, or 8 words from the short words list.
4. Use a password manager. Memorize one really strong password as your master password, and let the password manager handle the rest.
5. Don't reuse passwords. This is trivial to do if you use a password manager.

Everything else below is a more detailed discussion about the above points.

## What is entropy?

Entropy is a measure of how difficult it is to guess your password. We define it as the number of possibile passwords you might have chosen, given a procedure for choosing one (we assume that each choice is equally likely to be chosen).

* We use "bits" as the unit of entropy. Each additional bit double the number of possible passwords you could have chosen; N bits of entropy means 2^N possibilities.
* For a password with N bits of entropy, the expected number of guesses before your password is "cracked" is 1/2 * 2^N = 2^(N-1) guesses.

It is important to note that entropy measures the *number of possible passwords*, and *not* the length of the password! While the two are often correlated, they are not the same thing. Choosing a long (let's say 8 character) word from the English dictionary does not make a good password; there are probably fewer than 10,000 words you could have actually chosen. Testing 10,000 possibilities (13.3 bits of entropy) is trivially easy for an attacker. However, choosing an 8 letter sequence from the set of all possible 8 letter sequences provides 26^8 (most are gibberish like 'unllejhp' and not actual words) draws from a pool of 208,827,064,576 possibilities (37.6 bits of entropy), and is significantly harder to crack.

## Analyzing security

Some basic principles we will keep in mind are:

1. We must prove that our system is secure mathematically. Unproven systems are assumed to be broken until proven otherwise, not the other way around.
2. We define a clear, concrete threat model and defend against it. In defining this threat model, we wish to defend against the strongest possible threat, and so we will always err on the side of overestimating the attacker's abilities (if we are unsure of what the attacker is capable of, we must assume the worst case). In addition, building in a large margin of safety helps defend against future advances in computing.

### The threat model

1. The attacker wants to guess our password. We might imagine that this is a password protecting an important account (e.g. email) with lots of valuable information. "Cracking" a password means correctly guessing the value of the password; you can imagine the attacker repeated making guesses of the form "is the password X" and receiving a yes/no answer each time.
2. We assume the attacker has access to [all](https://en.wikipedia.org/wiki/List_of_data_breaches) [historic](https://www.theguardian.com/technology/2013/nov/07/adobe-password-leak-can-check) [password](https://www.nytimes.com/2017/10/03/technology/yahoo-hack-3-billion-users.html) [data](https://krebsonsecurity.com/2019/03/facebook-stored-hundreds-of-millions-of-user-passwords-in-plain-text-for-years/) [breaches](https://www.washingtonpost.com/news/the-switch/wp/2014/05/21/ebay-asks-145-million-users-to-change-passwords-after-data-breach/). Let's assume that every password in every breach has been cracked by now. In fact, let's go one step further (in the spirit of defending against the most difficult threat model) and simply assume every single password anyone has ever created (including all of your own old passwords) is known to your attacker, and that they have studied these passwords to identify patterns in how passwords are created. How do we create a new password that's still resistant to this attacker?
3. The corollary with #2 is that we assume the attacker knows exactly what procedure we are using to come up with a password. A scheme where the attacker can know exactly what we are doing and still be unable to guess the password is fundamentally more secure than a scheme that relies on the attacker not knowing the scheme; there is no security in obscurity.
4. We assume the attacker has access to vast compute resources. In particular, we will assume the attacker has stolen password data somehow and is attempting to crack it offline, rather than online (websites do often have rate limiting, but this doesn't protect against offline cracking), and that the attacker has vast resources available (e.g. they are a nation-state, or have a large botnet, or some *really* fancy GPUs). Let's say the attacker can attempt a trillion (10^12) guesses per second; you might imagine they have a million machines, each capable of guessing a million times per second.

How fast is 10^12 guesses per second?

* 13.3 bits of entropy (a list of 10,000 words) would take 0.00000001 seconds to crack.
* 37.6 bits of entropy (all 8 letter sequences) would take 0.2 seconds to crack.
* 50 bits of entropy would take 18 minutes to crack.
* 60 bits of entropy would take 13 days to crack.
* 70 bits of entropy would take 37 years to crack.
* 80 bits of entropy would take 38,334 years to crack.
* 90 bits of entropy would take 39,254,821 years to crack.
* 100 bits of entropy would take 40,196,936,841 years to crack.
* 128 bits of entropy (a standard size used in cryptography) would take 1e19 (10,000,000,000,000,000,000) years to crack.

80 bits of entropy seems like a reasonable minimum number of bits to aim for; even if computing achieves a 1000x speedup over our model, it would still take about 38 years to crack an 80 bit secret which is infeasible for an attacker.

### Schemes that do not work

First, let's examine some common schemes that are easily broken.

1. A word or common phrase from the dictionary (such as 'password', 'secret', 'topsecret', 'incorrect', etc).
2. #1, but with some numbers added to the end and some common replacements/capitalizations/etc ('secret' -> 'S3cr3t99').
3. Passwords involving personal information or history (e.g. a middle name, a past address, child name, pet name, year child was born, year pet was adopted, etc).
4. Passwords that involve multiple languages (e.g. one word in English, one word in German).
5. Passwords that look like gibberish, but actually have a pattern to them (e.g. take a phrase you remember, and use the first letter of each word).
6. Passwords that look like other passwords you have used (e.g. you have a "base password" and then change the number at the end each time). Or worse, you are reusing a password that has already been cracked.

The common theme with these schemes is that they may be clever, and an attacker with no experience might have a hard time figuring out what you did. However, our threat model is not a newbie attacker; we wish to defend against a highly experienced attacker who has certainly seen passwords similar to your scheme before. How likely is it that you are the only person in the world to have come up with your particular idea for a password? Even if you really are the first person to do so, have you used this scheme for more than one password? If an attacker knew other passwords you have created with this scheme (for example, a website might have been compromised and leaked this information), and learned what your scheme is, how guessable is the next password you create with this scheme?

This comic sums it up pretty well: https://xkcd.com/936/

* Note: I don't think 44 bits of entropy as mentioned is anywhere close to a good margin of safety, but otherwise agree with the comic wholeheartedly.

## Generate passwords randomly

Strong password generation *must* involve randomness. That way, the attacker can know exactly how you convert that randomness into a password, but still be unable to guess what that password is (they do not, of course, know how your random coin flips actually turned out). Randomness can come from human sources (e.g. flipping a coin or rolling dice) as well as computer sources (more on this later).

Let's examine a basic procedure for creating a password:

1. Flip a coin 80 times. Each time, if it comes up as heads, write down a 0. If it comes up tails, write down a 1.
  * Example: your results are 01010011111001100010110110100010110011100010000100010011011010101100111100011111.
2. Convert this bit sequence into a single integer in the range [0, 2^80). Call that integer X.
  * Example: X = 396202457632453138501407.
3. Decide on what you want your password to consist of. For example, you might want your password to be lowercase letters and digits (I will notate this as [a-z0-9]). There are 36 possible characters. We now convert X into base-36, which is written as a list of integers [a1, a2, a3, ..., aN]. These are the coefficients of each power of 36, and will be in the range [0, 35].
  * Example: 1 28 18 23 20 19 1 9 8 12 15 28 13 29 21 27.
4. For each number in your list, assign it to a character using a=0, b=1, c=2, ..., z=25, 0=26, 1=27, ..., 9=35.
  * Example: b2sxutbjimp2n3v1

And that's your password!

What this procedure does is that it samples uniformly from the first 2^80 sequences of [a-z0-9] characters. There are 2^80 possibilities, and so our password has 80 bits of entropy. Thus, we can be confident that our password is secure; an attacker who knows that this exact procedure was followed would still require 38,334 years to crack it at 10^12 guesses per second.

This procedure is roughly what I have implemented at https://github.com/allisonk2277/passwords. It's well suited for generating a password with computer assistance; it would be cumbersome to do this manually. For suggestions on generating passwords without using a computer, see below.

A note about password rules: any further modifications (e.g. capitalizing a letter, adding a symbol, etc) do not meaningfully add any additional security while making it more difficult to remember; we've already established that 80 bits is adequate security. Personally, I use a simple "capitalize the first letter and add ! at the end" when required by websites; I do not treat these modifications as adding any additional security.

## Diceware passwords

A perfectly reasonable objection is that 'b2sxutbjimp2n3v1' is hard to memorize, and that the above procedure is well suited for computers but not working things out on pen and paper. Diceware is a method of generating passwords that simply draws from a word list, rather than a set of characters, during steps 3 and 4 of the procedure mentioned above. You randomly choose words from a long list of words to come up with passphrases like 'correct horse battery staple'. These passphrases are just as secure as a character-based password (again, count the bits and not the length) created with the same entropy, and are often easier to remember since they use actual English words and don't look like gibberish.

When generating a diceware password manually, you roll a number of dice (usually 5) at a time and match the numbers that come up to a list of words to choose a word. Instructions may be found here: https://www.eff.org/dice.

A misinformed criticism that I've sometimes heard about diceware passwords is that they're vulnerable to dictionary attacks. This is simply not true; it's not any more true than saying character-based passwords are vulnerable because an attacker knows all the letters of the English alphabet. A 1- or 2- word diceware phrase lacks adequate entropy, but a 6- word diceware phrase chosen from a wordlist of 6^5 = 7776 words has 77 bits of entropy which is quite secure.

I personally like the EFF's published wordlists because they have been carefully curated to use well known, recognizable words that are easy to remember. They also publish a couple other short wordlists should you want to use more words with less entropy per word.
