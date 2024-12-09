import pandas as pd
import numpy as np

def create_fact_sales():
    clicked_samples = pd.read_csv('clicked_sample.csv')
    contexts = pd.read_csv('context_table.csv')

    contexts['datetime'] = pd.to_datetime(contexts['context_timestamp'], unit='s')

    # Create time dimension
    time_dim = pd.DataFrame({
        'full_datetime': contexts['datetime'].unique()
    }).sort_values('full_datetime').reset_index()
    time_dim.rename(columns={'index': 'time_key'}, inplace=True)


    # Merge and aggregate
    df = clicked_samples.merge(contexts, on='context_id')
    df = df.merge(time_dim, left_on='datetime', right_on='full_datetime')

    # Calculate aggregations
    fact_sales = df.groupby(['time_key', 'item_id', 'user_id', 'shop_id']).agg(
        total_views=('instance_id', 'count'),
        total_purchases=('is_trade', 'sum')
    ).reset_index()

    fact_sales['conversion_rate'] = fact_sales['total_purchases'] / fact_sales['total_views']
    fact_sales['conversion_rate'] = fact_sales['conversion_rate'].round(4)

    # Save fact table
    fact_sales.to_csv('fact_sales.csv', index=False)

if __name__ == '__main__':
    create_fact_sales()