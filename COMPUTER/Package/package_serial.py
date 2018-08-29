import pickle as serializer

def decode(frameType, frameData):
    # DECODE FRAME BY TYPE
    if frameType == 1:                     # FRAME 1: DATA TOUCH
        d = decodeFrame1(frameData)
        action1(d)
            
def decodeFrame1(frameData):
    # READ METADATA
    [user_id, orientation, configuration, condition] = readMetadata()
    
    # RETURN ALL THE INFORMATION
    return [user_id, orientation, configuration, condition, frameData[0], frameData[1], frameData[2], frameData[3], frameData[4], frameData[5], frameData[6]]
        
def action1(d):
    # BUILD MESSAGE
    msg = ""
    msg = msg + d[1] + ';'                      # ORIENTATION
    msg = msg + d[2] + ';'                      # CONFIGURATION
    msg = msg + d[3] + ';'                      # CONDITION
    msg = msg + d[4] + ';'                      # SCREEN_NUMBER
    msg = msg + d[5] + d[6] + d[7] + ';'        # X
    msg = msg + d[8] + d[9] + d[10]             # Y

    # DISPLAY MESSAGE TO THE ADMINISTRATOR
    print(msg)

    # BUILD RESULT PATH
    path = ""
    path = path + "./Results/" + d[0] + ".csv"

    # SAVE RESULT
    file = open(path, "a")
    file.write(msg + '\n')
    file.close()

def readMetadata():
    # READ METADATA FROM CONFIG FILE
    with open("./Data/metadata.txt", 'r') as f:
        metadata = [line.rstrip('\n') for line in f]

    # RETURN METADATA
    return metadata