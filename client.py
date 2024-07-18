import socket
import threading
import pickle

class Client:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.role = None
        self.secret_word = None
        threading.Thread(target=self.receive_info).start()

    def receive_info(self):
        while True:
            data = self.client.recv(1024)
            if not data:
                break
            info = pickle.loads(data)
            if 'role' in info:
                self.role = info['role']
                if 'secret_word' in info:
                    self.secret_word = info['secret_word']
                print(f"Received role: {self.role}, secret_word: {self.secret_word}")
            elif 'turn' in info:
                self.take_turn()
            elif 'vote' in info:
                self.vote()
            elif 'result' in info:
                print(f"Game result: {info['result']}")
            elif 'play_again' in info:
                self.play_again()

    def take_turn(self):
        word = input("Enter a word describing the secret word: ")
        self.client.send(pickle.dumps(word))

    def vote(self):
        vote = input("Enter the player number you think is the imposter: ")
        self.client.send(pickle.dumps(vote))
    
    def play_again(self):
        response = input("Do you want to play again? (yes/no): ")
        self.client.send(pickle.dumps(response))

    def start(self):
        pass  # Implement the interaction loop here if needed

if __name__ == "__main__":
    client = Client()
    client.start()
