CREATE TABLE product_to_tasting_note (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES product(id),
    tasting_note_id INTEGER NOT NULL REFERENCES tasting_note(id)
);

CREATE INDEX idx_product_to_tasting_note_product ON product_to_tasting_note(product_id);
CREATE INDEX idx_product_to_tasting_note_tasting_note ON product_to_tasting_note(tasting_note_id);

CREATE TABLE product_to_variety (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES product(id),
    variety_id INTEGER NOT NULL REFERENCES variety(id)
);

CREATE INDEX idx_product_to_variety_product ON product_to_variety(product_id);
CREATE INDEX idx_product_to_variety_variety ON product_to_variety(variety_id);
