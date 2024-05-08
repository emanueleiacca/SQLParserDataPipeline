import re

def extract_unnest_transformations(query):
    results = []
    
    # Find all JOIN operations and their contents up to the next JOIN, WHERE, ORDER BY, or the end of the query
    joins = re.findall(r'\b(JOIN|CROSS JOIN|INNER JOIN|LEFT JOIN|RIGHT JOIN)\s+(.*?)(?= JOIN|\sWHERE|\sORDER BY|\sLIMIT|;|$)', query, re.DOTALL | re.IGNORECASE)

    for join_type, join_content in joins:
        # Check for UNNEST in each join
        unnests = re.findall(r'UNNEST\(\s*ARRAY\[(.*?)\]\)\s+AS\s+(\S+)', join_content, re.DOTALL | re.IGNORECASE)
        
        for unnest_content, alias in unnests:
            # Extract unique values within UNNEST arrays
            unique_values = list(set(re.findall(r'\(([^()]*)\)', unnest_content)))
            filtered_values = []
            for value in unique_values:
                # Split by comma and filter out numeric or percent items
                items = [item.strip(" '") for item in value.split(',')]
                non_numeric_items = [item for item in items if not re.match(r'^\d+%?$', item)]
                filtered_values.extend(non_numeric_items)

            # Append results including type of join, alias, and unique values extracted
            results.append({
                'Join Type': join_type,
                'Alias': alias,
                'Unique Values': list(set(filtered_values))  # Use set to remove duplicates
            })

    return results
"""
# Example usage:
query = '''
SELECT t1.id,
       unnested_items.item_name,
       COUNT(*) OVER (PARTITION BY unnested_items.item_name) AS num_occurrences
FROM table1 t1
LEFT JOIN unnest(array[(1, 'apple'), (2, 'banana'), (3, 'apple'), (4, 'banana')]) AS unnested_items ON true;
'''

transformations = extract_unnest_transformations(query)
for transformation in transformations:
    print(f"Join Type: {transformation['Join Type']}")
    print(f"Alias: {transformation['Alias']}")
    print(f"Unique Values: {transformation['Unique Values']}")
    print()
"""

#Unnest function is used to understand where the information provided by it comes from, it return the type of join used, its alias to find it in the select statement and its unique values, so the column name used to obtain the final output. It's useful in building pipelines