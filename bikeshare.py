import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

session_data = {}

welcome_message = """
    Hello!, Welcome
    The bikeshare data for the following US states are explored by months (first 6 months) and days:
"""

city_dict = {'1': 'chicago', '2': 'new york', '3': 'washington'}

filter_dict = {'0': 'off', '1': 'month', '2': 'day', '3': 'both'}

month_dict = {'0': ['all', 'all months'], '1': ['jan', 'january'], '2': ['feb', 'february'],
                '3': ['mar', 'march'], '4': ['apr', 'april'],
                '5': ['may'], '6': ['jun', 'june']}

day_dict = {'0': ['all', 'all days'], '1': ['sun', 'sunday'], '2': ['mon', 'monday'], '3': ['tue', 'tuesday'],
            '4': ['wed', 'wednesday'], '5': ['thu', 'thursday'], '6': ['fri', 'friday'], '7': ['sat', 'saturday']}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_options = """
            [1] Chicago  [2] New York  [3] Washington
        """
        print(city_options)
        city = input("Select the number options or enter the city name to explore:\ncity->")
        if city != "" and get_input_helper(city_dict, city) is not None:
            city = get_input_helper(city_dict, city)
            session_data['city'] = city
            break
        else:
            print("[ERROR]> empty input for city OR input is not recognized. Try Again!")

    #get the filters to explore the data (none, month, day or both)
    while True:
        filter_options = """
            [0] none  [1] month  [2] day  [3] both
        """
        print(filter_options)
        filters = input("How would you like to filter the data? by month, day, both or none at all\nfilter->")
        if filters != "" and get_input_helper(filter_dict, filters) is not None:
            filters = get_input_helper(filter_dict, filters)
            session_data['filter'] = filters
            if filters == 'month':
                get_month_filter()
                session_data['day'] = "all days"
            elif filters == 'day':
                get_day_filter()
                session_data['month'] = "all months"
            elif filters == 'both':
                get_month_filter()
                get_day_filter()
            else:
                session_data['month'] = "all months"
                session_data['day'] = "all days"
            break
        else:
            print("[ERROR]> empty input for filter OR input is not recognized. Try Again!")
    ##End of get_filters
    return session_data['city'], session_data['month'], session_data['day']

def get_input_helper(inDict, inParam):
    """Helper function to find and validate the inputs from the user"""

    rparam = None
    for key, val in inDict.items():
        if key == inParam or inParam.lower() == val:
            rparam = inDict[key] if type(inDict[key]) == str else inDict[key][1]
    return rparam

def get_month_filter():
    """Gets user input for month (all, january, february, ... , june)"""

    while True:
        month_options = """
            [1] January      [2] February  [3] March
            [4] April        [5] May       [6] June
        """
        print(month_options)
        month = input("Select a month to explore:\nmonth->")
        if month != "" and get_input_helper(month_dict, month) is not None:
            month = get_input_helper(month_dict, month)
            session_data['month'] = month
            break
        else:
            print("[ERROR]> empty input for month OR input is not recognized. Try Again!")

def get_day_filter():
    """Gets user input for day of week (all, monday, tuesday, ... sunday)"""

    while True:
        day_options = """
            [1] Sunday    [2] Monday   [3] Tuesday
            [4] Wednesday [5] Thursday [6] Friday   [7] Saturday
        """
        print(day_options)
        day = input("Select a day of the week to explore:\nday->")
        if day != "" and get_input_helper(day_dict, day) is not None:
            day = get_input_helper(day_dict, day)
            session_data['day'] = day
            break
        else:
            print("[ERROR]> empty input for day OR input is not recognized. Try Again!")

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
    start_time = time.time()
    print(f"Loading data for {city.title()} ...")
    for key in CITY_DATA.keys():
        if key == city:
            df = pd.read_csv(CITY_DATA[key], index_col=0)

    #Data Wrangling
    df['Start Time'] = df['Start Time'].astype('datetime64[ns]')
    df['End Time'] = df['End Time'].astype('datetime64[ns]')
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour
    df['Combi Station'] = df['Start Station'] + " to " + df['End Station']

    #Select data by filters
    if month != "all months" and day == "all days":
        df = df[df['Month'] == month.title()]
    elif month == "all months" and day != "all days":
        df = df[df['Day'] == day.title()]
    elif month != "all months" and day != "all days":
        df = df[(df['Month'] == month.title()) & (df['Day'] == day.title())]
    else:
        pass
    exec_time = time.time() - start_time
    print("This took ", exec_time, "seconds")
    return df
    ##End of load_data

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    print(f"Most common month: {df['Month'].value_counts().idxmax()} - {df['Month'].value_counts().max()} counts")

    # display the most common day of week
    print(f"Most common day of the week: {df['Day'].value_counts().idxmax()} - {df['Day'].value_counts().max()} counts")

    # display the most common start hour
    start_hr = int(df['Hour'].value_counts().idxmax())
    str_hr = str(start_hr)+".00AM" if (start_hr <= 12) else str(start_hr - 12)+".00PM"
    print(f"Most common start hour: {str_hr} - {df['Hour'].value_counts().max()} counts")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"Most commonly used start station: {df['Start Station'].value_counts().idxmax()} - {df['Start Station'].value_counts().max()} counts")

    # display most commonly used end station
    print(f"Most commonly used end station: {df['End Station'].value_counts().idxmax()} - {df['End Station'].value_counts().max()} counts")

    # display most frequent combination of start station and end station trip
    print(f"Most commonly used combination of stations: {df['Combi Station'].value_counts().idxmax()} - {df['Combi Station'].value_counts().max()} counts")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(f"Total travel time: {df['Trip Duration'].sum()} seconds")

    # display mean travel time
    print(f"Mean travel time: {round(df['Trip Duration'].mean(), 2)} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"Distribution of Users:\n{df['User Type'].value_counts()}")

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
    except Exception as e:
        print("\nNo data for 'Gender' to explore")
    else:
        print(f"\nDistribution of Gender:\n{gender}")

    # Display earliest, most recent, and most common year of birth
    try:
        early_yr = df['Birth Year'].min()
        recent_yr = df['Birth Year'].max()
        common_yr = df['Birth Year'].value_counts().idxmax()
        common_yr_count = df['Birth Year'].value_counts().max()
    except Exception as e:
        print("\nNo data for 'Birth Year' to explore")
    else:
        print("\n")
        print(f"Birth Year of Oldest User: {int(early_yr)}")
        print(f"Birth Year of Youngest User: {int(recent_yr)}")
        print(f"Birth Year of Most Common Users: {int(common_yr)} ({common_yr_count} users)")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def welcome():
    """Prints the welcome message to the user"""

    print(welcome_message)

def display_5rows(df):
    """Generates 5 rows of the DataFrame for display"""

    row_count = 0
    row_gap = 20
    while True:
        rows_to_display = input("Do you want to view the filtered dataframe? Enter Yes(Y) or No(N): ")
        if rows_to_display.lower() in ['y', 'yes']:
            start_time = time.time()
            if len(df) - (row_count + row_gap) >= row_gap:
                print(f"\nViewing rows {row_count + 1} to {row_count + row_gap} of the filtered dataset")
                rows = df.iloc[row_count : row_count + row_gap]
                row_count = row_count + row_gap
                print(rows)
            else:
                print(f"\nViewing rows {row_count + 1} to {len(df)} of the filtered dataset")
                rows = df.iloc[row_count : len(df) + 1]
                print(rows)
            print("\nThis took %s seconds." % (time.time() - start_time))
        elif rows_to_display.lower() in ['n', 'no']:
            break
    print('-'*60)
    ##End of display_5_rows


def main():
    """Main Interface for the program"""

    city, month, day = get_filters()

    print('*'*60)
    print(f"Exploring the {city.title()} data for {month.title()} on {day.title()}")
    print('-'*60)

    df = load_data(city, month, day)
    print('-'*60)
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)
    display_5rows(df)
    while True:
        restart = input("\nWould you like to restart? Enter Yes(Y) or No(N): ")
        if restart.lower() in ['n', 'no']:
            print('-'*60)
            print("Exiting Application. Bye ...")
            print('-'*60)
            break
        elif restart.lower() in ['y', 'yes']:
            session_data = {}
            main()


if __name__ == "__main__":
    welcome()
    main()
