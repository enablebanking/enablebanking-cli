import json
import os


class CpStore:
    def __init__(self, root_path):
        self.root_path = root_path

    @property
    def cp_apps_path(self):
        return os.path.join(self.root_path, "cp", "apps")

    def get_app_filename(self, app_id):
        return f"{app_id}.json"

    def get_app_path(self, app_id=None):
        if app_id is None:
            return self.get_default_app_path()
        return os.path.join(self.cp_apps_path, self.get_app_filename(app_id))

    def get_default_app_path(self):
        with open(os.path.join(self.cp_apps_path, ".default"), "r") as f:
            app_filename = f.read().strip()
        return os.path.join(self.cp_apps_path, app_filename)

    def set_default_app_filename(self, app_filename):
        with open(os.path.join(self.cp_apps_path, ".default"), "w") as f:
            f.write(app_filename)

    def list_app_files(self):
        return [
            filename
            for filename in os.listdir(self.cp_apps_path)
            if os.path.splitext(filename)[1] == ".json"
        ]

    def load_app_files(self):
        default_app_path = self.get_default_app_path()
        apps_data = []
        for app_filename in self.list_app_files():
            app_path = os.path.join(self.cp_apps_path, app_filename)
            try:
                with open(app_path, "r") as f:
                    app_data = json.loads(f.read())
            except Exception as e:
                continue
            app_data["_default"] = default_app_path == app_path
            apps_data.append(app_data)
        return apps_data

    def load_app_file(self, app_id=None):
        app_path = self.get_app_path(app_id)
        with open(app_path, "r") as f:
            app_data = json.loads(f.read())
        return app_data

    @property
    def cp_users_path(self):
        return os.path.join(self.root_path, "cp", "users")

    def get_user_filename(self, user_id):
        return f"{user_id}.json"

    def get_user_path(self, user_id=None):
        if user_id is None:
            return self.get_default_user_path()
        return os.path.join(self.cp_users_path, self.get_user_filename(user_id))

    def get_default_user_path(self):
        with open(os.path.join(self.cp_users_path, ".default"), "r") as f:
            user_filename = f.read().strip()
        return os.path.join(self.cp_users_path, user_filename)

    def set_default_user_filename(self, user_filename):
        with open(os.path.join(self.cp_users_path, ".default"), "w") as f:
            f.write(user_filename)

    def list_user_files(self):
        return [
            filename
            for filename in os.listdir(self.cp_users_path)
            if os.path.splitext(filename)[1] == ".json"
        ]

    def load_user_files(self):
        default_user_path = self.get_default_user_path()
        users_data = []
        for user_filename in self.list_user_files():
            user_path = os.path.join(self.cp_users_path, user_filename)
            try:
                with open(user_path, "r") as f:
                    user_data = json.loads(f.read())
            except Exception as e:
                continue
            user_data["_default"] = default_user_path == user_path
            users_data.append(user_data)
        return users_data

    def remove_user_file(self, user_id=None):
        user_path = self.get_user_path(user_id)
        os.remove(user_path)
        users_data = self.load_user_files()
        if not len(users_data):
            os.remove(os.path.join(self.cp_users_path, ".default"))
        self.set_default_user_filename(f"{users_data[0]['localId']}.json")
