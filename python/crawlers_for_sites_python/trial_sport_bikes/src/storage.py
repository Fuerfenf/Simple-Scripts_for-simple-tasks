import pickle

DATA_FILE_NAME = 'bike_data.pkl'


class Storage(object):

    def __init__(self):
        self.bike_dict = {}

        with open(DATA_FILE_NAME, 'rb') as data_file:
            self.bike_dict = pickle.load(data_file)

    def write(self, data):
        with open(DATA_FILE_NAME, 'wb+') as data_file:
            pickle.dump(data, data_file)

    def read(self):
        return self.bike_dict
