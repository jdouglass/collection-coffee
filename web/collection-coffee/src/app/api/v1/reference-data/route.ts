import { pool } from "@/app/lib/db/db";
import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const client = await pool.connect();

    const brandsQuery = "SELECT name FROM brand ORDER BY name ASC";
    const vendorsQuery = "SELECT name FROM vendor ORDER BY name ASC";
    const tastingNotesQuery = "SELECT name FROM tasting_note ORDER BY name ASC";
    const varietiesQuery = "SELECT name FROM variety ORDER BY name ASC";
    const continentsQuery = "SELECT name FROM continent ORDER BY name ASC";
    const countriesQuery =
      "SELECT name, continent_id FROM country ORDER BY name ASC";
    const processCategoriesQuery =
      "SELECT name FROM process_category ORDER BY name ASC";

    const brands = (await client.query(brandsQuery)).rows.map(
      (row) => row.name
    );
    const vendors = (await client.query(vendorsQuery)).rows.map(
      (row) => row.name
    );
    const tastingNotes = (await client.query(tastingNotesQuery)).rows.map(
      (row) => row.name
    );
    const varieties = (await client.query(varietiesQuery)).rows.map(
      (row) => row.name
    );
    const continents = (await client.query(continentsQuery)).rows.map(
      (row) => row.name
    );
    const countries = (await client.query(countriesQuery)).rows.map(
      (row) => row.name
    );
    const processCategories = (
      await client.query(processCategoriesQuery)
    ).rows.map((row) => row.name);

    client.release();

    return NextResponse.json({
      brands,
      vendors,
      tastingNotes,
      varieties,
      continents,
      countries,
      processCategories,
    });
  } catch (error) {
    console.error("Database query failed:", error);
    return NextResponse.json(
      { error: "Failed to fetch reference data" },
      { status: 500 }
    );
  }
}
