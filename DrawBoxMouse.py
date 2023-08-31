import time
import pyautogui

class ActionRecorder:
    def __init__(self):
        self.actions = []

    def record_click(self, x, y):
        self.actions.append(("click", x, y))

    def record_key(self, key):
        self.actions.append(("key", key))

    def perform_actions(self):
        for action in self.actions:
            if action[0] == "click":
                pyautogui.click(action[1], action[2])
            elif action[0] == "key":
                pyautogui.write(action[1])
            time.sleep(0.5)

    def modify_action(self, action_type, *args):
        for index, action in enumerate(self.actions):
            if action[0] == action_type:
                if 0 <= index < len(self.actions):
                    self.actions[index] = (action_type,) + args



if __name__ == "__main__":
    recorder = ActionRecorder()

    recorder.record_click(500, 500)  # Click at coordinates (100, 100)
    recorder.record_key("hello")     # Type "hello"
    recorder.modify_action("key", "JJJJJJ")

    for action in recorder.actions:
        print(action)

    recorder.perform_actions()
