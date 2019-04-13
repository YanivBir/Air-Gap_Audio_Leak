def relative_english_freq():
    freqs = dict()

    freqs['a'] = 8.167
    freqs['b'] = 1.492
    freqs['c'] = 2.782
    freqs['d'] = 4.253
    freqs['e'] = 12.702
    freqs['f'] = 2.228
    freqs['g'] = 2.015
    freqs['h'] = 6.094
    freqs['i'] = 6.966
    freqs['j'] = 0.153
    freqs['k'] = 0.772
    freqs['l'] = 4.025
    freqs['m'] = 2.406
    freqs['n'] = 6.749
    freqs['o'] = 7.507
    freqs['p'] = 1.929
    freqs['q'] = 0.095
    freqs['r'] = 5.987
    freqs['s'] = 6.327
    freqs['t'] = 9.056
    freqs['u'] = 2.758
    freqs['v'] = 0.978
    freqs['w'] = 2.360
    freqs['x'] = 0.150
    freqs['y'] = 1.974
    freqs['z'] = 0.074

    freqs['A'] = 8.167
    freqs['B'] = 1.492
    freqs['C'] = 2.782
    freqs['D'] = 4.253
    freqs['E'] = 12.702
    freqs['F'] = 2.228
    freqs['G'] = 2.015
    freqs['H'] = 6.094
    freqs['I'] = 6.966
    freqs['J'] = 0.153
    freqs['K'] = 0.772
    freqs['L'] = 4.025
    freqs['M'] = 2.406
    freqs['N'] = 6.749
    freqs['O'] = 7.507
    freqs['P'] = 1.929
    freqs['Q'] = 0.095
    freqs['R'] = 5.987
    freqs['S'] = 6.327
    freqs['T'] = 9.056
    freqs['U'] = 2.758
    freqs['V'] = 0.978
    freqs['W'] = 2.360
    freqs['X'] = 0.150
    freqs['Y'] = 1.974
    freqs['Z'] = 0.074

    NUMBERS_FREQ = 3
    freqs['0'] = NUMBERS_FREQ
    freqs['1'] = NUMBERS_FREQ
    freqs['2'] = NUMBERS_FREQ
    freqs['3'] = NUMBERS_FREQ
    freqs['4'] = NUMBERS_FREQ
    freqs['5'] = NUMBERS_FREQ
    freqs['6'] = NUMBERS_FREQ
    freqs['7'] = NUMBERS_FREQ
    freqs['8'] = NUMBERS_FREQ
    freqs['9'] = NUMBERS_FREQ
    freqs[' '] = NUMBERS_FREQ
    freqs[','] = NUMBERS_FREQ
    freqs[':'] = NUMBERS_FREQ
    freqs['.'] = NUMBERS_FREQ
    freqs['\n'] = NUMBERS_FREQ

    for c in freqs.keys():
        freqs[c] /= 100

    return freqs

def str_freq(s):
    """Calculate the relative frequency of every character in the given string.

    The return format is mostly for easy feeding into the Huffman tree creator.

    :s: String.
    :returns: Dictionary of {character: frequency} pairs.

    """
    freqs = dict()

    for c in s:
        if c in freqs:
            freqs[c] += 1
        else:
            freqs[c] = 1

    # Turn the absolute frequencies into relative ones.
    slen = len(s)
    for c in freqs.keys():
        freqs[c] /= slen

    return freqs

def file_freq(name):
    with open(name) as f:
        return str_freq(f.read())