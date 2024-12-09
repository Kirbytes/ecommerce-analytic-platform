import pandas as pd
import numpy as np

def clean_list_field(field):
    """Clean fields containing semicolon-separated values"""
    if pd.isna(field):
        return []
    return str(field).split(';')

def clean_property_field(field):
    """Clean predict_category_property field with complex structure"""
    if pd.isna(field):
        return {}
    result = {}
    pairs = str(field).split(';')
    for pair in pairs:
        if ':' in pair:
            key, values = pair.split(':')
            result[key] = values.split(',') if ',' in values else [values]
    return result

# Define data types for all columns
dtypes = {
    'instance_id': 'int64',
    'item_id': 'int64',
    'item_brand_id': 'int64',
    'item_city_id': 'int64',
    'item_price_level': 'int32',
    'item_sales_level': 'int32',
    'item_collected_level': 'int32',
    'item_pv_level': 'int32',
    'user_id': 'int64',
    'user_gender_id': 'int32',
    'user_age_level': 'int32',
    'user_occupation_id': 'int32',
    'user_star_level': 'int32',
    'context_id': 'int64',
    'context_timestamp': 'int32',
    'context_page_id': 'int32',
    'shop_id': 'int64',
    'shop_review_num_level': 'int32',
    'shop_review_positive_rate': 'float64',
    'shop_star_level': 'int32',
    'shop_score_service': 'float64',
    'shop_score_delivery': 'float64',
    'shop_score_description': 'float64',
    'is_trade': 'int32'
}

try:
    # Read the original data
    df = pd.read_csv('round1_ijcai_18_train_20180301.txt', 
                     sep=' ', 
                     dtype=dtypes)
    
    # Clean list fields
    df['item_category_list'] = df['item_category_list'].apply(clean_list_field)
    df['item_property_list'] = df['item_property_list'].apply(clean_list_field)
    df['predict_category_property'] = df['predict_category_property'].apply(clean_property_field)

    # Create clicked sample DataFrame
    clicked_sample = df[[
        'instance_id', 'is_trade', 'item_id', 'user_id', 
        'context_id', 'shop_id'
    ]].copy()

    # Create advertising item DataFrame
    advertising_item = df[[
        'item_id', 'item_category_list', 'item_property_list', 
        'item_brand_id', 'item_city_id', 'item_price_level',
        'item_sales_level', 'item_collected_level', 'item_pv_level'
    ]].copy()

    # Create user DataFrame
    user_table = df[[
        'user_id', 'user_gender_id', 'user_age_level',
        'user_occupation_id', 'user_star_level'
    ]].copy()

    # Create context DataFrame
    context_table = df[[
        'context_id', 'context_timestamp', 'context_page_id',
        'predict_category_property'
    ]].copy()

    # Create shop DataFrame
    shop_table = df[[
        'shop_id', 'shop_review_num_level', 'shop_review_positive_rate',
        'shop_star_level', 'shop_score_service', 'shop_score_delivery',
        'shop_score_description'
    ]].copy()

    # Remove duplicates from dimension tables
    advertising_item.drop_duplicates(subset=['item_id'], inplace=True)
    user_table.drop_duplicates(subset=['user_id'], inplace=True)
    context_table.drop_duplicates(subset=['context_id'], inplace=True)
    shop_table.drop_duplicates(subset=['shop_id'], inplace=True)

    # Save to CSV files
    clicked_sample.to_csv('clicked_sample.csv', index=False)
    advertising_item.to_csv('advertising_item.csv', index=False)
    user_table.to_csv('user_table.csv', index=False)
    context_table.to_csv('context_table.csv', index=False)
    shop_table.to_csv('shop_table.csv', index=False)

    print("Data cleaning and separation completed successfully!")

except Exception as e:
    print(f"An error occurred: {str(e)}")