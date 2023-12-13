import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def box_chart(data, labels, c=[], bar_width=0.35, figsize=(8, 6), show_initial=True):
    """
    Create a box chart visualizing data for different labels.

    Args:
    - data (list): List of dictionaries containing data for each label.
    - labels (list): List of labels for x-axis.
    - c (list): List of colors for bars (optional).
    - bar_width (float): Width of each bar (optional).
    - figsize (tuple): Figure size (width, height) in inches (optional).
    - show_initial (bool): Whether to show initial values as bars (optional).

    Returns:
    - plt: Matplotlib plot object.

    This function generates a box chart using Matplotlib to visualize the provided data for different labels.
    It displays initial and average values for each label and visualizes min and max values with horizontal lines.
    """
    plt.rcParams['font.family'] = 'Segoe UI Emoji'

    labels_count = len(labels)
    index = np.arange(labels_count)
    plt.figure(figsize=figsize)  # Create a new figure with specified size

    initial_data = [data[i]["initial"] for i in range(labels_count)]  # Extract initial data for each label
    data_mins = []
    data_maxes = []
    data_means = []

    # Assign colors if not provided
    if len(c) < labels_count:
        c = (list(mcolors.TABLEAU_COLORS.keys())[:labels_count])

    for i in range(labels_count):
        recorded_data = data[i]["recorded"]

        initial_z = 1  # Z-order for initial values
        recorded_z = 2  # Z-order for recorded values

        data_mins.append(min(recorded_data))  # Calculate min value for the label
        data_maxes.append(max(recorded_data))  # Calculate max value for the label
        data_means.append(np.mean(recorded_data))  # Calculate mean value for the label

        if data_means[i] > initial_data[i]:  # Check if mean is greater than initial value for z-ordering
            initial_z = 2
            recorded_z = 1

        if show_initial:
            # Plot initial values as bars
            plt.bar(
                index[i], initial_data[i], bar_width, label='Initial', color=c[i], alpha=0.5,
                edgecolor='black', linewidth=1.2, hatch='///', zorder=initial_z
            )

        # Plot recorded data as bars
        plt.bar(
            index[i], data_means[i], bar_width, label='Average', color=c[i], alpha=0.5,
            edgecolor='black', linewidth=1.2, zorder=recorded_z
        )

        # Plot lines to indicate min and max values
        plt.plot([index[i], index[i]], [initial_data[i], data_maxes[i]], color='black', linewidth=1, zorder=3)
        plt.plot([index[i], index[i]], [0, data_mins[i]], color='black', linewidth=1, zorder=3)
        plt.plot([index[i] - 0.1, index[i] + 0.1], [data_mins[i], data_mins[i]], color='black', linewidth=1, zorder=3)
        plt.plot([index[i] - 0.1, index[i] + 0.1], [data_maxes[i], data_maxes[i]], color='black', linewidth=1, zorder=3)

        # Display min and max values next to the chart
        plt.text(index[i], data_mins[i] + 0.2, f"Min: {data_mins[i]}", color='black', fontsize=8, ha='center')
        plt.text(index[i], data_maxes[i] - 0.3, f"Max: {data_maxes[i]}", color='black', fontsize=8, ha='center')

    # Display values above bars
    for i, v in enumerate(initial_data):
        plt.text(i - 0.15, v + 0.1, str(v), color='black', fontweight='normal')

    for i, v in enumerate(data_means):
        plt.text(i + 0.2, v + 0.1, str(round(v, 2)), color='black', fontweight='bold')

    plt.xticks(index, labels)  # Set x-axis ticks to label values

    return plt  # Return the plot object
