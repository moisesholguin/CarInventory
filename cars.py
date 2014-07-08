#!/usr/bin/env python
#title           :cars.py
#description     :Used to monitor a car inventory
#author          :Moises Holguin
#date            :09-11-2013
#python_version  :2.7.3 
#==============================================================================
import pickle

try:
    # Initial Greeting
    print '\n' + ('-' * 50)
    print 'Bargain Bill\'s Inventory Program'

    # Global Variables
    menuChoice = None
    carDatabase = []

    # Loads from file or creates file if it doesn't already exist
    try:
        carDatabase = pickle.load(open("database.p","rb"))
    except IOError as e:
        open('database.p', 'w')
    except EOFError as e:
        open('database.p', 'w')

#========== Helper Functions ==================================================
    # Displays menu options
    def show_menu():
        print '-' * 50
        print '(a)dd a new car'
        print '(d)elete a car'
        print '(l)ist all cars'
        print '(s)ort by price and list'
        print '(q)uit'
        print '-' * 50
    
    # Handles the user input for the menu options
    def get_choice():
        valid = ['a', 'd', 'l', 's', 'q']
        while True:
            choice = get_input('Enter your choice: ')
            if choice.lower() in valid:
                return choice.lower()
            else:
                print 'Enter one of the letters listed in paren.'
                show_menu()

    # Single function used to get raw_input
    def get_input(message):
        return raw_input(message)
    
    # Used to properly display a car's information when listed
    def display_info(item): 
        return '{0[0]} {0[1]} {0[2]}, {0[3]} ({0[4]}): ${0[5]:.2f}'.format(item)

    # Handles the input validation for the 'String' details of a car
    def validate_car_info(prompt, info):
        valid = False
        while(not valid):
            try:
                someInfo = str(get_input(prompt))
                if(len(someInfo)==0): raise BaseException
            except BaseException as e:
                print 'Enter the car\'s %s.' % info
            else:
                valid = True
        return someInfo

    # Adds a car to the database
    def add_car():
        valid = False
        while(not valid):
            try:
                year = int(get_input('Year: '))
                if(year<1900 or year>2010): raise BaseException
            except BaseException as e:
                print 'Enter a year between 1900 and 2010'
            else:
                valid = True
        valid = False
        make = validate_car_info('Make: ', 'make')
        model = validate_car_info('Model: ', 'model')
        color = validate_car_info('Color: ', 'color')
        vin = validate_car_info('VIN: ', 'vin')
        while(not valid):
            try:
                price = float(get_input('Price: '))
                if(price<0): raise BaseException
            except BaseException as e:
                print 'Enter a dollar amount as a number.'
            else:
                valid = True
        carDatabase.append((year, make, model, color, vin, price))

    # Allows a car to be deleted from the database
    def delete_car():
        count = 1
        valid = False
        databaseSize = len(carDatabase)
        if(databaseSize<1):
            print 'No cars to delete.'
            return 1
        for car in carDatabase:
            print '(' + str(count) + ') ' + display_info(car) 
            count+=1
        while(not valid):
            try:
                numberOptions = '(1-1)' if (databaseSize == 1) else \
                                '(1-' + str(databaseSize) + ')'
                choice = None
                checkOne = str(get_input('(Hit Enter to return to main menu.)'
                             + '\nEnter car to delete '+numberOptions+': '))
                if(len(checkOne)==0): raise BaseException
                choice = checkOne
                checkTwo = int(choice)
                choice = checkTwo
                if(choice<1 or choice>databaseSize): raise BaseException
            except BaseException as e:
                if(choice==None): valid = True
                else: print 'Enter a number between 1 and ', str(databaseSize)
            else:
                del carDatabase[int(choice)-1]
                valid = True

    # Lists every car in the database sorted by year, make, model, etc.
    # and displays the total price
    def list_all():
        total = 0
        carDatabase.sort()
        for car in carDatabase:
            total += car[5]
            print display_info(car)
        print 'TOTAL VALUE: $%.2f' % total

    # Lists every car in the database sorted by price first then
    # year, make, model, etc. and displays the total price
    def sort_by_price():
        total = 0
        carDatabase.sort(key=lambda cars: cars[5])
        for car in carDatabase:
            total += car[5]
            print display_info(car)
        print 'TOTAL VALUE: $%.2f' % total

    # Handles possibly saving the database to a file and graceful termination
    def quit():
        toSaveOrNot = get_input('Exiting Inventory Program.\nSave Changes? ')
        if(toSaveOrNot.lower()=='y' or toSaveOrNot.lower()=='yes'):
            pickle.dump(carDatabase, open("database.p", "wb"))
            print 'Changes Saved.'
        print 'Goodbye.'
#========= End Helper Functions ===============================================

    # Main loop that controls everything
    while(menuChoice != 'q'):
        show_menu()
        menuChoice = get_choice()
        if menuChoice == 'a': add_car()
        elif menuChoice == 'd': delete_car()
        elif menuChoice == 'l': list_all()
        elif menuChoice == 's': sort_by_price()
except BaseException as e:
    pass
finally:
    quit()
