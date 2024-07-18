import socket
import threading
import random
import pickle

# Placeholder secret words
words = ['apple', 'banana', 'cherry', 'date', 'elderberry']

class Server:
    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(3)
        self.clients = []
        self.secret_word = None
        self.player_roles = {}

    def handle_client(self, client, addr):
        self.clients.append(client)
        if len(self.clients) == 3:
            self.secret_word = random.choice(words)
            self.assign_roles()
            self.send_start_info()
            self.start_gameplay()

    def assign_roles(self):
        role_list = random.sample(self.clients, len(self.clients))
        roles = {i + 1: 'detective' for i in range(2)}
        roles[3] = 'imposter'
        self.player_roles = roles
        print('Roles:', self.player_roles)

    def send_start_info(self):
        for idx, client in enumerate(self.clients, start=1):
            role = self.player_roles[idx]
            info = {'role': role}
            if role == 'detective':
                info['secret_word'] = self.secret_word
            client.send(pickle.dumps(info))

    def start_gameplay(self):
        for client in self.clients:
            client.send(pickle.dumps({"turn": True}))
            data = client.recv(1024)
            word = pickle.loads(data)
            print(f"Player said: {word}")
        self.collect_votes()

    def collect_votes(self):
        votes = {}
        for client in self.clients:
            client.send(pickle.dumps({"vote": True}))
            data = client.recv(1024)
            vote = pickle.loads(data)
            votes[vote] = votes.get(vote, 0) + 1
        alleged_imposter = int(max(votes, key=votes.get))
        self.announce_result(alleged_imposter)

    def announce_result(self, alleged_imposter):
        for _, client in enumerate(self.clients, start=1):
            if self.player_roles[alleged_imposter] == 'imposter':
                client.send(pickle.dumps({"result": 'Detectives win!'}))
            else:
                client.send(pickle.dumps({"result": 'Detectives lose...'}))
       # Ask players if they want to play again
        self.ask_play_again()

    def ask_play_again(self):
        responses = []
        for client in self.clients:
            client.send(pickle.dumps({"play_again": True}))
            data = client.recv(1024)
            response = pickle.loads(data)
            responses.append(response)

        if responses.count('yes') == len(self.clients):
            print("Restarting game...")
            self.reset_game()
        else:
            print("Shutting down server...")
            self.shutdown_server()

    def reset_game(self):
        self.secret_word = random.choice(words)
        self.assign_roles()
        self.send_start_info()
        self.start_gameplay()

    def start(self):
        print("Server started")
        try:
            while True:
                client, addr = self.server.accept()
                print(f"New connection: {addr}")
                threading.Thread(target=self.handle_client, args=(client, addr)).start()
        except Exception as e:
            print(f"Server stopped: {e}")
        finally:
            self.shutdown_server()


    def shutdown_server(self):
        print("Shutting down server...")
        # Close all client connections
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        # Close the server socket
        self.server.close()
        print("Server shut down successfully")


if __name__ == "__main__":
    server = Server()
    server.start()
