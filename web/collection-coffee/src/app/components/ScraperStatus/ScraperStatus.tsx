"use client";

import useSWR from "swr";
import { useEffect, useState } from "react";
import { ILastUpdatedResponse } from "@/app/lib/interfaces/ILastUpdatedResponse";
import RefreshIcon from "../../../../public/refreshIcon.svg";
import "./scraper-status.css";

const fetcher = (
  ...args: [input: RequestInfo, init?: RequestInit | undefined]
) => fetch(...args).then((res) => res.json() as Promise<ILastUpdatedResponse>);

const ScraperStatus = () => {
  const [showRefreshPrompt, setShowRefreshPrompt] = useState(false);
  const { data, error } = useSWR<ILastUpdatedResponse, Error>(
    "/api/v1/last-updated",
    fetcher,
    {
      refreshInterval: 5000,
    }
  );

  useEffect(() => {
    // This effect handles showing the refresh prompt based on the scraper's status and sessionStorage
    if (data) {
      const refreshPromptShown = sessionStorage.getItem("refreshPromptShown");

      if (data.isScraperRunning) {
        // If scraper starts running, ensure prompt is not shown and sessionStorage is cleared
        if (refreshPromptShown) {
          sessionStorage.removeItem("refreshPromptShown");
          setShowRefreshPrompt(false);
        }
      } else if (!refreshPromptShown) {
        // Show prompt only if scraper is not running and the prompt has not been shown
        setShowRefreshPrompt(true);
        sessionStorage.setItem("refreshPromptShown", "true");
      }
    }
  }, [data]); // Dependency on data ensures this effect runs only when data changes

  if (error) return <div>Failed to load scraper status</div>;
  if (!data) return <div>&nbsp;Loading...</div>;

  return (
    <>
      {data.isScraperRunning && (
        <span className={"scraper-indicator running"}></span>
      )}
      {!data.isScraperRunning && showRefreshPrompt && (
        <span className="scraper-completed">
          <a href="#" onClick={() => window.location.reload()}>
            <RefreshIcon className="refresh-icon" />
            &nbsp;Reload
          </a>
        </span>
      )}
    </>
  );
};

export default ScraperStatus;
