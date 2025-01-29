from reliable_finalizer import reliable_finalizer
from pickle import dump, load
from os import makedirs, path
from datetime import datetime


class Index:
    def __init__(self, save_file):
        self.save_file = save_file
        self.next_id = 0
        self.index = {}

    def get_file(self, id_):
        return self.index.get(id_)

    def new_file(self):
        dir_ = "logs"
        makedirs(dir_, exist_ok=True)
        filename = f"session{datetime.now().isoformat()}.txt".replace(":", "-")
        f_path = path.join(dir_, filename)

        with open(f_path, "w") as f:
            f.write("")

        self.index[self.next_id] = f_path
        self.next_id += 1
        return self.next_id - 1

    @reliable_finalizer
    def save(self):
        with open(self.save_file, "wb") as f:
            dump(self, f)


def get_index(save_file):
    try:
        with open(save_file, "rb") as f:
            return load(f)
    except IOError:
        return Index(save_file)
