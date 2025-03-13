import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const AdminPanel = ({ token }) => {
  const [slots, setSlots] = useState([]);
  const [newSlot, setNewSlot] = useState("");
  const [isVerified, setIsVerified] = useState(false);
  const navigate = useNavigate();
  
  // Function to verify the admin token with the backend
  const verifyToken = async () => {
    try {
      await axios.get("http://localhost:8000/admin/verify", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setIsVerified(true);
    } catch (error) {
      console.error("Token verification failed", error);
      setIsVerified(false);
      // If token is invalid, redirect to the admin login page
      navigate("/admin");
    }
  };

  // Verify token on component mount or when token changes
  useEffect(() => {
    verifyToken();
  }, [token]);

  // Fetch slot data only if token has been verified
  const fetchSlots = async () => {
    try {
      const response = await axios.get("http://localhost:8000/parking_status");
      setSlots(response.data);
    } catch (error) {
      console.error("Failed to fetch slots:", error);
    }
  };

  useEffect(() => {
    if (isVerified) {
      fetchSlots();
      const intervalId = setInterval(() => {
        fetchSlots();
      }, 1000); // Refresh every 10 seconds

      return () => clearInterval(intervalId);
    }
  }, [isVerified]);

  const addSlot = async () => {
    if (!newSlot) return;
    try {
      await axios.post(
        `http://localhost:8000/admin/add_slot/${newSlot}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setNewSlot("");
      fetchSlots();
    } catch (error) {
      console.error("Failed to add slot:", error);
    }
  };

  const deleteSlot = async (slotId) => {
    try {
      await axios.delete(`http://localhost:8000/admin/delete_slot/${slotId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchSlots();
    } catch (error) {
      console.error("Failed to delete slot:", error);
    }
  };

  const releaseSlot = async (slotId) => {
    try {
      await axios.post(
        `http://localhost:8000/release/${slotId}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchSlots();
    } catch (error) {
      console.error("Error releasing slot:", error);
    }
  };

  if (!isVerified) {
    return <div>Verifying token...</div>;
  }

  return (
    <div>
      <h2>Admin Panel</h2>
      <div>
        <input
          type="text"
          placeholder="New Slot ID"
          value={newSlot}
          onChange={(e) => setNewSlot(e.target.value)}
        />
        <button onClick={addSlot}>Add Slot</button>
      </div>
      <div>
        {slots.map((slot) => (
          <div
            key={slot.slot_id}
            style={{ border: "1px solid #ddd", padding: "0.5em", margin: "0.5em" }}
          >
            <p>
              Slot {slot.slot_id}: {slot.status}{" "}
              {slot.status === "Occupied" && slot.user && (
                <span>- Booked by: {slot.user}</span>
              )}
            </p>
            <button onClick={() => deleteSlot(slot.slot_id)}>Delete</button>
            {slot.status === "Occupied" && (
              <button onClick={() => releaseSlot(slot.slot_id)}>Release</button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminPanel;
