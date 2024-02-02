import { pool } from "@/app/lib/db/db";
import { NextResponse } from "next/server";

interface LastUpdatedResponse {
  start_time: Date;
  end_time: Date;
}

export async function GET() {
  try {
    const client = await pool.connect();

    const lastUpdatedQuery = `
      SELECT r.start_time, r.end_time
      FROM runtime r
      JOIN vendor v ON r.vendor_id = v.id
      WHERE r.end_time IS NOT NULL;
    `;

    const runtimes: LastUpdatedResponse[] = (
      await client.query(lastUpdatedQuery)
    ).rows;

    const lastUpdatedDateTime = runtimes.reduce((a, b) =>
      a.end_time > b.end_time ? a : b
    ).end_time;

    const localDate = new Date(lastUpdatedDateTime);
    const options: Intl.DateTimeFormatOptions = {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "numeric",
      minute: "2-digit",
      second: "2-digit",
      hour12: true,
    };
    const formattedDate = localDate.toLocaleString("en-US", options);

    const isScraperRunning = runtimes.some(
      (runtime) => runtime.start_time > runtime.end_time
    );

    client.release();

    return NextResponse.json({
      lastUpdatedDateTime: formattedDate,
      isScraperRunning,
    });
  } catch (error) {
    console.error("Database query failed:", error);
    return NextResponse.json(
      { error: "Failed to fetch system status data" },
      { status: 500 }
    );
  }
}
