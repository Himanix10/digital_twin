import "../styles/dashboard.css";

function MetricCard({ title, value, unit = "", accent = "cyan" }) {
  return (
    <div className={`metricCard metricCard--${accent}`}>
      <h4>{title}</h4>
      <h2>
        {value}
        {unit && <span className="metricUnit">{unit}</span>}
      </h2>
    </div>
  );
}

export default MetricCard;