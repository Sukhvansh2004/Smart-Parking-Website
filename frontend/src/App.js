import React, { useState } from "react";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import GoogleLoginComponent from "./components/GoogleLoginComponent";
import ParkingLot from "./components/ParkingLot";
import AdminLogin from "./components/AdminLogin";
import AdminPanel from "./components/AdminPanel";

const App = () => {
  const [googleToken, setGoogleToken] = useState(null);
  const [adminToken, setAdminToken] = useState(null);
  
  // Read the Google Client ID from the environment variable
  const googleClientId = process.env.REACT_APP_GOOGLE_CLIENT_ID;
  
  return (
    <GoogleOAuthProvider clientId={googleClientId}>
      <Router>
        <div>
          <nav>
            <Link to="/">Home</Link> | <Link to="/admin">Admin</Link>
          </nav>
          {!googleToken ? (
            <div style={{ textAlign: "center", marginTop: "50px" }}>
              <h2>Please sign in with Google to continue</h2>
              <GoogleLoginComponent onSuccess={(token) => setGoogleToken(token)} />
            </div>
          ) : (
            <Routes>
              <Route path="/" element={<ParkingLot googleToken={googleToken} />} />
              {/* Admin routes */}
              <Route path="/admin" element={<AdminLogin setToken={setAdminToken} />} />
              <Route path="/admin/panel" element={<AdminPanel token={adminToken} />} />
            </Routes>
          )}
        </div>
      </Router>
    </GoogleOAuthProvider>
  );
};

export default App;
