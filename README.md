# Expense Tracker

A simple command-line expense tracker built with Python. It's my first mini project, made while learning Python fundamentals.

## Features

1. **Add expense**: amount, category and a short note. Date and time are saved automatically.
2. **View today**: all of today's expenses with the total.
3. **View by date**: see every expense on a chosen date.
4. **Date total**: total spent on a chosen date.
5. **Exit**

## How to run

Requires **Python 3.10 or newer**.

```
python expense_tracker.py
```

## Important

The program stores data in a CSV file named exactly `_expense_data.csv`, in the same folder as the script. The first line of that file must be:

```
AMOUNT,CATEGORY,DESCRIPTION,TIME,DATE
```

## What I practiced

Functions, input validation, custom exceptions, file handling with CSV, and working with dates.
