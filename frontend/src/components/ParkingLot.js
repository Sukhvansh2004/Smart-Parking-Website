import React, { useEffect, useState } from "react";
import axios from "axios";
import Slot from "./Slot";

const ParkingLot = () => {
  const [slots, setSlots] = useState([]);

  const fetchSlots = async () => {
    const response = await axios.get("http://localhost:8000/parking_status");
    setSlots(response.data);
  };

  useEffect(() => {
    fetchSlots();
  }, []);

  const bookSlot = async (slotId) => {
    await axios.post(`http://localhost:8000/book/${slotId}`);
    fetchSlots();
  };

  const releaseSlot = async (slotId) => {
    await axios.post(`http://localhost:8000/release/${slotId}`);
    fetchSlots();
  };

  return (
    <div className="parking-lot">
      {slots.map((slot) => (
        <Slot key={slot.slot_id} slot={slot} onBook={bookSlot} onRelease={releaseSlot} />
      ))}
    </div>
  );
};

export default ParkingLot;
