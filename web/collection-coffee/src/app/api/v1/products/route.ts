import { NextResponse } from "next/server";
import { IQueryParams } from "@/app/lib/interfaces/IQueryParams";
import { pool } from "@/app/lib/db/db";
import { paramToColumnMapping } from "@/app/lib/utils/api/productQueryMappings";
import { IProductResponse } from "@/app/lib/interfaces/IProductResponse";
import { SORT_OPTIONS } from "@/app/lib/enums/sortOptions";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const queryParams: IQueryParams = {};

  const page = parseInt(url.searchParams.get("page") || "1", 10);
  const perPage = 12;
  const offset = (page - 1) * perPage;

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

    let baseQuery = `
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
      baseQuery += ` AND ${conditions.join(" AND ")}`;
    }

    // Query for total count
    const countQuery = `SELECT COUNT(DISTINCT pv.id) ${baseQuery}`;
    const countResult = await client.query(countQuery, values);
    const totalCount = countResult.rows[0].count;

    // Query for paginated results
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
      ${baseQuery}
    `;

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

    // Add sorting
    sqlQuery +=
      queryParams.sort === SORT_OPTIONS.NEWEST
        ? `
          ORDER BY p.discovered_date_time DESC, pv.id ASC
          `
        : queryParams.sort === SORT_OPTIONS.OLDEST
        ? `
          ORDER BY p.discovered_date_time ASC, pv.id ASC
          `
        : queryParams.sort === SORT_OPTIONS.ASCENDING
        ? `
          ORDER BY pv.product_price ASC, pv.id ASC
          `
        : queryParams.sort === SORT_OPTIONS.DESCENDING
        ? `
        ORDER BY pv.product_price DESC, pv.id ASC
        `
        : `
        ORDER BY p.discovered_date_time DESC, pv.id ASC
        `;

    // Add LIMIT and OFFSET for pagination
    sqlQuery += ` LIMIT $${counter} OFFSET $${counter + 1}`;
    values.push(perPage, offset);

    const { rows } = await client.query(sqlQuery, values);

    const products: IProductResponse[] = rows.map((row) => ({
      productId: row.product_id,
      variantId: parseInt(row.variant_id),
      productSize: row.product_size,
      productPrice: row.product_price,
      isSoldOut: row.is_sold_out,
      title: row.title,
      process: row.process,
      productUrl: row.product_url,
      imageUrl: row.image_url,
      discoveredDateTime: row.discovered_date_time,
      productHandle: row.product_handle,
      isDecaf: row.is_decaf,
      brand: row.brand_name,
      continent: row.continent_name,
      country: row.country_name,
      processCategory: row.process_category_name,
      tastingNotes: row.tasting_notes,
      varieties: row.varieties,
      vendor: row.vendor_name,
    }));

    client.release();

    return NextResponse.json({ products, totalCount });
  } catch (error) {
    console.error("Database query failed:", error);
    return NextResponse.json(
      { error: "Failed to fetch products" },
      { status: 500 }
    );
  }
}
