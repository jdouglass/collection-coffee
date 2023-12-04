ALTER TABLE product_variant
DROP COLUMN IF EXISTS product_original_price;

ALTER TABLE product_variant
ADD product_original_price Decimal(6, 2);