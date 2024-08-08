from itemadapter import ItemAdapter

class BookscraperPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                if value:
                    adapter[field_name] = value.strip()

        ## Category & Product Type --> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            if value:
                adapter[lowercase_key] = value.lower()

        ## Price --> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            if value:
                value = value.replace('£', '')
                adapter[price_key] = float(value)

        ## Availability --> extract number of books in stock
        availability_string = adapter.get('availability')
        if availability_string:
            split_string_array = availability_string.split('(')
            if len(split_string_array) < 2:
                adapter['availability'] = 0
            else:
                availability_array = split_string_array[1].split(' ')
                adapter['availability'] = int(availability_array[0])

        ## Reviews --> convert string to number
        num_reviews_string = adapter.get('num_reviews')
        if num_reviews_string:
            adapter['num_reviews'] = int(num_reviews_string)
        
        ## Stars --> convert text to number
        stars_string = adapter.get('stars')
        if stars_string:
            split_stars_array = stars_string.split(' ')
            stars_text_value = split_stars_array[1].lower()
            if stars_text_value == "zero":
                adapter['stars'] = 0
            elif stars_text_value == "one":
                adapter['stars'] = 1
            elif stars_text_value == "two":
                adapter['stars'] = 2
            elif stars_text_value == "three":
                adapter['stars'] = 3
            elif stars_text_value == "four":
                adapter['stars'] = 4
            elif stars_text_value == "five":
                adapter['stars'] = 5

        return item

import mysql.connector
import os

class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='3Ng05190699',
            database='books'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        ## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment, 
            url VARCHAR(255),
            title TEXT,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax FLOAT,
            price_incl_tax FLOAT,
            tax FLOAT,
            price FLOAT,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description TEXT,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## Ensure all fields are present
        for field in adapter.field_names():
            if adapter.get(field) is None:
                self.logger.error(f"Missing field {field} in item: {item}")
                return item

        ## Define insert statement
        self.cur.execute(""" 
        INSERT INTO books (
            url, 
            title, 
            upc, 
            product_type, 
            price_excl_tax,
            price_incl_tax,
            tax,
            price,
            availability,
            num_reviews,
            stars,
            category,
            description
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )""", (
            adapter["url"],
            adapter["title"],
            adapter["upc"],
            adapter["product_type"],
            adapter["price_excl_tax"],
            adapter["price_incl_tax"],
            adapter["tax"],
            adapter["price"],
            adapter["availability"],
            adapter["num_reviews"],
            adapter["stars"],
            adapter["category"],
            adapter["description"]
        ))

        ## Execute insert of data into database
        self.conn.commit()

        return item
    
    def close_spider(self, spider):
        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()
