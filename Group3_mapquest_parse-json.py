import json
import urllib.parse
import requests

# MapQuest API and Key
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "QIH00Aknfy7gGhpFAAxdSgEzAVLK74xF"

# Display Welcome Title
welcomeText = "Welcome To MapQuest"

print("\n")
print(welcomeText.center(100))
print("===============================================================================================================")
print("MapQuest provides simple directions and creates suitable route points depending on your preferred route type!")
print("Please enter the following details, or enter 'quit' or 'q' to terminate the program.")

while True:
    # Get User Input for Starting and Destination
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break

    # Get User Input for Route Types
    print("\nRoute Type")
    print("1 = Fastest")
    print("2 = Shortest")
    print("3 = Pedestrian")
    print("4 = Bicycle")

    routeType = input("Select Route Type Number: ")
    if routeType == "1":
        routeType = "fastest"
    elif routeType == "2":
        routeType = "shortest"
    elif routeType == "3":
        routeType = "pedestrian"
    elif routeType == "4":
        routeType = "bicycle"  
    else: 
        routeType = "fastest"
    
    url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest, "routeType":routeType})
    print("URL: " + (url))
    

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")

        print("=============================================")
        print("Directions from " + (orig) + " to " + (dest))
        print("Route Type: " + (routeType))
        print("Trip Duration: " + (json_data["route"]["formattedTime"]))

        print("\nDistance")
        print("Miles: " + str(json_data["route"]["distance"]))
        print("Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))

        print("\nFuel Used")
        print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))
        print("Fuel Used (Gal): " + str(json_data["route"]["fuelUsed"]))
        print("=============================================")

        print("=============================================")
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print(" (" + str("{:.2f}".format((each["distance"])*1.61) + " km)") + "\t" + (each["narrative"]))
        print("=============================================\n")

    elif json_status == 402:
        print("*********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("*********************************************\n")
    elif json_status == 611:
        print("*********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("*********************************************\n")
    else:
        print("*********************************************")
        print("For Status Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-code")
        print("*********************************************\n")