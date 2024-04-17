import toml
import os
import psutil
from datetime import datetime
import time

default_toml_location = "batterie_conf.toml"


def write_log_to_file(log):
    global file
    with open(file, 'a') as f:
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S: ")
        f.write(date_time + str(log) + "\n")

def write_log_to_terminal(log):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S: ")
    print(date_time + str(log))


def get_path():
    return os.path.dirname(os.path.realpath(__file__))


def load_toml():
    with open(default_toml_location, "r") as f:
        return toml.load(f)


class trigger_percentage():
    class percentage():
        def create_command(self):
            match self.command:
                case "default":
                    self.command = "dunstify -r " + str(self.dunstify_id) + " -I " + str(self.image) + " -u " + str(
                        self.massage_type) + " -t " + str(self.display_time) + " \"" + self.app_name + " \"" + " \"" + str(
                        self.massage) + "\""
                case "none":
                    self.command = ""
                case _:
                    if self.command.startswith("&& "):
                        self.command = "dunstify -r " + str(self.dunstify_id) + " -I " + str(self.image) + " -u " + str(
                            self.massage_type) + " \"" + str(self.massage) + "\" " + self.command

        def __init__(self, config, dunstify_id=17, app_name="Battery", log: bool = None, log_to_file:int = 0):
            if ["trigger_percent", "trigger_condition", "image", "massage", "massage_type", "display_time", "command",
                "log"] == list(config.keys()):
                self.trigger_percent = config["trigger_percent"]
                self.trigger_condition = config["trigger_condition"]
                self.image = config["image"]
                self.massage = config["massage"]
                self.massage_type = config["massage_type"]
                self.display_time = config["display_time"]
                self.command = config["command"]
                self.log_to_file = log_to_file
                if log == None:
                    if config["log"] == "true" or config["log"] == "True" or config["log"] == True:
                        self.log = True
                    elif config["log"] == "false" or config["log"] == "False" or config["log"] == False:
                        self.log = False
                    else:
                        raise Exception("log is not correct" + str(config["log"]))
                else:
                    self.log = log
                self.dunstify_id = dunstify_id
                self.app_name = app_name
            else:
                raise Exception("config file is not correct")
            self.massage = self.massage.replace('%%', str(self.trigger_percent) + "%")
            if self.image.startswith("/") or self.image.startswith("~"):
                pass
            else:
                self.image = os.path.join(get_path(), self.image)
            self.create_command()
            self.below_trigger_percent = (psutil.sensors_battery().percent <= self.trigger_percent)
            self.above_trigger_percent = (psutil.sensors_battery().percent >= self.trigger_percent)

        def log_state(self):
            match self.log_to_file:
                case 0:
                    pass
                case 1:
                    if self.log:
                        match self.massage_type:
                            case "0":
                                write_log_to_file("[INFO] " + self.massage)
                            case "1":
                                write_log_to_file("[WARNING] " + self.massage)
                            case "2":
                                write_log_to_file("[CRITICAL] " + self.massage)
                            case _:
                                write_log_to_file("[WARNING] massage_type is not correct: " + str(self.massage_type))
                                write_log_to_file("[INFO] " + self.massage)
                case 2:
                    if self.log:
                        match self.massage_type:
                            case "0":
                                write_log_to_terminal("[INFO] " + self.massage)
                            case "1":
                                write_log_to_terminal("[WARNING] " + self.massage)
                            case "2":
                                write_log_to_terminal("[CRITICAL] " + self.massage)
                            case _:
                                write_log_to_terminal("[WARNING] massage_type is not correct: " + str(self.massage_type))
                                write_log_to_terminal("[INFO] " + self.massage)
                case 3:
                    if self.log:
                        match self.massage_type:
                            case "0":
                                write_log_to_file("[INFO] " + self.massage)
                                write_log_to_terminal("[INFO] " + self.massage)
                            case "1":
                                write_log_to_file("[WARNING] " + self.massage)
                                write_log_to_terminal("[WARNING] " + self.massage)
                            case "2":
                                write_log_to_file("[CRITICAL] " + self.massage)
                                write_log_to_terminal("[CRITICAL] " + self.massage)
                            case _:
                                write_log_to_file("[WARNING] massage_type is not correct: " + str(self.massage_type))
                                write_log_to_file("[INFO] " + self.massage)
                                write_log_to_terminal("[WARNING] massage_type is not correct: " + str(self.massage_type))
                                write_log_to_terminal("[INFO] " + self.massage)
                case 4:
                    match self.massage_type:
                        case "0":
                            write_log_to_file("[INFO] " + self.massage)
                        case "1":
                            write_log_to_file("[WARNING] " + self.massage)
                        case "2":
                            write_log_to_file("[CRITICAL] " + self.massage)
                        case _:
                            write_log_to_file("[WARNING] massage_type is not correct: " + str(self.massage_type))
                            write_log_to_file("[INFO] " + self.massage)
                case 5:
                    match self.massage_type:
                        case "0":
                            write_log_to_terminal("[INFO] " + self.massage)
                        case "1":
                            write_log_to_terminal("[WARNING] " + self.massage)
                        case "2":
                            write_log_to_terminal("[CRITICAL] " + self.massage)
                        case _:
                            write_log_to_terminal("[WARNING] massage_type is not correct: " + str(self.massage_type))
                            write_log_to_terminal("[INFO] " + self.massage)
                case 6:
                    match self.massage_type:
                        case "0":
                            write_log_to_file("[INFO] " + self.massage)
                            write_log_to_terminal("[INFO] " + self.massage)
                        case "1":
                            write_log_to_file("[WARNING] " + self.massage)
                            write_log_to_terminal("[WARNING] " + self.massage)
                        case "2":
                            write_log_to_file("[CRITICAL] " + self.massage)
                            write_log_to_terminal("[CRITICAL] " + self.massage)
                        case _:
                            write_log_to_file("[WARNING] massage_type is not correct: " + str(self.massage_type))
                            write_log_to_file("[INFO] " + self.massage)
                            write_log_to_terminal("[WARNING] massage_type is not correct: " + str(self.massage_type))
                            write_log_to_terminal("[INFO] " + self.massage)
                case _:
                    pass

        def check(self):
            match self.trigger_condition:
                case "discharging":
                    if psutil.sensors_battery().power_plugged == False:
                        if round(psutil.sensors_battery().percent) <= self.trigger_percent:
                            if self.below_trigger_percent == False:
                                os.system(self.command)
                                self.log_state()
                                self.below_trigger_percent = True
                        else:
                            self.below_trigger_percent = False
                case "charging":
                    if psutil.sensors_battery().power_plugged == True:
                        if round(psutil.sensors_battery().percent) >= self.trigger_percent:
                            if self.above_trigger_percent == False:
                                os.system(self.command)
                                self.log_state()
                                self.above_trigger_percent = True
                        else:
                            self.above_trigger_percent = False
                case "both":
                    if psutil.sensors_battery().power_plugged == False:
                        if round(psutil.sensors_battery().percent) <= self.trigger_percent:
                            if self.below_trigger_percent == False:
                                os.system(self.command)
                                self.log_state()
                                self.below_trigger_percent = True
                        else:
                            self.below_trigger_percent = False
                    else:
                        if round(psutil.sensors_battery().percent) >= self.trigger_percent:
                            if self.above_trigger_percent == False:
                                os.system(self.command)
                                self.log_state()
                                self.above_trigger_percent = True
                        else:
                            self.above_trigger_percent = False

    def check(self):
        for i in self.percentages:
            self.percentages[i].check()

    def __init__(self, config, dunstify_id=17, app_name="Battery", log: bool = None, log_to_file:int = 0):
        self.percentages = {}
        for i in list(config.keys()):
            self.percentages[i] = self.percentage(config[i], dunstify_id, app_name, log, log_to_file)


class trigger_chargingstate():
    class percentage():
        def create_command(self):
            match self.command:
                case "default":
                    self.command = "dunstify -r " + str(self.dunstify_id) + " -I " + str(self.image) + " -u " + str(
                        self.massage_type) + " -t " + str(
                        self.display_time) + " \"" + self.app_name + " \"" + " \"" + str(self.massage) + "\""
                case "none":
                    self.command = ""
                case _:
                    if self.command.startswith("&& "):
                        self.command = "dunstify -r " + str(self.dunstify_id) + " -I " + str(
                            self.image) + " -u " + str(self.massage_type) + " \"" + str(
                            self.massage) + "\" " + self.command

        def __init__(self, min, max, image, command, dunstify_id, app_name, massage, massage_type, display_time, log, charging, log_to_file:int=0):
            self.min = min
            self.max = max
            self.image = image
            self.command = command
            self.dunstify_id = dunstify_id
            self.app_name = app_name
            self.massage = massage
            self.massage_type = massage_type
            self.display_time = display_time
            self.log = log
            self.charging = charging
            self.log_to_file = log_to_file
            self.create_command()

        def log_state(self):
            match self.log_to_file:
                case 0:
                    pass
                case 1:
                    if self.log:
                        massage = self.massage.replace('%%', str(round(psutil.sensors_battery().percent)) + "%")
                        match self.massage_type:
                            case "0":
                                write_log_to_file("[INFO] " + massage)
                            case "1":
                                write_log_to_file("[WARNING] " + massage)
                            case "2":
                                write_log_to_file("[CRITICAL] " + massage)
                            case _:
                                write_log_to_file("[WARNING] massage_type is not correct: " + str(self.massage_type))
                                write_log_to_file("[INFO] " + massage)
                case 2:
                    if self.log:
                        massage = self.massage.replace('%%', str(round(psutil.sensors_battery().percent)) + "%")
                        match self.massage_type:
                            case "0":
                                write_log_to_terminal("[INFO] " + massage)
                            case "1":
                                write_log_to_terminal("[WARNING] " + massage)
                            case "2":
                                write_log_to_terminal("[CRITICAL] " + massage)
                            case _:
                                write_log_to_terminal("[WARNING] massage_type is not correct: " + str(self.massage_type))
                                write_log_to_terminal("[INFO] " + massage)
                case 3:
                    if self.log:
                        massage = self.massage.replace('%%', str(round(psutil.sensors_battery().percent)) + "%")
                        match self.massage_type:
                            case "0":
                                write_log_to_file("[INFO] " + massage)
                                write_log_to_terminal("[INFO] " + massage)
                            case "1":
                                write_log_to_file("[WARNING] " + massage)
                                write_log_to_terminal("[WARNING] " + massage)
                            case "2":
                                write_log_to_file("[CRITICAL] " + massage)
                                write_log_to_terminal("[CRITICAL] " + massage)
                            case _:
                                write_log_to_file("[WARNING] massage_type is not correct: " + str(self.massage_type))
                                write_log_to_file("[INFO] " + massage)
                                write_log_to_terminal("[WARNING] massage_type is not correct: " + str(self.massage_type))
                                write_log_to_terminal("[INFO] " + massage)
                case 4:
                    massage = self.massage.replace('%%', str(round(psutil.sensors_battery().percent)) + "%")
                    match self.massage_type:
                        case "0":
                            write_log_to_file("[INFO] " + massage)
                        case "1":
                            write_log_to_file("[WARNING] " + massage)
                        case "2":
                            write_log_to_file("[CRITICAL] " + massage)
                        case _:
                            write_log_to_file("[WARNING] massage_type is not correct: " + str(self.massage_type))
                            write_log_to_file("[INFO] " + massage)
                case 5:
                    massage = self.massage.replace('%%', str(round(psutil.sensors_battery().percent)) + "%")
                    match self.massage_type:
                        case "0":
                            write_log_to_terminal("[INFO] " + massage)
                        case "1":
                            write_log_to_terminal("[WARNING] " + massage)
                        case "2":
                            write_log_to_terminal("[CRITICAL] " + massage)
                        case _:
                            write_log_to_terminal("[WARNING] massage_type is not correct: " + str(self.massage_type))
                            write_log_to_terminal("[INFO] " + massage)
                case 6:
                    massage = self.massage.replace('%%', str(round(psutil.sensors_battery().percent)) + "%")
                    match self.massage_type:
                        case "0":
                            write_log_to_file("[INFO] " + massage)
                            write_log_to_terminal("[INFO] " + massage)
                        case "1":
                            write_log_to_file("[WARNING] " + massage)
                            write_log_to_terminal("[WARNING] " + massage)
                        case "2":
                            write_log_to_file("[CRITICAL] " + massage)
                            write_log_to_terminal("[CRITICAL] " + massage)
                        case _:
                            write_log_to_file("[WARNING] massage_type is not correct: " + str(self.massage_type))
                            write_log_to_file("[INFO] " + massage)
                            write_log_to_terminal("[WARNING] massage_type is not correct: " + str(self.massage_type))
                            write_log_to_terminal("[INFO] " + massage)
                case _:
                    pass

        def check(self):
            if psutil.sensors_battery().power_plugged == self.charging:
                if psutil.sensors_battery().percent >= self.min and psutil.sensors_battery().percent <= self.max:
                    os.system(self.command.replace("%%", str(round(psutil.sensors_battery().percent)) + "%"))
                    self.log_state()

    def up(self):
        break_after = False
        for i in range(len(self.list_of_percentages)):
            print(i)
            min = self.list_of_percentages[i]
            if i == len(self.list_of_percentages) - 1:
                max = 100.0
            elif self.list_of_percentages[i + 1] == 100.0:
                max = 100.0
                break_after = True
            else:
                max = self.list_of_percentages[i + 1]
            self.trigger_percentages[i] = self.percentage(min, max, self.percentages[self.list_of_percentages[i]],
                                                              self.command, self.dunstify_id, self.app_name,
                                                              self.massage, self.massage_type, self.display_time,
                                                              self.log, self.charging, self.log_to_file)
            if break_after:
                break

    def down(self):
        for i in range(len(self.list_of_percentages) - 1, -1, -1):
            skip = False
            print(i)
            max = self.list_of_percentages[i]
            if i == 0 and self.list_of_percentages[i] == 0.0:
                continue
            elif i == 0:
                min = 0.0
            else:
                min = self.list_of_percentages[i - 1]
            self.trigger_percentages[i] = self.percentage(min, max, self.percentages[self.list_of_percentages[i]],
                                                              self.command, self.dunstify_id, self.app_name,
                                                              self.massage, self.massage_type, self.display_time,
                                                              self.log, self.charging, self.log_to_file)

    def nearest_to(self):
        for i in range(len(self.list_of_percentages)):
            if i == 0:
                min = 0.0
            else:
                min = (self.list_of_percentages[i]-self.list_of_percentages[i - 1]) / 2 + self.list_of_percentages[i - 1]
            if i == len(self.list_of_percentages) - 1:
                max = 100.0
            else:
                max = (self.list_of_percentages[i+1]-self.list_of_percentages[i]) / 2 + self.list_of_percentages[i]
            self.trigger_percentages[i] = self.percentage(min, max, self.percentages[self.list_of_percentages[i]],
                                                              self.command, self.dunstify_id, self.app_name,
                                                              self.massage, self.massage_type, self.display_time,
                                                              self.log, self.charging, self.log_to_file)

    def check(self):
        if self.is_charging != psutil.sensors_battery().power_plugged:
            for i in self.trigger_percentages:
                self.trigger_percentages[i].check()
            self.is_charging = psutil.sensors_battery().power_plugged

    def __init__(self, charging: bool, config, dunstify_id: int = 17, app_name: str = "Battery", log_to_file:int =4):
        self.is_charging = not(psutil.sensors_battery().power_plugged)
        self.charging = charging
        self.dunstify_id = dunstify_id
        self.app_name = app_name
        self.log_to_file = log_to_file
        self.trigger_percentages = {}
        if "display" in config.keys():
            self.display = config["display"]
            config.pop("display")
        else:
            raise Exception("config file is not correct")
        if "massage" in config.keys():
            self.massage = config["massage"]
            config.pop("massage")
        else:
            raise Exception("config file is not correct")
        if "massage_type" in config.keys():
            self.massage_type = config["massage_type"]
            config.pop("massage_type")
        else:
            raise Exception("config file is not correct")
        if "display_time" in config.keys():
            self.display_time = config["display_time"]
            config.pop("display_time")
        if "command" in config.keys():
            self.command = config["command"]
            config.pop("command")
        else:
            raise Exception("config file is not correct")
        if "log" in config.keys():
            if config["log"] == "true" or config["log"] == "True" or config["log"] == True:
                self.log = True
            elif config["log"] == "false" or config["log"] == "False" or config["log"] == False:
                self.log = False
            else:
                raise Exception("log is not correct" + str(config["log"]))
            config.pop("log")
        else:
           raise Exception("config file is not correct")
        self.percentages = {}
        for i in list(config.keys()):
            try:
                float_i = float(i)
            except:
                raise Exception("is no number: " + str(i))
            self.percentages[float_i] = config[i]
        match self.display:
            case "up":
                self.list_of_percentages = sorted(list(self.percentages.keys()), key=float, reverse=not (self.charging))
                self.up()
            case "down":
                self.list_of_percentages = sorted(list(self.percentages.keys()), key=float, reverse=not (self.charging))
                self.down()
            case "nearest to":
                self.list_of_percentages = sorted(list(self.percentages.keys()), key=float, reverse=False)
                self.nearest_to()
            case _:
                raise Exception("display is not correct: " + str(self.display))

def start():
    global file
    if os.path.isfile(default_toml_location):
        toml_file = load_toml()
        if "config" in toml_file.keys():
            if "log" in toml_file["config"].keys() and "log_to" in toml_file["config"].keys():
                match toml_file["config"]["log"]:
                    case "false":
                        log_to_file = 0
                    case "custom":
                        match toml_file["config"]["log_to"]:
                            case "file":
                                log_to_file = 1
                            case "terminal":
                                log_to_file = 2
                            case "both":
                                log_to_file = 3
                            case _:
                                raise Exception("log_to is not correct")
                    case "true":
                        match toml_file["config"]["log_to"]:
                            case "file":
                                log_to_file = 4
                            case "terminal":
                                log_to_file = 5
                            case "both":
                                log_to_file = 6
                            case _:
                                raise Exception("log_to is not correct")
                    case _:
                        raise Exception("log is not correct")
            else:
                raise Exception("config file is not correct")
            if "file_path" in toml_file["config"].keys() and toml_file["config"]["file_path"] != "" and toml_file["config"]["log_to"] != "terminal":
                match toml_file["config"]["file_path"][-1]:
                    case "~":
                        if os.path.exists(os.path.dirname(toml_file["config"]["file_path"])):
                            file = toml_file["config"]["file_path"]
                    case "/":
                        if os.path.exists(os.path.dirname(toml_file["config"]["file_path"])):
                            file = toml_file["config"]["file_path"]
                    case _:
                        file = os.path.join(get_path(), toml_file["config"]["file_path"])
            else:
                file = os.path.join(get_path(), "battery-log.txt")
            if "update_interval" in toml_file["config"].keys():
                try:
                    update_interval = float(toml_file["config"]["update_interval"])
                except:
                    raise Exception("update_interval is not correct")
            else:
                raise Exception("update_interval is not correct")
            if "dunstify_id" in toml_file["config"].keys():
                try:
                    dunstify_id = int(toml_file["config"]["dunstify_id"])
                except:
                    raise Exception("dunstify_id is not correct")
            else:
                raise Exception("dunstify_id is not correct")
            if "app_name" in toml_file["config"].keys():
                app_name = toml_file["config"]["app_name"]
            else:
                raise Exception("app_name is not correct")
        program = []
        if "trigger" in toml_file.keys():
            if "chargingstate" in toml_file["trigger"].keys():
                if "charging" in toml_file["trigger"]["chargingstate"].keys():
                    program.append(trigger_chargingstate(True, toml_file["trigger"]["chargingstate"]["charging"], dunstify_id, app_name, log_to_file))
                if "discharging" in toml_file["trigger"]["chargingstate"].keys():
                    program.append(trigger_chargingstate(False, toml_file["trigger"]["chargingstate"]["discharging"], dunstify_id, app_name, log_to_file))
            if "percentage" in toml_file["trigger"].keys():
                program.append(trigger_percentage(toml_file["trigger"]["percentage"], dunstify_id, app_name, log_to_file))
        while True:
            for i in program:
                i.check()
            match log_to_file:
                case 0:
                    pass
                case 4:
                    write_log_to_file("[capacity] " + str(round(psutil.sensors_battery().percent,1)) + "%")
                case 5:
                    write_log_to_terminal("[capacity] " + str(round(psutil.sensors_battery().percent,1)) + "%")
                case 6:
                    write_log_to_file("[capacity] " + str(round(psutil.sensors_battery().percent,1)) + "%")
                    write_log_to_terminal("[capacity] " + str(round(psutil.sensors_battery().percent,1)) + "%")
                case _:
                    pass
            time.sleep(update_interval)

if __name__ == "__main__":
    start()