class Session(object):

    def __init__(self, session={}, namespace='visualcaptcha'):
        self.session = session
        self.namespace = namespace

    def clear(self):
        self.session[self.namespace] = {}

    def get(self, key):
        if not self.session.get(self.namespace, None):
            self.clear()

        return self.session.get(self.namespace, {}).get(key, None)

    def set(self, key, value):
        if not self.session.get(self.namespace, None):
            self.clear()

        self.session[self.namespace][key] = value
