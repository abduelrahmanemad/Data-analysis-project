import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    c=input('Enter the name of the city(chicago-new york city-washington) : ').lower()
    while c not in CITY_DATA.keys():
        print('please enter valid data\n')
        c=input('Enter the name of the city : ').lower()
        print('\n')
    
    print('Enter name of the month all, january, february, ... , june')
    months=['january',' february','march','abril','may','june','all']
    while True:
        m=input('Enter month : ')
        print('\n')
        if m in months:
            break
        else:
            print('Enter valid month\n')
    print('Enter the day (all, monday, tuesday, ... sunday)')
    days=['all','saturday','sunday','monday','tuesday','wednesday','thursday','friday']
    while True:
        d=input('Enter day : ')
        print('\n')
        if d in days:
            break
        else:
            print('Enter valid day')
    global cityglobal
    cityglobal = c
    print('-'*40)
    return c, m, d

def load_data(city, month, day):
    
    df=pd.read_csv(CITY_DATA[city])

    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['Start hour']= pd.DatetimeIndex(df['Start Time']).hour
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('the most common month is {}'.format(df['month'].mode()[0]))
    print('\n')
    # display the most common day of week
    print('the most common day is {}'.format(df['day_of_week'].mode()[0]))
    print('\n')
    # display the most common start hour
    
    print('the most common start hour is {}'.format(df['Start hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    ss=df['Start Station'].mode()[0]
    print('the most commonly used start station is : ',ss,'\n')

    # display most commonly used end station
    es=df['End Station'].mode()[0]
    print('the most commonly used End Station is : ',es,'\n')

    # display most frequent combination of start station and end station trip
    df['trip']=df['Start Station']+','+df['End Station']
    t=df['trip'].mode()[0]
    print('the most frequent combination of start station and end station trip is :',t,'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tt=df["Trip Duration"].sum()/3600
    print('total travel time ',int(tt),'H')

    # display mean travel time
    tm=df['Trip Duration'].mean()/60
    print('Averege time per trip is ',tm,'Minute')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    ut =df['User Type'].value_counts()
    print("User count statistics: {}".format(ut))

    if cityglobal=="washington":
        return print("Washington Data do not have Gender and birth year statistics!")
    
    # Display counts of gender
    g = df['Gender'].value_counts()

    print("Gender count statistics: {}".format(g))


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
        f=0
        e=5
        QA=input("Would you like me to show you 5 rows of the Dataset ? (yes or no)")
        while QA =="yes":
            print(df.iloc[f:e])
            QA=input("Would you like to see the next 5 rows ? (yes or no)")
            f +=5
            e +=5  
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break           
       

if __name__ == "__main__":
	main()
