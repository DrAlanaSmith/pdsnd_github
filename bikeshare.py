import time
import pandas as pd
import calendar

#valid inputs
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
VALID_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
VALID_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
VALID_ANSWER = ['yes', 'no']

def get_yes_no() -> bool:
    while True:
        answer = input().lower()
        if answer.startswith('y'):
            return True
        if answer.startswith('n'):
            return False
        else: 
            print("Invalid input. Please type yes or no.")

#get input filters from user
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). 
    print('Input Chicago, New York City, or Washington')
    city_valid = False
    while not city_valid: 
        city = input()
        city = city.lower()
        if city in CITY_DATA:
            city_valid = True
        else:
            print('Invalid input, please try again')
    # Get user input for month (all, january, february, ... , june)
    print('Please input month: all, January, February, ... , June')
    month_valid = False
    while not month_valid:
        global month
        month = input()
        month = month.lower()
        if month in VALID_MONTHS:
            month_valid = True
        else:
            print('Invalid month, please try again')

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    print('Please input day: all, Monday, Tuesday, ... Sunday')
    day_valid = False
    while not day_valid:
        global day
        day = input()
        day = day.lower()
        if day in VALID_DAYS:
            day_valid = True
        else:
            print('Invalid day, please try again')

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

    df = pd.read_csv(CITY_DATA[city])
    
    #extract date and time data
    df['Month'] = pd.to_datetime(df['Start Time']).dt.month
    df['Day'] = pd.to_datetime(df['Start Time']).dt.day
    df['Datetime_column'] = pd.to_datetime(df['Start Time'])
    df['Day_of_week'] = df['Datetime_column'].dt.day_name()
    df['Start_hour'] = df['Datetime_column'].dt.hour
    
    #filter df by month
    if month != 'all':
        df = df[df['Month'] == VALID_MONTHS.index(month) + 1]  
        
    #filter df by day
    if day != 'all':
        df = df[df['Day_of_week'] == day.title()] 
    
    #extract station data
    df['common_start_station'] = df['Start Station'].mode()[0]
    df['common_end_station'] = df['End Station'].mode()[0]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    #ask user if they want to see data
    print('Would you like to see travel time statistics? Yes or no')


    if get_yes_no():
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()

        #display most common month
        most_common_month_number = df['Month'].mode()[0]
        most_common_month = calendar.month_name[most_common_month_number]
        print('The most common month is:', most_common_month)

        #display the most common day of week
        most_common_day = df['Day_of_week'].mode()[0]
        print('The most common day of the week is:', most_common_day)
        
        #display the most common start hour
        most_common_hour = df['Start_hour'].mode()[0]
        print("The most common start hour is:", str(most_common_hour) + "00h")
       
        print("\nThis took %s seconds." % (round(time.time() - start_time, 2)))
        print('-'*40)

    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    #ask user if they want to see data
    print('Would you like to see station statistics? Yes or no')
    input_valid = False
    while not input_valid: 
        answer = input()
        answer = answer.lower()
        if answer in VALID_ANSWER:
            input_valid = True
        else:
            print('Invalid answer, please try again')    

    if answer == 'yes':
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()

        #display most commonly used start station
        common_start_station = df['common_start_station'].iloc[0]
        print('The most commonly used start station is:', common_start_station)

        #display most commonly used end station
        common_end_station = df['common_end_station'].iloc[0]
        print('The most commonly used end station is:', common_end_station)

        #display most frequent combination of start station and end station trip
        frequent_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
        print('The most frequent combination of start station and end station trip is:')
        print('Start Station:', frequent_combination[0])
        print('End Station:', frequent_combination[1])
    
        print("\nThis took %s seconds." % (round(time.time() - start_time, 2)))
        print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    #ask user if they want to see data
    print('Would you like to see trip duration statistics? Yes or no')
    input_valid = False
    while not input_valid: 
        answer = input()
        answer = answer.lower()
        if answer in VALID_ANSWER:
            input_valid = True
        else:
            print('Invalid answer, please try again')    

    if answer == 'yes':
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        #calculate total travel time
        total_travel_time = df['Trip Duration'].sum()
    
        #convert travel time into days, hours, minutes, and seconds
        total_travel_time_days = total_travel_time // (24 * 3600)
        remaining_time = total_travel_time % (24 * 3600)
        total_travel_time_hours = remaining_time // 3600
        remaining_time %= 3600
        total_travel_time_minutes = remaining_time // 60
        total_travel_time_seconds = remaining_time % 6
    
        #display travel time
        print("The total travel time is:", total_travel_time_days, "days,", total_travel_time_hours, "hours, and", total_travel_time_minutes, "minutes", total_travel_time_seconds, "seconds")

        #calculate  mean travel time
        mean_travel_time = df['Trip Duration'].mean()
    
        #convert travel time into minutes and seconds
        mean_travel_time_minutes = mean_travel_time // 60
        mean_travel_time_seconds = remaining_time % 6
    
        #display mean travel time
        print("The mean travel time is:", mean_travel_time_minutes, "minutes", mean_travel_time_seconds, "seconds")

        print("\nThis took %s seconds." % (round(time.time() - start_time, 2)))
        print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    #ask user if they want to see data
    print('Would you like to see user statistics? Yes or no')
    input_valid = False
    while not input_valid: 
        answer = input()
        answer = answer.lower()
        if answer in VALID_ANSWER:
            input_valid = True
        else:
            print('Invalid answer, please try again')    

    if answer == 'yes':
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        #display count of user types
        user_type_counts = df['User Type'].value_counts()
        print("Counts of user types:")
        print(user_type_counts)
        
        #display count of genders
        try:  
            gender_counts = df['Gender'].value_counts()
            print('Counts of Gender:')
            print(gender_counts)
        except: 
            pass

        #display earliest, most recent, and most common year of birth
        try:
            earliest_birth_year = int(df['Birth Year'].min())
            most_recent_birth_year = int(df['Birth Year'].max())
            most_common_birth_year = int(df['Birth Year'].mode()[0])

            print('Earliest Birth Year:', earliest_birth_year)
            print('Most Recent Birth Year:', most_recent_birth_year)
            print('Most Common Birth Year:', most_common_birth_year)
        except:
            pass

        print("\nThis took %s seconds." % (round(time.time() - start_time, 2)))
        print('-'*40)

    def display_data(df):

        i = 0
        show_data = input('Would you like to see the first 5 rows of data? Yes or no\n')
        if show_data == 'yes':
            print(df.head())
            show_more = input('Would you like to see the next 5 rows of data? Yes or no.\n').lower()
            while show_more == 'yes':
                i +=5
                print(df[i:i+5])
                show_more = input('Would you like to see the next 5 rows of data? Yes or no.\n').lower()
                
        
        print('Thank you for using the data display feature.')
    display_data(df)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

