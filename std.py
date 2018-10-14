from talon.voice import Word, Context, Key, Rep, Str, press
from talon import ctrl
import string

# If you're used to VC alphabet, use the line below instead
#alpha_alt = 'arch brov char dell etch fomp goof hark ice jinks koop lug mowsh nerb ork pooch quash rosh souk teek unks verge womp trex yang zooch'.split()
alpha_alt = 'air bat cap drum each fine gust harp sit jury crunch look made night odd pit quench red sun trap urge vest whale plex yank zip'.split()

alnum = list(zip(alpha_alt, string.ascii_lowercase)) + \
    [(str(i), str(i)) for i in range(0, 10)]

alpha = {}
alpha.update(dict(alnum))
alpha.update({'ship %s' % word: letter for word,
              letter in zip(alpha_alt, string.ascii_uppercase)})

# TODO replace this ugly stuff with something from here https://github.com/dwighthouse/unofficial-talonvoice-docs/blob/master/docs/UserScriptOverview.md
alpha.update({'con %s' % k: Key('ctrl-%s' % v) for k, v in alnum})
alpha.update({'con big %s' % k: Key('ctrl-shift-%s' % v) for k, v in alnum})
alpha.update({'con altering %s' % k: Key('ctrl-alt-%s' % v) for k, v in alnum})
alpha.update({'cherrio %s' % k: Key('cmd-%s' % v) for k, v in alnum})
alpha.update({'cherrio big %s' % k: Key('cmd-shift-%s' % v) for k, v in alnum})
alpha.update({'cherrio altering big %s' % k: Key('cmd-alt-shift-%s' % v) for k, v in alnum})
alpha.update({'cherrio altering big %s' % k: Key('cmd-alt-shift-%s' % v) for k, v in alnum})
alpha.update({'altering %s' % k: Key('alt-%s' % v) for k, v in alnum})
alpha.update({'altering big %s' % k: Key('alt-%s' % v) for k, v in alnum})
alpha.update({'mash mod %s' % k: Key('ctrl-shift-cmd-%s' % v) for k, v in alnum})

mapping = {
    'semicolon': ';',
    r'new-line': '\n',
    r'new-paragraph': '\n\n',
}


def parse_word(word):
    word = word.lstrip('\\').split('\\', 1)[0]
    word = mapping.get(word, word)
    return word


def text(m):
    tmp = [str(s).lower() for s in m.dgndictation[0]._words]
    words = [parse_word(word) for word in tmp]
    Str(' '.join(words))(None)


def word(m):
    tmp = [str(s).lower() for s in m.dgnwords[0]._words]
    words = [parse_word(word) for word in tmp]
    Str(' '.join(words))(None)

def surround(by):
    def func(i, word, last):
        if i == 0:
            word = by + word
        if last:
            word += by
        return word
    return func


def rot13(i, word, _):
    out = ''
    for c in word.lower():
        if c in string.ascii_lowercase:
            c = chr((((ord(c) - ord('a')) + 13) % 26) + ord('a'))
        out += c
    return out

formatters = {
    'dunder': (True, lambda i, word, _: '__%s__' % word if i == 0 else word),
    'cram':  (True, lambda i, word, _: word if i == 0 else word.capitalize()),
    'pathway':  (True, lambda i, word, _: word if i == 0 else '/'+word),
    'dotsway':  (True, lambda i, word, _: word if i == 0 else '.'+word),
    'snake':  (True, lambda i, word, _: word if i == 0 else '_'+word),
    'yellsnik':  (True, lambda i, word, _: word.capitalize() if i == 0 else '_'+word.capitalize()),
    'smash':  (True, lambda i, word, _: word),
    'dollcram': (True, lambda i, word, _: '$'+word if i == 0 else word.capitalize()),
    'champ': (True, lambda i, word, _: word.capitalize() if i == 0 else " "+word),
    'lowcram': (True, lambda i, word, _: '@'+word if i == 0 else word.capitalize()),
    'criff': (True, lambda i, word, _: word.capitalize()),

    'spine':  (True, lambda i, word, _: word if i == 0 else '-'+word),
    'title':  (False, lambda i, word, _: word.capitalize()),
    'yeller': (False, lambda i, word, _: word.upper()),
    'dub-string': (False, surround('"')),
    'string': (False, surround("'")),
    'padded': (False, surround(" ")),
    'rot thirteen':  (False, rot13),
}


def FormatText(m):
    fmt = []
    for w in m._words:
        if isinstance(w, Word):
            fmt.append(w.word)
    words = [str(s).lower() for s in m.dgndictation[0]._words]

    tmp = []
    spaces = True
    for i, word in enumerate(words):
        word = parse_word(word)
        for name in reversed(fmt):
            smash, func = formatters[name]
            word = func(i, word, i == len(words)-1)
            spaces = spaces and not smash
        tmp.append(word)
    words = tmp

    sep = ' '
    if not spaces:
        sep = ''
    Str(sep.join(words))(None)

ctx = Context('input')

keymap = {}
keymap.update(alpha)
keymap.update({
    'phrase <dgndictation> [over]': text,
    'word <dgnwords>': word,
    '(%s)+ <dgndictation>' % (' | '.join(formatters)): FormatText,
})

ctx.keymap(keymap)
