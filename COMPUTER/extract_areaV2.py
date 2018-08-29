"""
@object: Script to get results for data save on experimentation
@author: PECCHIOLI Mathieu
"""
# LIBRAIRIES IMPORT
import os
from csv import reader
from numpy import array, sqrt, arange
from scipy.spatial import Delaunay
from matplotlib import pyplot as plt
from matplotlib.colors import to_rgba
import matplotlib.patches as mpatches
from shapely.geometry import MultiLineString
from shapely.geometry.polygon import LinearRing, Polygon
from shapely.ops import polygonize, unary_union, cascaded_union
from Package.package_area import calc_alpha2
from descartes import PolygonPatch

# FUNCTION DEFINITION
def stringToInt(object, numberOfChar, type):
    res = 0
    for i in range(0, numberOfChar):
        res = res + (ord(object[i]) - ord('0')) * 10**(numberOfChar - 1 - i)

    return res

# PARAMETERS POSSIBILITIES
valOrientation = ['1', '2']
valConfiguration = ['00', '01', '02', '03', '10', '11', '12', '13', '20', '21', '22', '23', '30', '31', '32', '33']
valScreen = ['1', '2']
valCondition = ['2', '1', '3']

# STARTING PROGRAM
print("RESULTS EXTRACT PROGRAM\n")
input("PRESS ENTER TO CONTINUE")

# EXTRACT RESULT FILE LIST
files = os.listdir('./Results/')
message = "User_ID,Orientation,Configuration,Condition,Screen,Area\n"

for file in files:
    fileId, extension = os.path.splitext(file)
    if extension == ".csv":
        # Print ID
        print("File ID: " + fileId)

        # Extract csv file path
        filePath = "./Results/" + file

        # List to save frame data
        results = []

        # Read CSV file
        with open(filePath, newline='') as csvfile:
            # Build reader
            spamreader = reader(csvfile, delimiter=';')

            # Save frame part
            orientation = []
            configuration = []
            condition = []
            screen = []
            x = []
            y = []		

            # Extract frame part
            for lineSplited in spamreader:
                orientation.append(lineSplited[0])
                configuration.append(lineSplited[1])
                condition.append(lineSplited[2])
                screen.append(lineSplited[3])
                x.append(lineSplited[4])
                y.append(lineSplited[5])

            # Save all the frame part on results list
            results = [orientation, configuration, condition, screen, x, y]

		# Scan frame data
        for orientation in valOrientation:							
            for configuration in valConfiguration:
                for screen in valScreen:
                    # Create figure
                    fig = plt.figure()
                    ax = fig.add_subplot(111)
                    flag = False

                    area1 = 0
                    area2 = 0

                    for condition in valCondition:
						# Save the points corresponding to the conditions
                        points = []

						# Extract points corresponding to the conditions
                        for i in range(0, len(results[0])):
                            if orientation == results[0][i] and configuration == results[1][i] and condition == results[2][i] and screen == results[3][i]:
                                points.append([stringToInt(results[4][i], 3, 'x'), stringToInt(results[5][i], 3, 'y')])

                        if points != []:
                            if condition in ['1', '2']:
                                flag = True

                                # Convert list to array
                                points = array(points)

                                # Build Delannay tri
                                tri = Delaunay(points)
                                
                                # Test with different alpha as a parameter
                                for alp in arange(0,350,100):
                                    # Triangle filtering
                                    if condition == '1':
                                        n, area1 = calc_alpha2(alp, tri, points)
                                    elif condition == '2':
                                        n, area2 = calc_alpha2(alp, tri, points)

                                    # Polygonisation
                                    m = MultiLineString(n)
                                    triangles = list(polygonize(m))

                                    # Triangles unification
                                    a = unary_union(triangles)
                                    
                                    # Single polygon test
                                    if a.geom_type == "Polygon":
                                        # Merge triangles
                                        shape = cascaded_union(triangles)
                                        
                                        # Generate Figure
                                        patch = PolygonPatch(shape)
                                        if condition == '1':
                                            patch.set_color(to_rgba('red', alpha = 0.6))
                                        elif condition == '2':
                                            patch.set_color(to_rgba('orange', alpha = 1))
                                        ax.add_patch(patch)   
                                        break
                                    else:
                                        # If not a single polygon
                                        continue
                            
                            # Extract rest position
                            elif condition == '3':
                                xaverage = 0
                                yaverage = 0
                                for p in points:
                                    xaverage = xaverage + p[0]
                                    yaverage = yaverage + p[1]
                                xaverage = xaverage / len(points)
                                yaverage = yaverage / len(points)
                                cross = plt.plot(xaverage, yaverage, "b+") 

                    if flag == True:
                        # Print results on console
                        msg1 = "" "Orientation: " + orientation + "\t" + "Configuration: " + configuration + "\t" + "Condition: " + '1' + "\t" + "Screen: " + screen + "\t" + "Area: " + str(int(area1))
                        msg2 = "" "Orientation: " + orientation + "\t" + "Configuration: " + configuration + "\t" + "Condition: " + '2' + "\t" + "Screen: " + screen + "\t" + "Area: " + str(int(area2))
                        print(msg1)
                        print(msg2)
                        msg1 = fileId + ',' + orientation + ',' + configuration + ',' + '1' + ',' + screen + ',' + str(int(area1))
                        msg2 = fileId + ',' + orientation + ',' + configuration + ',' + '2' + ',' + screen + ',' + str(int(area2))
                        message = message + msg1 + "\n" + msg2 + "\n"

                        red_patch = mpatches.Patch(color='red', label='Comfort area = ' + str(int(area1)) + ' mm²')
                        orange_patch = mpatches.Patch(color='orange', label='Useful area = ' + str(int(area2)) + ' mm²')
                        plt.legend(handles=[red_patch, orange_patch])

                        # Print and save figure
                        ax = plt.axis([0, 240, 0, 320])     # resolution = 240 x 320
                        figName = "" + fileId + '-' + orientation + '-' + configuration + '-' + screen
                        figPath = "" + "./DataExtract/" + figName + ".png"
                        plt.title(figName, fontsize=14, fontweight='bold')
                        plt.savefig(figPath)
                        # plt.show()
                        flag = False
                    plt.close()

        filePath = "./DataExtract/FinalAreaResults" + fileId + ".csv"
        with open(filePath, "w") as f:
            f.write(message)

print("\nEND OF THE EXTRACTION")