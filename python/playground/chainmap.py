from collections import ChainMap

globals = {"python":"3.9", "java":"11"}
locals = {"python":"3.8"}

# priority map, faster than merging the dicts
cm = ChainMap(locals, globals)

print(cm["python"] == "3.8")
print(cm["java"] == "11")

# updates the first level (locals)
cm["python"] = "3.10"

print(cm["python"])
print(cm)
