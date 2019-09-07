# Password security basics

The goal of this article is to discuss what are widely considered good and bad practices for choosing and managing passwords, aimed at a general audience. If you're already familiar with these ideas and are simply looking for a strong password generation tool, you might look at  [password generation script](https://github.com/allisonk2277/passwords) that supports common strong password formats.

There are many articles that talk about what you should or shouldn't do with passwords. Some are well written and give sound advice; others less so. I hope to use this article to present a more rigorous approach to thinking about your computer security, without assuming more than a minimal mathematical background. If anything is unclear, I'm always happy to answer questions or discuss ideas!

## Recommended best practices, in short

1. Strong passwords must be chosen randomly. *There are no exceptions to this rule.* If there's a single idea I hope is the takeaway from this article, it's that *&lt;insert Clever Password Scheme&trade;&gt;* is likely broken and must be avoided.
2. Without sacrificing entropy, choose passwords that are easier to remember.
3. As of this writing, ~80 bits of entropy is a reasonable choice for password entropy (more is better, of course). This is approximately 16 alphanumeric characters, or 6 words from the large words list, or 8 words from the short words list.
4. Use a password manager. Memorize one really strong password as your master password, and let the password manager handle the rest.
5. Don't reuse passwords. This is trivial to do if you use a password manager.

Everything else below is a more detailed discussion about the above points.

## What is entropy?

Entropy is a measure of how difficult it is to guess your password. We define it as the number of possibile passwords you might have chosen, given a procedure for choosing one (we assume that each choice is equally likely to be chosen).

* We measure entropy in bits, which is the base-2 log of the number of possibilities. Each additional bit double the number of possible passwords you could have chosen; N bits of entropy means 2^N possibilities.
* Adding 10 bits to your password's entropy makes it ~1000x harder to guess.
* For a password with N bits of entropy, the expected number of guesses before your password is "cracked" is 1/2 * 2^N = 2^(N-1) guesses.

It is important to note that entropy measures the *number of possible passwords*, and *not* the length of the password! While the two are often correlated, they are not the same thing. Choosing a long (let's say 8 character) word from the English dictionary does not make a good password; there are probably fewer than 10,000 words you could have actually chosen. Testing 10,000 possibilities (13.3 bits of entropy) is trivially easy for an attacker. However, choosing an 8 letter sequence from the set of all possible 8 letter sequences provides 26^8 (most of these sequences are gibberish like 'unllejhp' and not actual words) draws from a pool of 208,827,064,576 possibilities (37.6 bits of entropy), and is significantly harder to crack (this still isn't a large amount of entropy, but it's 16,000,000x better than 13.3 bits).

## Analyzing security

Some basic principles we will keep in mind are:

1. We must prove that our system is secure mathematically. Unproven systems are assumed to be broken until proven otherwise, not the other way around.
2. We define a clear, concrete threat model and defend against it. In defining this threat model, we wish to defend against the strongest possible threat, and so we will always err on the side of overestimating the attacker's abilities (if we are unsure of what the attacker is capable of, we must assume the worst case). In addition, building in a large margin of safety helps defend against future advances in computing.

### The threat model

1. The attacker wants to guess our password. We might imagine that this is a password protecting an important account (e.g. email) with lots of valuable information. "Cracking" a password means correctly guessing the value of the password; you can imagine the attacker repeatedly making guesses of the form "is the password X" and receiving a yes/no answer each time.
2. We assume the attacker has access to [all](https://en.wikipedia.org/wiki/List_of_data_breaches) [historic](https://www.theguardian.com/technology/2013/nov/07/adobe-password-leak-can-check) [password](https://www.nytimes.com/2017/10/03/technology/yahoo-hack-3-billion-users.html) [data](https://krebsonsecurity.com/2019/03/facebook-stored-hundreds-of-millions-of-user-passwords-in-plain-text-for-years/) [breaches](https://www.washingtonpost.com/news/the-switch/wp/2014/05/21/ebay-asks-145-million-users-to-change-passwords-after-data-breach/). Let's assume that every password in every breach has been cracked by now. In fact, let's go one step further (in the spirit of defending against the most difficult threat model) and simply assume every single password anyone has ever created (including all of your own old passwords) is known to your attacker, and that they have studied these passwords to identify patterns in how passwords are created.
3. We assume the attacker knows exactly what procedure we are using to come up with a password. A scheme where the attacker can know exactly what we are doing and still be unable to guess the password is fundamentally more secure than a scheme that relies on the attacker not knowing what you did; there is no security in obscurity.
  * What this means: the attacker knows what all of the possible passwords you could have chosen are, and will only attempt passwords from this set of possibilities.
4. We assume the attacker has access to vast compute resources. In particular, we will assume the attacker has stolen password data somehow and is attempting to crack it offline, rather than online (websites do often have rate limiting, but this doesn't protect against offline cracking), and that the attacker has a lot of computers available (e.g. they have capabilities similar to the NSA/Russia/China, or have a large botnet, or maybe some *really* fancy GPUs). Let's say the attacker can attempt a trillion (10^12) guesses per second; you could think of this as a million machines, each capable of guessing a million times per second.

How fast is 10^12 guesses per second?

* 13.3 bits of entropy (e.g. a list of 10,000 words) would take 0.00000001 seconds to crack.
* 37.6 bits of entropy (e.g. all 8 letter sequences) would take 0.2 seconds to crack.
* 50 bits of entropy would take 18 minutes to crack.
* 60 bits of entropy would take 13 days to crack.
* 70 bits of entropy would take 37 years to crack.
* 80 bits of entropy would take 38,334 years to crack.
* 90 bits of entropy would take 39,254,821 years to crack.
* 100 bits of entropy would take 40,196,936,841 years to crack.
* 128 bits of entropy (a standard size used in cryptography) would take 1e19 (10,000,000,000,000,000,000) years to crack.

80 bits of entropy seems like a reasonable minimum number of bits to aim for; even if advances in computing achieve a 1000x speedup over our threat model, it would still take about 38 years to crack an 80 bit secret. This seems like a good margin of safety (more entropy is certainly better, but this is point at which you begin encountering diminishing returns).

### Schemes that do not work

First, let's examine some common schemes that are easily broken.

1. A word or common phrase from the dictionary (such as 'password', 'secret', 'topsecret', 'incorrect', etc).
2. #1, but with some numbers added to the end and some common replacements/capitalizations/etc ('secret' -> 'S3cr3t99').
3. Passwords involving personal information or history (e.g. a middle name, a past address, child name, pet name, year child was born, year pet was adopted, etc).
4. Passwords that involve multiple languages (e.g. one word in English, one word in German).
5. Passwords that look like gibberish, but actually have a pattern to them (e.g. take a phrase you remember, and use the first letter of each word).
6. Passwords that look like other passwords you have used (e.g. you have a "base password" and then change the number at the end each time). Or worse, you are reusing a password that has already been cracked.

The common theme with these schemes is that they may be clever, and a newbie attacker with no experience might have a hard time figuring out what you did. However, our threat model is not that of a newbie attacker; we wish to defend against a highly experienced attackers. If you're not convinced that your password scheme is weak, consider these questions:

* How likely is it that you are the only person in the world to have come up with your particular idea for a password?
* If an attacker sees one password generated with the scheme, how easy is it to come up with others?
  * Remember, passwords are regularly exposed in data breaches, so you must assume the attacker has prior examples of passwords like yours.
* Perhaps most importantly, how many possible passwords can you generate with one of these methods? Does it come anywhere close to the 80 bits of entropy we've been aiming for (2^80 = 1.2e24 = 1.2 trillion trillion possibilities)? If you can only generate 1,000 or even 1,000,000 possibilities, then it is broken.

This comic sums it up pretty well: [https://xkcd.com/936/](https://xkcd.com/936/).

## Generate passwords randomly

Strong password generation *must* involve randomness. That way, the attacker can know exactly how you convert that randomness into a password, but still be unable to guess what that password is (they do not, of course, know how your random coin flips actually turned out). Randomness can come from human sources (e.g. flipping a coin or rolling dice) as well as computer sources (more on this later).

Let's examine a basic procedure for creating a password:

1. Flip a coin 80 times. Each time, if it comes up as heads, write down a 0. If it comes up tails, write down a 1.
  * Example: your results are 01010011111001100010110110100010110011100010000100010011011010101100111100011111.
  * We can just as easily use dice rolls to generate entropy instead of flipping coins. To maximize the number of bits gained per roll, we could use a scheme where a roll of 1-4 generates 2 bits and a roll of 5-6 generates one bit.
2. Convert this bit sequence into a single integer in the range [0, 2^80 - 1]. Call that integer X.
  * Example: X = 396202457632453138501407.
3. Decide on what elements you want your password to consist of. For example, you might want your password to be lowercase letters and digits (I will notate this as [a-z0-9]). There are 26 + 10 = 36 possible characters. We now convert X into base-36, which is written as a list of integers [a1, a2, a3, ..., aN]. These are the coefficients of each power of 36, and each will be in the range [0, 35].
  * Example: 1 28 18 23 20 19 1 9 8 12 15 28 13 29 21 27.
4. For each number in your list, assign it to a character using a=0, b=1, c=2, ..., z=25, 0=26, 1=27, ..., 9=35.
  * Example: b2sxutbjimp2n3v1

And that's your password!

What this procedure does is that it samples uniformly from the first 2^80 sequences of [a-z0-9] characters (all it does is convert a number in base-2 to a number in base-36). There are 2^80 possibilities, and so our password has 80 bits of entropy. Thus, we can be confident that our password is secure; an attacker who knows that this exact procedure was followed would still require 38,334 years to crack it at 10^12 guesses per second.

This procedure is roughly what I have implemented at [https://github.com/allisonk2277/passwords](https://github.com/allisonk2277/passwords). It's well suited for generating a password with computer assistance, though it would be cumbersome to do this manually. For suggestions on generating passwords without using a computer, see the diceware section below.

A note about password rules: any further modifications (e.g. capitalizing a letter, adding a symbol, etc) make it harder to remember but do not meaningfully add any additional security; we've already established that 80 bits is adequate security. Personally, I use a simple "capitalize the first letter and add ! at the end" if a website requires me to do so. This is so I can remember what I did; I do not treat these modifications as adding any additional entropy.

### Diceware passwords

A perfectly reasonable objection is that 'b2sxutbjimp2n3v1' is hard to memorize, and that the above procedure is well suited for computers but not for working things out on pen and paper. Diceware is a method of generating passwords that simply draws from a word list, rather than a set of characters, during steps 3 and 4 of the procedure mentioned above. You randomly choose words from a long list of words to come up with passphrases like 'correct horse battery staple'. These passphrases are just as secure as a character-based password (again, count the bits and not the length) created with the same entropy, and are often easier to remember since they use actual English words and don't look like gibberish.

When generating a diceware password manually, you roll a number of dice (usually 5) at a time and match the numbers that come up to a list of words to choose a word. Instructions for doing this may be found here: [https://www.eff.org/dice](https://www.eff.org/dice).

A (misinformed) criticism that I've sometimes heard about diceware passwords is that they're vulnerable to dictionary attacks. This is simply not true; it's not any more true than saying a password like 'b2sxutbjimp2n3v1' is vulnerable just because an attacker knows all the letters of the English alphabet. A 1- or 2- word diceware phrase lacks adequate entropy, but a 6- word diceware phrase chosen from a wordlist of 6^5 = 7776 words has 77 bits of entropy which is quite secure.

I personally like the EFF's published wordlists because they have been carefully curated to use well known, recognizable words that are easy to remember. They also publish a couple other short wordlists should you want to use more words with less entropy per word.

### Generating passwords with computer help

There are a lot of programs that can help you generate a password, including [mine](https://github.com/allisonk2277/passwords). They are convenient and save you the work of manually looking up words from a list. Should you decide to use or write such a program, here are some things to keep in mind:

1. I strongly suggest you use an offline program (one you download and run on your own computer), rather than one hosted on a website - this minimizes the chance that someone else could have seen your password (the author doesn't need to have ill intent for this to be a problem; you could imagine the website itself being compromised by a third party).
  * Even if the website claims that it's all kept on the client, have you really looked at the entire source to verify that? And I mean the source that your browser actually loaded, not just the code they claim is the source.
2. Only generate passwords on your own trusted computer, and not a shared computer. If you can't trust your own computer, then you have larger problems than password generation (and you should fix those problems before generating a new password, or else your password must be assumed to be compromised as well).
  * Sometimes you don't have a choice (e.g. you share a computer with family members), but do recognize that it introduces new complexities into your threat model.
3. If you have a programming background, do read the full source to understand exactly what it's doing.
  * A pitfall to watch out for if the program is incorporating system-generated entropy is whether or not that entropy is coming from a cryptographically secure source. Default random libraries are not suitable for cryptographic purposes (many standard libraries use [MT19337](https://en.wikipedia.org/wiki/Mersenne_Twister), which has nice statistical properties but is completely broken for cryptographic purposes. In Python, a good implementation will use `random.SystemRandom` or the newer `secrets` library.

## Managing your passwords

So we've (hopefully) established how to create a strong password. But now do we really need to do this for 100+ websites, with a different password for each one? Hopefully not. Here are some recommendations:

1. Use a reputable password manager to store your website passwords. You then only need to memorize a single strong password to use as your master password, instead of 100+.
2. Each time you create an account with a website, generate a *unique* strong password and store it using the password manager. You should never have a reason to use the same password on more than one website. Password reuse is one of the most common ways by which accounts are hacked - attackers will compromise some random site (like an old web forum running phpBB from 2006), then turn around and try all the learned username/password combinations on valuable sites like your email and bank accounts (related: [https://xkcd.com/792/](https://xkcd.com/792/)).
3. Do use a 2-factor (2FA) method to further protect your accounts. Ideally a token- or hardware device-based mechanism like [Google Authenticator](https://en.wikipedia.org/wiki/Google_Authenticator) or [YubiKey](https://en.wikipedia.org/wiki/YubiKey) is best, but if those aren't available then text-message based 2FA is okay too.
  * Text-message based 2FA is inherently weaker because it relies on the security of the cellular networks in order to be secure; see [this article](https://www.theverge.com/2017/9/18/16328172/sms-two-factor-authentication-hack-password-bitcoin). Token based 2FA like Google Authenticator are more secure because there is no communication from the website to your phone for an attacker to intercept (do note that you're still vulernable to phishing if you're manually entering the token into a website - a YubiKey [defends against this](https://www.yubico.com/phishing/) by taking an additional step of cryptographically checking the website first).

### Should I write my master password down?

This one is really up to you to decide what your threat model looks like. If you're worried about a household member attempting to hack one of your accounts, then your threat model involves physical access to your computer. In addition to not writing your password down on paper, this also makes computer security *much* harder; all sorts of hardware based attacks, such as a keyboard logging device, are now possible. On the other hand, if you do trust the members of your household, then you probably shouldn't worry about this type of threat (unless you are the victim of a highly targeted attack, it's extremely unlikely an attacker will try to gain physical access to your computer). Everyone's situation is different, and so I don't have a real recommendation here.

It's worth mentioning that writing down your password may be a good idea so that friends and/or family members may have access to important documents/etc should have a medical emergency. If you're really into cryptography and have trusted friends who are as well, you could also consider encrypting a file containing your master passwords with two of your friends' public keys, such that both would need to cooperate in order to decrypt your passwords.

### What I personally do

Note: I am not affiliated with AgileBits (the owners of 1Password) in any way; I'm simply describing my current password management setup.

* I use [1Password](https://1password.com/) as my password manager.
* I have two strong passwords memorized - one for 1password and the other for email. I don't rely on 1password for my email credentials because I do not want to be vulnerable to any single site becoming unavailable; if 1password goes down then I can still recover most accounts with an email-based password reset.
* I have 2FA set up on every account of value.
* I have a list of recovery tokens I can use for 2FA stored in 1password for each account that has 2FA enabled, in case I lose my 2FA device.
