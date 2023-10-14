from enums.continent import Continent


country_to_continent = {
    'Brazil': Continent.SOUTH_AMERICA,
    'Vietnam': Continent.ASIA,
    'Colombia': Continent.SOUTH_AMERICA,
    'Indonesia': Continent.ASIA,
    'Ethiopia': Continent.AFRICA,
    'Honduras': Continent.NORTH_AMERICA,
    'India': Continent.ASIA,
    'Mexico': Continent.NORTH_AMERICA,
    'Guatemala': Continent.NORTH_AMERICA,
    'Peru': Continent.SOUTH_AMERICA,
    'Nicaragua': Continent.NORTH_AMERICA,
    'China': Continent.ASIA,
    'Costa Rica': Continent.NORTH_AMERICA,
    'Kenya': Continent.AFRICA,
    'Tanzania': Continent.AFRICA,
    'El Salvador': Continent.NORTH_AMERICA,
    'Ecuador': Continent.SOUTH_AMERICA,
    'Gabon': Continent.AFRICA,
    'Thailand': Continent.ASIA,
    'Venezuela': Continent.SOUTH_AMERICA,
    'Rwanda': Continent.AFRICA,
    'Burundi': Continent.AFRICA,
    'Yemen': Continent.ASIA,
    'Panama': Continent.NORTH_AMERICA,
    'Bolivia': Continent.SOUTH_AMERICA,
    'Timor Leste': Continent.ASIA,
    'Paraguay': Continent.SOUTH_AMERICA,
    'Myanmar': Continent.ASIA,
    'Papua New Guinea': Continent.OCEANIA
}


def get_continent(country_name):
    return country_to_continent.get(country_name, "Unknown")
