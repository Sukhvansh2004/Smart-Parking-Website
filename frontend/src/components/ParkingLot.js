import React, { useState, useEffect } from "react";
import axios from "axios";
import BookingForm from "./BookingForm";

const ParkingLot = ({ googleToken }) => {
  const [slots, setSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [bookingMessage, setBookingMessage] = useState("");

  const fetchSlots = async () => {
    try {
      const response = await axios.get("http://localhost:8000/parking_status");
      setSlots(response.data);
    } catch (err) {
      console.error("Failed to fetch slots", err);
    }
  };

  useEffect(() => {
    fetchSlots();
  }, []);

  return (
    <div>
      <h2>Parking Lot Status</h2>
      <div className="parking-lot">
        {slots.map((slot) => (
          <div key={slot.slot_id} style={{ border: "1px solid #ddd", padding: "0.5em", margin: "0.5em" }}>
            <p>
              Slot {slot.slot_id}: {slot.status}
            </p>
            {slot.status === "Available" && (
              <button onClick={() => setSelectedSlot(slot.slot_id)}>Book this slot</button>
            )}
          </div>
        ))}
      </div>

      {selectedSlot && (
        <BookingForm
          slotId={selectedSlot}
          googleToken={googleToken}
          onBookingSuccess={(msg) => {
            setBookingMessage(msg);
            setSelectedSlot(null);
            fetchSlots();
          }}
        />
      )}

      {bookingMessage && <p>{bookingMessage}</p>}
    </div>
  );
};

export default ParkingLot;
