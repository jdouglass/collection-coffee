DROP POLICY IF EXISTS "Admin privileges for authenticated users 16wiy3a_1" ON "storage"."objects";
DROP POLICY IF EXISTS "Admin privileges for authenticated users 16wiy3a_2" ON "storage"."objects";
DROP POLICY IF EXISTS "Admin privileges for authenticated users 16wiy3a_3" ON "storage"."objects";
DROP POLICY IF EXISTS "Anon users allowed to read all files 16wiy3a_0" ON "storage"."objects";

create policy "Admin privileges for authenticated users 16wiy3a_1"
on "storage"."objects"
as permissive
for insert
to authenticated
with check ((bucket_id = 'product-images'::text));


create policy "Admin privileges for authenticated users 16wiy3a_2"
on "storage"."objects"
as permissive
for update
to authenticated
using ((bucket_id = 'product-images'::text));


create policy "Admin privileges for authenticated users 16wiy3a_3"
on "storage"."objects"
as permissive
for delete
to authenticated
using ((bucket_id = 'product-images'::text));


create policy "Anon users allowed to read all files 16wiy3a_0"
on "storage"."objects"
as permissive
for select
to anon
using ((bucket_id = 'product-images'::text));



