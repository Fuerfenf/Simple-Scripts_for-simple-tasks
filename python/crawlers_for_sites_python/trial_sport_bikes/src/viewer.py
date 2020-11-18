from storage import Storage


if __name__ == '__main__':
    storage = Storage()
    bike_list = storage.read()
    print(bike_list[0])
