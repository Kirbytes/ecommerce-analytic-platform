USE alibaba_analysis;

-- Time dimension
CREATE TABLE dim_time (
    time_key INT PRIMARY KEY AUTO_INCREMENT, 
    full_datetime DATETIME,
    date_only DATE,
    hour_of_day INT,
    is_peak_hour BOOLEAN,  -- 10:00-20:00
    is_night BOOLEAN, -- 22:00-06:00
    day_of_week INT,
    is_weekend BOOLEAN,
    time_segment VARCHAR(20) -- 'Morning','Afternoon','Evening','Night'
);

-- Product dimension
CREATE TABLE dim_product (
    item_id BIGINT PRIMARY KEY,  
    category_list TEXT,
    property_list TEXT,
    brand_id BIGINT,
    city_id BIGINT,
    price_level INT,
    sales_level INT,
    collected_level INT,
    pv_level INT
);

-- User dimension
CREATE TABLE dim_user (
    user_id BIGINT PRIMARY KEY, 
    gender_id TINYINT,
    age_level INT,
    occupation_id INT,
    star_level INT
);

-- Shop dimension
CREATE TABLE dim_shop (
    shop_id BIGINT PRIMARY KEY, 
    review_num_level INT,
    review_positive_rate DECIMAL(5,4),
    star_level INT,
    score_service DECIMAL(5,4),
    score_delivery DECIMAL(5,4),
    score_description DECIMAL(5,4)
);

-- Sales fact table
CREATE TABLE fact_sales (
    time_key INT,
    item_id BIGINT,
    user_id BIGINT,
    shop_id BIGINT,
    total_views INT,
    total_purchases INT,
    conversion_rate DECIMAL(5,4),
    PRIMARY KEY (time_key, item_id, user_id, shop_id),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key),
    FOREIGN KEY (item_id) REFERENCES dim_product(item_id),
    FOREIGN KEY (user_id) REFERENCES dim_user(user_id),
    FOREIGN KEY (shop_id) REFERENCES dim_shop(shop_id)
);



-- Populate dim_time from contexts
INSERT INTO dim_time (full_datetime, date_only, hour_of_day, is_peak_hour, 
                     is_night, day_of_week, is_weekend, time_segment)
SELECT DISTINCT
    FROM_UNIXTIME(context_timestamp) as full_datetime,
    DATE(FROM_UNIXTIME(context_timestamp)) as date_only,
    HOUR(FROM_UNIXTIME(context_timestamp)) as hour_of_day,
    CASE 
        WHEN HOUR(FROM_UNIXTIME(context_timestamp)) BETWEEN 10 AND 20 THEN TRUE 
        ELSE FALSE 
    END as is_peak_hour,
    CASE 
        WHEN HOUR(FROM_UNIXTIME(context_timestamp)) BETWEEN 22 AND 23 
        OR HOUR(FROM_UNIXTIME(context_timestamp)) BETWEEN 0 AND 6 THEN TRUE 
        ELSE FALSE 
    END as is_night,
    DAYOFWEEK(FROM_UNIXTIME(context_timestamp)) as day_of_week,
    CASE 
        WHEN DAYOFWEEK(FROM_UNIXTIME(context_timestamp)) IN (1,7) THEN TRUE 
        ELSE FALSE 
    END as is_weekend,
    CASE 
        WHEN HOUR(FROM_UNIXTIME(context_timestamp)) BETWEEN 6 AND 11 THEN 'Morning'
        WHEN HOUR(FROM_UNIXTIME(context_timestamp)) BETWEEN 12 AND 17 THEN 'Afternoon'
        WHEN HOUR(FROM_UNIXTIME(context_timestamp)) BETWEEN 18 AND 21 THEN 'Evening'
        ELSE 'Night'
    END as time_segment
FROM contexts
ORDER BY full_datetime;

-- Populate dim_product from items
INSERT INTO dim_product
SELECT 
    item_id,
    item_category_list,
    item_property_list,
    item_brand_id,
    item_city_id,
    item_price_level,
    item_sales_level,
    item_collected_level,
    item_pv_level
FROM items;

-- Populate dim_user from users
INSERT INTO dim_user
SELECT 
    user_id,
    user_gender_id,
    user_age_level,
    user_occupation_id,
    user_star_level
FROM users;

-- Populate dim_shop from shops
INSERT INTO dim_shop
SELECT 
    shop_id,
    shop_review_num_level,
    shop_review_positive_rate,
    shop_star_level,
    shop_score_service,
    shop_score_delivery,
    shop_score_description
FROM shops;

-- Populate fact_sales
LOAD DATA LOCAL INFILE 'D:/emory/fall/bigdata/group_project/fact_sales.csv' 
INTO TABLE fact_sales
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- Add indexes
CREATE INDEX idx_time_date ON dim_time(date_only);
CREATE INDEX idx_fact_sales_time ON fact_sales(time_key);
CREATE INDEX idx_fact_sales_shop ON fact_sales(shop_id);



