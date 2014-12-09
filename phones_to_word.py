consonants = [
    'B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH',
    'K', 'L', 'M', 'N', 'NG', 'P', 'R', 'S',
    'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH'
]

short_vowel_replacement = {
    'AE': 'a', # after
    'EH': 'e', # hen
    'IH': 'i', # hit
    'AA': 'o', # hot
    'AO': 'o', # taught
    'AH': 'e', # hut
    'UH': 'oo', # good
    'ER': 'ur', # hurt
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

def phones_to_word(phones):
    """Convert a list of phones like 'AA' to a string.
    Note: Assumes emphasis numbers have been stripped.
    """
    # First, handle vowel sounds
    # Iterate over phones starting from the end
    for index in range(len(phones))[-1::-1]:
        phone = phones[index]
        if phone in long_vowel_replacement.keys():
            pass

    lowered_phones = [phone.lower() for phone in phones]
    word = ''.join(lowered_phones)
    return word

def _protect_short_vowels(phones):
    """Double consonants following short vowels."""
    protected_phones = phones
    if len(phones) > 2:
        for index, phone in enumerate(protected_phones):
            if phone in short_vowel_replacement:
                if index+2 < len(protected_phones):
                    if protected_phones[index+1] in consonants:
                        # Make sure you don't double HH, TH, SH, ZH, DH, JH
                        if len(protected_phones[index+1]) == 1:
                            if protected_phones[index+2] not in consonants:
                                protected_phones[index+1] = protected_phones[index+1].lower()*2
    return protected_phones

def _handle_short_vowels(phones):
    """Short vowels get replaced by single, lowercase letter"""
    short_replaced = []
    for phone in phones:
        if phone in short_vowel_replacement:
            short_replaced.append(short_vowel_replacement[phone])
        else:
            short_replaced.append(phone)
    return short_replaced

def _handle_long_vowels(phones):
    # Handle start long vowels
    long_replaced = phones
    if phones[0] in long_vowel_replacement:
        long_replaced[0] = long_vowel_replacement[phones[0]][0]

    # Handle long vowel before last consonant
    if len(phones) > 1:
        if phones[-1] not in vowels:
            previous_long_vowel = phones[-2]
            # Special case handling for 'ates' types (['EY', 'T', 'S'])
            if phones[-2] in long_vowel_replacement:
                long_replaced[-2] = long_vowel_replacement[phones[-2]][2]
                long_replaced.append('e')
            elif phones[-2] in consonants:
                if len(phones) > 2 and phones[-3] in long_vowel_replacement:
                    long_replaced[-3] = long_vowel_replacement[phones[-3]][2]
                    long_replaced.insert(-1, 'e')

    # Handle ending long vowels
    if phones[-1] in long_vowel_replacement:
        long_replaced[-1] = long_vowel_replacement[phones[-1]][3]

    # Handle remaining (intermediate) long vowels
    for index, phone in enumerate(long_replaced):
        if phone in long_vowel_replacement:
            long_replaced[index] = long_vowel_replacement[phone][1]

    return long_replaced


def _handle_q(phones):
    q_replaced = []
    index = 0
    while index < len(phones):
        phone = phones[index]
        if index+1 < len(phones):
            if phone == 'K' and phones[index+1] == 'W':
                phone = 'qu'
                # Skip the w and continue with the rest of the phones
                index += 1
        q_replaced.append(phone)
        index += 1
    return q_replaced


def _handle_c(phones):
    """Replace C sounds."""

    c_replaced = phones

    # cc to protect short vowel
    # ck protects short vowel when followed by e i or y
    for index, phone in enumerate(c_replaced):
        if phone == 'kk':
            c_replaced[index] = 'cc'
            if index+1 < len(c_replaced):
                if c_replaced[index+1][0] in ['e', 'i', 'y']:
                    c_replaced[index] = 'ck'

    # use k when followed by e i or y
    for index, phone in enumerate(c_replaced):
        if index+1 < len(c_replaced):
            if phone == 'K' and c_replaced[index+1][0] in ['e', 'i', 'y']:
                c_replaced[index] = 'k'

    # ck always follows short vowel at the end of a monosyllable
    if c_replaced[-1] == 'K':
        c_replaced[-1] = 'ck'

    # fall back to using plain c
    for index, phone in enumerate(c_replaced):
        if phone == 'K':
            c_replaced[index] = 'c'

    return c_replaced


def _handle_jh(phones):
    """Replace JH sounds."""
    jh_replaced = phones
    if jh_replaced[-1] == 'JH':
        jh_replaced[-1] = 'g'
    for index, phone in enumerate(jh_replaced):
        if phone == 'JH':
            jh_replaced[index] = 'j'
    return jh_replaced

def _handle_hh(phones):
    """Replace HH sounds."""
    h_replaced = phones
    for index, phone in enumerate(h_replaced):
        if phone == "HH":
            h_replaced[index] = 'h'
    return h_replaced

def _handle_dh(phones):
    """Replace DH sounds."""
    h_replaced = phones
    for index, phone in enumerate(h_replaced):
        if phone == "DH":
            h_replaced[index] = 'th'
    return h_replaced  