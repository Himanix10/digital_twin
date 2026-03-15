import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import { FaBrain } from "react-icons/fa";
import "../styles/dashboard.css";

function Models() {
  return (
    <div className="layout">
      <Sidebar />
      <div className="main">
        <Header />
        <div className="content">
          <div className="pageHeader">
            <h1>AI Models</h1>
            <p>Model configuration and performance comparison</p>
          </div>
          <div className="emptyState">
            <FaBrain style={{ fontSize: 28, color: "var(--text-muted)" }} />
            <p>Model configuration panel — coming soon</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Models;