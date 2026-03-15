// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBV9yZi7EH6kK62RaizKMYyQ1Vof4TEfqg",
  authDomain: "digital-twin-6298a.firebaseapp.com",
  projectId: "digital-twin-6298a",
  storageBucket: "digital-twin-6298a.firebasestorage.app",
  messagingSenderId: "909695210609",
  appId: "1:909695210609:web:db6abfb78a06502df2f7d0",
  measurementId: "G-0EN0SFES55"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// ✅ create auth instance
const auth = getAuth(app);

// ✅ create google provider
const provider = new GoogleAuthProvider();

// ✅ export them
export { auth, provider };