import argparse
from constants import VERB_PREFIXES, SIMPLE_DIACR_SUBS, ETM_DIACR_SUBS, DEFAULT_UNITS, BASE_ISV_TOKEN_REGEX


def dodavaj_bukvy(word, etm_morph):
    corrected = [f.word for f in etm_morph.parse(word)]
    if len(set(corrected)) == 1:
        return corrected[0]
    if len(set(corrected)) == 0:
        return word + "/?"
    return "/".join(set(corrected))


def spellcheck_text(paragraph, std_morph):
    delimiters = BASE_ISV_TOKEN_REGEX.finditer(paragraph)
    proposed_corrections = []
    for delim in delimiters:
        token = delim.group().lower()
        is_word = any(c.isalpha() for c in delim.group())
        is_known = None
        corrected = None
        confident_correction = None

        if is_word:
            is_known = True
            candidates = set([f.word for f in std_morph.parse(token)])
            if candidates != {token} or not std_morph.word_is_known(token):
                is_known = False
            if len(set(candidates)) >= 1:
                corrected = "/".join(set(candidates))

        markup = "" if is_known or not is_word else "^" * len(token)
        if corrected and corrected != token:
            proposed_corrections.append(corrected)
            confident_correction = corrected
            markup = str(len(proposed_corrections))
        span_data = (delim.start(), delim.end(), markup)
        yield span_data, confident_correction


def perform_spellcheck(text, std_morph):
    data = list(spellcheck_text(text, std_morph))
    spans = [entry[0] for entry in data if entry[0][2]]
    proposed_corrections = [entry[1] for entry in data if entry[1]]
    return text, spans, proposed_corrections

