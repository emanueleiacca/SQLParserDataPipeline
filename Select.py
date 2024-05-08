import re

def parse_select_statement(query):
    # Find the main SELECT ... FROM block, ignoring nested FROMs
    depth = 0  # Depth of nested parentheses
    select_start = query.upper().find('SELECT')
    if select_start == -1:
        return "Error: No SELECT keyword found in the query."
    
    # Start from the index found for 'SELECT' and find the first 'FROM' at top level
    from_index = -1
    for i in range(select_start, len(query)):
        char = query[i]
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif depth == 0 and query[i:i+4].upper() == 'FROM':
            from_index = i
            break

    if from_index == -1:
        return "Error: No valid top-level FROM found after SELECT."

    selected_columns = query[select_start + 6:from_index].strip()

    # Process to add a newline after top-level commas
    depth = 0  # Reset depth for parsing inside SELECT clause
    output = []
    for i, char in enumerate(selected_columns):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        
        output.append(char)

        # Ensure comma at top level gets new line if not followed by a newline and space
        if char == ',' and depth == 0:
            if i + 1 < len(selected_columns) and not selected_columns[i + 1:i + 3] == '\n ':
                output.append('\n ')

    selected_columns = ''.join(output)

    # Split into individual column definitions
    columns = selected_columns.strip().split('\n')

    processed_columns = []
    # Process each column for aliases and handle nested expressions
    for column in columns:
        column = column.strip()
        parts = column.rsplit(' AS ', 1)  # Split on last ' AS ' to correctly parse alias
        if len(parts) > 1: 
            column_name = parts[0].strip()
            alias = parts[1].strip()
        else:
            column_name = parts[0].strip()
            alias = column_name  # No alias provided

        processed_columns.append((column_name, alias))
# We procede with cleaning the output with deal with some problems like functions 
    updated_columns = []
    for column in processed_columns:
        text = column[0]
        while True:
    # To deal with function we select the innest parentheses to select only the important part of the row which contains the column name and its parameters
            innermost_texts = re.findall(r'\(([^()]*)\)', text)
            if not innermost_texts:
                break
    # Since we are only interested in the column name we remove all the unwanted part like parameters
            names = [item.split(',')[0].strip().replace("'", '').replace('$', '').split(' as ')[0] for item in innermost_texts]
            unique_names = [name for name in set(names) if not name.startswith('%')]
            for innermost_text in innermost_texts:
                text = re.sub(r'.*\(([^()]*)\).*', r', '.join(unique_names), text)
        updated_columns.append((text, column[1]))

    return updated_columns


"""
query = 
'''
SELECT 
    user_id,
    CONCAT(first_name, ' ', last_name) AS full_name,
    email,
    CONCAT('Phone: ', SUBSTR(phone_number, 1, 3), ' - ', SUBSTR(phone_number, 4, 3), '-', SUBSTR(phone_number, 7)) AS formatted_phone
FROM users;
'''
parsed_columns = parse_select_statement(query)
for column in parsed_columns:
    print(column)
"""

"""Select function deal with a wide range of select statement, from easy query like every other parser avaible online to more complex query with nested selected statement, function, use of placeholders and other difficulties we can find in our select statement.
It outperform other SQL Parser in python in parsing column name, this was the goal of a project I was doing and I didn't find a single parser able to deal with query a little bit more complex from the most basic one.
It was developed for BigQuery but it should be able to work on other dialect as well since it doesn't focus on the sintex bit in the nested structure of SQL queries.
I'm gonna point out a few queries that our library is able to parse correctly, difficulty goes from medium to really hard, you can try of course other queries:
"""