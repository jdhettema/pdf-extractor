from fastapi import FastAPI, UploadFile
import shutil
from extract import extract_purchase_order_data

app = FastAPI()

@app.post("/extract")
async def extract_from_pdf(file: UploadFile):
    with open("temp.pdf", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = extract_purchase_order_data("temp.pdf")
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}