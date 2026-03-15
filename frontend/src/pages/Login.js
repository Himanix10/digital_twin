import { signInWithPopup } from "firebase/auth";
import { auth, provider } from "../firebase";

function Login() {

  const loginWithGoogle = async () => {

    try {

      const result = await signInWithPopup(auth, provider);

      const user = result.user;

      console.log("User:", user.email);

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

        <p>Sign in to access the monitoring dashboard</p>

        <button className="googleBtn" onClick={loginWithGoogle}>
          Sign in with Google
        </button>

      </div>

    </div>

  );

}

export default Login;