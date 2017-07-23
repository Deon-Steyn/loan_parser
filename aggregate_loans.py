 #!/usr/bin/python3
import os
import argparse
import csv
import logging
import logging.handlers

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
LOG_FILENAME = os.path.basename(__file__)+'.log'
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=10485760, backupCount=3)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def validate_file(filename, required_columns):
    """Validate CSV file contains required columns"""
    logger.debug("Checking required columns %s", required_columns)
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')

        for column in required_columns:
            if column not in reader.fieldnames:
                logger.critical('File must contain column named \'%s\'' % column, exc_info=True)
                exit


def load_totals_from_CSV(filename=None):
    """Return dictionary of aggregates loaded from CSV file
    
    Dictionary key: tuple of columns (Network,Product,Date)
    Dictionary val: aggregate of Amount column and counter
    """

    if filename is None:
        filename = args.input
    
    logger.debug('Parsing input file %s', filename)

    validate_file(filename, required_columns=('Network','Product','Date','Amount'))

    with open(filename) as loanfile:
        reader = csv.DictReader(loanfile, delimiter=',')
        mydict = {}
        for rownum, row in enumerate(reader):
            try:
                key = (row['Network'].lstrip('\'').rstrip('\''), 
                       row['Product'].lstrip('\'').rstrip('\''),
                       row['Date'][4:].rstrip('\''))

                if key in mydict:
                    mydict[key][0] += float(row['Amount'])
                    mydict[key][1] += 1
                else:
                    mydict[key] = [float(row['Amount']), 1]

            except:
                logger.critical('Loans.csv line %d is invalid!' % (rownum+1), exc_info=True)

        logger.info('Read %d records from %s' % (rownum, filename))
    return mydict


def write_dict_to_CSV(lines, filename=None):
    """Write dictionary as CSV file"""

    if filename is None:
        filename = args.output

    logger.debug('Writing to output file %s', filename)

    with open(filename, 'w', newline='') as f:
        w = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, quotechar="'", delimiter=',', lineterminator='\n')
        if args.no_output_header is not True:
            w.writerow(['Network','Product','Month','Amount','Count'])
        for key, value in lines.items():
            w.writerow(list(key) + value)

    logger.info('Created %s' % filename)

if __name__ == '__main__':
    """Aggregate loan amounts by (Network, Product, Month) for Loans.CSV file"""

    parser = argparse.ArgumentParser(allow_abbrev=False,
                                    description='Aggregate amount from input file and output to CSV file')

    parser.add_argument('--input', default='Loans.csv', help='CSV file to parse')
    parser.add_argument('--output', default='Output.csv', help='CSV file to store aggregates')
    parser.add_argument('--no_output_header', action="store_true", help='No column header in output file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--verbose', action="store_true", help='Log all messages to log file')
    group.add_argument('--nolog', action="store_true", help='Do not create log file')
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.nolog:
        logger.removeHandler(handler)

    # Process file
    logger.info("--------------------------------------------------------------")
    logger.info("Aggregating totals from %s into CSV file %s" % (args.input, args.output))
    totals = load_totals_from_CSV()
    write_dict_to_CSV(totals)
