
def get_id(object):
    if "jet_id" not in object.keys():
        object["jet_id"] = str(hash(object))
    return object["jet_id"]