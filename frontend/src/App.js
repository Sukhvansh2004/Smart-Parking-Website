import React, { useState } from "react";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import GoogleLoginComponent from "./components/GoogleLoginComponent";
import ParkingLot from "./components/ParkingLot";
import AdminLogin from "./components/AdminLogin";
import AdminPanel from "./components/AdminPanel";

const App = () => {
  const [googleToken, setGoogleToken] = useState(null);

  return (
    <GoogleOAuthProvider clientId="705225432757-hdkc806vmj8por78b3cs1v57i3t86vrn.apps.googleusercontent.com">
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
              <Route path="/admin" element={<AdminLogin setToken={setGoogleToken} />} />
              <Route path="/admin/panel" element={<AdminPanel token={googleToken} />} />
            </Routes>
          )}
        </div>
      </Router>
    </GoogleOAuthProvider>
  );
};

export default App;
