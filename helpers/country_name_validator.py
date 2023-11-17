import pycountry
from config.constants import UNKNOWN, MULTIPLE
import re


def validate_country_name(country_str):
    if '&' in country_str or '+' in country_str or '%' in country_str:
        return MULTIPLE

    # Get all country names
    countries = [country.name for country in pycountry.countries]

    countries_found = set()

    for country in countries:
        if re.search(r'\b' + re.escape(country) + r'\b', country_str, re.IGNORECASE):
            countries_found.add(country)

    if len(countries_found) > 1:
        return MULTIPLE
    elif len(countries_found) == 1:
        return next(iter(countries_found))
    return UNKNOWN
