def normalize_variety_names(varieties):
    mapping = {
        'Geisha': 'Gesha',
        'Ruiru': 'Ruiru 11',
        '74158': 'Ethiopian Landraces',
        'Yellow Catuaí': 'Yellow Catuai',
        'Paraïso': 'Paraiso',
        '34': 'SL-34',
        'Sl28': 'SL-28',
        'Sl34': 'SL-34',
        'Sl32': 'SL-32',
        'Sl 28': 'SL-28',
        'Sl Varieties': 'SL Varieties',
        'Landraces': 'Ethiopian Landraces'
    }

    normalized_varieties = [mapping.get(
        variety, variety) for variety in varieties]

    return normalized_varieties
