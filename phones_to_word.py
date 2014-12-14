consonants = [
    'B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH',
    'K', 'L', 'M', 'N', 'NG', 'P', 'R', 'S',
    'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH'
]

short_vowel_replacement = {
    # vowel: (intermediate, ending)
    'AE': ('a', 'ah'), # after
    'EH': ('e', 'eh'), # hen
    'IH': ('i', 'ih'), # hit
    'AA': ('o', 'aw'), # hot
    'AO': ('o', 'aw'), # taught
    'AH': ('u', 'uh'), # hut
    'UH': ('oo', 'uh'), # good
    'ER': ('er', 'er'), # hurt
}
long_vowel_replacement = {
    # vowel: (VVC form, VCV form, CVV form (end form))
    'AW': ('ou', '', 'ow'), # loud, , cow
    'EY': ('ai', 'a', 'ay'), # braid, ate, delay
    'OW': ('oa', 'o', 'ow'), # oat, broke, flow
    'AY': ('ie', 'i', 'igh'), # fried, ice, nigh
    'IY': ('ee', 'e', 'y'), # sleep, impede, early
    'OY': ('oi', '', 'oy'), # boil, , toy
    'UW': ('oo', 'u', 'ue'), # boom, flute, subdue
}
vowels = [short_vowel_replacement.keys() + long_vowel_replacement.keys()]

suffixes = {
    ('SH', 'AH', 'N'): 'tion',
    ('SH', 'AH', 'N', 'S'): 'tions',
    ('S', 'AH', 'M'): 'some',
    ('EH', 'R', 'IY'): 'ary',
    ('ER', 'IY'): 'ery'
}

def phones_to_word(phones):
    """Convert a list of phones like 'AA' to a string.
    Note: Assumes emphasis numbers have been stripped.
    """
    # Handle spellings of any known suffixes
    for phone_length in [4, 3, 2]:
        ending_phones = tuple(phones[-phone_length:])
        if ending_phones in suffixes:
            spelling = suffixes[ending_phones]
            phones[-phone_length:] = [spelling]

    # First, handle vowel sounds
    # Start with ending long vowels
    if phones[-1] in long_vowel_replacement.keys():
        long_vowel = phones[-1]
        spelling = long_vowel_replacement[long_vowel][2]
        phones[-1] = spelling
    elif phones[-1] in short_vowel_replacement.keys():
        spelling = short_vowel_replacement[phones[-1]][1]
        phones[-1] = spelling
    # Iterate over phones starting from the end
    for index in range(len(phones))[-2::-1]:
        phone = phones[index]
        if phone in long_vowel_replacement.keys():
            # Replace long vowels
            if (index-1 >= 0 and phones[index - 1] in consonants) and (index+1 < len(phones) and phones[index + 1] in consonants):
                # Previous phone is a consonant. Next phone is a consonant.
                # Safe to use VVC form.
                spelling = long_vowel_replacement[phone][0]
                phones[index] = spelling
            elif index+1 < len(phones) and phones[index+1] in consonants:
                # Previous phone is a vowel. Next phone is a consonant.
                # VCV Form
                spelling = long_vowel_replacement[phone][1]
                if spelling:
                    phones[index] = spelling
                    phones.insert(index+2, 'e')
                else:
                    spelling = long_vowel_replacement[phone][0]
                    phones[index] = spelling
            else:
                # Next phone is a vowel
                phones[index] = long_vowel_replacement[phone][1] or long_vowel_replacement[phone][0]
        elif phone in short_vowel_replacement.keys():
            # Replace short vowels
            spelling = short_vowel_replacement[phone][0]
            phones[index] = spelling
        else:
            # Handle multi-letter consonants
            if phone == 'ZH':
                phones[index] = 'si'
            elif phone == 'JH':
                phones[index] = 'j'
            elif phone == 'HH':
                phones[index] = 'h'
            elif phone == 'DH':
                phones[index] = 'th'
            elif len(phone) == 2:
                # Keep the spelling of the remaining consonants
                pass
            # Protect short vowels
            elif index+1 < len(phones) and phones[index+1][0] == 'e':
                if index-1 >= 0 and phones[index-1] in short_vowel_replacement.keys():
                    if phone == 'K':
                        # Special case handling of doubles
                        phones[index] = 'ck'
                    elif phones[index-1] != 'ER':
                        phones.insert(index+1, phone)
            # Handle remaining K sounds
            elif phone == 'K':
                phones[index] = 'c'


    # Handle ending consonants not altered by VCV form
    if phones[-1] == 'JH':
        phones[-1] = 'ge'
    elif phones[-1] == 'Z':
        phones[-1] = 's'

    lowered_phones = [phone.lower() for phone in phones]
    word = ''.join(lowered_phones)
    if 'kw' in word or 'cw' in word:
        letters = [letter for letter in word]
        for index, letter in enumerate(letters):
            if letter == 'w' and index > 0 and letters[index-1] in ['k', 'c']:
                letters[index-1] = 'q'
                letters[index] = 'u'
        word = ''.join(letters)
    return word
