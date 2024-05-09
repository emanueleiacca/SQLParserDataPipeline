from From import *
from Select import *
from Unnest import *
query = """
SELECT t1.id,
       unnested_items.item_name,
       COUNT(*) OVER (PARTITION BY unnested_items.item_name) AS num_occurrences
FROM table1 t1
LEFT JOIN unnest(array[(1, 'apple'), (2, 'banana'), (3, 'apple'), (4, 'banana')]) AS unnested_items ON true;
"""

# Parse the SELECT clause
parsed_query = parse_select_statement(query)
print(parsed_query)

# Analyze the FROM clause
from_analysis = extract_tables_and_aliases(query)
print(from_analysis)

# Extract UNNEST transformations
unnest_details = extract_unnest_transformations(query)
print(unnest_details)