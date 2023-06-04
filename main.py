import cv2 as cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import math
from googleplaces import GooglePlaces, types, lang
import requests
import json
import googlemaps
from datetime import datetime
from geopy.geocoders import Nominatim
import time
import gmaps
import polyline
import matplotlib.pyplot as plt
import folium
from folium import plugins

#33.744765412118596,72.78665559675179

API_KEY = 'AIzaSyArQKlHQYYgGkqTZD_eI5yobM9dqkReJ3Y'
google_places = GooglePlaces(API_KEY)

window = tk.Tk()
window.title("Age and Gender Detection")
window.geometry("800x800")

image_path = tk.StringVar()
coordinates = tk.StringVar()
placeOne = tk.StringVar()

def browse_image():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if path:
        image_path.set(path)
        display_image(path)

def display_image(path):
    image = Image.open(path)
    image.thumbnail((300, 300))  
    photo = ImageTk.PhotoImage(image)
    image_label.configure(image=photo)
    image_label.image = photo

def getFaceBox(net, frame, conf_threshold=0.7):
    frameOpencvDnn=frame.copy()
    frameHeight=frameOpencvDnn.shape[0]
    frameWidth=frameOpencvDnn.shape[1]
    blob=cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections=net.forward()
    faceBoxes=[]
    for i in range(detections.shape[2]):
        confidence=detections[0,0,i,2]
        if confidence>conf_threshold:
            x1=int(detections[0,0,i,3]*frameWidth)
            y1=int(detections[0,0,i,4]*frameHeight)
            x2=int(detections[0,0,i,5]*frameWidth)
            y2=int(detections[0,0,i,6]*frameHeight)
            faceBoxes.append([x1,y1,x2,y2])
            cv2.rectangle(frameOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn,faceBoxes

faceProto="opencv_face_detector.pbtxt"
faceModel="opencv_face_detector_uint8.pb"
ageProto="age_deploy.prototxt"
ageModel="age_net.caffemodel"
genderProto="gender_deploy.prototxt"
genderModel="gender_net.caffemodel"

MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList=['Male','Female']

faceNet=cv2.dnn.readNet(faceModel,faceProto)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)

padding = 20
res = []

def age_gender_detector(frame):
    t = time.time()
    frameFace, bboxes = getFaceBox(faceNet, frame)

    for bbox in bboxes:
        face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        print(f'Gender: {gender}')
        res.append(gender)

        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        print(f'Age: {age[1:-1]} years')
        res.append(age[1:-1])

        label = "{},{}".format(gender, age)
        cv2.putText(frameFace, label, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
    return frameFace

def perform_google_places_queries(lat, lng, age_range):
    array = []

    if age_range == '0-2':
            query_result = google_places.nearby_search(
                lat_lng ={'lat': lat, 'lng':lng},
                radius = 5000,
                types =[types.TYPE_ZOO])
            if query_result.has_attributions:
                print (query_result.html_attributions)

            for place in query_result.places:
                print(place)
                print (place.name)
                print("Latitude", place.geo_location['lat'])
                print("Longitude", place.geo_location['lng'])
                array.append(place.name)
                array.append(place.geo_location['lat'])
                array.append(place.geo_location['lng'])
                
                print()
                
            query_result = google_places.nearby_search(
                lat_lng ={'lat': lat, 'lng':lng},
                radius = 5000,
                types =[types.TYPE_PARK])

            if query_result.has_attributions:
                print (query_result.html_attributions)

            for place in query_result.places:
                print(place)
                print (place.name)
                print("Latitude", place.geo_location['lat'])
                print("Longitude", place.geo_location['lng'])
                array.append(place.name)
                array.append(place.geo_location['lat'])
                array.append(place.geo_location['lng'])
                print()

    elif age_range == '4-6':
        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_SCHOOL])
        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()

    elif age_range == '8-12':
        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_RESTAURANT])

        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()

        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_PARK])
        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()
            
        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_SCHOOL])

        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()

    elif age_range == '15-20':
        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_RESTAURANT])
        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()
            
        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_UNIVERSITY])

        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()
            
    elif age_range == '25-32':
        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_GYM])

        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()

        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_RESTAURANT])
        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()
            
        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_CAFE])

        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()

    elif age_range == '38-43':
        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_SHOPPING_MALL])
        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()
            
        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_MUSEUM])

        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()

    elif age_range == '48-53':
        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_SHOPPING_MALL])
        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()
            
        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_LIBRARY])

        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()

    elif age_range == '60-100':
        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_ZOO])
        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()

        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_MUSEUM])

        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()

        query_result = google_places.nearby_search(
            lat_lng ={'lat': lat, 'lng':lng},
            radius = 5000,
            types =[types.TYPE_PARK])

        if query_result.has_attributions:
            print (query_result.html_attributions)

        for place in query_result.places:
            print(place)
            print (place.name)
            print("Latitude", place.geo_location['lat'])
            print("Longitude", place.geo_location['lng'])
            array.append(place.name)
            array.append(place.geo_location['lat'])
            array.append(place.geo_location['lng'])
            print()
    return array
    pass

def get_coordinates(place):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if data["status"] == "OK":
            result = data["results"][0]
            location = result["geometry"]["location"]
            latitude = location["lat"]
            longitude = location["lng"]
            return latitude, longitude
        else:
            print("Unable to geocode the place.")
            return None
    except requests.exceptions.RequestException as e:
        print("Error occurred during the request:", e)
        return None
    except KeyError:
        print("Unable to parse the response.")
        return None

def plot():
    coordinates_value = coordinates.get()
    place_value = placeOne.get()
    print(place_value)
    c = get_coordinates(place_value)

    if c:
        s1, s2 = c
        print(f"Latitude: {s1}")
        print(f"Longitude: {s2}")

        lat, lng = coordinates_value.split(',')
        lat = float(lat)
        lng = float(lng)
        start = (lat, lng)
        stop = (s1, s2)
        
        map_obj = folium.Map(location=start, zoom_start=12)
        folium.plugins.AntPath([start, stop], color="blue", weight=2.5, dash_array=[10, 10]).add_to(map_obj)
        map_obj.save("map.html")
        print("Map saved to map.html")

def detect_age_gender():
    path = image_path.get()
    lat, lng = map(float, coordinates.get().split(','))

    try:
        input_image = cv2.imread(path)
        resized_image = cv2.resize(input_image, (300, 300))
        output_image = age_gender_detector(resized_image)

        output_image_pil = Image.fromarray(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
        output_image_pil.thumbnail((300, 300)) 
        photo = ImageTk.PhotoImage(output_image_pil)

        output_label = tk.Label(window, image=photo)
        output_label.image = photo
        output_label.pack(pady=10)

        age_range = res[1] 
        places = perform_google_places_queries(lat, lng, age_range)
        arr = places
        places_window = tk.Toplevel(window)
        places_window.title("Recommended Places")
        places_window.geometry("400x400")

        places_text = tk.Text(places_window)
        places_text.pack()

        place_entry = tk.Entry(places_window, textvariable=placeOne)
        place_entry.pack(pady=5)

        plot_button = tk.Button(places_window, text="plot", command=plot)
        plot_button.pack(pady=10)

        for place in places:
            if (type(place) == str):
                places_text.insert(tk.END, place + "\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))

browse_button = tk.Button(window, text="Browse", command=browse_image)
browse_button.pack(pady=10)

image_label = tk.Label(window)
image_label.pack(pady=10)

coordinates_label = tk.Label(window, text="Coordinates (lat,lng):")
coordinates_label.pack()

coordinates_entry = tk.Entry(window, textvariable=coordinates)
coordinates_entry.pack(pady=5)

go_button = tk.Button(window, text="Go", command=detect_age_gender)
go_button.pack(pady=10)

results_frame = tk.Frame(window)
results_frame.pack()

window.mainloop()
