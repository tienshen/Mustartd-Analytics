#!/usr/bin/python
import sys
import csv
import datetime

class Location:
    def __init__(self, loc, count):
        self.loc = loc
        self.count = count
    def __repr__(self):
        return repr((self.loc, self.count))

# COMPSCI 383 Homework 0 
#  
# Fill in the bodies of the missing functions as specified by the comments and docstrings.


# Exercise 0. (8 points)
#  
def read_data(file_name):
    """Read in the csv file and return a list of tuples representing the data.

    Transform each field as follows:
      date: class date (see datetime module)
      mileage: integer
      location: string
      gallons: float
      price: float

    Do not return a tuple for the header row.  While you can process the rawtext using string
    functions, to receive full credit you must use Python's built in csv module.
    """

    rows = []
    #
    # fill in function body here
    #
    # open file
    with open(file_name, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        csvreader.__next__() # skips the header row

        for row in csvreader:
            if row[0] is not '': # check if field is valid
                date = row[0].split('/') # split date into m, d, y
                row[0] = datetime.date(int(date[2]), int(date[0]), int(date[1]))
            if row[1] is not '': # mileage
                row[1] = int(row[1])
            if row[2] is not '': # location
                row[2] = str(row[2])
            if row[3] is not '': # gallons
                row[3] = float(row[3])
            if row[4] is not '': # price
                row[4] = float(row[4][1:])
            rows.append(row)
        print(rows)

    return rows


# Exercise 1. (5 points)
#
def total_cost(rows):
    """Return the total amount of money spent on gas as a float.  Depressing."""
    #
    # fill in function body here
    #

    cost = 0
    for row in rows:
        if row[4] is not '':
            cost += row[4]

    return cost


# Exercise 2. (5 points)
#
def num_single_locs(rows):
    """Return the number of refueling locations that were visited exactly once."""
    #
    # fill in function body here
    #

    loclist =[]

    # check if location is already in the list.
    # if it is, it means it was visited more than once, so we remove it
    # otherwise, the location is new and we add it to the list
    for row in rows:
        loc = row[2]
        if loc in loclist:
            loclist.remove(loc)
        else:
            loclist.append(loc)

    return len(loclist)


# Exercise 3. (8 points)
#
def most_common_locs(rows):
    """Return a list of the 10 most common refueling locations, along with the number of times
    they appear in the data, in descending order.  Each list item should be a two-element tuple
    of the form (name, count):
    ("Honolulu, HI", 42)

    Hint: store the locations and counts in a dictionary, then convert the dictionary into a list of
    tuples that can be sorted using Python's sorted() or sort() functions (the "Key Functions"
    section of https://docs.python.org/3.6/howto/sorting.html might be helpful).
    """
    #
    # fill in function body here
    #
    loclist = []
    for row in rows:
        if row[2] is not '':
            loclist.append(row[2])

    # sort the list first so its easier to count
    loclist.sort()
    # print(loclist)

    finallist = []
    count = 0
    prev = loclist[0]
    for item in loclist:
        if prev == item:
            count += 1
        else:
            # previous counting is done, store it into the finalllist
            finallist.append((prev,count))
            # setting new count
            prev = item
            count = 1
    # sort it and finish
    finallist = sorted(finallist, key = lambda student: student[1], reverse = True)
    # print(finallist)

    return finallist[0:9]


# Exercise 4. (8 points)
#
def state_totals(rows):
    """Return a dictionary containing the total number of visits (value) for each state as designated by
    the two-letter abbreviation at the end of the location string (keys).  To do this, you'll have to pull
    apart the location string and extract the state abbreviation.

    The return value should be of the form:
        { "CA" -> 42,
          "HI" -> 19,
          etc. }
    """
    #
    # fill in function body here
    #
    loclist = []
    for row in rows:
        if row[2] is not '':
            loc = row[2].split(', ')
            loclist.append(loc[-1])

    loclist.sort()

    finaldict = {}
    count = 0
    prev = loclist[0]
    for item in loclist:
        if prev == item:
            count += 1
        else:
            # previous counting is done, store it into the finaldict
            finaldict[prev] = count
            # setting new count
            prev = item
            count = 1

    return finaldict


# Exercise 5. (8 points)
#
def num_unique_dates(rows):
    """
    Return the total number unique dates in the calendar year that refueling took place.
    (This number should be less than 366!)
    """
    #
    # fill in function body here
    #
    datelist = []
    for row in rows:
        if row[0] is not '':
            # convert date object to tuples of month, day and append to the date list
            datelist.append((row[0].month, row[0].day))

    uniquelist = []

    # check if date is already in the unique list.
    # if it is, it means it was visited more than once
    # otherwise, the date is new and we add it to the list
    for date in datelist:
        if date not in uniquelist:
            uniquelist.append(date)

    return len(uniquelist)


# Exercise 6. (8 points)
#
def month_avg_price(rows):
    """Return a dictionary containing the average price per gallon as a float (values) for each month (keys).

    Use the functions in Python's datetime module to parse and manipulate the date objects.

    The return value should be of the form:
        { "January" -> 3.12,
          "February" -> 2.89,
          ... }
    """
    #
    # fill in function body here
    #
    tuples = []
    for row in rows:
        if row[0] is not '' and row[3] is not '' and row[4] is not '': # making sure all fields in use are not blank
            tuples.append((row[0].strftime('%B'), row[4]/row[3]))

    # tuples = sorted(tuples, key = lambda t: datetime.datetime.strptime(t[0], '%B').month)
    tuples = sorted(tuples, key = lambda student: student[0])

    dict = {}
    prev = tuples[0][0]
    count = 1
    price = 0
    for tuple in tuples:
        if prev == tuple[0]:
            count += 1
            price += tuple[1] #add to the price
        else:
            x = price/count
            dict[prev] = x

            count = 1
            prev = tuple[0]
            price = 0

    return dict

# EXTRA CREDIT (+10 points)
#
def highest_thirty(rows):
    """Return the start and end dates for top three thirty-day periods with the most miles driven.

     The periods should not overlap (you should select them in a greedy manner; that is, find the
     highest mileage period first, and then select the next highest that is outside that window).
     Return a list with the start and end dates (as a Python datetime object) for each period,
     followed by the total mileage, stored in a tuple.  Again, you should use the date wrangling
     functions found in Python's datetime module to manipulate the dates.

    The return value should be of the form:
        [ (1995-02-14, 1995-03-16, 502),
          (1991-12-21, 1992-01-16, 456),
          (1997-06-01, 1997-06-28, 384) ]
    """
    #
    # fill in function body here
    #


    return []  # fix this!


# The main() function below will be executed when your program is run.
# Note that Python does not require a main() function, but it is
# considered good style (as is including the __name__ == '__main__'
# conditional below)
#
def main(file_name):
    rows = read_data(file_name)
    print("Exercise 0: {} rows\n".format(len(rows)))

    cost = total_cost(rows)
    print("Exercise 1: ${:.2f}\n".format(cost))

    singles = num_single_locs(rows)
    print("Exercise 2: {}\n".format(singles))

    print("Exercise 3:")
    for loc, count in most_common_locs(rows):
        print("\t{}\t{}".format(loc, count))
    print("")

    print("Exercise 4:")
    for state, count in sorted(state_totals(rows).items()):
        print("\t{}\t{}".format(state, count))
    print("")

    unique_count = num_unique_dates(rows)
    print("Exercise 5: {}\n".format(unique_count))

    print("Exercise 6:")
    for month, price in sorted(month_avg_price(rows).items(),
                               key=lambda t: datetime.datetime.strptime(t[0], '%B').month):
        print("\t{}\t${:.2f}".format(month, price))
    print("")

    print("Extra Credit:")
    for start, end, miles in sorted(highest_thirty(rows)):
        print("\t{}\t{}\t{} miles".format(start.strftime("%Y-%m-%d"),
                                          end.strftime("%Y-%m-%d"), miles))
    print("")


#########################

if __name__ == '__main__':
    
    data_file_name = 'mustard_data.csv'  # you must pass in the path to the data file
    main(data_file_name)




