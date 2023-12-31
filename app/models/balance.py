from flask import current_app as app
from flask import flash
from datetime import datetime
from .. import DB


class Balance:
    def __init__(self, user_id, balance_timestamp, balance):
        self.user_id = user_id
        self.balance_timestamp = balance_timestamp
        self.balance = balance

    @staticmethod
    def current_balance(user_id):
        rows = app.db.execute('''
SELECT user_id, balance_timestamp, balance 
FROM Balance 
WHERE user_id = :user_id 
ORDER BY balance_timestamp DESC 
LIMIT 1
''',
                              user_id=user_id)
        if rows:
            return rows[0][2]
        else:
            current_time = datetime.utcnow()
            # Assuming your Balance model has a 'user_id', 'balance_timestamp', and 'balance' fields
            app.db.execute('''
INSERT INTO Balance (user_id, balance_timestamp, balance)
VALUES (:user_id, :balance_timestamp, :balance)
''',
                            user_id=user_id,
                            balance_timestamp=current_time,
                            balance=0)
            # Fetch the newly created balance again to return it
            new_rows = app.db.execute('''
SELECT user_id, balance_timestamp, balance
FROM Balance 
WHERE user_id = :user_id 
ORDER BY balance_timestamp DESC 
LIMIT 1
''',
                                    user_id=user_id)
            return Balance(*(new_rows[0])) if new_rows else None
        
    @staticmethod
    def get_all_balance_by_uid(user_id):
        rows = app.db.execute('''
SELECT user_id, balance_timestamp, balance
FROM Balance
WHERE user_id = :user_id
ORDER BY balance_timestamp DESC
''',
                              user_id=user_id)
        return [Balance(*row) for row in rows]
    

    @staticmethod
    def get_paged_balance(user_id, page, per_page):
        offset = (page - 1) * per_page

        # Query to count the total number of balances for pagination
        total_count_query = '''
        SELECT COUNT(*)
        FROM Balance
        WHERE user_id = :user_id
        '''
        total_count = app.db.execute(total_count_query, user_id=user_id)
        total_count = total_count[0][0] if total_count else 0

        # Calculating the total number of pages
        total_pages = (total_count + per_page - 1) // per_page

        # Query to fetch specific range of orders
        transactions_query = '''
        SELECT user_id, balance_timestamp, balance
        FROM Balance
        WHERE user_id = :user_id
        ORDER BY balance_timestamp DESC
        LIMIT :limit OFFSET :offset
        '''
        transactions = app.db.execute(transactions_query, user_id=user_id, limit=per_page, offset=offset)

        # Convert rows to OrderFact objects if necessary
        # Assuming OrderFact is a class that can be instantiated with a row
        transactions = [Balance(*row) for row in transactions] if transactions else []

        return transactions, total_pages



    @staticmethod
    def calculate_new_balance(user_id, amount):
        latest_balance = Balance.current_balance(user_id)
        return latest_balance + amount
    

    @staticmethod
    def insert_new_balance(user_id, new_balance):
        current_time = datetime.utcnow()
        app.db.execute('''
            INSERT INTO Balance (user_id, balance_timestamp, balance)
            VALUES (:user_id, :balance_timestamp, :balance)
        ''',
        user_id=user_id,
        balance_timestamp=current_time,
        balance=new_balance)

    @staticmethod
    def first_balance_date(user_id):
        date = app.db.execute('''
        SELECT balance_timestamp
        FROM Balance
        WHERE user_id = :user_id
        ORDER BY balance_timestamp DESC 
        LIMIT 1
        ''',
        user_id=user_id)
        return date[0][0].year
