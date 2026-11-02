"use client";

import { useEffect, useState } from "react";

type Item = { id: number; name: string, watt: number, priority: number, status: string, userInput: string };

export default function Home() {
  async function toggleStatus(id: number) {
    await fetch(`/api/items/${id}/toggle`, { method: "POST" });
    await load();
  }

  const [items, setItems] = useState<Item[]>([]);
  const [name, setName] = useState("");
  const [watt, setWatt] = useState(0);
  const [priority, setPriority] = useState(0);
  const [status, setStatus] = useState("off");
  const [userInput, setUserInput] = useState("off");

  async function load() {
    const response = await fetch("/api/items");
    setItems(await response.json());
  }

  useEffect(() => {
    void load();
  }, []);

  async function addItem() {
    await fetch("/api/items", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, watt, priority, status, userInput }),
    });
    setName("");
    setWatt(0);
    setPriority(0);
    setStatus("off");
    setUserInput("off");
    await load();
  }

  return (
    <main>
      <div>
        <span>Name: </span>
        <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
        <span>Watt: </span>
        <input type="number" placeholder="Watt" value={watt} onChange={(e) => setWatt(Number(e.target.value))} />
        <span>Priority: </span>
        <input type="number" placeholder="Priority" value={priority} onChange={(e) => setPriority(Number(e.target.value))} /> 
      </div>
      <button type="button" onClick={addItem}>Add Appliance</button>
      <div>
        {items.map((item) => (
          <div key={item.id}>
            <div>
            {item.name} - {item.watt}W - Priority {item.priority} - Status {item.status}
             
             </div>
             <div>
                <button type="button" onClick={() => toggleStatus(item.id)}>
                {item.userInput}
                </button>
            </div>
          </div>
           
        ))}
       
      </div>
    </main>
  );
}