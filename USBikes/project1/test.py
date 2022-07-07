import imp
import time
import pandas as pd
import numpy as np

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
    while True:
        cityinput = input("Please type in the city.(available cities: Chicago ,Washington ,New York City )")
        cityinput=cityinput.lower() # this makes the input not case sensitive which is better for the user.
        if (cityinput=="chicago" or cityinput=="washington" or cityinput=="new york city"):
            city = cityinput
            print("Valid input! the city you have chosen is {}".format(cityinput))
            break # breaks from the loop when if func satisfied!
        else:
            print("Invalid input Please try again.")
            continue # loops again when not satisfied   


    # get user input for month (all, january, february, ... , june)
    while True:
        monthinput= input("Please type in a month from january to June and 'all' for filtering for all months ")
        monthinput= monthinput.lower() # this makes the input not case sensitive which is better for the user.
        if (monthinput =="all" or monthinput =="january" or monthinput =="february" or monthinput =="march" or monthinput =="april" or monthinput =="may" or monthinput =="june"):
            month = monthinput
            print("Valid input! the month selection you have seleced is {}!".format(month))
            break # breaks from the loop when if func satisfied
        else:
            print("Invalid input Please try again.")
            continue # loops again when not satisfied



    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        dayinput= input("Please type in a day name. if you do not want to filter by day type 'all'")
        dayinput= dayinput.lower() # this makes the input not case sensitive which is better for the user.
        if (dayinput =="all" or dayinput =="sunday" or dayinput =="monday" or dayinput =="tuesday" or dayinput =="wednesday" or dayinput =="thrusday" or dayinput =="friday" or dayinput=="saturday"):
            day = dayinput
            print("Valid input! the day selection you have seleced is {}!".format(day))
            break # breaks from the loop when if func satisfied
        else:
            print("Invalid input Please type a valid day name.")
            continue # loops again when not satisfied

    global cityglobal
    cityglobal = city
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

    # converts Start Time to Datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # making Month and day of week columns from Start Time. day of week contains the day name.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

   
    if month != 'all':
        # here I added 1 to the index because the array index starts from 0. so that each month name is synced with its number
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # loads the data by filtering month entered by user
        df = df[df['month'] == month]

    # loads the data by filtering day entered by user
    if day != 'all':
        
        df = df[df['day_of_week'] == day]

    return df
    


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # here I convert Start Time column to Datetime 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour

    # The mode alone finds the number of the month due to the Datetime conversion Howevers its more understandable
    # to show the name month using an If function and change the variable to contain the month in words
    popular_month = df['month'].mode()[0]
    if popular_month==1:
        popular_month ="January"
    elif popular_month==2:
        popular_month="February"
    elif popular_month==3:
        popular_month="March"
    elif popular_month==4:
        popular_month="April"
    elif popular_month==5:
        popular_month="May"
    else:
        popular_month="June"

    print("The most popular month in the data is: {}".format(popular_month))


    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most popular day in the period selected is: {}".format(popular_day))
    
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The most popular hour in the period selected is: {}".format(popular_hour))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station=df['Start Station'].mode()[0]
    print("Most popular start station: {}".format(popular_start_station))

    # display most commonly used end station
    popular_end_station=df['End Station'].mode()[0]
    print("Most popular End station: {}".format(popular_end_station))

    # Here I combined the Start Station and End Station into one column and found the most common stations!
    df["StartEndStat"] = df["Start Station"] +" and "+ df["End Station"]
    CombinedSTENDcol= df["StartEndStat"].mode()[0]
    print("The most popular Start and End stations by individuals: {}".format(CombinedSTENDcol))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    Total_time=df["Trip Duration"].sum().sum()/3600
    Total_time = int(Total_time)
    # Here the sum of the total time in seconds would be very hectic to undestand
    # so I divided by 3600 to make it in hours cuz its easier to understand by the user.
    print("Total riding duration by people in the selected period {} Hours".format(Total_time))


    # display mean travel time
    MeantimeS=df["Trip Duration"].mean()
    MeantimeM =MeantimeS/60
    MeantimeS =int(MeantimeS)
    MeantimeM =int(MeantimeM) 
    # The trip duration is in seconds so dividing by 60 makes it 
    #in minutes which is easier to undestand to the user!
    
    print("Average trip duration by individuals: {} seconds or {} minutes".format(MeantimeS,MeantimeM))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types =df['User Type'].value_counts()
    print("User count statistics: {}".format(user_types))

    if cityglobal=="washington":
        return print("Washington Data do not have Gender and birth year statistics!")
    
    # Display counts of gender
    gender_counts = df['Gender'].value_counts()

    print("Gender count statistics: {}".format(gender_counts))


    # Display earliest, most recent, and most common year of birth
    # mode finds the most repeating birth year.
    most_birth = df['Birth Year'].mode()[0]
    mostbirth_age= 2022-most_birth
    print("The most common year of birth is {} , that is the age of {}!".format(most_birth,mostbirth_age))

   
    # here .min() finds the lowest number in the birth years so its the oldest.
    
    old_birth = df['Birth Year'].min()
    oldbirth_age=2022 - old_birth
    print("The eldest year of birth is {} , that is the age of {}! If they are alive.".format(old_birth,oldbirth_age))
    
    
    # here .max() finds the highest number in the birth years so its the youngest
    young_birth = df['Birth Year'].max()
    young_age= 2022-young_birth
    print("The youngest year of birth is {} , that is the age of {}!".format(young_birth,young_age))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)        
        user_stats(df)
        stiloc=0
        endiloc=5
        QA=input("Would you like me to show you 5 rows of the Dataset ? (yes or no)")
        while QA =="yes":
            print(df.iloc[stiloc:endiloc])
            QA=input("Would you like to see the next 5 rows ? (yes or no)")
            stiloc +=5
            endiloc +=5



        # a small feedback system
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            rating=input("Thank you for using the program. Please rate the program from 1 to 5! (type no to skip rating)")
            if rating !="no":
                print("Thank you for your feedback!") # thanking the user if they tried to send feedback
                break
            else:
                break        



            



if __name__ == "__main__":
	main()
