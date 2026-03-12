import { NavLink } from "react-router-dom";
import {
  FaChartLine,
  FaBrain,
  FaFileAlt,
  FaCog,
  FaMicrochip
} from "react-icons/fa";

import "../styles/dashboard.css";

function Sidebar() {

  return (

    <div className="sidebar">

      <div className="logo">

        <FaMicrochip className="logoIcon" />
        <span>Hybrid Twin</span>

      </div>

      <div className="menu">

        <NavLink
          to="/"
          className={({ isActive }) =>
            isActive ? "menuItem active" : "menuItem"
          }
        >
          <FaChartLine className="icon" />
          Dashboard
        </NavLink>


        <NavLink
          to="/models"
          className={({ isActive }) =>
            isActive ? "menuItem active" : "menuItem"
          }
        >
          <FaBrain className="icon" />
          Models
        </NavLink>


        <NavLink
          to="/reports"
          className={({ isActive }) =>
            isActive ? "menuItem active" : "menuItem"
          }
        >
          <FaFileAlt className="icon" />
          Reports
        </NavLink>


        <NavLink
          to="/settings"
          className={({ isActive }) =>
            isActive ? "menuItem active" : "menuItem"
          }
        >
          <FaCog className="icon" />
          Settings
        </NavLink>

      </div>


      <div className="sidebarFooter">

        <div className="statusDot"></div>

        <span>System Online</span>

      </div>

    </div>

  );
}

export default Sidebar;