Copyright (c) 2017 Deon Steyn

-------------
What Is This?
-------------

The aggregate_loans.py file reads a CSV file (default name Loans.CSV) and 
aggregates the 'Amount' over combinations (or tuples) of 'Network', 'Product'
and 'Date' (month portion).

The aggregates are written to a new CSV file (default name Output.csv)

A rotating log is generated as aggregate_loans.py.log.1/2/3

-----------
Assumptions
-----------

    1 ) The input file contains a header record listing columns named:
        'Network', 'Product', 'Date', 'Amount'

    2 ) The Date format is "DD-MON-YYYY", e.g. '16-Apr-2017'

    3 ) Aggregation on "month" is month and year, e.g. 'Apr-2017' 
        not month ('Apr') only.

    4 ) Output file includes header row (column names)
        remove header with option:  --no_output_header


----------------------
Command Line arguments
----------------------

    python aggregate_loans.py [--input MyLoans.CSV] [--output MyResults.CSV] [--verbose | --nolog] [-h|--help]

    Optional arguments:
        -h, --help          show this help message and exit
        --input INPUT       CSV file to parse
        --output OUTPUT     CSV file to store aggregates
        --no_output_header  No column header in output file
        --verbose           Log all messages to log file
        --nolog             Do not create log file

    Examples:

        python aggregate_loans.py
        python aggregate_loans.py --verbose
        python aggregate_loans.py --input MyLoans.CSV --nolog
        python aggregate_loans.py --output MyResults.CSV
        python aggregate_loans.py --input MyLoans.CSV --output MyResults.CSV --verbose
