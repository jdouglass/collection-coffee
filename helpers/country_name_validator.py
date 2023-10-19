import pycountry
from config.constants import UNKNOWN, MULTIPLE


def validate_country_name(country_str):
    country_str = country_str.title()

    # Check if '&' or '+' is present, which indicates multiple countries
    if '&' in country_str or '+' in country_str:
        return MULTIPLE

    # Validate if the string is a valid country name
    try:
        country = pycountry.countries.lookup(country_str)
        return country.name
    except LookupError:
        return UNKNOWN
