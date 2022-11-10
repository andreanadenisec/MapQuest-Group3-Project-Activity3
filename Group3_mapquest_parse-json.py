from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.ttk import Combobox, Treeview
import json
import urllib.parse
import requests

# MapQuest API and Key
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "QIH00Aknfy7gGhpFAAxdSgEzAVLK74xF"

def clear_frame():
   for widgets in right_frame.winfo_children():
      widgets.destroy()

def checkInput():
    clear_frame()
    entered_From = FromInput.get() 
    entered_To= ToInput.get() 
    entered_RouteType = selected_type.get() 
    entered_Avoid = selected_avoid.get()
    entered_Locale = selected_locale.get()

    if (entered_Locale == "English"):
        language = "en_US"
    elif (entered_Locale == "French"):
        language = "fr_FR"
    elif (entered_Locale == "Spanish"):
        language = "es_ES"
    elif (entered_Locale == "Russian"):
        language = "ru_RU"
 
    if(entered_From == '' or entered_To == ''):
        showinfo(
        title='Error',
        message=f'Enter Complete Details!'
    ) 
    else:
        getMapQuest(entered_From,entered_To,entered_RouteType,entered_Avoid,language)


        
def getMapQuest(orig,dest,routeType,avoid,language):

    if(avoid != 'None'):
        url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest, "routeType":routeType,'avoids':avoid,'locale':language})
    else:
        url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest, "routeType":routeType,'locale':language})
    
    print("URL: " + (url))

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        displayInfo(orig,dest,routeType,avoid,json_data,json_status,url)
    elif json_status == 402:
        showinfo(  
            title='Error',
            message=f"Status Code: " + str(json_status) + "\nInvalid user inputs for one or both locations."
        ) 

    elif json_status == 611:
        showinfo(  
            title='Error',
            message=f"Status Code: " + str(json_status) + "\nMissing an entry for one or both locations."
        ) 
    else:
        showinfo(  
            title='Error',
            message=f"For Status Code: " + str(json_status) + "\nRefer to: https://developer.mapquest.com/documentation/directions-api/status-code"
        ) 

def displayInfo(orig,dest,routeType,avoid,json_data,json_status,url):
    Label(right_frame, text="Directions from " + (orig) + " to " + (dest),bg='white', justify="left").grid(row=1, column=0, padx=5, pady=5,sticky = 'w')

    Label(right_frame, text="Route Type: " + (routeType),bg='white', justify="left").grid(row=2, column=0, padx=5, pady=2,sticky = 'w')

    Label(right_frame, text="Trip Duration: " + (json_data["route"]["formattedTime"]),bg='white', justify="left").grid(row=3, column=0, padx=5, pady=2,sticky = 'w')

    Label(right_frame, text="Avoid: " + (avoid),bg='white', justify="left").grid(row=4, column=0, padx=5, pady=2,sticky = 'w')

    Label(right_frame, text="Distance: ",bg='white', justify="left").grid(row=5, column=0, padx=5, pady=0,sticky = 'w')
    Label(right_frame, text="\tIn Miles: " + str(json_data["route"]["distance"]),bg='white', justify="left").grid(row=6 , column=0, padx=0, pady=0,sticky = 'w')
    Label(right_frame, text="\tIn Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)),bg='white', justify="left").grid(row=7 , column=0, padx=0, pady=0,sticky = 'w')


    routeFrame =  Frame(right_frame, width=1000, height=400,bg='white')
    routeFrame.grid(row=8, column=0, padx=5, pady=20)
    

    counter = 1 
    Label(routeFrame, text="Distance",bg='white', justify="left").grid(row=0 , column=0, padx=0, pady=0,sticky = 'w')
    Label(routeFrame, text="  Direction",bg='white', justify="left").grid(row=0 , column=1, padx=0, pady=0,sticky = 'w')
    for each in json_data["route"]["legs"][0]["maneuvers"]:

        if (counter <= 25):
            Label(routeFrame, text=" (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"),bg='white', justify="left").grid(row=counter , column=0, padx=0, pady=0,sticky = 'w')
            Label(routeFrame, text='  '+(each["narrative"]),bg='white', justify="left").grid(row=counter , column=1, padx=0, pady=0,sticky = 'w')
        counter += 1

root = Tk()  # create root window
root.title("MapQuest")  # title of the GUI window
root.config(bg="skyblue")  # specify background color

# Create left and right frames
left_frame = Frame(root, width=200, height=400, bg='white')
left_frame.grid(row=0, column=0, padx=10, pady=5)

right_frame = Frame(root, width=800, height=400, bg='white')
right_frame.grid(row=0, column=1, padx=10, pady=5)


# Create frames and labels in left_frame
Label(left_frame, text="Map Quest",bg='white').grid(row=0, column=0, padx=5, pady=5)
Label(left_frame, text="MapQuest provides simple directions \n and creates suitable route points \n depending on your preferred route type!",bg='white').grid(row=1, column=0, padx=5, pady=5)

Label(left_frame, text="Please enter the following details",bg='white').grid(row=2, column=0, padx=10, pady=5)


inputFrom = Frame(left_frame, width=180, height=185,bg='white')
inputFrom.grid(row=3, column=0, padx=5, pady=5)
Label(inputFrom, text='From',bg='white').grid(row=0, column=0,sticky = 'w')
FromInput = Entry(inputFrom,bg='white')
FromInput.grid(row=1, column=0)

inputTo = Frame(left_frame, width=180, height=185,bg='white')
inputTo.grid(row=4, column=0, padx=5, pady=5)
Label(inputTo, text='To',bg='white').grid(row=0, column=0,sticky = 'w')
ToInput = Entry(inputTo,bg='white')
ToInput.grid(row=1, column=0)

inputRouteType = Frame(left_frame, width=180, height=185,bg='white')
inputRouteType.grid(row=5, column=0, padx=5, pady=5)
Label(inputRouteType, text='Route Type',bg='white').grid(row=0, column=0,sticky = 'w')
selected_type = StringVar()
selected_type.set('Fastest')
routeType_cb = Combobox(inputRouteType, textvariable=selected_type)
routeType_cb['values'] = ['Fastest','Shortest','Pedestrian','Bicycle']
routeType_cb['state'] = 'readonly'
routeType_cb.grid(row=1, column=0,sticky = 'w')

inputAvoids = Frame(left_frame, width=180, height=185,bg='white')
inputAvoids.grid(row=6, column=0, padx=5, pady=5)
Label(inputAvoids, text='Avoid',bg='white').grid(row=0, column=0,sticky = 'w')
selected_avoid = StringVar()
selected_avoid.set('None')
Avoids_cb = Combobox(inputAvoids, textvariable=selected_avoid)
Avoids_cb['values'] = ['None','Toll Road','Ferry','Bridge','Tunnel']
Avoids_cb['state'] = 'readonly'
Avoids_cb.grid(row=1, column=0,sticky = 'w')

inputLocale = Frame(left_frame, width=180, height=185,bg='white')
inputLocale.grid(row=7, column=0, padx=5, pady=5)
Label(inputLocale, text='Route Language',bg='white').grid(row=0, column=0,sticky = 'w')
selected_locale = StringVar()
selected_locale.set('English')
Locale_cb = Combobox(inputLocale, textvariable=selected_locale)
Locale_cb['values'] = ['English','French','Spanish','Russian']
Locale_cb['state'] = 'readonly'
Locale_cb.grid(row=1, column=0,sticky = 'w')

go_button = Button(left_frame, text="Enter", command=checkInput, width=20)
go_button.grid(row=8, column=0, padx=5, pady=5)


root.mainloop()