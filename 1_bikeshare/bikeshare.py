# ***********************************************************
# Author: Aaron Balson Caroltin .J
# Udacity Machine Learning Foundation ND 2018-2019
# Project - 1 (Bikeshare)
# Rubrics - https://review.udacity.com/#!/rubrics/1379/view
# ***********************************************************

import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None 
    while True:
        city = input('\nEnter name of city (as character): c-Chicago, n-New york, w-Washington\n').lower()
        if city == 'c':
            city = 'chicago'
            break
        elif city == 'n':
            city = 'new york city'
            break
        elif city == 'w':
            city = 'washington'
            break
        else:
            print("Invalid city, try again!\n")

    # Get user input for month (all, january, february, ... , june)
    month = None
    while True:
        month = input('\nEnter name of month: all, jan, feb, mar, apr, may, jun\n').lower()
        if month == 'all':
            break
        elif month == 'jan':
            month = 'january'
            break
        elif month == 'feb':
            month = 'february'
            break
        elif month == 'mar':
            month = 'march'
            break
        elif month == 'apr':
            month = 'april'
            break
        elif month == 'may':
            month = 'may'
            break
        elif month == 'jun':
            month = 'june'
            break
        else:
            print("Invalid month, try again!\n")
    
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    while True:
        day = input('\nEnter day of week: all, sun, mon, tue, wed, thu, fri, sat\n').lower()
        if day == 'all':
            break
        elif day == 'sun':
            day = 'sunday'
            break
        elif day == 'mon':
            day = 'monday'
            break
        elif day == 'tue':
            day = 'tuesday'
            break
        elif day == 'wed':
            day = 'wednesday'
            break
        elif day == 'thu':
            day = 'thursday'
            break
        elif day == 'fri':
            day = 'friday'
            break
        elif day == 'sat':
            day = 'saturday'
            break
        else:
            print("Invalid day, try again!\n")

    raw = input('\nShow Raw Data? y or n:\n').lower()
    print('-'*40)
    
    return city, month, day, raw


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # make datetime columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    df['Start Hour'] = df['Start Time'].dt.hour

    df['Route'] = df['Start Station'] + " to " + df['End Station']
    #df['Trip Seconds'] = (df['End Time'] - df['Start Time']) / timedelta(seconds=1)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        (dataframe) df - dataframe containing the selected city's data.
    Returns:
        None
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print('Most Common Month:', get_monthname(df['month'].mode()[0]))

    # Display the most common day of week
    print('Most Common Day of week:', df['day_of_week'].mode()[0])

    # Display the most common start hour
    print('Most Common Start Hour:', format_AMPM(df['Start Hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def format_AMPM(num):
    '''Returns AM/PM format from 24H format

    Args:
        (int) 0 - 23.
    Returns:
        (str) 17 returns "17 (5 PM)"
    '''
    return "{0} ({1})".format(num, (str(num-12) + " PM") if (num>12) else (str(num) + " AM"))


def get_monthname(num):
    '''Returns Month name from month number.

    Args:
        month number.
    Returns:
        (str) String represention of Month name e.g. returns January for 1
    '''
    
    if num == 0:
        return 'All'
    elif num == 1:
        return 'January'
    elif num == 2:
        return 'Febraury'
    elif num == 3:
        return 'March'
    elif num == 4:
        return 'April'
    elif num == 5:
        return 'May'
    elif num == 6:
        return 'June'
    else:
        return 'Unknown'

def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        (dataframe) df - dataframe containing the selected city's data.
    Returns:
        None
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    #print(df['Start Station'].value_counts())
    print('Most Common Start Station:', df['Start Station'].mode()[0])

    # Display most commonly used end station
    print('Most Common End Station:', df['End Station'].mode()[0])

    # Display most frequent combination of start station and end station trip
    print('Most Common Route:', df['Route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        (dataframe) df - dataframe containing the selected city's data.
    Returns:
        None
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #desc
    total_trips = df.shape[0]
    total_seconds = df['Trip Duration'].sum()
    mean_seconds = total_seconds / total_trips

    # Display total trips
    print('Total trips:', total_trips)

    # Display total travel time
    print('Total travel time:', '{0:.3f} seconds'.format(total_seconds))
    print_DHMS(total_seconds)

    # Display mean travel time
    print('Mean travel time:','{0:.3f} seconds'.format(mean_seconds))
    print_DHMS(mean_seconds)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def print_DHMS(duration):
    
    """Prints duration into days, hours, minutes, seconds format.
    Args:
        (int) duration - trip duration in seconds.
    Returns:
        None
    """

    sec = timedelta(seconds=int(duration))
    d = datetime(1,1,1) + sec
    print("   >>> %d days, %d hours, %d mins, %d seconds" % (d.day-1, d.hour, d.minute, d.second))


def user_stats(df, hide_gender_birth):
    """Displays statistics on bikeshare users.
    Args:
        (dataframe) df - dataframe containing the selected city's data
        (bool) hide_gender_birth - whether to calculate gender and birth year stats
    Returns:
        None
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    #print('Types of users:')
    #a = df.groupby('User Type')['User Type'].count()
    
    utypes = df.groupby(['User Type']).size().reset_index(name='counts')
    print(utypes, "\n")

    if (hide_gender_birth == False):
        # Display counts of gender
        #print('Gender distribution:')
        #print(df.groupby('Gender')['Gender'].count())
        gender = df.groupby(['Gender']).size().reset_index(name='counts')
        print(gender, "\n")
        # Display earliest, most recent, and most common year of birth
        print('Birth Years:')
        print("   >>> Oldest:", int(df['Birth Year'].min()))
        print("   >>> Youngest:", int(df['Birth Year'].max()))
        print("   >>> Most Common: year", int(df['Birth Year'].value_counts().idxmax()), "has", df['Birth Year'].value_counts().max(), "users born.")
    else:
        print('Gender, Birth Year stats N/A for this city\n')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def test_logics():
    """local testing function for testing date difference.
    Args:
        None
    Returns:
        None
    """

    d1 = datetime.now()
    time.sleep(5)
    d2 = datetime.now()
    secs = (d1-d2) / timedelta(seconds=1)
    print(secs)


def main():
    """main function used to start the application.
    Args:
        None
    Returns:
        None
    """    

    while True:
        city, month, day, raw = get_filters()
        df = load_data(city, month, day)

        if(raw=='y'):
            print(" ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Sample Raw Records ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n ")
            print(df.head())
            print(" ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n ")

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city=='washington')

        restart = input('\nWould you like to restart? Enter y or n.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
