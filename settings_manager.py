import os


class SettingsManager:
    def __init__(self):
        # Set default values
        self.settings = {
            "width": 1280,
            "height": 720,
            "fullscreen": False,
            "vsync": False,
            "sound": True,
            "music": True,
            "show_fps": True,
            "sensitivity": 0.002,
            "fov": 36,
            "texture_size": 0
        }

        # Validation requirements for each value:
        # Type (int, float or string); minimum value; maximum value
        self.validation = {
            "width": (int, 1, None),
            "height": (int, 1, None),
            "fullscreen": (bool, None, None),
            "vsync": (bool, None, None),
            "sound": (bool, None, None),
            "music": (bool, None, None),
            "show_fps": (bool, None, None),
            "sensitivity": (float, None, None),
            "fov": (float, 1, 179),
            "texture_size": (int, 0, None)
        }

    def load(self, filename="saves/settings.txt"):
        try:
            with open(filename, "r") as settings_file:
                while line := settings_file.readline():
                    # Ignore blank or comment lines
                    if len(line) == 0 or line[0] == '#':
                        continue

                    # Split key and value
                    try:
                        key, value = line.split(" ", 1)
                    except ValueError:
                        continue

                    # Parse numbers without a decimal separator as ints and
                    # numbers with a separator as floats
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            # :)
                            value = value.strip()
                            pass

                    # Parse boolean if value is specified as such
                    if key in self.validation and self.validation[key][0] == bool:
                        if value == "true":
                            value = True
                        elif value == "false":
                            value = False
                        else:
                            print("Settings value", key, "is not a boolean! Value",value)
                            continue

                    # Validate value
                    if key in self.validation:
                        # Allow int if required type is float
                        if not (type(value) == self.validation[key][0] or (type(value) == int and self.validation[key][0] == float)):
                            print("Settings value", key, "is of wrong type!")
                            continue

                        if not self.validation[key][1] == None and value < self.validation[key][1]:
                            print("Settings value", key, "is too small!")
                            continue

                        if not self.validation[key][2] == None and value > self.validation[key][2]:
                            print("Settings value", key, "is too large!")
                            continue

                    self.settings[key] = value
        except FileNotFoundError:
            pass

    def save(self, filename="saves/settings.txt"):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        with open(filename, "w") as settings_file:
            for key in self.settings:
                # Replace boolean values with correct strings
                if type(self.settings[key]) == bool:
                    if self.settings[key] == True:
                        self.settings[key] = "true"
                    elif self.settings[key] == False:
                        self.settings[key] = "false"

                settings_file.write(key + " " + str(self.settings[key]) + "\n")
