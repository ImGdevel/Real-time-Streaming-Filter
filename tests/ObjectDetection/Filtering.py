import ObjectFiltering
class Filtering:
    
    def __init__(self, savePath):
        self.object = ObjectFiltering()
        self.savePath = savePath
        
    def filtering(self, img, face, objects):
        boxesList = []
        boxesList.append(self.object.objectDetect(objects))
        return boxesList