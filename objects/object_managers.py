

class G_Object_Manager():
    class __G_Object_Manager():
        def __init__(self):
            self.g_list = []

        def list(self):
            return self.g_list

        def add(self, g_object):
            self.g_list.append(g_object)

        def remove(self, g_object):
            self.g_list.remove(g_object)

    instance = None

    def __init__(self):
        if not G_Object_Manager.instance:
            G_Object_Manager.instance = G_Object_Manager.__G_Object_Manager()
