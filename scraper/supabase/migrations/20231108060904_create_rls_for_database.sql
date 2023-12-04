DROP POLICY IF EXISTS "Enable select access for anon users" on brand;
DROP POLICY IF EXISTS "Enable select access for anon users" on continent;
DROP POLICY IF EXISTS "Enable select access for anon users" on currency_code;
DROP POLICY IF EXISTS "Enable select access for anon users" on process_category;
DROP POLICY IF EXISTS "Enable select access for anon users" on product_type;
DROP POLICY IF EXISTS "Enable select access for anon users" on tasting_note;
DROP POLICY IF EXISTS "Enable select access for anon users" on variety;
DROP POLICY IF EXISTS "Enable select access for anon users" on tasting_note;
DROP POLICY IF EXISTS "Enable select access for anon users" on variety;
DROP POLICY IF EXISTS "Enable select access for anon users" on country;
DROP POLICY IF EXISTS "Enable select access for anon users" on vendor;
DROP POLICY IF EXISTS "Enable select access for anon users" on product;
DROP POLICY IF EXISTS "Enable select access for anon users" on product_variant;

-- Create SELECT (READ) policy for anon users on all tables
CREATE POLICY "Enable select access for anon users" ON brand AS PERMISSIVE FOR SELECT TO anon USING (true);
CREATE POLICY "Enable select access for anon users" ON continent AS PERMISSIVE FOR SELECT TO anon USING (true);
CREATE POLICY "Enable select access for anon users" ON currency_code AS PERMISSIVE FOR SELECT TO anon USING (true);
CREATE POLICY "Enable select access for anon users" ON process_category AS PERMISSIVE FOR SELECT TO anon USING (true);
CREATE POLICY "Enable select access for anon users" ON product_type AS PERMISSIVE FOR SELECT TO anon USING (true);
CREATE POLICY "Enable select access for anon users" ON tasting_note AS PERMISSIVE FOR SELECT TO anon USING (true);
CREATE POLICY "Enable select access for anon users" ON variety AS PERMISSIVE FOR SELECT TO anon USING (true);
CREATE POLICY "Enable select access for anon users" ON country AS PERMISSIVE FOR SELECT TO anon USING (true);
CREATE POLICY "Enable select access for anon users" ON vendor AS PERMISSIVE FOR SELECT TO anon USING (true);
CREATE POLICY "Enable select access for anon users" ON product AS PERMISSIVE FOR SELECT TO anon USING (true);
CREATE POLICY "Enable select access for anon users" ON product_variant AS PERMISSIVE FOR SELECT TO anon USING (true);

DROP POLICY IF EXISTS "Enable insert access for all authenticated users" on brand;
DROP POLICY IF EXISTS "Enable insert access for all authenticated users" on continent;
DROP POLICY IF EXISTS "Enable insert access for all authenticated users" on currency_code;
DROP POLICY IF EXISTS "Enable insert access for all authenticated users" on process_category;
DROP POLICY IF EXISTS "Enable insert access for all authenticated users" on product_type;
DROP POLICY IF EXISTS "Enable insert access for all authenticated users" on tasting_note;
DROP POLICY IF EXISTS "Enable insert access for all authenticated users" on variety;
DROP POLICY IF EXISTS "Enable insert access for all authenticated users" on tasting_note;
DROP POLICY IF EXISTS "Enable insert access for all authenticated users" on variety;
DROP POLICY IF EXISTS "Enable insert access for all authenticated users" on country;
DROP POLICY IF EXISTS "Enable insert access for all authenticated users" on vendor;
DROP POLICY IF EXISTS "Enable insert access for all authenticated users" on product;
DROP POLICY IF EXISTS "Enable insert access for all authenticated users" on product_variant;

-- Create policies for INSERT
-- (The USING clause is not typically used with INSERT, so we use WITH CHECK instead)
CREATE POLICY "Enable insert access for all authenticated users" ON brand AS PERMISSIVE FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Enable insert access for all authenticated users" ON continent AS PERMISSIVE FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Enable insert access for all authenticated users" ON currency_code AS PERMISSIVE FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Enable insert access for all authenticated users" ON process_category AS PERMISSIVE FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Enable insert access for all authenticated users" ON product_type AS PERMISSIVE FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Enable insert access for all authenticated users" ON tasting_note AS PERMISSIVE FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Enable insert access for all authenticated users" ON variety AS PERMISSIVE FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Enable insert access for all authenticated users" ON country AS PERMISSIVE FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Enable insert access for all authenticated users" ON vendor AS PERMISSIVE FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Enable insert access for all authenticated users" ON product AS PERMISSIVE FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Enable insert access for all authenticated users" ON product_variant AS PERMISSIVE FOR INSERT TO authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "Enable update access for all authenticated users" on brand;
DROP POLICY IF EXISTS "Enable update access for all authenticated users" on continent;
DROP POLICY IF EXISTS "Enable update access for all authenticated users" on currency_code;
DROP POLICY IF EXISTS "Enable update access for all authenticated users" on process_category;
DROP POLICY IF EXISTS "Enable update access for all authenticated users" on product_type;
DROP POLICY IF EXISTS "Enable update access for all authenticated users" on tasting_note;
DROP POLICY IF EXISTS "Enable update access for all authenticated users" on variety;
DROP POLICY IF EXISTS "Enable update access for all authenticated users" on tasting_note;
DROP POLICY IF EXISTS "Enable update access for all authenticated users" on variety;
DROP POLICY IF EXISTS "Enable update access for all authenticated users" on country;
DROP POLICY IF EXISTS "Enable update access for all authenticated users" on vendor;
DROP POLICY IF EXISTS "Enable update access for all authenticated users" on product;
DROP POLICY IF EXISTS "Enable update access for all authenticated users" on product_variant;

-- Create policies for UPDATE
CREATE POLICY "Enable update access for all authenticated users" ON brand AS PERMISSIVE FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Enable update access for all authenticated users" ON continent AS PERMISSIVE FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Enable update access for all authenticated users" ON currency_code AS PERMISSIVE FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Enable update access for all authenticated users" ON process_category AS PERMISSIVE FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Enable update access for all authenticated users" ON product_type AS PERMISSIVE FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Enable update access for all authenticated users" ON tasting_note AS PERMISSIVE FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Enable update access for all authenticated users" ON variety AS PERMISSIVE FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Enable update access for all authenticated users" ON country AS PERMISSIVE FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Enable update access for all authenticated users" ON vendor AS PERMISSIVE FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Enable update access for all authenticated users" ON product AS PERMISSIVE FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Enable update access for all authenticated users" ON product_variant AS PERMISSIVE FOR UPDATE TO authenticated USING (true);

DROP POLICY IF EXISTS "Enable delete access for all authenticated users" on brand;
DROP POLICY IF EXISTS "Enable delete access for all authenticated users" on continent;
DROP POLICY IF EXISTS "Enable delete access for all authenticated users" on currency_code;
DROP POLICY IF EXISTS "Enable delete access for all authenticated users" on process_category;
DROP POLICY IF EXISTS "Enable delete access for all authenticated users" on product_type;
DROP POLICY IF EXISTS "Enable delete access for all authenticated users" on tasting_note;
DROP POLICY IF EXISTS "Enable delete access for all authenticated users" on variety;
DROP POLICY IF EXISTS "Enable delete access for all authenticated users" on tasting_note;
DROP POLICY IF EXISTS "Enable delete access for all authenticated users" on variety;
DROP POLICY IF EXISTS "Enable delete access for all authenticated users" on country;
DROP POLICY IF EXISTS "Enable delete access for all authenticated users" on vendor;
DROP POLICY IF EXISTS "Enable delete access for all authenticated users" on product;
DROP POLICY IF EXISTS "Enable delete access for all authenticated users" on product_variant;

-- Create policies for DELETE
CREATE POLICY "Enable delete access for all authenticated users" ON brand AS PERMISSIVE FOR DELETE TO authenticated USING (true);
CREATE POLICY "Enable delete access for all authenticated users" ON continent AS PERMISSIVE FOR DELETE TO authenticated USING (true);
CREATE POLICY "Enable delete access for all authenticated users" ON currency_code AS PERMISSIVE FOR DELETE TO authenticated USING (true);
CREATE POLICY "Enable delete access for all authenticated users" ON process_category AS PERMISSIVE FOR DELETE TO authenticated USING (true);
CREATE POLICY "Enable delete access for all authenticated users" ON product_type AS PERMISSIVE FOR DELETE TO authenticated USING (true);
CREATE POLICY "Enable delete access for all authenticated users" ON tasting_note AS PERMISSIVE FOR DELETE TO authenticated USING (true);
CREATE POLICY "Enable delete access for all authenticated users" ON variety AS PERMISSIVE FOR DELETE TO authenticated USING (true);
CREATE POLICY "Enable delete access for all authenticated users" ON country AS PERMISSIVE FOR DELETE TO authenticated USING (true);
CREATE POLICY "Enable delete access for all authenticated users" ON vendor AS PERMISSIVE FOR DELETE TO authenticated USING (true);
CREATE POLICY "Enable delete access for all authenticated users" ON product AS PERMISSIVE FOR DELETE TO authenticated USING (true);
CREATE POLICY "Enable delete access for all authenticated users" ON product_variant AS PERMISSIVE FOR DELETE TO authenticated USING (true);