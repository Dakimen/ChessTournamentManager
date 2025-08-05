# Chess Tournament Manager

A command-line based chess tournament manager built in Python. It allows you to create and manage chess tournaments, keep track of players and rounds, and generate reports.

## Features

    Create new tournaments and manage existing ones

    Add and manage players

    Generate and display match pairings

    Track round results

    Save and load tournament data using TinyDB

    Generate HTML reports with flake8 for code quality

## Getting Started

1. Clone the repository

```
git clone https://github.com/Dakimen/ChessTournamentManager.git
cd ChessTournamentManager
```

2. Create and Activate a Virtual Environment
   On Windows:

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

   On macOS/Linux:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Dependencies

   ```
   pip install -r requirements.txt
   ```

## How to Run the Program

To start the application:

```
python main.py
```

Follow the on-screen menu to create tournaments, add players, and manage rounds.

### Code Quality Report

1. Install flake8 and flake8-html
   If not already installed, you can add them with:

```
pip install flake8 flake8-html
```

2. Generate the HTML Report
   From the project root, run:

```
flake8 --exclude=venv --format=html --htmldir=flake8-report
```

Note that after --exclude= you should insert the name of your Virtual Environment.
This will generate a directory flake8_report/ containing the HTML report. Open index.html inside that folder in your browser to view it.

### Project Structure

```
ChessTournamentManager/
├── controllers/       # Business logic and flow control
├── models/            # Data models and storage logic
├── views/             # Terminal-based UI
├── data_manager/      # Database interaction logic
├── flake8-rapport/    # Contains the flake8-html report
├── main.py            # Entry point of the program
├── requirements.txt   # List of dependencies
├── .flake8            # Additional flake8 configuration
└── README.md
```

### Requirements

    Python 3.10+

    TinyDB

    flake8

    flake8-html

Install all dependencies using the requirements.txt file.
