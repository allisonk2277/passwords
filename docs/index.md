# Password basics (aka "How to Think About Passwords")

The goal of this article is to discuss what are generally considered good and bad practices for choosing and managing passwords. If you're already familiar with these ideas and are simply looking for a strong password generation tool, you might look at my [password generation tool](https://github.com/allisonk2277/passwords) that supports a variety of common password formats.

## Best practices, the short version

1. Strong passwords must be chosen randomly. There are no exceptions to this rule.
2. Password strength is described in terms of *entropy*, which is a measure of the number of possible passwords that could have been chosen.
3. Without sacrificing entropy, choose passwords that are easier to remember.
4. As of this writing, ~80 bits of entropy is a pretty reasonable choice for password entropy. This is approximately 16 alphanumeric characters, or 6 words from the large words list, or 8 words from the short words list.
5. Use a password manager. Memorize one really strong password as your master password, and let the password manager handle the rest.
6. Don't reuse passwords. This is trivial to do if you use a password manager.

Everything else in this article is a more detailed discussion about the above points.
