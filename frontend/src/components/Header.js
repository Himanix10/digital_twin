import "../styles/dashboard.css";

function Header() {
  const now = new Date();
  const timeStr = now.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  const dateStr = now.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" }).toUpperCase();

  return (
    <div className="header">
      <div className="headerLeft">
        <span className="headerLabel">System</span>
        <h1>Hybrid Digital Twin Monitoring</h1>
      </div>
      <div className="headerRight">
        <span className="headerDate">{dateStr}</span>
        <div className="user">
          <div className="statusIndicator"></div>
          System Active
        </div>
      </div>
    </div>
  );
}

export default Header;