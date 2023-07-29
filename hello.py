from flask import Flask
from flask import render_template
from flask import request
import pandas as pd
import bcrypt
import random
import hashlib
import json
from flask import redirect
import qrcode

app = Flask(__name__)



# ==================== HASHING ====================
#  USANDO BCRYPT
# # # example password
# password = 'password123'
# # converting password to array of bytes
# bytes = password.encode('utf-8')
# # generating the salt

# # Hashing the password
# hash = bcrypt.hashpw(bytes, salt)
# print(hash)
# ==================== HASHING ====================



@app.route('/', methods=['GET', 'POST'])
@app.route('/<hashurl>')
def hello_world(hashurl=None):
    # input url
    # output: hash de una url
    new_hash = None 
    website_result = None
    new_hash2 = None
    image_path = None

    if request.method == 'GET' and hashurl != None:
        with open("hashes.json", "r") as archivo:
            d = json.load(archivo)

        for dictionario in d:
            if hashurl in dictionario:
                website = dictionario[hashurl]
                website_result = website
                break
        
        if website_result:
            if "https:" not in website:
                website = "https://"+website

            return render_template('redirect.html', website=website)

            
    if request.method == 'POST':
        url = request.form['url']
        bytes = url.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        hash = hash.decode('utf-8')
        hash = hash.strip("$2b$")
        random_number = random.randint(1, 49)
        new_hash = hash[random_number:random_number+7]
        dictionario = {}
        dictionario[new_hash] = url

        d = None
        with open("hashes.json", "r") as archivo:
            d = json.load(archivo)

        d.append(dictionario)
        serialized = json.dumps(d)

        with open("hashes.json", "w") as outfile:
            outfile.write(serialized)

        new_hash2 = "http://192.168.0.211:5000/"+new_hash 
        img = qrcode.make(new_hash2)
        image_path = "static/images/"+new_hash+".png"
        img.save(image_path)

    return render_template('index.html', hash=new_hash2, qrimage=image_path)
