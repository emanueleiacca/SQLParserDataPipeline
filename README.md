# SQLParserDataPipeline Library

## Overview
The SQLParserDataPipeline is a powerful Python package designed for parsing and interpreting complex SQL queries. It was developed with a focus on BigQuery but is adaptable to other SQL dialects due to its flexible parsing strategy that doesn't consider the function itself but the most inner parentheses..
This Parser is specifically tuned to handle intricate query structures that go beyond the capabilities of standard SQL parsers.

### Features
- **Select Clause Parsing**: Handles a wide range of `SELECT` statements, from simple queries to those with nested statements, functions, and placeholders.
- **From Clause Analysis**: Identifies table names and associated aliases in medium complexity SQL queries, suitable for LeetCode-level challenges.
- **Unnest Transformations**: Extracts details from `UNNEST` operations, such as the type of join, aliases, and unique values, which are crucial for building data pipelines.

## Capabilities

### Select Function
The `select` function outperforms typical SQL parsers by accurately parsing column names in queries that include:
- Nested `SELECT` statements
- Functions within columns
- Use of placeholders and complex syntax

### From Function
The `from` function is optimized for medium complexity queries. It can accurately identify table names and their aliases within a query. Future updates aim to extend its capabilities to handle more complex scenarios.

### Unnest Function
The `unnest` function is crucial for understanding complex joins in queries. It returns:
- The type of join used
- The alias of the join, for easy reference in `SELECT` statements
- Unique values of columns involved in the `UNNEST` operation

This function is particularly useful for those developing data pipelines where understanding the flow of data transformation is critical.

## Getting Started

To get started with SQL Query Tools, install the package using pip:

```bash
pip SQLParserDataPipeline==0.5
```

## Usage

An example on how to call the functions and use the library is provided on Usage.py , feel free to use it with your queries

## Avaible functions
- from SQLParserDataPipeline.Select import parse_select_statement
- from SQLParserDataPipeline.From import extract_tables_and_aliases
- from SQLParserDataPipeline.Unnest import extract_unnest_transformations

## Queries Examples

On Example_Query.SQL a few examples were provided to demostrate how our library perform on gradually more complex queries. In each example we experiment a potential issue that other parser can't deal with.

## Info Regarding the library

All the info regarding the library can be found on [PYPI site](https://pypi.org/project/SQLParserDataPipeline/)
