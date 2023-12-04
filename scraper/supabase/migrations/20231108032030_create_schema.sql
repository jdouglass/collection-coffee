CREATE TABLE brand (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE continent (
    id SERIAL PRIMARY KEY,
    name VARCHAR(14) UNIQUE
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

-- Seed the `continent` table
INSERT INTO continent (name) VALUES
('Africa'),
('Antarctica'),
('Asia'),
('Europe'),
('North America'),
('Oceania'),
('South America'),
('Unknown')
ON CONFLICT (name) DO NOTHING;

-- Seed the `currency_code` table
INSERT INTO currency_code (code) VALUES
('CAD'),
('USD')
ON CONFLICT (code) DO NOTHING;

-- Seed the country table
INSERT INTO country (name, continent_id) VALUES
('Burundi', (SELECT id FROM continent WHERE name = 'Africa')),
('Bolivia', (SELECT id FROM continent WHERE name = 'South America')),
('Brazil', (SELECT id FROM continent WHERE name = 'South America')),
('Canada', (SELECT id FROM continent WHERE name = 'North America')),
('Chile', (SELECT id FROM continent WHERE name = 'South America')),
('China', (SELECT id FROM continent WHERE name = 'Asia')),
('Congo', (SELECT id FROM continent WHERE name = 'Africa')),
('Colombia', (SELECT id FROM continent WHERE name = 'South America')),
('Costa Rica', (SELECT id FROM continent WHERE name = 'North America')),
('Ecuador', (SELECT id FROM continent WHERE name = 'South America')),
('Ethiopia', (SELECT id FROM continent WHERE name = 'Africa')),
('United Kingdom', (SELECT id FROM continent WHERE name = 'Europe')),
('Guinea', (SELECT id FROM continent WHERE name = 'Africa')),
('Guatemala', (SELECT id FROM continent WHERE name = 'North America')),
('Honduras', (SELECT id FROM continent WHERE name = 'North America')),
('Indonesia', (SELECT id FROM continent WHERE name = 'Asia')),
('India', (SELECT id FROM continent WHERE name = 'Asia')),
('Kenya', (SELECT id FROM continent WHERE name = 'Africa')),
('Mexico', (SELECT id FROM continent WHERE name = 'North America')),
('Myanmar', (SELECT id FROM continent WHERE name = 'Asia')),
('Nicaragua', (SELECT id FROM continent WHERE name = 'North America')),
('Panama', (SELECT id FROM continent WHERE name = 'North America')),
('Peru', (SELECT id FROM continent WHERE name = 'South America')),
('Philippines', (SELECT id FROM continent WHERE name = 'Asia')),
('Papua New Guinea', (SELECT id FROM continent WHERE name = 'Oceania')),
('Paraguay', (SELECT id FROM continent WHERE name = 'South America')),
('Rwanda', (SELECT id FROM continent WHERE name = 'Africa')),
('El Salvador', (SELECT id FROM continent WHERE name = 'North America')),
('Thailand', (SELECT id FROM continent WHERE name = 'Asia')),
('Tunisia', (SELECT id FROM continent WHERE name = 'Africa')),
('Tanzania', (SELECT id FROM continent WHERE name = 'Africa')),
('United States', (SELECT id FROM continent WHERE name = 'North America')),
('Yemen', (SELECT id FROM continent WHERE name = 'Asia')),
('South Africa', (SELECT id FROM continent WHERE name = 'Africa')),
('Unknown', (SELECT id FROM continent WHERE name = 'Unknown')),
('Multiple', (SELECT id FROM continent WHERE name = 'Unknown'))
ON CONFLICT (name) DO NOTHING;

