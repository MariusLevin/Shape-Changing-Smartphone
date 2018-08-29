"""
@object: Script to get results for data save on experimentation
@author: PECCHIOLI Mathieu
"""
# LIBRAIRIES IMPORT
import os

# VARIABLES
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

valConfigurationNormalized = ['00', '01', '02', '03', '10', '11', '12', '13', '20', '21', '22', '23', '30', '31', '32', '33']

# STARTING PROGRAM
print("RESULTS EXTRACT PROGRAM\n")
input("PRESS ENTER TO CONTINUE")

# EXTRACT RESULT FILE LIST
files = os.listdir('./Results/')

for file in files:
    fileId, extension = os.path.splitext(file)

    if extension == ".txt":
        # Print ID
        print("File ID: " + str(fileId))

        # Extract csv file path
        filePath = "./Results/" + file

        # List to save frame data
        results = []

        # Extract notes
        with open(filePath, 'r') as f:
            notes = [line.rstrip('\n') for line in f]
		
        # Create configuration dictionnaries
        dictConfig1 = {}
        dictConfig2 = {}
        i = 0

        # Fill configuration dictionnaries
        for c in valConfiguration[fileId]:
            dictConfig1[c] = notes[i]
            i = i + 1
        for c in valConfiguration[fileId]:
            dictConfig2[c] = notes[i]
            i = i + 1

        message = ""
        if valOrientation[fileId][0] == '1':
            for c in valConfigurationNormalized:
                message = message + dictConfig1[c] + ','
            for c in valConfigurationNormalized:
                message = message + dictConfig2[c] + ','
        
        elif valOrientation[fileId][0] == '2':
            for c in valConfigurationNormalized:
                message = message + dictConfig2[c] + ','
            for c in valConfigurationNormalized:
                message = message + dictConfig1[c] + ','
        message = message + '\n'

        # Save results
        with open("./DataExtract/FinalNotesResults.csv", "a") as f:
	        f.write(message)

print("\nEND OF THE EXTRACTION")