import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    print('New change made for refactoring')

    while True:
        city = input("Would you like to see data for Chicago, New York, or Washington? ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please enter one of the provided cities.")

    while True:
        filter_type = input("Would you like to filter the data by month, day, or not at all? ").lower()
        if filter_type in ['month', 'day', 'none']:
            break
        else:
            print("Invalid input. Please enter 'month', 'day', or 'none'.")

    month = 'all'
    day = 'all'

    if filter_type == 'month':
        while True:
            month_input = input("Which month - January, February, March, April, May, or June? ").lower()
            if month_input in ['january', 'february', 'march', 'april', 'may', 'june']:
                month = month_input
                break
            else:
                print("Invalid input. Please enter a valid month.")

    elif filter_type == 'day':
        while True:
            day_input = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ").lower()
            if day_input in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                day = day_input
                break
            else:
                print("Invalid input. Please enter a valid day of the week.")

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
    try:
        df = pd.read_csv(CITY_DATA[city])
    except FileNotFoundError:
        print("Data file not found for the selected city.")
        return None

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print("Most common month:", common_month)

    common_day = df['day_of_week'].mode()[0]
    print("Most common day of week:", common_day)

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("Most common hour of day:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print("Most common start station:", common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print("Most common end station:", common_end_station)

    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Trip'].mode()[0]
    print("Most common trip:", common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time:", total_travel_time)

    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print("Counts of user types:")
    print(user_types)

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:")
        print(gender_counts)
    else:
        print("\nGender data not available for this city.")

    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print("\nEarliest birth year:", earliest_birth_year)
        print("Most recent birth year:", recent_birth_year)
        print("Most common birth year:", common_birth_year)
    else:
        print("\nBirth year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """
    Display raw data upon request by the user.
    """
    start_index = 0
    while True:
        print(df.iloc[start_index:start_index+5])
        start_index += 5
        more_raw_data = input('\nWould you like to see more raw data? Enter yes or no.\n')
        if more_raw_data.lower() != 'yes' or start_index >= len(df):
            break


def additional_questions(df):
    """
    Ask and answer additional questions about the data beyond the questions already provided.
    """
    print('\nAnswering Additional Questions...\n')
 
    # 1. Distribution of trip durations across different user types and genders
    if 'User Type' in df.columns:
        trip_duration_by_user_type = df.groupby('User Type')['Trip Duration'].mean()
        print("Average trip duration by user type:")
        print(trip_duration_by_user_type)
    else:
        print("\nUser type data not available for this city.")
 
    if 'Gender' in df.columns:
        trip_duration_by_gender = df.groupby('Gender')['Trip Duration'].mean()
        print("\nAverage trip duration by gender:")
        print(trip_duration_by_gender)
    else:
        print("\nGender data not available for this city.")
 
    # 2. Seasonal trends in bike share usage, and variation between cities
    if 'month' in df.columns:
        seasonal_trends = df.groupby('month').size()
        print("\nSeasonal trends in bike share usage (Trip counts by month):")
        print(seasonal_trends)
    else:
        print("\nMonth data not available for this city.")
 
 
    # 3. Average trip duration variation based on time of day or day of the week
    if 'hour' in df.columns:
        avg_trip_duration_by_hour = df.groupby('hour')['Trip Duration'].mean()
        print("\nAverage trip duration by hour of the day:")
        print(avg_trip_duration_by_hour)
    else:
        print("\nHour data not available for this city.")
 
    if 'day_of_week' in df.columns:
        avg_trip_duration_by_day = df.groupby('day_of_week')['Trip Duration'].mean()
        print("\nAverage trip duration by day of the week:")
        print(avg_trip_duration_by_day)
    else:
        print("\nDay of week data not available for this city.")
 
 
    # 4. Popularity of bike share usage between weekdays and weekends
    if 'day_of_week' in df.columns:
        df['weekend'] = df['day_of_week'].apply(lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday')
        weekend_vs_weekday = df.groupby('weekend').size()
        print("\nBike share usage between weekdays and weekends:")
        print(weekend_vs_weekday)
    else:
        print("\nDay of week data not available for this city.")
 
    # 5. Busiest hours of the day for bike share usage, and comparison between cities
    if 'hour' in df.columns:
        busiest_hours = df.groupby('hour').size()
        print("\nBusiest hours of the day for bike share usage (Trip counts by hour):")
        print(busiest_hours)
    else:
        print("\nHour data not available for this city.")
 
    print('-'*40)
 

def main():
    while True:
        city, month, day = get_filters()
        if city is None:
            continue  # Skip to the next iteration if city data is not found

        df = load_data(city, month, day)
        if df is None:
            continue  # Skip to the next iteration if data loading fails

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data_display = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if raw_data_display.lower() == 'yes':
            display_raw_data(df)

        additional_questions_prompt = input('\nWould you like to explore additional questions about the data? Enter yes or no.\n')
        if additional_questions_prompt.lower() == 'yes':
            additional_questions(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
