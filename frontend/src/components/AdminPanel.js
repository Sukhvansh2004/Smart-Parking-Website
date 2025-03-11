import React, { useEffect, useState } from "react";
import axios from "axios";

const AdminPanel = ({ token }) => {
  const [slots, setSlots] = useState([]);
  const [newSlot, setNewSlot] = useState("");

  useEffect(() => {
    fetchSlots();
  }, []);

  const fetchSlots = async () => {
    const response = await axios.get("http://localhost:8000/parking_status");
    setSlots(response.data);
  };

  const addSlot = async () => {
    if (!newSlot) return;
    await axios.post(`http://localhost:8000/admin/add_slot/${newSlot}`, {}, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setNewSlot("");
    fetchSlots();
  };

  const deleteSlot = async (slotId) => {
    await axios.delete(`http://localhost:8000/admin/delete_slot/${slotId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    fetchSlots();
  };

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
          <div key={slot.slot_id}>
            {slot.slot_id} - {slot.status}
            <button onClick={() => deleteSlot(slot.slot_id)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminPanel;
