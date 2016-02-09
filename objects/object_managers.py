# singleton class to hold a list of objects,
class SingletonList():
    class __SingletonList():
        def __init__(self):
            self.l_list = []

        def list(self):
            return self.l_list

        def add(self, l_object):
            self.l_list.append(l_object)

        def remove(self, l_object):
            self.l_list.remove(l_object)

    instance = None

    def __init__(self):
        if not SingletonList.instance:
            SingletonList.instance = SingletonList.__SingletonList()
