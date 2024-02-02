import "./last-updated-details.css";

type LastUpdatedDetailsProps = {
  lastUpdatedDateTime: string;
  isScraperRunning: boolean;
};

const LastUpdatedDetails = ({
  lastUpdatedDateTime,
  isScraperRunning,
}: LastUpdatedDetailsProps) => {
  return (
    <div className="last-updated-details-container">
      <div className="last-updated-details">
        Last Updated:&nbsp;
        <div className="last-updated-details-value">{lastUpdatedDateTime}</div>
      </div>
      <span
        className={`scraper-indicator ${isScraperRunning ? "running" : ""}`}
      ></span>
    </div>
  );
};

export default LastUpdatedDetails;
