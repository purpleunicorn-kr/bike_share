import time
import pandas as pd
import numpy as np

# City Dictionary
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = ""

    city_names = list(CITY_DATA.keys())
    while not (city in city_names):
        city = input(f"Enter a valid city name {city_names}: ").lower()


    # get user input for month (all, january, february, ... , june)
    month = ""
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    while not (month in valid_months):
        month = input(f"Enter a valid month ex) 'all', 'january' ... 'december': ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while not (day in valid_days):
        day = input(f"Enter a valid day ex) 'all', 'monday' ... 'sunday': ").lower()


    print(f"\nYou enterd '{city}' and '{month}' and '{day}'")
    print('-'*40)



    return city, month, day


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

    file_path = CITY_DATA[city]
 
    df_city = pd.read_csv(file_path)


    # Convert 'Start Time' to datetime format
    df_city['Start Time'] = pd.to_datetime(df_city['Start Time'])

    df_city['Month'] = df_city['Start Time'].dt.strftime('%B').str.lower()
    df_city['Day'] = df_city['Start Time'].dt.day_name().str.lower()
    
    # "all"이 아닌 경우 필터 적용
    if month != 'all':
        df_city = df_city[df_city['Month'] == month]
    if day != 'all':
        df_city = df_city[df_city['Day'] == day]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month'].mode()[0]
    print(f"The most common month is: {common_month}")

    # display the most common day of week
    common_day = df['Day'].mode()[0]
    print(f"The most common day is: {common_day}")

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print(f"The most common hour is: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {common_start_station}")

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {common_end_station}")

    # display most frequent combination of start station and end station trip
    start_and_end_station = df['Start Station'] + " , " + df['End Station']
    freq_start_and_end_station = start_and_end_station.mode()[0]
    print(f"The most frequent combination of start station and end station trip is: \n {freq_start_and_end_station}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    total_hours, total_mins, total_secs = get_hours_mins_secs(total_travel_time)
    print(f"The total travel time is {total_hours} hours {total_mins} minutes {total_secs} seconds")


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_hours, mean_mins, mean_secs = get_hours_mins_secs(mean_travel_time)

    print(f"The mean travel time is {mean_hours} hours {mean_mins} minutes {mean_secs} seconds")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_hours_mins_secs(total_time):
    hours = int(total_time//3600)
    mins = int((total_time%3600)//60)
    secs = round(total_time%60,2)    
    return hours, mins, secs


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_of_user_type = df['User Type'].value_counts()
    print("The counts of user types")
    print('-'*40)
    print(f"{counts_of_user_type}\n")

    # Display counts of gender
    if 'Gender' in df.columns:
        counts_of_gender = df['Gender'].value_counts()
        print("The counts of gender")
        print('-'*40)
        print(f"{counts_of_gender}\n")
    else:
        print("No gender data available.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        min_birth_year = int(df['Birth Year'].min())
        print(f"The earlest year of birth is {min_birth_year}\n")

        max_birth_year = int(df['Birth Year'].max())
        print(f"The most recent year of birth is {max_birth_year}\n")

        common_birth_year = int(df['Birth Year'].mode()[0])
        print(f"The most common year of birth is {common_birth_year}")

    else:
        print("No birth year data available.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Displays raw data in increments of 5 rows based on user request.

    Args:
        df (DataFrame): The filtered DataFrame to display.
    """
    start_row = 0
    end_row = 5
    while True:
        show_data = input("\nWould you like to see 5 rows of raw data? Enter 'yes' or 'no': ").lower()
        if show_data == 'yes':
            print(df.iloc[start_row:end_row])
            start_row += 5
            end_row += 5
            # Check if we've reached the end of the DataFrame
            if start_row >= len(df):
                print("\nNo more data to display.")
                break
        elif show_data == 'no':
            print("\nExiting raw data display.")
            break
        else:
            print("\nInvalid input. Please enter 'yes' or 'no'.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

	# It shows raw data
        display_raw_data(df)

        if len(df) == 0:
            print("The condition you specified has no matching data.")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
