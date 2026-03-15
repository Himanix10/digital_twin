import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import { FaFileAlt } from "react-icons/fa";
import "../styles/dashboard.css";

function Reports() {
  return (
    <div className="layout">
      <Sidebar />
      <div className="main">
        <Header />
        <div className="content">
          <div className="pageHeader">
            <h1>Reports</h1>
            <p>Download analytics and export session data</p>
          </div>
          <div className="emptyState">
            <FaFileAlt style={{ fontSize: 28, color: "var(--text-muted)" }} />
            <p>Report generation panel — coming soon</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Reports;