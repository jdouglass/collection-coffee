import { NextResponse } from "next/server";
import { IQueryParams } from "@/app/lib/interfaces/IQueryParams";
import { pool } from "@/app/lib/db/db";
import { paramToColumnMapping } from "@/app/lib/utils/api/productQueryMappings";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const queryParams: IQueryParams = {};

  url.searchParams.forEach((value, key) => {
    if (Array.isArray(queryParams[key])) {
      (queryParams[key] as string[]).push(value);
    } else if (queryParams[key]) {
      queryParams[key] = [queryParams[key] as string, value];
    } else {
      queryParams[key] = value;
    }
  });

  try {
    const client = await pool.connect();

    let sqlQuery = `
      SELECT
        p.id AS product_id,
        pv.variant_id,
        pv.product_size,
        pv.product_price,
        pv.is_sold_out,
        p.title,
        p.process,
        p.product_url,
        p.image_url,
        p.discovered_date_time,
        p.product_handle,
        p.is_decaf,
        b.name AS brand_name,
        cont.name AS continent_name,
        c.name AS country_name,
        pc.name AS process_category_name,
        ARRAY_AGG(DISTINCT t.name) FILTER (WHERE t.name IS NOT NULL) AS tasting_notes,
        ARRAY_AGG(DISTINCT v.name) FILTER (WHERE v.name IS NOT NULL) AS varieties,
        ven.name AS vendor_name
      FROM product_variant pv
      JOIN product p ON pv.product_id = p.id
      JOIN brand b ON p.brand_id = b.id
      JOIN country c ON p.country_of_origin_id = c.id
      JOIN continent cont ON c.continent_id = cont.id
      JOIN process_category pc ON p.process_category_id = pc.id
      JOIN vendor ven ON p.vendor_id = ven.id
      LEFT JOIN product_to_tasting_note ptn ON p.id = ptn.product_id
      LEFT JOIN tasting_note t ON ptn.tasting_note_id = t.id
      LEFT JOIN product_to_variety ptv ON p.id = ptv.product_id
      LEFT JOIN variety v ON ptv.variety_id = v.id
      WHERE 1=1
    `;

    const conditions: string[] = [];
    const values: (string | number)[] = [];
    let counter = 1;

    // Adjust the SQL query construction to use the mapped column names
    for (const [key, value] of Object.entries(queryParams)) {
      const column = paramToColumnMapping[key];
      if (!column) {
        continue; // Skip if the parameter does not have a corresponding column mapping
      }

      if (Array.isArray(value)) {
        conditions.push(
          `${column} IN (${value
            .map((_, index) => `$${counter + index}`)
            .join(", ")})`
        );
        values.push(...value);
        counter += value.length;
      } else {
        conditions.push(`${column} = $${counter}`);
        values.push(value);
        counter++;
      }
    }

    // Add conditions to the base SQL query
    if (conditions.length > 0) {
      sqlQuery += ` AND ${conditions.join(" AND ")}`;
    }

    // Add the GROUP BY clause
    sqlQuery += `
      GROUP BY
        pv.id,
        p.id,
        b.id,
        c.id,
        cont.id,
        pc.id,
        ven.id
    `;

    const { rows } = await client.query(sqlQuery, values);

    client.release();

    return NextResponse.json(rows);
  } catch (error) {
    console.error("Database query failed:", error);
    return NextResponse.json(
      { error: "Failed to fetch products" },
      { status: 500 }
    );
  }
}
