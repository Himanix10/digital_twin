import { NavLink } from "react-router-dom";
import {
  FaChartLine,
  FaBrain,
  FaFileAlt,
  FaCog,
  FaMicrochip,
} from "react-icons/fa";
import "../styles/dashboard.css";

const navItems = [
  { to: "/",        icon: FaChartLine, label: "Dashboard" },
  { to: "/models",  icon: FaBrain,     label: "Models"    },
  { to: "/reports", icon: FaFileAlt,   label: "Reports"   },
  { to: "/settings",icon: FaCog,       label: "Settings"  },
];

function Sidebar() {
  return (
    <div className="sidebar">
      <div className="logo">
        <FaMicrochip className="logoIcon" />
        <span>Hybrid Twin</span>
      </div>

      <p className="menuLabel">Navigation</p>

      <div className="menu">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/"}
            className={({ isActive }) => `menuItem${isActive ? " active" : ""}`}
          >
            <Icon className="icon" />
            {label}
          </NavLink>
        ))}
      </div>

      <div className="sidebarFooter">
        <div className="statusDot"></div>
        <span>All systems online</span>
      </div>
    </div>
  );
}

export default Sidebar;