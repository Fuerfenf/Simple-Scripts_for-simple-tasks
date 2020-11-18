import pickle

DATA_FILE_NAME = 'habr_vacances.pkl'


class Storage(object):

    def __init__(self):
        self.vacancy = {}

    def write(self, data):
        with open(DATA_FILE_NAME, 'wb+') as data_file:
            pickle.dump(data, data_file)
        return DATA_FILE_NAME

    def read(self):
        try:
            with open(DATA_FILE_NAME, 'rb') as data_file:
                self.vacancy = pickle.load(data_file)
                return self.vacancy
        except FileNotFoundError:
            print("Process Error: No such file.")


