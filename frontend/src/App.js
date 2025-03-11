import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ParkingLot from "./components/ParkingLot";
import AdminLogin from "./components/AdminLogin";
import AdminPanel from "./components/AdminPanel";

const App = () => {
  const [token, setToken] = useState(null);

  return (
    <Router>
      <div>
        <nav>
          <Link to="/">Home</Link> | <Link to="/admin">Admin</Link>
        </nav>
        <Routes>
          <Route path="/" element={<ParkingLot />} />
          <Route path="/admin" element={<AdminLogin setToken={setToken} />} />
          <Route path="/admin/panel" element={<AdminPanel token={token} />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
