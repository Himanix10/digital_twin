import { useState } from "react";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import { auth } from "../firebase";
import { signOut } from "firebase/auth";
import "../styles/dashboard.css";

function Settings() {
  const user = auth.currentUser;
  const [tab, setTab] = useState("profile");

  const [smoothChart, setSmoothChart] = useState(
    JSON.parse(localStorage.getItem("smoothChart")) || false
  );

  const [notifications, setNotifications] = useState(
    JSON.parse(localStorage.getItem("notifications")) || true
  );

  const toggleSmooth = () => {
    const value = !smoothChart;
    setSmoothChart(value);
    localStorage.setItem("smoothChart", JSON.stringify(value));
  };

  const toggleNotifications = () => {
    const value = !notifications;
    setNotifications(value);
    localStorage.setItem("notifications", JSON.stringify(value));
  };

  const resetSystem = () => {
    localStorage.clear();
    window.location.reload();
  };

  const logout = async () => {
    await signOut(auth);
    window.location.reload();
  };

  return (
    <div className="layout">
      <Sidebar />

      <div className="main">
        <Header />

        <div className="content">

          <div className="pageHeader">
            <h1>Settings</h1>
            <p>Manage account and system preferences</p>
          </div>

          {/* Tabs */}
          <div className="settingsTabs">
            <button
              className={tab === "profile" ? "activeTab" : ""}
              onClick={() => setTab("profile")}
            >
              Profile
            </button>
            <button
              className={tab === "toggle" ? "activeTab" : ""}
              onClick={() => setTab("toggle")}
            >
              Preferences
            </button>
            <button
              className={tab === "reset" ? "activeTab" : ""}
              onClick={() => setTab("reset")}
            >
              Reset
            </button>
          </div>

          {/* PROFILE TAB */}
          {tab === "profile" && (
            <div className="settingsPanel">

              <img
                src={user?.photoURL || `https://ui-avatars.com/api/?name=${encodeURIComponent(user?.displayName || "User")}&background=0a1628&color=00c8ff&size=100&bold=true`}
                alt="avatar"
                className="settingsAvatar"
              />

              <h3>{user?.displayName}</h3>
              <p>{user?.email}</p>
              <p className="settingsMeta">Logged in via Google Authentication</p>

              <button
                className="logoutBtn"
                onClick={logout}
                style={{ marginTop: 24 }}
              >
                Logout
              </button>

            </div>
          )}

          {/* TOGGLE TAB */}
          {tab === "toggle" && (
            <div className="settingsPanel">

              <div className="toggleRow">
                <span>Chart Smoothing</span>
                <input
                  type="checkbox"
                  checked={smoothChart}
                  onChange={toggleSmooth}
                />
              </div>

              <div className="toggleRow">
                <span>System Notifications</span>
                <input
                  type="checkbox"
                  checked={notifications}
                  onChange={toggleNotifications}
                />
              </div>

            </div>
          )}

          {/* RESET TAB */}
          {tab === "reset" && (
            <div className="settingsPanel">

              <p className="settingsWarning">
                Reset will clear stored preferences and cached session data.
              </p>

              <button className="primaryBtn" onClick={resetSystem}>
                Reset System
              </button>

            </div>
          )}

        </div>
      </div>
    </div>
  );
}

export default Settings;