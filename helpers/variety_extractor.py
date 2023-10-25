from fuzzywuzzy import fuzz
from data.coffee_varieties import KNOWN_VARIETIES, VARIETY_MAPPINGS
from config.constants import UNKNOWN
import re


def preprocess_variety_name(variety_string):
    variety_string = re.sub(r'\(.*?\)', '', variety_string).strip()

    for old_name, new_name in VARIETY_MAPPINGS.items():
        variety_string = variety_string.replace(old_name, new_name)
    return variety_string


def extract_varieties(input_str, threshold=60):
    input_str = preprocess_variety_name(input_str)
    words = input_str.split()
    sorted_known_varieties = sorted(
        KNOWN_VARIETIES, key=lambda x: len(x.split()), reverse=True)

    i = 0
    extracted_varieties = []

    while i < len(words):
        best_matches = []
        best_ratio = 0
        potential_match = None

        for known_variety in sorted_known_varieties:
            known_words = known_variety.split()
            current_potential_match = ' '.join(words[i:i+len(known_words)])

            current_ratio = fuzz.ratio(
                current_potential_match, known_variety)

            if current_ratio > best_ratio:
                best_matches = [known_variety]
                best_ratio = current_ratio
                potential_match = current_potential_match
            elif current_ratio == best_ratio:
                best_matches.append(known_variety)

        if best_ratio >= threshold:
            # Select the best match (highest score and shortest length in case of a tie)
            best_match = min(best_matches, key=len)
            extracted_varieties.append(best_match)
            i += len(best_match.split())

            with open("logs.txt", "a") as logfile:
                logfile.write(
                    f"Best match for '{potential_match}': {best_match} with ratio {best_ratio}\n")
        else:
            i += 1

    extracted_varieties = list(dict.fromkeys(extracted_varieties))

    return extracted_varieties if len(extracted_varieties) > 0 else [UNKNOWN]
