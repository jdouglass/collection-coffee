import { pool } from "@/app/lib/db/db";
import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const client = await pool.connect();

    const systemStatusQuery = `
      SELECT v.name, r.start_time, r.end_time
      FROM runtime r
      JOIN vendor v ON r.vendor_id = v.id
      WHERE r.end_time IS NOT NULL;
    `;

    const systemStatus = (await client.query(systemStatusQuery)).rows;

    client.release();

    return NextResponse.json({
      systemStatus,
    });
  } catch (error) {
    console.error("Database query failed:", error);
    return NextResponse.json(
      { error: "Failed to fetch system status data" },
      { status: 500 }
    );
  }
}
