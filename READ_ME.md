# Thousand Day Compounding Growth
- 📈📈📈 1000 Day Challenge 📈📈📈
- A project tracking the power of daily compound growth over 1000 days, simulating a 0.51% daily growth rate.

## Overview
This project simulates and tracks a financial growth journey where:
- Timeline: March 6, 2025 - January 20, 2029 (Trump's last day in White House)
- Daily Growth Rate: 0.51% on working days
- Starting Amount: 1,357,945 ¥
- Target Amount: 233,704,160 ¥
- Total Days: 1416
- Working Days: 1012

## Key Features
- 📊 Daily compound growth calculations
- 📝 Automated audit report generation
- ✅ Actual vs Projected balance tracking
- 📈 CSV data export for analysis
- 🔄 Easy daily balance updates

## Purpose
This serves as a tracker to understand the impact of consistent compound growth. It's particularly useful for:
- Visualizing long-term compound growth effects
- Visualizing the power of consistent small gains
- Tracking personal growth goals


## Prerequisites
- Python 3.8+
- [Just](https://github.com/casey/just) command runner

## Setup
1. Clone the repository:

```bash
git clone https://github.com/ernshahi/thousand-day-compounding-growth
cd thousand-day-compounding-growth
```

2. Install dependencies:

```bash
just install
```

3. Run the program:

```bash
just run
```

## Usage
The program provides two main commands:
1. Generate an audit report:

```bash
just generate
```

2. Update today's balance:
```bash
just update
```


