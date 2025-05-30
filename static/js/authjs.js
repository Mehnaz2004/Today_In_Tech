import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-analytics.js";
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-app.js";
import {
    createUserWithEmailAndPassword,
    getAuth,
    GoogleAuthProvider,
    signInWithEmailAndPassword,
    signInWithPopup
} from "https://www.gstatic.com/firebasejs/11.8.1/firebase-auth.js";

    const firebaseConfig = {
      apiKey: "AIzaSyD41-VckzDCse3K3M659iAyk5kMcOUnSN8",
      authDomain: "todayintech-f238a.firebaseapp.com",
      projectId: "todayintech-f238a",
      storageBucket: "todayintech-f238a.appspot.com",
      messagingSenderId: "484902409160",
      appId: "1:484902409160:web:16d8b86d681aa11baf66fd",
      measurementId: "G-C01K6XGZDJ"
    };

    const app = initializeApp(firebaseConfig);
    const analytics = getAnalytics(app);
    const auth = getAuth(app);

    const loginEmail = document.getElementById('login-email');
    const loginPassword = document.getElementById('login-password');
    const loginBtn = document.getElementById('login-btn');
    const loginAlert = document.getElementById('login-alert');
    const loginGoogleBtn = document.getElementById('login-google-btn');

    const signupEmail = document.getElementById('signup-email');
    const signupPassword = document.getElementById('signup-password');
    const signupBtn = document.getElementById('signup-btn');
    const signupAlert = document.getElementById('signup-alert');
    const signupGoogleBtn = document.getElementById('signup-google-btn');

    function showAlert(element, message) {
      element.style.display = 'block';
      element.textContent = message;
      setTimeout(() => {
        element.style.display = 'none';
      }, 5000);
    }

    async function handlePostLogin() {
      try {
        const user = auth.currentUser;
        if (!user) throw new Error("No user found after login/signup.");
        const idToken = await user.getIdToken(true);
        localStorage.setItem('firebaseIdToken', idToken);
        window.location.href = "/dashboard";  // ✅ Flask route
      } catch (error) {
        alert("Error fetching ID token: " + error.message);
      }
    }

    loginBtn.addEventListener('click', () => {
      const email = loginEmail.value.trim();
      const password = loginPassword.value;
      if (!email || !password) {
        showAlert(loginAlert, 'Please enter email and password.');
        return;
      }
      signInWithEmailAndPassword(auth, email, password)
        .then(handlePostLogin)
        .catch((error) => {
          if (error.code === 'auth/user-not-found') {
            showAlert(loginAlert, 'Account not registered. Please sign up first.');
          } else if (error.code === 'auth/wrong-password') {
            showAlert(loginAlert, 'Incorrect password. Please try again.');
          } else {
            showAlert(loginAlert, error.message);
          }
        });
    });

    signupBtn.addEventListener('click', () => {
      const email = signupEmail.value.trim();
      const password = signupPassword.value;
      if (!email || !password) {
        showAlert(signupAlert, 'Please enter email and password.');
        return;
      }
      createUserWithEmailAndPassword(auth, email, password)
        .then(handlePostLogin)
        .catch((error) => {
          showAlert(signupAlert, error.message);
        });
    });

    async function googleSignIn() {
      const provider = new GoogleAuthProvider();
      try {
        await signInWithPopup(auth, provider);
        await handlePostLogin();
      } catch (error) {
        alert('Google Sign-In failed: ' + error.message);
      }
    }

    loginGoogleBtn.addEventListener('click', googleSignIn);
    signupGoogleBtn.addEventListener('click', googleSignIn);


    document.getElementById("show-signup").addEventListener("click", function (e) {
      e.preventDefault();
      document.getElementById("login-section").style.display = "none";
      document.getElementById("signup-section").style.display = "block";
    });

    document.getElementById("show-login").addEventListener("click", function (e) {
      e.preventDefault();
      document.getElementById("signup-section").style.display = "none";
      document.getElementById("login-section").style.display = "block";
    });

    document.getElementById("show-signup").addEventListener("click", function (e) {
  e.preventDefault();
  document.querySelector(".auth-wrapper").classList.add("signup-active");
});

document.getElementById("show-login").addEventListener("click", function (e) {
  e.preventDefault();
  document.querySelector(".auth-wrapper").classList.remove("signup-active");
});