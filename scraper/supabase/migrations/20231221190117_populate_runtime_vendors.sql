ALTER TABLE runtime ADD UNIQUE (vendor_id);

INSERT INTO runtime (vendor_id)
SELECT id FROM vendor WHERE name IN (
    'Black Creek Coffee',
    'Continuum Coffee Roasters',
    'De Mello',
    'Heart Coffee Roasters',
    'House of Funk Brewing',
    'Library Specialty Coffee',
    'Luna Coffee',
    'Matchstick',
    'Monogram Coffee',
    'Nemesis Coffee',
    'Pallet Coffee Roasters',
    'Phil & Sebastian',
    'Pirates of Coffee',
    'Prairie Lily Coffee',
    'Quietly Coffee',
    'Rabbit Hole Roasters',
    'Rosso Coffee',
    'Sam James Coffee Bar',
    'September Coffee',
    'Sey Coffee',
    'Sorellina Coffee',
    'Subtext Coffee Roasters',
    'The Angry Roaster',
    'Thom Bargen Coffee Roasters',
    'Transcend Coffee',
    'Zab Café',
    'Rogue Wave Coffee',
    'Hatch Coffee Roasters',
    'Prototype Coffee',
    'Timbertrain Coffee Roasters',
    'Traffic Coffee',
    'Eight Ounce Coffee',
    'Revolver Coffee'
)
ON CONFLICT (vendor_id) DO NOTHING;