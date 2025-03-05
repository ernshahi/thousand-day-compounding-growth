import os
import pandas as pd
import argparse
from datetime import datetime, timedelta

# Initialize variables
START_DATE = datetime(2025, 3, 5)  # First day of the audit
END_DATE = datetime(2029, 1, 20)  # End day of the audit

# Calculate total weekdays between START_DATE and END_DATE
TOTAL_DAYS = sum(1 for day in range((END_DATE - START_DATE).days + 1) if (START_DATE + timedelta(days=day)).weekday() < 5)

INITIAL_VALUE = 1_357_945.00  # First day's value
INCREMENT_PERCENT = 0.0051  # 0.51%
TODAY = datetime.now().strftime("%Y-%m-%d")
FILE_PATH = "data/audit_data.csv"


def _get_current_time():
    """get current time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Generate data
def generate_audit_report():
    print("Starting audit report generation")
    os.makedirs("data", exist_ok=True)
    if "audit_data.csv" in os.listdir("data/"):
        print("\033[91mWarning: audit_data.csv already exists\033[0m")
        if input("\033[91mDo you want to reset it? (y/n): \033[0m") != "y":
            print("Exiting program")
            return
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.rename(FILE_PATH, f"{FILE_PATH}_{timestamp}.csv")
        print(f"Backup of old file created: {FILE_PATH}_{timestamp}.csv")

    data = [[TODAY, 0, TOTAL_DAYS, INCREMENT_PERCENT, '-', f"{INITIAL_VALUE:_.2f}", '-', '-', '-']]
    total = INITIAL_VALUE
    actual_day_count = 0  # Counter for actual days added to the report

    for day in range(1, (END_DATE - START_DATE).days + 1):
        date = START_DATE + timedelta(days=day)
        if date.weekday() < 5:  # 0-4 are Monday to Friday
            actual_day_count += 1  # Increment the actual day count
            increment = total * INCREMENT_PERCENT
            total += increment
            data.append([
                date.strftime("%Y-%m-%d"),
                actual_day_count,  # Use the actual day count
                f"{TOTAL_DAYS - actual_day_count}",
                f"{INCREMENT_PERCENT}",
                f"{increment:_.2f}",
                f"{total:_.2f}",
                "-",
                "-",
                "-",
            ])
    
    df = pd.DataFrame(
        data,
        columns=[
            "date",
            "day",
            "remaining_days",
            "increment_percent",
            "increment_value",
            "projected_balance",
            "actual_balance",
            "difference",  # difference between actual and projected_balance
            "difference_percent",  # percentage difference from projected balance
        ],
    )
    # Save to CSV file
    df.to_csv(FILE_PATH, index=False)
    print(f"Audit report generation completed, file: {FILE_PATH}")


def _input_balance():
    """
    Input the balance on the current day.
    it can be 1,999,255 or 1_999_255
    """
    max_attempts = 3
    for i in range(0, max_attempts):
        try:
            input_balance = float(
                input(f"Enter the balance on {TODAY}: ").replace(",", "").replace("_", "")
            )
            break
        except ValueError:
            print("Invalid input. Please enter a valid amount.")
    else:
        print(f"Exiting program, invalid input {max_attempts} times")
        exit()
    return input_balance


def update_today_balance():
    input_balance = _input_balance()
    df = pd.read_csv("data/audit_data.csv")
    df.loc[df["date"] == TODAY, "actual_balance"] = f"{input_balance:_.2f}"
    # Calculate and update difference
    today_row = df.loc[df["date"] == TODAY]
    if not today_row.empty:
        projected = float(today_row["projected_balance"].iloc[0].replace("_", ""))
        difference = input_balance - projected
        df.loc[df["date"] == TODAY, "difference"] = f"{difference:_.2f}"
        # Calculate and update difference percentage
        difference_percent = (difference / projected) * 100
        df.loc[df["date"] == TODAY, "difference_percent"] = f"{difference_percent:.2f}%"

    df.to_csv("data/audit_data.csv", index=False)
    print(f"Today's ({TODAY}) balance updated to {input_balance}")
    print(f"Difference from projected: {difference:_.2f} ({difference_percent:.2f}%)")


def main():
    parser = argparse.ArgumentParser(description="Compound Growth Demo")
    parser.add_argument("--generate", action="store_true", help="Generate audit report")
    parser.add_argument("--update", action="store_true", help="Update today's balance")
    args = parser.parse_args()

    print(f"Program started at {_get_current_time()}")

    if args.generate:
        generate_audit_report()
    elif args.update:
        update_today_balance()
    else:
        print(
            "\033[93mNo arguments provided. Please use --generate or --update, or "
            "check justfile for available commands\033[0m"
        )
    print(f"Program ended at {_get_current_time()}")


if __name__ == "__main__":
    main()
