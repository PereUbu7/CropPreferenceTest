import json
from random import shuffle


def pickCrop(id):
    for crop in data["Crops"]:
        if crop["Id"] == id and crop["Picked"] <= crop["Amount"]:
            crop["Picked"] += 1
            break
        elif crop["Picked"] > crop["Amount"]:
            raise Exception("Cannot pick more (", crop["Picked"], ") than what we have (", crop["Amount"], ") of", crop["Name"])

with open('a.json', encoding='utf-8') as file:
    data = json.load(file)

shuffle(data["Members"])

for crop in data["Crops"]:
    crop["Picked"] = 0

for member in data["Members"]:
    member["Delivery"] = []

    # Add featured items
    featuredCrops = list(filter(lambda x : x['Featured'] and x["Picked"] < x["Amount"], data["Crops"]))

    for featured in featuredCrops:
        score = next(filter(lambda x : x["Crop"] == featured["Id"], member["Preferences"]))["Score"]

        if score >= 3:
            member["Delivery"].append(featured["Name"])
            pickCrop(featured["Id"])

        if score == 5 and len(member["Delivery"]) < data["NumberOfCrops"]:
            member["Delivery"].append(featured["Name"])
            pickCrop(featured["Id"])

    for score in range(5,0,-1):
        crops = list(filter(lambda x : x["Score"] == score, member["Preferences"]))

        for crop in crops:
            cropNames = list(map(lambda x: x["Name"], filter(lambda x: x["Id"] == crop["Crop"] and x["Picked"] < x["Amount"], data["Crops"])))

            if len(cropNames) == 1 and len(list(filter(lambda x : x == cropNames[0], member["Delivery"]))) == 0:
                member["Delivery"].append(cropNames[0])
                pickCrop(crop["Crop"])
            if len(member["Delivery"]) >= data["NumberOfCrops"]:
                break

        if len(member["Delivery"]) >= data["NumberOfCrops"]:
            break

for crop in data["Crops"]:
    print(crop["Name"])
    print("\tAmount:", crop["Amount"], "\tPicked:", crop["Picked"])

print("\n")

for member in data["Members"]:
    print(member["Name"])
    print("\tPreferences:")
    for pref in member["Preferences"]:
        cropName = next(map(lambda x: x["Name"], filter(lambda x: x["Id"] == pref["Crop"], data["Crops"])))
        print("\t", pref["Score"], cropName)
    print("\n\tDelivery:", member["Delivery"], "\n")

