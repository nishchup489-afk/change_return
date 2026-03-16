# Cash Register Change Calculator

**Project 8 of 100 Python Live Project Mission**

**GitHub URL:** [https://github.com/nishchup489-afk/change_return](https://github.com/nishchup489-afk/change_return)

**Live Preview:** [https://change-return.onrender.com](https://change-return.onrender.com)

**CLI Version:** `sample.py`

---

## Overview

This project is a **Cash Register Change Calculator** built with both a **pure Python CLI version** and a **FastAPI + Jinja2 web version**.

The goal is simple:

* take the **total cost**
* take the **cash given by the customer**
* calculate whether the payment is **pending** or **successful**
* if successful, break the returned change into bills and coins using a **greedy algorithm**

This project is a clean example of how a small real-world problem can teach:

* input handling
* money calculation
* dictionaries and loops
* greedy algorithms
* FastAPI form handling
* Jinja2 templating
* frontend and backend integration

---

## Pure Theory

A cash register system has one main job:

> Determine whether the customer has paid enough, and if so, return the correct change in the simplest breakdown possible.

If:

$$
\text{given} < \text{cost}
$$

then the customer still owes money.

If:

$$
\text{given} \geq \text{cost}
$$

then the change is:

$$
\text{change} = \text{given} - \text{cost}
$$

That change is then split into denominations such as:

* $100
* $50
* $20
* $10
* $5
* $1
* quarter
* dime
* nickel
* cent

The key challenge is not just finding the total change.
The real challenge is finding the **best breakdown**.

For example, if the change is:

$$
18.36
$$

A good cashier system should return:

* 1 × $10
* 1 × $5
* 3 × $1
* 1 × quarter
* 1 × dime
* 1 × cent

instead of some ugly random breakdown with too many small coins.

That is where the **greedy algorithm** comes in.

---

## Greedy Algorithm

A **greedy algorithm** makes the best possible choice at the current step.

In this project, that means:

> Always take the largest bill or coin possible before moving to the next smaller denomination.

### Example

Suppose the change is:

$$
18.36
$$

The greedy steps are:

1. Take $10 → remaining = 8.36
2. Take $5 → remaining = 3.36
3. Take $1 three times → remaining = 0.36
4. Take 1 quarter → remaining = 0.11
5. Take 1 dime → remaining = 0.01
6. Take 1 cent → remaining = 0.00

Done.

### Why greedy works here

For standard US currency, the greedy method gives the correct and efficient breakdown because the denominations are structured in a way that supports this approach.

### Use cases of greedy algorithms

Greedy algorithms are used in many classic computer science problems, such as:

* coin change systems
* scheduling problems
* shortest path strategies like Dijkstra's algorithm
* Huffman coding and data compression
* resource allocation problems

This project is a beginner-friendly real-world example of a greedy algorithm in action.

---

## Python Code Explanation

The backend logic is centered around a function like this:

```python
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
```

### Step-by-step explanation

#### 1. Convert dollars into cents

```python
cost = int(round(cost * 100))
given = int(round(given * 100))
```

This is extremely important.
Money should not be handled directly with floating-point arithmetic because decimal values like `12.37` can become inaccurate in binary floating-point form.

By converting everything into cents, the calculation becomes safer and cleaner.

#### 2. Check whether payment is enough

```python
if given < cost:
```

If the customer gave less money than required, the function returns a `pending` status and shows how much is still owed.

#### 3. Store denominations

```python
coins = [
    ("100$", 10000),
    ("50$", 5000),
    ...
]
```

Each denomination is stored as a tuple:

$$
(\text{name}, \text{value in cents})
$$

The list is ordered from largest to smallest because the greedy strategy depends on that order.

#### 4. Compute total change

```python
change = given - cost
```

This is the raw amount that must be returned.

#### 5. Break the change using greedy logic

```python
for name, value in coins:
    count = change // value
```

The `//` operator performs integer division.
It calculates how many times the denomination fits into the remaining change.

If the count is greater than zero, that denomination is added to the result dictionary.

Then the remaining amount is reduced:

```python
change -= count * value
```

This repeats until the remaining change becomes zero.

#### 6. Return structured output

The function returns a dictionary containing:

* status
* given amount
* cost
* total change
* detailed denomination breakdown

That dictionary is perfect for both CLI display and HTML rendering.

---

## CLI Version

The CLI version is the pure Python version of the project.
It focuses only on logic and terminal interaction.

Typical CLI flow:

1. ask the user for cost
2. ask the user for given amount
3. calculate change
4. print either pending amount or change breakdown

This version is useful because it lets you test the algorithm before adding a frontend or web backend.

---

## HTML + Jinja2 Explanation

The web version uses **FastAPI** for the backend and **Jinja2 templates** for rendering the UI.

### What the HTML does

The HTML page has three main parts:

#### 1. Cost input

A number input where the user enters the total cost.

#### 2. Cash given screen and buttons

A second input holds the amount given by the customer.
Cash buttons such as `100$`, `50$`, `20$`, `10$`, and `1$` are used to simulate a real POS register.

A little JavaScript adds the button values into the `given` input so the cashier can build the payment amount quickly.

#### 3. Result section

The result section is rendered dynamically with Jinja2.

If the result status is `pending`, the page shows:

* total given
* remaining amount due

If the result status is `success`, the page shows:

* total given
* total change
* a table of returned bills and coins

### Why Jinja2 matters here

Jinja2 lets Python send data directly into the HTML template.
That means your backend calculates the change and your frontend displays it immediately.

For example:

```jinja2
{% if result['status'] == 'success' %}
```

This checks whether the payment succeeded.

Then:

```jinja2
{% for coin, amount in result['change'].items() %}
```

This loops over the returned change dictionary and prints each denomination in the table.

That is the bridge between backend logic and frontend presentation.

---

## FastAPI Workflow

The app usually has two routes.

### GET `/`

This loads the homepage and sends an empty result:

```python
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": None}
    )
```

### POST `/calculate`

This route receives the submitted form data, runs the algorithm, and sends the result back into the same HTML page:

```python
@app.post("/calculate", response_class=HTMLResponse)
def calculate(request: Request, cost: float = Form(...), given: float = Form(...)):
    result = change_return(cost, given)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result}
    )
```

This is a very common server-rendered web app pattern.

---

## What This Project Teaches

This project teaches more than it first appears to teach.

It covers:

* basic financial logic
* safe money calculation using cents
* greedy algorithm implementation
* dictionaries and tuple lists
* loops and integer division
* FastAPI form handling
* Jinja2 conditional rendering
* HTML structure for a small product UI
* simple JavaScript interaction for button-driven input

That makes it a strong beginner-to-intermediate portfolio project.

---

## Suggested Stack

* **Python**
* **FastAPI**
* **Jinja2**
* **HTML**
* **Tailwind CSS**
* **Vanilla JavaScript**

Optional extras:

* Rich for a prettier CLI version
* Render / Railway / Fly.io for deployment

---

## Final Note

This project may look small, but it represents a very practical software pattern:

> user input → backend processing → algorithmic decision → structured output → UI rendering

That pattern appears everywhere in real software.

A project like this is a nice step forward because it is not just a toy calculator. It simulates a small real-world cashier workflow using proper algorithmic thinking and backend/frontend integration.

---

## Footer

Check out the rest of the **100 Python Live Project Mission** once you add them to your main repository.
