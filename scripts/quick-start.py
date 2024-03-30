from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import cv2

'''
Authenticate
Authenticates your credentials and creates a client.
'''
subscription_key = os.environ["VISION_KEY"]
endpoint = os.environ["VISION_ENDPOINT"]

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
'''
END - Authenticate
'''

'''
OCR: Read File using the Read API, extract text - remote
This example will extract text in an image, then print results, line by line.
This API call can also extract handwriting style text (not shown).
'''
print("===== Read File - remote =====")
# Get an image with text
# read_image_url = "https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png"
read_image_url = "https://iiitaphyd-my.sharepoint.com/:i:/g/personal/tallapragada_s_research_iiit_ac_in/EW5n2gM6gF5HsQhNUNwQpuwBq5rFeJLIVvHOjiNn-Pb1Zw?download=1"
# read_image_url = "https://iiitaphyd-my.sharepoint.com/:i:/g/personal/tallapragada_s_research_iiit_ac_in/EZMkY7e_bydDhGK-LWf5S6UBJffJK12jvatNaFkueu0kwA?download=1"

# Call API with URL and raw response (allows you to get the operation location)
read_response = computervision_client.read(read_image_url,  raw=True, model_version="latest", readingOrder="basic")

# Get the operation location (URL with an ID at the end) from the response
read_operation_location = read_response.headers["Operation-Location"]
# Grab the ID from the URL
operation_id = read_operation_location.split("/")[-1]

# Call the "GET" API and wait for it to retrieve the results 
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

line_bbox = []
word_bbox = []
# Print the detected text, line by line
if read_result.status == OperationStatusCodes.succeeded:
    print(read_result)
    print(type(read_result))
    print(read_result.analyze_result)
    print(type(read_result.analyze_result))
    print(read_result)

    #load read_result as json
    read_result_json = read_result.as_dict()
    # print(read_result_json)

    print(type(read_result.analyze_result.read_results))
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            line_bbox.append(line.bounding_box)
            print(line.text)
            print(line.bounding_box)
            for word in line.words:
                print(word.text)
                print(word.bounding_box)
                word_bbox.append(word.bounding_box)
print()

direc = "/home/vatsasree/Downloads/Pages/Pagg/Dataset/Dataset/176.jpg"
img = cv2.imread(direc)
order=0
# for bbox in line_bbox:
for bbox in word_bbox:
    cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[4]), int(bbox[5])), (0, 255, 0), 2)
    cv2.putText(img, str(order), (int(bbox[0])-10, int(bbox[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
    order+=1
os.makedirs("outputs", exist_ok=True)    
cv2.imwrite("outputs/output_{}.jpg".format(direc.split('/')[-1].split('.')[0]), img)
'''
END - Read File - remote
'''

print("End of Computer Vision quickstart.")