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