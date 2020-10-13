import json
from random import shuffle

with open('a.json', encoding='utf-8') as file:
    data = json.load(file)

shuffle(data["Members"])

for member in data["Members"]:
    member["Delivery"] = []

    for score in range(5,0,-1):
        crops = list(filter(lambda x : x["Score"] == score, member["Preferences"]))

        for crop in crops:
            cropName = next(map(lambda x: x["Name"], filter(lambda x: x["Id"] == crop["Crop"], data["Crops"])))

            member["Delivery"].append(cropName)
            if len(member["Delivery"]) >= data["NumberOfCrops"]:
                break

        if len(member["Delivery"]) >= data["NumberOfCrops"]:
            break


for member in data["Members"]:
    print(member["Name"])
    print("\tPreferences:")
    for pref in member["Preferences"]:
        cropName = next(map(lambda x: x["Name"], filter(lambda x: x["Id"] == pref["Crop"], data["Crops"])))
        print("\t", pref["Score"], cropName)
    print("\n\tDelivery:", member["Delivery"], "\n")