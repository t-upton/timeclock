import pandas as pd

def get_total_durations(start_date, end_date):
    # Define column names and read CSV
    columns = ["Name", "PIN", "Action", "Timestamp", "Duration"]
    df = pd.read_csv("times.csv", names=columns, parse_dates=["Timestamp"])

    # Filter data based on date range and action type
    mask = (df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date) & (df['Action'] == 'clock-out')
    filtered_data = df[mask]

    # Group by 'Name' and sum 'Duration'
    total_durations = filtered_data.groupby('Name')['Duration'].sum()

    return total_durations

if __name__ == "__main__":
    start_date = input("Enter the beginning date (YYYY-MM-DD HH:MM:SS): ")
    end_date = input("Enter the end date (YYYY-MM-DD HH:MM:SS): ")

    total_durations = get_total_durations(start_date, end_date)
    for name, total in total_durations.items():  # Changed from iteritems() to items()
        print(f"Total duration for {name} between {start_date} and {end_date}: {total:.2f} hours")
