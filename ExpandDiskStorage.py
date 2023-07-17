'''
This expands the disk storage and allocates partition space for the new storage 
'''
import time
import boto3

EC2_CLIENT = boto3.client('ec2')
ssm = boto3.client('ssm')

#get the current size of the first volume
def get_current_size(volume_id):
    print("Getting current size of volume")
    response = EC2_CLIENT.describe_volumes(
        VolumeIds=[
            volume_id
        ]
    )
    print("Current size of volume is: " + str(response['Volumes'][0]['Size']))
    return response['Volumes'][0]['Size']


# get the current modification state
def get_modification_state(volume_id):
    print("Getting modification state")
    response = EC2_CLIENT.describe_volumes_modifications(
        VolumeIds=[
            volume_id
        ]
    )
    state = response['VolumesModifications'][0]['ModificationState'] #state is either 'modifying', 'optimizing', 'completed', or 'failed'
    #print("Modification state is: " + state)
    return state


#modify the volume
def modify_volume(volume_id, current_size, amountToExtend):
    #if not a num
    if not isinstance(amountToExtend, int):
        print("Amount to extend is not a number")
        return
    modify_volume_response = EC2_CLIENT.modify_volume(
        VolumeId=volume_id,
        Size= current_size + amountToExtend
    )
    print("Volume modification response: " + str(modify_volume_response))

#extend the drive using ssm
def extend_drive(drivenum, instanceId):
    print("Extending drive with ssm document")
    response = ssm.send_command(
        InstanceIds = [instanceId],
        DocumentName = 'DDS-ExpandDiskStorage', #name of ssm run document
        DocumentVersion = "$LATEST"
    )
    return response




def lambda_handler(event, context):
        
    #setting the volumID, amount to extend, and drive number from event parameters
    VOLUME_ID = event['volumeId']
    #the amount to extend in GB
    amountToExtend = event['amountToExtend']
    #setting the drive number to extend
    drivenum = 0
    if event['drive'] == 'C':
        drivenum = 0
    elif event['drive'] == 'D':
        drivenum = 1
    instanceId = event['instanceId']

    # get the current size of the volume, add "amountToExtend" to it, and modify the volume
    current_size = get_current_size(VOLUME_ID)
    
    
    modify_volume(VOLUME_ID, current_size, amountToExtend)
    #track the modification state and progress 
    previous = set()
    while True:
        state = get_modification_state(VOLUME_ID)
        if state not in previous:
            print("The current state is ", state)
            previous.add(state)
        if state == 'completed' or state == None:
            break
        elif state == 'failed':
            raise Exception('Failed to modify volume size')
        else:
            time.sleep(1)
    print(f'Volume {VOLUME_ID} successfully resized')
    
    #run the ssm document to extend the drive
    extend_drive(drivenum, instanceId)




