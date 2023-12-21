DROP POLICY IF EXISTS "Enable select access for anon users" on runtime;

-- Create SELECT (READ) policy for anon users on all tables
CREATE POLICY "Enable select access for anon users" ON runtime AS PERMISSIVE FOR SELECT TO anon USING (true);


DROP POLICY IF EXISTS "Enable insert access for all authenticated users" on runtime;


-- Create policies for INSERT
-- (The USING clause is not typically used with INSERT, so we use WITH CHECK instead)
CREATE POLICY "Enable insert access for all authenticated users" ON runtime AS PERMISSIVE FOR INSERT TO authenticated WITH CHECK (true);


DROP POLICY IF EXISTS "Enable update access for all authenticated users" on runtime;


-- Create policies for UPDATE
CREATE POLICY "Enable update access for all authenticated users" ON runtime AS PERMISSIVE FOR UPDATE TO authenticated USING (true);


DROP POLICY IF EXISTS "Enable delete access for all authenticated users" on runtime;


-- Create policies for DELETE
CREATE POLICY "Enable delete access for all authenticated users" ON runtime AS PERMISSIVE FOR DELETE TO authenticated USING (true);
