DROP POLICY IF EXISTS "Enable select access for anon users" ON product_to_variety;
DROP POLICY IF EXISTS "Enable insert access for all authenticated users" ON product_to_variety;
DROP POLICY IF EXISTS "Enable update access for all authenticated users" ON product_to_variety;
DROP POLICY IF EXISTS "Enable delete access for all authenticated users" ON product_to_variety;
DROP POLICY IF EXISTS "Enable select access for anon users" ON product_to_tasting_note;
DROP POLICY IF EXISTS "Enable insert access for all authenticated users" ON product_to_tasting_note;
DROP POLICY IF EXISTS "Enable update access for all authenticated users" ON product_to_tasting_note;
DROP POLICY IF EXISTS "Enable delete access for all authenticated users" ON product_to_tasting_note;

CREATE POLICY "Enable select access for anon users" ON product_to_variety AS PERMISSIVE FOR SELECT TO anon USING (true);
CREATE POLICY "Enable insert access for all authenticated users" ON product_to_variety AS PERMISSIVE FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Enable update access for all authenticated users" ON product_to_variety AS PERMISSIVE FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Enable delete access for all authenticated users" ON product_to_variety AS PERMISSIVE FOR DELETE TO authenticated USING (true);
CREATE POLICY "Enable select access for anon users" ON product_to_tasting_note AS PERMISSIVE FOR SELECT TO anon USING (true);
CREATE POLICY "Enable insert access for all authenticated users" ON product_to_tasting_note AS PERMISSIVE FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Enable update access for all authenticated users" ON product_to_tasting_note AS PERMISSIVE FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Enable delete access for all authenticated users" ON product_to_tasting_note AS PERMISSIVE FOR DELETE TO authenticated USING (true);
