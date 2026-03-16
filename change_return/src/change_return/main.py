from fastapi import FastAPI , Request , Response , Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI()

def change_return(cost, given):

    cost = int(round(cost * 100))
    given = int(round(given * 100))

    if given < cost:
        pending = cost - given
        return {
            "status": "pending",
            "cost": cost / 100,
            "given": given / 100,
            "amount": pending / 100
        }

    coins = [
        ("100$", 10000),
        ("50$", 5000),
        ("20$", 2000),
        ("10$", 1000),
        ("5$", 500),
        ("1$", 100),
        ("quarter", 25),
        ("dime", 10),
        ("nickel", 5),
        ("cent", 1)
    ]

    change = given - cost
    change_total = change / 100

    result = {}

    for name, value in coins:
        count = change // value

        if count > 0:
            result[name] = int(count)
            change -= count * value

    return {
        "status": "success",
        "given": given / 100,
        "cost": cost / 100,
        "change": result,
        "change_total": change_total
    }



@app.get("/", response_class=HTMLResponse)
def Home(request : Request):
    return templates.TemplateResponse("index.html" , {"request" : request , "result": None})


@app.post("/calculate" , response_class=HTMLResponse)
def calculate(request : Request , cost : float = Form(...), given : float = Form(...)):
    result = change_return(cost , given)
    return templates.TemplateResponse("index.html" , {"request" : request , "result" : result})
                                      
