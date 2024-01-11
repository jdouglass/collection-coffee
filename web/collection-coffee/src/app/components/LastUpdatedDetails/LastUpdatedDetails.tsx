import "./last-updated-details.css";

type LastUpdatedDetailsProps = {
  lastUpdatedDateTime: Date;
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
        <div className="last-updated-details-value">
          {lastUpdatedDateTime.toString().replace("T", " ").split(".")[0]}
        </div>
      </div>
      <span
        className={`scraper-indicator ${
          isScraperRunning ? "running" : "stopped"
        }`}
      ></span>
    </div>
  );
};

export default LastUpdatedDetails;
