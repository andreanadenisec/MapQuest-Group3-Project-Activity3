import json
import urllib.parse
import requests

# MapQuest API and Key
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "QIH00Aknfy7gGhpFAAxdSgEzAVLK74xF"


def getMapQuest(orig, dest, routeType, avoid, language):

    if(avoid != 'None'):
        url = main_api + urllib.parse.urlencode(
            {"key": key, "from": orig, "to": dest, "routeType": routeType, 'avoids': avoid, 'locale': language})
    else:
        url = main_api + urllib.parse.urlencode(
            {"key": key, "from": orig, "to": dest, "routeType": routeType, 'locale': language})

    print("URL: " + (url))

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("API Status: " + str(json_status) +
              " = A successful route call.\n")
    elif json_status == 402:
        print("API Status: " + str(json_status) +
              " = Invalid user inputs for one or both locations.\n")
    elif json_status == 611:
        print("API Status: " + str(json_status) +
              " = Missing an entry for one or both locations\n")
    return (json_status, url)


def test_getMapQuest():
    assert getMapQuest("Manila", "Muntinlupa", "Fastest",
                       "Toll Road", "en_US") == (0, "https://www.mapquestapi.com/directions/v2/route?key=QIH00Aknfy7gGhpFAAxdSgEzAVLK74xF&from=Manila&to=Muntinlupa&routeType=Fastest&avoids=Toll+Road&locale=en_US")

    assert getMapQuest("Roma, Italia", "Frascati, Italia", "Shortest", "Bridge",
                       "es_ES") == (0, "https://www.mapquestapi.com/directions/v2/route?key=QIH00Aknfy7gGhpFAAxdSgEzAVLK74xF&from=Roma%2C+Italia&to=Frascati%2C+Italia&routeType=Shortest&avoids=Bridge&locale=es_ES")

    assert getMapQuest("Nangis", "Lizines", "Pedestrian", "None",
                       "fr_FR") == (0, "https://www.mapquestapi.com/directions/v2/route?key=QIH00Aknfy7gGhpFAAxdSgEzAVLK74xF&from=Nangis&to=Lizines&routeType=Pedestrian&locale=fr_FR")

    assert getMapQuest("BF Homes, Paranaque", "Alabang Hills, Muntinlupa", "Bicycle",
                       "Toll Road", "en_US") == (0, "https://www.mapquestapi.com/directions/v2/route?key=QIH00Aknfy7gGhpFAAxdSgEzAVLK74xF&from=BF+Homes%2C+Paranaque&to=Alabang+Hills%2C+Muntinlupa&routeType=Bicycle&avoids=Toll+Road&locale=en_US")

    assert getMapQuest("From", "To", "Fastest",
                       "None", "en_US") == (402, "https://www.mapquestapi.com/directions/v2/route?key=QIH00Aknfy7gGhpFAAxdSgEzAVLK74xF&from=From&to=To&routeType=Fastest&locale=en_US")

    assert getMapQuest("Seoul", "Bu", "Shortest", "Toll Road", "en_US") == (
        402, "https://www.mapquestapi.com/directions/v2/route?key=QIH00Aknfy7gGhpFAAxdSgEzAVLK74xF&from=Seoul&to=Bu&routeType=Shortest&avoids=Toll+Road&locale=en_US")