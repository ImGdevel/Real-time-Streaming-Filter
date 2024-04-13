class FilterInfo:
    
    def __init__(self):
        self.active_filters = []

    def add_filter(self, filter_label):
        if filter_label not in self.active_filters:
            self.active_filters.append(filter_label)

    def remove_filter(self, filter_label):
        if filter_label in self.active_filters:
            self.active_filters.remove(filter_label)

    def get_active_filters(self):
        return self.active_filters

    
class FaceFilter:

    def __init__(self):
        self.known_people = {}

    def add_person(self, name, face_encoding):
        self.known_people[name] = face_encoding

    def is_known_person(self, name, face_encoding):
        known_encoding = self.known_people.get(name)
        if known_encoding is not None:
            return True
        return False


class FilterManager:
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.active_filters = {}
        return cls._instance

    def add_filter(self, filter_label):
        self.filter_info.add_filter(filter_label)

    def remove_filter(self, filter_label):
        self.filter_info.remove_filter(filter_label)

    def get_active_filters(self):
        return self.filter_info.get_active_filters()

    def add_person(self, name, face_encoding):
        self.face_filter.add_person(name, face_encoding)

    def is_known_person(self, name, face_encoding):
        return self.face_filter.is_known_person(name, face_encoding)

    def test(self):
        testDict = dict()
        obj = self.filtering.object
        for cls in obj.orgNames:
            testDict[obj.orgNames[cls]] = 0
        for cls in obj.custNames:
            testDict[obj.custNames[cls]] = 1
        testDict["Human face"] = 1
        return testDict
