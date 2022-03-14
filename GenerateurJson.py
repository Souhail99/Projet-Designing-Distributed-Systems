import json
from datetime import *

#{'id': 781168593, 'price': '2581.65000000', 'qty': '0.04960000', 
# 'quoteQty': '128.04984000', 'time': 1647268765598, 'isBuyerMaker': True, 'isBestMatch': True}
def product(id,prix,timestamp,pair):
    itemId = id
    price = prix
    time=datetime.fromtimestamp(timestamp)
    availableColorAndSize = {
        'color': {'blue-black': ['M', 'L', 'XL'],
                  'black-white': ['L']}
    }
    
    # Returns a JSON formatted file based on the dictionary shown
    return json.dump(
        {'itemId': itemId,
         'price': price,
         'date': time,
         'Pair': pair})


liste=[]
jsonfile=[]
for element in liste:
    for i in range(len(element)-4):
        jsonfile.append(product(element[i],element[i+1],element[i+2],element[i+3],element[i+4]))


with open("fichier.txt", "w") as file:
    file.write("\n".join(jsonfile))