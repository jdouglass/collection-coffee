import pycountry


def remove_country_names(input_string):
    # Get a list of all country names
    countries = [country.name for country in pycountry.countries]

    # Remove all country names from the input string
    for country in countries:
        input_string = input_string.replace(country, "")

    return input_string
