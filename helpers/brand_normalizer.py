def normalize_brand_name(brand):
    mapping = {
        'September': 'September Coffee Co',
        'Hatch': 'Hatch Coffee Roasters',
        'Onyx': 'Onyx Coffee Lab',
        'Rabbit Hole': 'Rabbit Hole Roasters',
        'Keen': 'Keen Coffee',
        'Rooftop': 'Rooftop Coffee Roasters',
        'Sloane': 'Sloane Coffee',
        'Firebat': 'Firebat Coffee Roasters',
        'Sorellina': 'Sorellina Coffee',
        'Roasti': 'Roasti Coffee',
        'Transcend': 'Transcend Coffee',
        'Dak': 'DAK Coffee Roasters',
        'Ethica': 'Ethica Coffee Roasters',
        'Manhattan': 'Manhattan Coffee Roasters',
        'Hasty': 'Hasty Coffee'
    }

    return mapping.get(brand, brand)
