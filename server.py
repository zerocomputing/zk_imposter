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
        roles = {client: 'detective' for client in role_list[:2]}
        roles[role_list[2]] = 'imposter'
        self.player_roles = roles
        print('Roles: ', roles)

    def send_start_info(self):
        for client in self.clients:
            role = self.player_roles[client]
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
            print(votes)
        alleged_imposter = max(votes, key=votes.get)
        print('Alleged imposter: ', alleged_imposter) 
        print('Alleged imposter role: ', list(self.player_roles.items())[int(alleged_imposter)-1])
        print('(type)', type(list(self.player_roles.items())[int(alleged_imposter)-1]))
        if list(self.player_roles.items())[int(alleged_imposter)-1] == 'imposter':
            print('Imposter caught!')
            client.send(pickle.dumps({"result": "Detectives win!"}))
        else:
            print('Imposter not caught!')
            client.send(pickle.dumps({"result": "Detectives lose..."})) 

    # def announce_result(self, imposter_client):
    #     for client in self.clients:
    #         result = "imposter" if client == imposter_client else "detective"
    #         client.send(pickle.dumps({"result": result}))

    def start(self):
        print("Server started")
        try:
            while True:
                client, addr = self.server.accept()
                print(f"New connection: {addr}")
                threading.Thread(target=self.handle_client, args=(client, addr)).start()
        except KeyboardInterrupt:
            print("Shutting down the server...")
            # Perform cleanup here, like closing client connections
            for client in self.clients:
                client.close()
            print("Server shut down successfully.")

if __name__ == "__main__":
    server = Server()
    server.start()
