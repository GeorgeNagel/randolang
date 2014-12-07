vowels = [
    'AA', # odd
    'AH', # hut
    'AW', # cow
    'EH', # Ed
    'EY', # ate
    'IH', # it
    'OW', # oat
    'UH', # hood
    'AE', # at
    'AO', # ought
    'AY', # hide
    'ER', # hurt
    'IY', # eat
    'OY', # toy
    'UW', # two
]
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
}
long_vowel_replacement = {
    # Syl: (start, intermediate, before last cons., after last cons.)
    'AW': ('ou', 'ou', 'ou', 'ow'), # cow
    'EY': ('a', 'a', 'a', 'ay'), # ate
    'OW': ('o', 'o', 'oa', 'o'), # oat
    'UH': ('u', 'oo', 'oo', 'u'), # hood
    'AY': ('i', 'ie', 'i', 'ye'), # hide
    'ER': ('ur', 'ur', 'er', 'er'), # hurt
    'IY': ('ea', 'ee', 'ee', 'y'), # eat
    'OY': ('oy', 'oy', 'oi', 'oy'), # toy
    'UW': ('u', 'u', 'oo', 'oo'), # two
}

def phones_to_word(phones):
    """Convert a list of phones like 'AA' to a string.
    Note: Assumes emphasis numbers have been stripped.
    """

    # Replace short vowels
    dh_replaced = _handle_dh(phones)
    hh_replaced = _handle_hh(dh_replaced)
    jh_replaced = _handle_jh(hh_replaced)
    q_replaced = _handle_q(jh_replaced)
    protected = _protect_short_vowels(q_replaced)
    short_replaced = _handle_short_vowels(protected)
    long_replaced = _handle_long_vowels(short_replaced)
    c_replaced = _handle_c(long_replaced)

    lowered_phones = [phone.lower() for phone in c_replaced]
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