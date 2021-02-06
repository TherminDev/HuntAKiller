"""Fixes server indentation"""
with open('server.py', 'r') as file:
    script = file.read()

script = script.replace("\t", "    ")

with open('server.py', 'w') as file:
    file.truncate()
    file.write(script)
