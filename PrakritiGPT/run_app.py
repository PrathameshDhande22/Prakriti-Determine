import subprocess

#Run model.py
with open('./model.py','r') as f:
    exec(f.read())
# #Run get_intent.py
with open('./get_intent.py','r') as f:
    exec(f.read())

# #Run app.py
with open('./app.py','r') as f:
    exec(f.read())

