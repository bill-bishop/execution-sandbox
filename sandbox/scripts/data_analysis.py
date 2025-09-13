# data_analysis.py
# This script analyzes Mega Millions data for frequency and patterns.

import pandas as pd
import matplotlib.pyplot as plt

# Function to load data
def load_data(filepath):
    """Loads Mega Millions data from a CSV file."""
    return pd.read_csv(filepath)

# Function to analyze frequency
def analyze_frequency(data):
    """Analyzes number frequency in the Mega Millions dataset."""
    # Analyze main numbers
    main_numbers = data[[f"Number_{i+1}" for i in range(5)]].melt(value_name="Number", var_name="Position")
    main_number_freq = main_numbers["Number"].value_counts().sort_index()

    # Analyze Mega Ball numbers
    mega_ball_freq = data["Mega Ball"].value_counts().sort_index()

    return main_number_freq, mega_ball_freq

# Function to visualize frequency
def visualize_frequency(main_freq, mega_freq):
    """Visualizes the frequency of numbers."""
    # Plot the frequency of main numbers
    plt.figure(figsize=(12, 6))
    main_freq.plot(kind="bar", title="Frequency of Main Numbers", xlabel="Number", ylabel="Frequency")
    plt.show()

    # Plot the frequency of Mega Ball numbers
    plt.figure(figsize=(12, 6))
    mega_freq.plot(kind="bar", title="Frequency of Mega Ball Numbers", xlabel="Number", ylabel="Frequency")
    plt.show()

if __name__ == "__main__":
    # Example usage
    filepath = "../data/mega_millions_data.csv"  # Adjust path if necessary
    data = load_data(filepath)

    main_freq, mega_freq = analyze_frequency(data)
    visualize_frequency(main_freq, mega_freq)