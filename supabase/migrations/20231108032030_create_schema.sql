CREATE TABLE brand (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE continent (
    id SERIAL PRIMARY KEY,
    name VARCHAR(10) UNIQUE
);

CREATE TABLE currency_code (
    id SERIAL PRIMARY KEY,
    code VARCHAR(3) UNIQUE
);

CREATE TABLE process_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE product_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE tasting_note (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE variety (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    continent_id INTEGER NOT NULL,
    CONSTRAINT fk_continent FOREIGN KEY (continent_id) REFERENCES continent(id)
);

-- Index on continent_id helps in JOIN operations with continent.
CREATE INDEX idx_country_continent ON country(continent_id);

CREATE TABLE vendor (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    country_id INTEGER NOT NULL,
    currency_code_id INTEGER NOT NULL,
    CONSTRAINT fk_country FOREIGN KEY (country_id) REFERENCES country(id),
    CONSTRAINT fk_currency_code FOREIGN KEY (currency_code_id) REFERENCES currency_code(id)
);

-- Indexes on foreign keys for faster JOINs.
CREATE INDEX idx_vendor_country ON vendor(country_id);
CREATE INDEX idx_vendor_currency_code ON vendor(currency_code_id);

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER NOT NULL,
    country_of_origin_id INTEGER NOT NULL,
    vendor_id INTEGER NOT NULL,
    process_category_id INTEGER NOT NULL,
    product_type_id INTEGER NOT NULL,
    title VARCHAR(255),
    process VARCHAR(255),
    product_url TEXT UNIQUE,
    image_url TEXT,
    discovered_date_time TIMESTAMP,
    product_handle VARCHAR(255),
    is_decaf BOOLEAN,
    CONSTRAINT fk_brand FOREIGN KEY (brand_id) REFERENCES brand(id),
    CONSTRAINT fk_country_of_origin FOREIGN KEY (country_of_origin_id) REFERENCES country(id),
    CONSTRAINT fk_vendor FOREIGN KEY (vendor_id) REFERENCES vendor(id),
    CONSTRAINT fk_process_category FOREIGN KEY (process_category_id) REFERENCES process_category(id),
    CONSTRAINT fk_product_type FOREIGN KEY (product_type_id) REFERENCES product_type(id)
);

-- Indexes on foreign keys to enhance JOIN performance.
CREATE INDEX idx_product_brand ON product(brand_id);
CREATE INDEX idx_product_country_of_origin ON product(country_of_origin_id);
CREATE INDEX idx_product_vendor ON product(vendor_id);
CREATE INDEX idx_product_process_category ON product(process_category_id);
CREATE INDEX idx_product_product_type ON product(product_type_id);

CREATE TABLE product_variant (
    id SERIAL PRIMARY KEY,
    variant_id BIGINT,
    product_id INTEGER NOT NULL,
    product_size DECIMAL(5,2),
    product_price DECIMAL(5,2),
    is_sold_out BOOLEAN,
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES product(id)
);

-- Indexes on product_id for faster lookups and JOIN operations.
CREATE INDEX idx_product_variant_product ON product_variant(product_id);

