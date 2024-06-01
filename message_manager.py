import os
class messageManager():
    def __init__(self):
        self.messages = []
        current_file = open("resources/messages.txt", "r")

    def add_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def clear_messages(self):
        self.messages = []

    def save_messages(self):
        current_file = open("resources/messages.txt", "w")
        for message in self.messages:
            current_file.write(message + "\n")
        current_file.close()

    def get_latest_save_index(self):
        len(os.listdir("resources/conversations"))