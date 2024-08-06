from sklearn.model_selection import train_test_split


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

    for i in range(n):
        stratify_cols = df[columns]

        if i == n - 1:
            batch = df

        else:
            df, batch = train_test_split(df, test_size=batch_size, stratify=stratify_cols)

        batches.append(batch)

    return batches
