import ScraperStatus from "../ScraperStatus/ScraperStatus";
import "./last-updated-details.css";

type LastUpdatedDetailsProps = {
  lastUpdatedDateTime: Date;
  isScraperRunning: boolean;
};

const LastUpdatedDetails = ({
  lastUpdatedDateTime,
  isScraperRunning,
}: LastUpdatedDetailsProps) => {
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
  return (
    <div className="last-updated-details-container">
      <div className="last-updated-details">
        Last Updated:&nbsp;
        <div className="last-updated-details-value">{formattedDate}</div>
      </div>
      <ScraperStatus lastUpdatedDateTime={lastUpdatedDateTime} />
    </div>
  );
};

export default LastUpdatedDetails;
