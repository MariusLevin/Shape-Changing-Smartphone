"""
@object: Implementing a client to modify the server's metadata as part of a data recovery project
@author: PECCHIOLI Mathieu
"""
# LIBRAIRY IMPORT
from os import system
from csv import reader

def sendAndClear(user_id, orientation, configuration, condition):
    # SEND METADATA CHANGES
    with open("./Data/metadata.txt", 'w') as f:
        frame = [user_id, orientation, configuration, condition]
        for data in frame:
            f.write(data + '\n')

    # CLEAR SCREENS
    with open("./Data/commands.txt", 'w') as f:
        f.write('1')

def buildInformation(orientation, configuration, condition):
    conf = ""
    if condition == '1':
        conf = conf + "CONDITION: COMFORT AREA\n"
    elif condition == "2":
        conf = conf + "CONDITION: USEFUL AREA\n"
    elif condition == "3":
        conf = conf + "CONDITION: REST POSITION\n"
    if configuration != 'ee':
        conf = conf + "CONFIGURATION: LINK NUMBER " + configuration + "\n"
    if orientation == '1':
        conf = conf + "ORIENTATION: VERTICAL\n"
    elif orientation == '2':
        conf = conf + "ORIENTATION: HORIZONTAL\n"
    return conf

# VARIABLES
frame = ""
user_id = "ee"
orientation = "e"
configuration = "ee"
condition = "e"
valCondition = ['3', '1', '2']
valConfiguration = {'00': ['30', '12', '01', '32', '10', '03', '31', '02', '00', '13', '21', '20', '33', '11', '22', '23'],
                    '01': ['31', '12', '13', '21', '32', '01', '33', '11', '10', '22', '23', '20', '03', '30', '00', '02'],
                    '02': ['33', '30', '02', '31', '21', '10', '32', '03', '01', '00', '13', '11', '12', '22', '23', '20'],
                    '03': ['23', '21', '12', '22', '10', '20', '11', '32', '01', '00', '13', '33', '31', '02', '30', '03'],
                    '04': ['32', '30', '03', '23', '33', '13', '01', '02', '12', '20', '21', '31', '22', '10', '00', '11'],
                    '05': ['11', '30', '22', '02', '31', '00', '01', '21', '12', '32', '33', '03', '13', '10', '20', '23'],
                    '06': ['01', '11', '30', '02', '21', '13', '22', '23', '32', '20', '10', '31', '00', '12', '33', '03'],
                    '07': ['22', '31', '13', '03', '11', '00', '21', '10', '12', '01', '20', '33', '23', '32', '30', '02'],
                    '08': ['11', '10', '01', '02', '03', '32', '13', '22', '21', '30', '31', '33', '23', '00', '12', '20'],
                    '09': ['00', '32', '03', '10', '31', '22', '02', '21', '23', '13', '30', '12', '20', '01', '33', '11'],
                    '10': ['32', '13', '02', '31', '33', '23', '01', '20', '10', '12', '30', '21', '22', '00', '11', '03'],
                    '11': ['13', '22', '12', '20', '33', '31', '21', '11', '00', '02', '23', '32', '01', '10', '03', '30'],
                    '12': ['11', '12', '30', '22', '20', '21', '00', '02', '03', '31', '23', '33', '01', '10', '13', '32']}
valOrientation = {'00': ['1', '2'], '01': ['2', '1'], '02': ['1', '2'], '03': ['2', '1'],
                    '04': ['1', '2'], '05': ['2', '1'], '06': ['1', '2'], '07': ['2', '1'],
                    '08': ['1', '2'], '09': ['2', '1'], '10': ['1', '2'], '11': ['2', '1'],
                    '12': ['2', '1']}

# START
system('clear')
print("Administrator opened\n")

print("Please enter your ID (2 DIGITS):")
user_id = input()

# INITIALIZATION
sendAndClear(user_id, orientation, configuration, condition)

while True:
    # MENU
    system('clear')
    print("What do you want to do?")
    print("1 - MANUAL CHANGES")
    print("2 - AUTOMATIC CHANGES")
    print("3 - EXIT")
    choice = input()

    # MANUAL CHANGES
    if choice == '1':
        system('clear')
        print("\nWhat do you want to do?")
        print("1 - SEND COMPLETE FRAME")
        print("2 - CHANGE ORIENTATION")
        print("3 - CHANGE CONFIGURATION")
        print("4 - CHANGE CONDITION")
        print("5 - CLEAR SCREENS")
        choice = input()
        
        # CHANGE ORIENTATION
        if choice == '1' or choice == '2':
            system('clear')
            print("Select orientation please:")
            print("1 - VERTICAL")
            print("2 - HORIZONTAL")
            orientation = input()
            
        # CHANGE CONFIGURATION
        if choice == '1' or choice == '3':
            system('clear')
            print("Enter the configuration number between 00 and 33 please:")
            configuration = input()
            
        # CHANGE CONDITION
        if choice == '1' or choice == '4':
            system('clear')
            print("Select area condition please:")
            print("1 - COMFORT AREA")
            print("2 - UTILITY AREA")
            condition = input()

        sendAndClear(user_id, orientation, configuration, condition)

    # AUTOMATIC CHANGES
    elif choice == '2':
        flagChanges = 0
        while True:
            # INITIALIZATION
            if orientation == 'e' and configuration == 'ee' and condition == 'e':
                sendAndClear('ee', orientation, configuration, condition)
                system('clear')
                input("GRIP TESTS\n" + "\nPRESS ENTER TO CONTINUE")

                condition = valCondition[0]
                configuration = valConfiguration[user_id][0]
                orientation = valOrientation[user_id][0]
                flagChanges = 0
            # INCREASE CONDITION
            elif valCondition.index(condition) < (len(valCondition) - 1):
                condition = valCondition[valCondition.index(condition) + 1]
                flagChanges = 1
            # INCREASE CONFIGURATION
            elif valConfiguration[user_id].index(configuration) < (len(valConfiguration[user_id]) - 1):
                condition = valCondition[0]
                configuration = (valConfiguration[user_id])[valConfiguration[user_id].index(configuration) + 1]
                flagChanges = 0
            # INCREASE ORIENTATION
            elif valOrientation[user_id].index(orientation) < (len(valOrientation[user_id]) - 1):
                condition = valCondition[0]
                configuration = valConfiguration[user_id][0]
                orientation = valOrientation[user_id][valOrientation[user_id].index(orientation) + 1]
                flagChanges = 0
            # END OF THE EXPERIMENT
            else:
                system('clear')
                print("END OF THE EXPERIMENT")
                break

            # BUILD CONFIGURATION MESSAGE
            conf = buildInformation(orientation, configuration, condition)

            if flagChanges == 0:
                sendAndClear('ee', orientation, configuration, condition)
                system('clear')
                input("CHANGING THE LINK\n\n" + conf + "\nPRESS ENTER TO CONTINUE")

                sendAndClear(user_id, orientation, configuration, condition)
                system('clear')
                input("RECORD RESULTS\n\n" + conf + "\nPRESS ENTER TO CONTINUE")
            elif flagChanges == 1:
                # sendAndClear('ee', orientation, configuration, condition)
                # system('clear')
                # input("CONDITION CHANGE\n\n" + conf + "\nPRESS ENTER TO CONTINUE")
                sendAndClear(user_id, orientation, configuration, condition)
                system('clear')
                input("RECORD RESULTS\n\n" + conf + "\nPRESS ENTER TO CONTINUE")

        break 

    # EXIT
    elif choice == '3':
        print("\nAdministrator closed")
        break
