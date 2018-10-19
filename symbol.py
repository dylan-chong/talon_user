from talon.voice import Context, Key

ctx = Context('symbol')

keymap = {
    'quit': Key('esc'),

    'enter': Key('enter'),
    'delete': Key('backspace'),
    'spunk': Key('delete'),

    'tab': Key('tab'),
    'left': Key('left'),
    'right': Key('right'),
    'up': Key('up'),
    'down': Key('down'),

    'question': '?',
    'dash': '-',
    'plus': '+',
    'equals': '=',
    'tilde': '~',
    'backtick': Key('backtick'), # TODO NEXT this doesnt work
    'bang': '!',
    'dollar': '$',
    'underscore': '_',
    'semi': ';',
    'ratio': ':',

    'lacket': '[',
    'racket': ']',
    'push': '(',
    'pop': ')',
    'lace': '{',
    'race': '}',
    'langle': '<',
    'wrangle': '>',

    'aster': '*',
    'hash': '#',
    'percent': '%',
    'caret': '^',
    'at sign': '@',
    'ampersand': '&',
    'piper': '|',

    'dubquote': '"',
    'singquote': "'",
    'point': '.',
    'comma': ',',
    'swipe': ', ',
    'space': ' ',
    'slash': '/',
    'backslash': '\\',
}

ctx.keymap(keymap)
