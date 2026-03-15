import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import { FaCog } from "react-icons/fa";
import "../styles/dashboard.css";

function Settings() {
  return (
    <div className="layout">
      <Sidebar />
      <div className="main">
        <Header />
        <div className="content">
          <div className="pageHeader">
            <h1>Settings</h1>
            <p>System configuration and preferences</p>
          </div>
          <div className="emptyState">
            <FaCog style={{ fontSize: 28, color: "var(--text-muted)" }} />
            <p>System configuration panel — coming soon</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;