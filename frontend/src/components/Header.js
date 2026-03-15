import "../styles/dashboard.css";
import { auth } from "../firebase";
import { signOut } from "firebase/auth";

const logout = async () => {
  await signOut(auth);
  window.location.reload();
};

function Header() {
  const now     = new Date();
  const dateStr = now.toLocaleDateString("en-GB", {
    day: "2-digit", month: "short", year: "numeric"
  }).toUpperCase();

  const user = auth.currentUser;

  return (
    <div className="header">
      <div className="headerLeft">
        <span className="headerLabel">System</span>
        <h1>Hybrid Digital Twin Monitoring</h1>
      </div>
      <div className="headerRight">
        <span className="headerDate">{dateStr}</span>
        {user && (
          <span className="headerEmail">{user.email}</span>
        )}
        <div className="user">
          <div className="statusIndicator"></div>
          System Active
        </div>
        <button className="logoutBtn" onClick={logout}>
          Logout
        </button>
      </div>
    </div>
  );
}

export default Header;