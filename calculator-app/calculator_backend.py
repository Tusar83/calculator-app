from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS to allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operation: str

# Define response model
class CalculationResponse(BaseModel):
    result: Optional[float] = None
    error: Optional[str] = None

@app.post("/calculate")
def calculate(request: CalculationRequest):
    """
    Receives two numbers and an operation, returns the result.
    Operations: +, -, *, /
    """
    try:
        num1 = request.num1
        num2 = request.num2
        operation = request.operation

        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            if num2 == 0:
                return CalculationResponse(result=None, error="Cannot divide by zero")
            result = num1 / num2
        else:
            return CalculationResponse(result=None, error=f"Invalid operation: {operation}")

        return CalculationResponse(result=result)

    except Exception as e:
        return CalculationResponse(result=None, error=str(e))

@app.get("/")
def read_root():
    return {"message": "Calculator API is running! Use POST /calculate to calculate"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)