import re

def extract_tables_and_aliases(query):
    # Normalize the query to simplify processing
    query = query.upper().replace('\n', ' ').replace('\t', ' ')
    
    # Use regex to find table names and aliases
    results = []
    # Define regex patterns for FROM/JOIN clauses, capturing table names and aliases
    pattern = re.compile(r'\b(?:FROM|JOIN)\b\s+(\w+)\s+(?:AS\s+(\w+)|(\w+))?\s*(?=(?:ON|LEFT JOIN|JOIN|WHERE|\bGROUP\b|\bHAVING\b|\bORDER\b|$))', re.IGNORECASE)
    matches = pattern.findall(query)
    for match in matches:
        table_name, alias1, alias2 = match
        # Determine the alias based on the matched groups
        alias = alias1 if alias1 else alias2
        # If alias is not provided, use an empty string
        results.append({"Table Name": table_name, "Alias": alias if alias else ''})
    
    # Additional step to remove aliases that are used in subqueries
    subquery_aliases = re.findall(r'\b(?:AS\s+)?(\w+)\s*$', query, re.IGNORECASE | re.MULTILINE)
    results = [res for res in results if res['Alias'] not in subquery_aliases]
    
    return results

# Example usage:
"""
query = 

'''
SELECT e.employee_name, d.department_name
FROM employees AS e
LEFT JOIN departments AS d ON e.department_id = d.department_id AND YEAR(e.hire_date) = 2020
ORDER BY d.department_name;
'''

print(extract_tables_and_aliases(query)) 
"""

#The from function is easier and can be upgraded to handle more difficult scenario. It's able to deal with medium level queries, it's able to find the table name and associated alias in query on LeetCode level. 
