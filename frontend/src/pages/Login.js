import { signInWithPopup } from "firebase/auth";
import { auth, provider } from "../firebase";
import "../styles/login.css";

function Login() {

  const loginWithGoogle = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      const user = result.user;
      localStorage.setItem("user", JSON.stringify(user));
      window.location.href = "/";
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="loginPage">
      <div className="loginCard">

        <h1>Hybrid Digital Twin</h1>
        <p>AI-Powered System Monitoring Platform</p>

        <button className="googleLoginBtn" onClick={loginWithGoogle}>
          <img
            src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
            alt="google"
          />
          Sign in with Google
        </button>

      </div>
    </div>
  );
}

export default Login;