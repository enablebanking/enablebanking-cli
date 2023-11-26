import os


class CpStore:
    def __init__(self, root_path):
        self.root_path = root_path

    @property
    def cp_users_path(self):
        return os.path.join(self.root_path, "cp", "users")

    def get_default_user_path(self):
        with open(os.path.join(self.cp_users_path, ".default"), "r") as f:
            user_filename = f.read().strip()
        return os.path.join(self.cp_users_path, user_filename)

    def set_default_user_filename(self, user_filename):
        with open(os.path.join(self.cp_users_path, ".default"), "w") as f:
            f.write(user_filename)
