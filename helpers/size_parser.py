from config.constants import LBS_TO_GRAMS, KG_TO_GRAMS


def parse_size(size):
    if 'kg' in size:
        return int(size.split('kg')[0].strip()) * KG_TO_GRAMS
    elif 'g' in size:
        return int(size.split('g')[0].strip())
    elif 'lb' in size:
        return int(float(size.split('lb')[0].strip()) * LBS_TO_GRAMS)
    elif 'capsule' in size:
        return int(size.split('capsule')[0].strip())
    elif 'sachet' in size:
        return int(size.split('sachet')[0].strip())
    elif 'box of' in size:
        return int(size.split('box of')[1].strip())
    elif '-pack' in size:
        return int(size.split('-pack')[0].strip())
    elif 'pack of' in size:
        return int(size.split('pack of')[1].strip())
    elif 'pods' in size:
        return int(size.split('pods')[0].strip())
    elif 'packs' in size:
        return int(size.split('packs')[0].strip())
    return 0
