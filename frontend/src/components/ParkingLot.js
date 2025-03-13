import React, { useState, useEffect } from "react";
import axios from "axios";

const ParkingLot = ({ googleToken }) => {
  const [slots, setSlots] = useState([]);
  const [user, setUser] = useState(null);

  const fetchSlots = async () => {
    try {
      const response = await axios.get("http://localhost:8000/parking_status");
      setSlots(response.data);
      const userResponse = await axios.get(`http://localhost:8000/user?token=${googleToken}`);
      setUser(userResponse.data.user);
    } catch (err) {
      console.error("Failed to fetch slots", err);
    }
  };

  const bookSlot = async (slotId) => {
    try {
      await axios.post(`http://localhost:8000/book/${slotId}?token=${googleToken}`, {});
      fetchSlots();
    } catch (error) {
      console.error("Error booking slot:", error);
    }
  };

  const releaseSlot = async (slotId) => {
    try {
      await axios.post(`http://localhost:8000/release/${slotId}`, {});
      fetchSlots();
    } catch (error) {
      console.error("Error releasing slot:", error);
    }
  };

  useEffect(() => {
    fetchSlots();

    // Set up polling every 10 seconds
    const intervalId = setInterval(() => {
      fetchSlots();
    }, 1000);

    // Cleanup interval on component unmount
    return () => clearInterval(intervalId);
  }, [googleToken]);

  return (
    <div>
      <h2>Parking Lot Status</h2>
      <div className="parking-lot">
        {slots.map((slot) => (
          <div
            key={slot.slot_id}
            style={{ border: "1px solid #ddd", padding: "0.5em", margin: "0.5em" }}
          >
            <p>
              Slot {slot.slot_id}: {slot.status}
            </p>
            {slot.status === "Available" && (
              <button onClick={() => bookSlot(slot.slot_id)}>Book</button>
            )}
            {slot.status === "Occupied" &&
              user &&
              slot.user === user && (
                <button onClick={() => releaseSlot(slot.slot_id)}>Release</button>
              )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ParkingLot;
