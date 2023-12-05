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

  console.log(queryParams);

  try {
    const client = await pool.connect();

    let sqlQuery = "";
    const conditions = [];
    const values: string | any[] | undefined = [];
    let counter = 1;

    if (Object.keys(queryParams).length === 0) {
      // No query params, get counts for each unique value in filters
      sqlQuery = `
        SELECT
          'brand' AS filter_type,
          b.name AS name,
          COUNT(DISTINCT p.id) AS count
        FROM product p
        JOIN brand b ON p.brand_id = b.id
        GROUP BY b.name

        UNION ALL

        SELECT
          'continent' AS filter_type,
          cont.name AS name,
          COUNT(DISTINCT p.id) AS count
        FROM product p
        JOIN country c ON p.country_of_origin_id = c.id
        JOIN continent cont ON c.continent_id = cont.id
        GROUP BY cont.name

        UNION ALL

        SELECT
          'country' AS filter_type,
          c.name AS name,
          COUNT(DISTINCT p.id) AS count
        FROM product p
        JOIN country c ON p.country_of_origin_id = c.id
        GROUP BY c.name

        UNION ALL

        SELECT
          'process_category' AS filter_type,
          pc.name AS name,
          COUNT(DISTINCT p.id) AS count
        FROM product p
        JOIN process_category pc ON p.process_category_id = pc.id
        GROUP BY pc.name

        
      `;
    } else {
      let joinClauses = `
        FROM product p
        JOIN brand b ON p.brand_id = b.id
        JOIN country c ON p.country_of_origin_id = c.id
        JOIN process_category pc ON p.process_category_id = pc.id
        JOIN product_variant pv ON p.id = pv.product_id
      `;

      if (queryParams.brand) {
        conditions.push(`b.name = $${counter}`);
        values.push(queryParams.brand);
        counter++;
      }
      if (queryParams.continent) {
        conditions.push(`c.name = $${counter}`);
        values.push(queryParams.continent);
        counter++;
      }
      if (queryParams.country) {
        conditions.push(`p.country_of_origin_id = $${counter}`);
        values.push(queryParams.country);
        counter++;
      }
      if (queryParams.processCategory) {
        conditions.push(`pc.name = $${counter}`);
        values.push(queryParams.processCategory);
        counter++;
      }
      // Add similar conditions for other filters like 'tastingNote', 'variety', etc.

      sqlQuery = `
        SELECT COUNT(DISTINCT p.id) AS product_count
        ${joinClauses}
        WHERE ${conditions.length > 0 ? conditions.join(" AND ") : "1=1"}
      `;
    }

    const { rows } = await client.query(
      sqlQuery,
      values.length > 0 ? values : undefined
    );

    // Process rows into the desired structure
    const filterCounts = rows.reduce((acc, row) => {
      if (!acc[row.filter_type]) {
        acc[row.filter_type] = [];
      }
      acc[row.filter_type].push({
        name: row.name,
        count: row.count,
      });
      return acc;
    }, {});

    client.release();

    return NextResponse.json(filterCounts);
  } catch (error) {
    console.error("Database query failed:", error);
    return NextResponse.json(
      { error: "Failed to fetch attribute counts" },
      { status: 500 }
    );
  }
}
