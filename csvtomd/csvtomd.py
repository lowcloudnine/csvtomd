#!/usr/bin/env python3

"""
csvtomd v0.1.2

Convert your CSV files into Markdown tables.

More info: http://github.com/mplewis/csvtomd
"""

import argparse
from csv import reader


def check_negative(value):
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            '"%s" must be an integer' % value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(
            '"%s" must not be a negative value' % value)
    return ivalue


def pad_to(unpadded, target_len):
    """
    Pad a string to the target length in characters, or return the original
    string if it's longer than the target length.
    """
    under = target_len - len(unpadded)
    if under <= 0:
        return unpadded
    return unpadded + (' ' * under)


def md_table(table, *, padding=1, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    # Output data buffer
    output = ''
    # Pad short rows to the length of the longest row to fix issues with
    # rendering "jagged" CSV files
    longest_row_len = max([len(row) for row in table])
    for row in table:
        while len(row) < longest_row_len:
            row.append('')
    # Get max length of any cell for each column
    col_sizes = [max(map(len, col)) for col in zip(*table)]
    # Set up the horizontal header dividers
    header_divs = [None] * len(col_sizes)
    num_cols = len(col_sizes)
    # Pad header divs to the column size
    for cell_num in range(num_cols):
        header_divs[cell_num] = header_div * (col_sizes[cell_num] +
                                              padding * 2)
    # Trim first and last padding chars, if they exist
    if padding > 0:
        header_div_row = divider.join(header_divs)[padding:-padding]
    else:
        header_div_row = divider.join(header_divs)
    # Pad each cell to the column size
    for row in table:
        for cell_num, cell in enumerate(row):
            row[cell_num] = pad_to(cell, col_sizes[cell_num])
    # Split out the header from the body
    header = table[0]
    body = table[1:]
    # Build the inter-column dividers using the padding settings above
    multipad = ' ' * padding
    divider = multipad + divider + multipad
    output += divider.join(header) + '\n'
    output += header_div_row + '\n'
    for row in body:
        output += divider.join(row) + '\n'
    # Strip the last newline
    if output.endswith('\n'):
        output = output[:-1]
    return output


def main():

    parser = argparse.ArgumentParser(
        description='Read one or more CSV files and output their contents in the '
                    'form of Markdown tables.')
    parser.add_argument('files', metavar='csv_file', type=str,
                        nargs='+', help='One or more CSV files to be converted')
    parser.add_argument('-n', '--no-filenames', action='store_false',
                        dest='show_filenames',
                        help="Don't display filenames when outputting multiple "
                             "Markdown tables.")
    parser.add_argument('-p', '--padding', type=check_negative, default=2,
                        help="The number of spaces to add between table cells "
                             "and column dividers. Default is 2 spaces.")
    parser.add_argument('-d', '--delimiter', default=',',
                        help="CSV delimiter, expected values: ',', ';'. Default is %(default)s")
    parser.add_argument('-c', '--comment', default='#',
                        help="Ignore comment lines, the default comment is %(default)s")

    args = parser.parse_args()
    first = True
    for file_num, filename in enumerate(args.files):
        # Print space between consecutive tables
        if not first:
            print('')
        else:
            first = False
        # Read the CSV files
        with open(filename, 'rU') as f:
            csv = reader(f, delimiter=args.delimiter)
            table = []
            for row in csv:
                # ignore the line if blank or starts with the comment symbol(s)
                if len(row) == 0 or row[0].startswith(args.comment):
                    pass
                else:
                    table.append(row)

        # Print filename for each table if --no-filenames wasn't passed and more
        # than one CSV was provided
        file_count = len(args.files)
        if args.show_filenames and file_count > 1:
            print(filename + '\n')
        # Generate and print Markdown table
        print(md_table(table, padding=args.padding))

if __name__ == '__main__':
    main()
