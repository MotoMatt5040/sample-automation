from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def stratified_split(df, columns, n: int = 20):
    """
    Stratified split a dataframe into n batches. A default of 20 is used when no amount is specified.
    :param df: pandas.dataframe
    :param columns: list of columns to stratify by
    :param n: amount of batches
    :return: batchified dataframes
    """
    batches = []
    batch_size = len(df) // n
    stratify_col = df[columns].astype(str).agg('-'.join, axis=1)

    stratify_counts = stratify_col.value_counts()
    low_count_groups = stratify_counts[stratify_counts < n].index
    low_counts = df[stratify_col.isin(low_count_groups)]
    df = df[~stratify_col.isin(low_count_groups)]

    # print("Low count groups:")
    # print(low_count_groups)
    # print("Stratify column distribution (excluding low counts):")
    # print(df[columns].astype(str).agg('-'.join, axis=1).value_counts())

    for i in range(n):
        stratify_col = df[columns].astype(str).agg('-'.join, axis=1)
        # print("Stratify column distribution:")
        # print(stratify_col.value_counts())

        if i == n - 1:
            batch = df

        else:
            df, batch = train_test_split(df, test_size=batch_size, stratify=stratify_col)

        batches.append(batch)

    if batches:
        # print(low_counts.to_string())
        # print(low_counts.shape[0])
        batches[0] = pd.concat([batches[0], low_counts], ignore_index=True)

    return batches


def plot_batches(batches, columns, source, save_dir='plots'):
    """
    Plot specified columns for each batch and save the plots to files.
    :param batches: list of pandas.DataFrame
    :param columns: list of columns to plot
    :param save_dir: directory to save the plots
    """
    import os

    # Create save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for i, batch in enumerate(batches):
        # print(f"Saving plots for Batch {i + 1}")
        plt.figure(figsize=(15, 10))

        # Track the position for subplots
        subplot_index = 1

        for col in columns:
            plt.subplot(len(columns), 1, subplot_index)  # Create subplot for each column
            if pd.api.types.is_numeric_dtype(batch[col]):
                sns.barplot(x=batch[col].value_counts().index, y=batch[col].value_counts().values, color='blue')
                plt.title(f'Batch {i + 1} - {col}')
                plt.xlabel(col)
                plt.ylabel('Count')
            else:
                sns.countplot(x=batch[col], color='blue')
                plt.title(f'Batch {i + 1} - {col}')
                plt.xlabel(col)
                plt.ylabel('Frequency')
            subplot_index += 1

        plt.tight_layout()  # Adjust layout to prevent overlap

        # Save the plot
        plot_filename = os.path.join(save_dir, f'{source}batch_{i + 1}.png')
        plt.savefig(plot_filename, format='png', dpi=300, bbox_inches='tight', pad_inches=0.1)
        plt.close()  # Close the figure to free memory

        # print(f"Batch {i + 1} plots saved as {plot_filename}")