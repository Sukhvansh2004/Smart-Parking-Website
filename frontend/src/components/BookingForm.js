import React, { useState } from "react";
import axios from "axios";

const BookingForm = ({ slotId, googleToken, onBookingSuccess }) => {
  const [bookingDate, setBookingDate] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Client-side validations:
    const today = new Date();
    const selectedDate = new Date(bookingDate);
    const twoDaysAhead = new Date();
    twoDaysAhead.setDate(today.getDate() + 2);

    if (selectedDate < today || selectedDate > twoDaysAhead) {
      setError("Booking date must be today or within the next 2 days.");
      return;
    }

    // Check that start time is before end time
    if (startTime >= endTime) {
      setError("Start time must be before end time.");
      return;
    }

    // Ensure booking times are between 06:00 and 23:00
    const [startHour] = startTime.split(":").map(Number);
    const [endHour] = endTime.split(":").map(Number);
    if (startHour < 6 || endHour > 23) {
      setError("Bookings must be between 6:00 AM and 11:00 PM.");
      return;
    }

    try {
      // POST request to backend; adjust the URL if necessary
      const response = await axios.post(
        "http://localhost:8000/book",
        {
          slot_id: slotId,
          booking_date: bookingDate,
          start_time: startTime,
          end_time: endTime,
        },
        {
          headers: { google_token: googleToken },
        }
      );
      onBookingSuccess(response.data.message);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Booking failed. Please try again.");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ border: "1px solid #ccc", padding: "1em", marginTop: "1em" }}>
      <h3>Book Slot {slotId}</h3>
      <div>
        <label>Booking Date:</label>
        <input
          type="date"
          value={bookingDate}
          onChange={(e) => setBookingDate(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Start Time:</label>
        <input
          type="time"
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
          required
        />
      </div>
      <div>
        <label>End Time:</label>
        <input
          type="time"
          value={endTime}
          onChange={(e) => setEndTime(e.target.value)}
          required
        />
      </div>
      <button type="submit">Book Slot</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
};

export default BookingForm;
