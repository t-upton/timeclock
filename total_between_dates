import pandas as pd

def get_total_duration(name, start_date, end_date):
    # Read the CSV data from a file named "times.csv"
    df = pd.read_csv("times.csv", parse_dates=[3])  # Parsing the timestamp as date
    
    # Filter data
    mask = (df['Name'] == name) & (df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)
    filtered_data = df[mask]
    
    # Calculate total duration
    total_duration = filtered_data['Duration'].sum()

    return total_duration

if __name__ == "__main__":
    name = input("Enter the name: ")
    start_date = input("Enter the beginning date (YYYY-MM-DD HH:MM:SS): ")
    end_date = input("Enter the end date (YYYY-MM-DD HH:MM:SS): ")
    
    total = get_total_duration(name, start_date, end_date)
    print(f"Total duration for {name} between {start_date} and {end_date}: {total:.2f} hours")
