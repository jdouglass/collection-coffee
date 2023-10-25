from data.coffee_varieties import VARIETY_MAPPINGS


def normalize_variety_names(varieties):

    normalized_varieties = [VARIETY_MAPPINGS.get(
        variety, variety) for variety in varieties]

    return normalized_varieties
