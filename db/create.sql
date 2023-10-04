CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL
);

CREATE TABLE Sellers (
    id INT NOT NULL UNIQUE REFERENCES Users(id),
    email_address VARCHAR UNIQUE NOT NULL,
    business_address VARCHAR NOT NULL
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) NOT NULL,
    creator_id INT NOT NULL REFERENCES Users(id), -- must be a user to be a creator? Do we want that constraint?
    category VARCHAR(255) NOT NULL,
    product_description VARCHAR(255) NOT NULL,
    price DECIMAL(12,2) NOT NULL
); -- not sure how to include 'image'

CREATE TABLE Balance (
    user_id INT NOT NULL REFERENCES Users(id),
    balance_timestamp timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    balance FLOAT NOT NULL
);

CREATE TABLE Search (
    user_id INT NOT NULL REFERENCES Users(id),
    search_timestamp timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    query VARCHAR
);

CREATE TABLE CartContents (
    user_id INT NOT NULL REFERENCES Users(id),
    product_id INT NOT NULL REFERENCES Products(id),
    seller_id INT NOT NULL REFERENCES Sellers(id),
    quantity INT NOT NULL CHECK (quantity >= 0)
);

CREATE TABLE SavedForLaterContents (
    user_id INT NOT NULL REFERENCES Users(id),
    product_id INT NOT NULL REFERENCES Products(id),
    seller_id INT NOT NULL REFERENCES Sellers(id),
    quantity INT NOT NULL CHECK (quantity >= 0)
);

CREATE TABLE HasInventory (
    seller_id INT NOT NULL REFERENCES Sellers(id),
    product_id INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL CHECK (quantity >= 0)
);

CREATE TABLE OrderFact (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    buyer_id INT NOT NULL REFERENCES Users(id),
    total_price FLOAT NOT NULL CHECK (total_price > 0),
    fufillment_status BOOLEAN DEFAULT False,
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE OrderContents (
    order_id INT NOT NULL REFERENCES OrderFact(id),
    product_id INT NOT NULL REFERENCES Products(id),
    seller_id INT NOT NULL REFERENCES Sellers(id),
    quantity INT NOT NULL CHECK (quantity >= 0)
);

CREATE TABLE Fulfills (
    order_id INT NOT NULL REFERENCES OrderFact(id),
    seller_id INT NOT NULL REFERENCES Sellers(id),
    fufillment_status BOOLEAN DEFAULT False
);

CREATE TABLE ReviewedSeller (
    user_id INT NOT NULL REFERENCES Users(id),
    seller_id INT NOT NULL REFERENCES Sellers(id),
    review VARCHAR(500),
    time_reviewed_seller timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE ReviewedProduct (
    user_id INT NOT NULL REFERENCES Users(id),
    product_id INT NOT NULL REFERENCES Products(id),
    review VARCHAR(500),
    time_reviewed_product timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Wishes (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_added timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);