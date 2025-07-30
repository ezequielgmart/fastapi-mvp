from fastapi import FastAPI, HTTPException

app = FastAPI()

items = ["Apple","Mango","Pear"]

@app.get("/")
def root():
    return items  

@app.get("/items")
def create_item():
    
    
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int) -> str:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")

