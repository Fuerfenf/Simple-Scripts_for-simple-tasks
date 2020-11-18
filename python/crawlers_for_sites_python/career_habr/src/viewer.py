from package.storage import Storage

if __name__ == "__main__":
    storage = Storage()
    vacancy = storage.read()
    if isinstance(vacancy, dict):
        for k, v in vacancy.items():
            print(k, v)

