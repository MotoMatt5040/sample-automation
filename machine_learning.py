from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os


def stratified_split(df, columns, n: int = 20):
    """
    Stratified split a dataframe into n batches. A default of 20 is used when no amount is specified.
    :param df: pandas.dataframe
    :param columns: list of columns to stratify by
    :param n: amount of batches
    :return: batchified dataframes
    """

    stratify_col = df[columns].astype(str).agg('-'.join, axis=1)
    # print(stratify_col.to_string())
    # print(stratify_col.value_counts().to_string())
    # print(stratify_col.shape[0])

    # for col in columns:
    #     print(col, df[col].value_counts().shape[0])

    stratify_counts = stratify_col.value_counts()
    low_count_groups = stratify_counts[stratify_counts < n].index
    low_counts = df[stratify_col.isin(low_count_groups)]
    # print(low_counts.shape[0])
    df = df[~stratify_col.isin(low_count_groups)]

    batches = []
    batch_size = len(df) // n

    for i in range(n):
        stratify_col = df[columns].astype(str).agg('-'.join, axis=1)

        if i == n - 1:
            batch = df

        else:
            df, batch = train_test_split(df, test_size=batch_size, stratify=stratify_col)

        batches.append(batch)

    low_count_per_batch = len(low_counts) // n
    remainder = len(low_counts) % n
    start = 0

    for i in range(n):
        end = start + low_count_per_batch
        if i < remainder:
            end += 1
        batch_low_counts = low_counts.iloc[start:end]
        batches[i] = pd.concat([batches[i], batch_low_counts], ignore_index=True)
        start = end

    return batches


def plot_batches(batches, columns, source, save_dir='plots'):
    """
    Plot specified columns for each batch and save the plots to files.
    :param batches: list of pandas.DataFrame
    :param columns: list of columns to plot
    :param source:
    :param save_dir: directory to save the plots
    """

    # Create save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for i, batch in enumerate(batches):
        # print(f"Saving plots for Batch {i + 1}")
        plt.figure(figsize=(20, 15))

        # Track the position for subplots
        subplot_index = 1

        for col in columns:
            plt.subplot(len(columns), 1, subplot_index)  # Create subplot for each column
            custom_x_values = sorted(batch[col].astype(str).unique())  # Sort the unique values

            if pd.api.types.is_numeric_dtype(batch[col]):
                # Count values and reindex with custom x-values
                counts = batch[col].value_counts().reindex(custom_x_values, fill_value=0)
                ax = sns.barplot(x=custom_x_values, y=counts.values, color='blue')
                plt.ylabel('Count')
            else:
                ax = sns.countplot(x=batch[col].astype(str), order=custom_x_values, color='blue')
                plt.ylabel('Frequency')

            plt.title(f'Batch {i + 1} - {col}')
            plt.xlabel(col)

            for p in ax.patches:
                ax.annotate(
                    f'{p.get_height()}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='baseline',
                    fontsize=10, color='black', xytext=(0, 3),
                    textcoords='offset points'
                )

            # plt.xticks(rotation=45)
            subplot_index += 1
            # print(col, "PLOTTED")

        plt.tight_layout()  # Adjust layout to prevent overlap

        # Save the plot
        plot_filename = os.path.join(save_dir, f'{source}batch_{i + 1}.png')
        plt.savefig(plot_filename, format='png', dpi=300, bbox_inches='tight', pad_inches=0.1)
        plt.close()  # Close the figure to free memory
