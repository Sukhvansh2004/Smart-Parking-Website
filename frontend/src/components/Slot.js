import React from "react";

const Slot = ({ slot, onBook, onRelease }) => {
  return (
    <div className={`slot ${slot.status === "Available" ? "available" : "occupied"}`}>
      <p>{slot.slot_id}</p>
      <p>Status: {slot.status}</p>
      {slot.status === "Available" ? (
        <button onClick={() => onBook(slot.slot_id)}>Book</button>
      ) : (
        <button onClick={() => onRelease(slot.slot_id)}>Release</button>
      )}
    </div>
  );
};

export default Slot;
