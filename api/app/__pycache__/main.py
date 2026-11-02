from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.db import get_connection

app = FastAPI(title="My API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
Limit = 800;

class ItemIn(BaseModel):
    name: str
    watt: int
    priority: int
    status: str = "off"
    userInput: str = "off"
    


@app.get("/api/items")
def list_items():
    breakpoint()
    with get_connection() as connection:
        rows = connection.execute("SELECT id, name, watt, priority, status, userInput FROM items ORDER BY id").fetchall()
    return [{"id": row["id"], "name": row["name"], "watt": row["watt"], "priority": row["priority"], "status": row["status"], "userInput": row["userInput"]} for row in rows]

@app.post("/api/items")
def create_item(item: ItemIn):
   
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO items (name, watt, priority, status, userInput) VALUES (?, ?, ?, ?, ?)",
            (item.name, item.watt, item.priority, item.status, item.userInput)
        )
        connection.commit()
        return {"id": cursor.lastrowid, "name": item.name, "watt": item.watt, "priority": item.priority, "status": item.status, "userInput": item.userInput}

@app.post("/api/deleteall")
def delete_all_items():
    with get_connection() as connection:
        connection.execute("DELETE FROM items")
        connection.commit()
    return {"status": "success"}

@app.post("/api/items/{item_id}/toggle")
def toggle_item_status(item_id: int):
    with get_connection() as connection:
       
        row = connection.execute("SELECT id, watt, status, userInput FROM items WHERE id = ?", (item_id,)).fetchone()
        if row is None:
            return {"error": "Item not found"}
        all_rows = connection.execute("SELECT id, watt, userInput FROM items").fetchall()
        statusToUpdate = controlLogic(row, all_rows)

        connection.execute("UPDATE items SET status = ?, userInput = ? WHERE id = ?", (statusToUpdate, statusToUpdate, item_id))
        connection.commit()
    return {"id": item_id, "status": statusToUpdate}



def controlLogic(item, all_rows):
    if item["userInput"] == "off":
        excludeCurrent = [i for i in all_rows if i["id"] != item["id"]]
        otherInpputsPower = sum(i["watt"] for i in excludeCurrent if i["userInput"] == "on")
        if item["watt"] + otherInpputsPower <= Limit:
            return "on"
        return "off"
   # if item["userInput"] == "on":
            # itemsData = list_items()
            # excludeCurrent = [i for i in itemsData if i["id"] != item["id"]]
            # otherInpputsPower = sum(i["watt"] for i in excludeCurrent if i["userInput"] == "on")
            # if item["watt"] + otherInpputsPower <= Limit:
    
            #     return "on"
            # return "off"
    return "off"
