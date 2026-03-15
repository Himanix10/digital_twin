import "../styles/dashboard.css";
import { auth } from "../firebase";

function Header() {
  const now     = new Date();
  const dateStr = now.toLocaleDateString("en-GB", {
    day: "2-digit", month: "short", year: "numeric"
  }).toUpperCase();

  const user = auth.currentUser;

  const hour = now.getHours();
  const greeting =
    hour < 12 ? "Good Morning" :
    hour < 18 ? "Good Afternoon" :
                "Good Evening";

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
          {user
            ? `${greeting}, ${user.displayName || user.email}`
            : "System Active"}
        </div>
      </div>
    </div>
  );
}

export default Header;