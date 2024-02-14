import pandas as pd
import matplotlib.pyplot as plt

def plot_band_averages(csv_file):
    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Calculate average for each band
    alpha_avg = df.filter(like='Alpha').mean(axis=1)
    beta_avg = df.filter(like='Beta').mean(axis=1)
    gamma_avg = df.filter(like='Gamma').mean(axis=1)
    delta_avg = df.filter(like='Delta').mean(axis=1)
    theta_avg = df.filter(like='Theta').mean(axis=1)

    # Create a time series plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['Time'], alpha_avg, label='Alpha')
    plt.plot(df['Time'], beta_avg, label='Beta')
    plt.plot(df['Time'], gamma_avg, label='Gamma')
    plt.plot(df['Time'], delta_avg, label='Delta')
    plt.plot(df['Time'], theta_avg, label='Theta')

    # Customize the plot
    plt.xlabel('Time')
    plt.ylabel('Average Band Power')
    plt.title('Average Band Power Over Time')
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()

# Example usage
csv_file_path = 'power_by_band_data.csv'  # Replace with the actual path to your CSV file
plot_band_averages(csv_file_path)
