# ITB Gate Simulation
A web-based parking gate simulation built with **Flask**, **HTML**, **CSS**, and **JavaScript**. Simulate vehicle entry and exit, manage parking cards and balances, calculate parking fees, and view transaction records.
## Features
- **Interactive gate simulation:** Drag a vehicle card into the gate's target area to trigger entry or exit.
- **Entry and exit modes:** Switch between entry and exit operations.
- **Adjustable simulation time:** Set a date and time, or advance the simulation by 15 minutes, 1 hour, or 1 day.
- **Vehicle card management:** Edit cardholder names, vehicle types, and balances.
- **Parking fee calculation:** Includes a 15-minute grace period, hourly charges, maximum fee limits, and overnight fees.
- **Balance validation:** Exit is rejected when a card's balance is insufficient.
- **Persistent records:** Parking sessions and transaction history are stored in a JSON file.
- **Browser persistence:** Card configuration and balances are retained using localStorage.
- **Session synchronization:** Active parking sessions are synchronized with the backend when the page loads.
## Tech Stack
- Python
- Flask
- HTML
- CSS
- JavaScript
- JSON
- Browser localStorage
## Getting Started
### 1. Clone the repository
```bash
git clone https://github.com/arsyadfr/itb-gate-simulation.git
cd itb-gate-simulation

2. Install Python

Make sure Python 3 is installed on your computer.

3. Install Flask

pip install flask

4. Run the application

python app.py

5. Open the simulator

Open the following URL in your browser:

http://127.0.0.1:5000

How to Use

* Open the simulator in your browser.
* Choose Entry or Exit in Simulation Settings.
* Set the simulation date and time.
* Drag a vehicle card into the Drop here target.
* The simulation will process the operation and display the result.
* Use the Cards section in Simulation Settings to edit cardholder names, vehicle types, or balances.

Parking Tariffs

Vehicle	Hourly Rate	Maximum Fee	Overnight Fee
Motorcycle (motor)	Rp 2,000	Rp 5,000	Rp 5,000
Car (mobil)	Rp 3,000	Rp 10,000	Rp 15,000

Fee Rules

* First 15 minutes: Free.
* Hourly billing: After the free period, parking is charged by rounding up to the next hour.
* Maximum fee: Hourly charges are capped at the vehicle’s maximum fee.
* Overnight fee: Each calendar day crossed between entry and exit adds the vehicle’s overnight fee.
* Balance: The parking fee is deducted from the card balance upon successful exit.

The fee calculation uses the elapsed parking duration for hourly charges and the difference between entry and exit calendar dates for overnight charges.

How the Code Works

Backend — app.py

The Flask application handles the simulation logic, parking sessions, fee calculations, and transaction records.

Frontend — templates/index.html

The frontend displays the simulated gate, draggable vehicle cards, and simulation settings. JavaScript handles:

* Dragging cards using pointer events.
* Detecting when a card overlaps the gate’s drop target.
* Sending entry and exit requests to the Flask API.
* Updating card balances and statuses.
* Saving card settings to browser localStorage.
* Synchronizing card status with active backend sessions.

Data Storage

The simulator uses two storage mechanisms:

* parking_data.json — Backend storage for active parking sessions and transaction history. This file is created when the application saves data for the first time.
* localStorage — Browser storage for cardholder configuration, including card IDs, names, vehicle types, balances, and displayed status.

API Endpoints

GET /api/sessions

Returns the IDs of currently active parking sessions.

POST /api/entry

Registers a vehicle entering the parking area.

Example request:

{
  "card_id": "1e2f3g2dwa",
  "owner": "Budi",
  "vehicle": "motor",
  "balance": 100000,
  "time": "2026-11-18T10:00"
}

POST /api/exit

Processes a vehicle exit, calculates the fee, and deducts it from the submitted balance.

GET /api/transactions

Returns recorded entry and exit transactions.

Project Structure

itb-gate-simulation/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── parking_data.json   # Generated when data is saved

Notes

* This project is a simulation and does not control a real parking gate or payment system.
* The backend runs locally by default at 127.0.0.1:5000.
* The simulator uses sample cardholder data by default.
* The Flask application is configured with debug mode enabled for development.

License

No license has been specified for this repository yet.
