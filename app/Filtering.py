import ObjectFiltering
class Filtering:
    
    def __init__(self):
        self.object = ObjectFiltering.ObjectFiltering()
        
    def filtering(self, img, objects, face = None):
        boxesList = []
        objList = self.object.objectDetect(img, objects)
        for obj in objList:
            boxesList.append(obj)
        return boxesList