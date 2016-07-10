# Vim Notes

### Movement/Selection

`.` repeats the last command

`*` executes a search on the current word

`%` goes to the next brace or paren

`>aB` indents the current block

`viB` visually selects the current block

`vi{` visually selects inside the brace or paren

`vaw` deletes whitespace after word

`gv` reselects the last visual thing

`gi` go to last edited location

`C` to change remaining text on line

`dt` `dT` delete TO something

`~` toggle case

`<C-I>`, `<C-O>` rewind/forward past movements

`gf` go to file under cursor


### Buffer / Split Commands

`bd` buffer delete

`ls` list buffers

`sb` split all buffers

`Sex` open Explore in split


### Other

`<C-N>` autocomplete

`:r!` read in the contents of a command

`:r` read in the contents of a file

`<C-r>=` and a calculation will insert value into text

### Cool Patterns

`f <space>` `r <enter>` to break on props

then `f <space> .` to repeat

### Encryption

__Encrypting__

Select the text you'd like to encrypt in visual mode. (for example, select the
lines using `V`).

Then, type `:` to being entering a command, and `!gpg -ca`.   The `c` argument
instructs gpg to use symmetric, passphrase based encryption, and running this
command will prompt you for a password.  The `a` argument adds 'ascii armor' the
encrypted text, so that the original plaintext will be replaced with this:

```
-----BEGIN PGP MESSAGE-----
Version: GnuPG v1

jA0EBwMCEXxPltvl7GJg0sBFAUFetQsNCNH9pgpKfP0b+YVcv4TKuH36riJJC2kB
kyKbT/pDoTWxfLsPAfFZOyGl37VeLuyPrzdu/OUiHaSMOCXtizI0mv6yd1ovVY4P
e/gQU7jDhlLJrVdU2fYV6qwAJLGi8lRuRbNzTdqNPw37jxA/YQN5IOYAenRFB2Sr
w2kgpkDwPcwT8IOc9J9ViH5Vinxmks2JhgrNdhw4DIB29+77N5ui09Vegkbud4Te
pAY4zNgVLRCR8Zg2+BX2ns4OyeIjt/eROquUqz0BItAK50mTSi1uQlkBfNZ8PSlH
wvKwAwhLIu4Y0OyYOCz26cxJR4EhSoZEy3ByY8kE6itI8BcgQqIW
=dbgJ
-----END PGP MESSAGE-----
```

__Decrypting__

To decrypt, select the 'armored' block of text in visual mode, type `:` and
enter the command `!gpg -qd`, as above.  The `d` argument will decrypt the
visually selected text, and will prompt you for a password.  The `q` argument
prevents various other info from being printed.  Enter the password you entered
when encrypting, and the 'armored' PGP message will be replaced by your original
plaintext!

__TLDR:__

This assumes you have `gpg` installed and on your path.

To encrypt, select the plaintext visually, press `:`, and then enter the command `!gpg -ca`.

To decrypt, select the PGP message visually, press `:`, and then enter the command `!gpg -qd`.


