
query = """
SELECT user_id, CONCAT(first_name, ' ', last_name) AS full_name FROM users;
"""

# Parse the SELECT clause
parsed_query = sql_query_tools.select_function(query)
print(parsed_query)

# Analyze the FROM clause
from_analysis = sql_query_tools.from_function(query)
print(from_analysis)

# Extract UNNEST transformations
unnest_details = sql_query_tools.unnest_function(query)
print(unnest_details)
