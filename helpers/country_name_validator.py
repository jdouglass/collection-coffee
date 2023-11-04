import pycountry
from config.constants import UNKNOWN, MULTIPLE


def validate_country_name(country_str):
    # Check if '&' or '+' is present, which indicates multiple countries
    if '&' in country_str or '+' in country_str or '%' in country_str:
        return MULTIPLE

    # Get all country names
    countries = sorted(
        (country.name for country in pycountry.countries), key=len, reverse=True)

    for country in countries:
        if country.lower() in country_str.lower():
            return country.title()
    return UNKNOWN
