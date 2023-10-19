from enums.product_type import ProductType


def verify_product_type(string_to_check):
    return string_to_check in ProductType._value2member_map_
