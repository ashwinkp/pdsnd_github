import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
fliter_choice = ''

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ''
    month = ''
    day = ''
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while not city :
        city = input('Would you like to see data for Chicago, New York or Washington?\n')
        city = city.lower().strip()
        #validate the input value agaist permissible values
        if city in ("chicago", "new york", "washington"):
            break
        else:
            print("Invalid choice")
            city =''
            continue


    
    while not fliter_choice:
        filter_choice = input('Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter.\n')
        filter_choice = filter_choice.lower().strip()
        #validate the input value agaist permissible values
        if filter_choice not in ("month", "day", "both", "none"):
            print("Invalid filter choice")
            continue
        else:
            break
            
        
        
    # Get user input for month (all, january, february, ... , june)
    if filter_choice in ('both', 'month'):
        while month not in months:
            month = input("Which month? January, February, March, April, May or June?\n").lower()
    else:
        month = "all"
        

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_choice in ('both', 'day'):
        while day not in ('1', '2', '3', '4', '5', '6', '7'):
            day = input("Which day? Please type your response as an integer e.g. Sunday=1\n")
    else:
        day = "all"


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

    print("City:{}, Month:{} Day:{}".format(city,month,day))
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

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
        df = df[df['day_of_week'] == (int(day) -1)]


    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month if we have multiple month data in df
    if df['month'].nunique() != 1:
        most_common_month = df['month'].value_counts().idxmax()
        print('\nThe most common month is:',most_common_month)

    # Display the most common dow if we have multiple dow data in df
    if df['day_of_week'].nunique() != 1:
        most_common_dow = df['day_of_week'].value_counts().idxmax()
        print('\nThe most common day of week is:',most_common_dow)
    

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].value_counts().idxmax()
    print("\nMost popular hour:",popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Display most commonly used start station
    most_common_startstn = df['Start Station'].value_counts().idxmax()
    print("\nMost popular Start Station:",most_common_startstn)

    # TO DO: display most commonly used end station
    most_common_endstn = df['End Station'].value_counts().idxmax()
    print("\nMost popular End Station:",most_common_endstn)

    # Display most frequent combination of start station and end station trip
    most_common_trip = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station : {}, {}"\
            .format(most_common_trip[0], most_common_trip[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total time travel: ", total_travel)
    

    #Display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time: ", mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type= df['User Type'].value_counts()
    print ('\nUser types: \n',user_type)
    
    
    # Display counts of gender
    print ('\nGender types: ')
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print(gender)
    else:
        print("There is no gender information in this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print ('\nBirth Year Information:')
        earliest = df['Birth Year'].min()
        print(" Earliest :", earliest)
        recent = df['Birth Year'].max()
        print(" Recent :", recent)
        common_birth = df['Birth Year'].mode()[0]
        print(" Most Common Birth Year:", common_birth)
    else:
        print("There is no birth year information in this city.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw(df):
    """Displays 5 lines of raw data if user wishes."""
    n=0
    
    d=input("Would you like to view 5 rows of data? ").lower()
    while True:
        
        if d in ('yes','y'):
            print(df.iloc[n:n+5])
            n=n+5
        elif d in ('no','n'):
            break 
        else:
            print("Please enter a valid input either yes or no: ")
            continue
        d=input("Do you want to next 5 rows of data ? ")
    return



def main():
    while True:
        #Get the filters from the user
        city, month, day = get_filters()
        #Load the data based on the user selection
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
