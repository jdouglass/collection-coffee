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
  const formattedDate = localDate.toLocaleString();
  return (
    <div className="last-updated-details-container">
      <div className="last-updated-details">
        Last Updated:&nbsp;
        <div className="last-updated-details-value">{formattedDate}</div>
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
