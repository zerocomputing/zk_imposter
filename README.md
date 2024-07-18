# Imposter

Multiplayer game where players are assigned roles of either 'detective' or 'imposter'. Detectives know a secret word, imposters don't. 

## Gameplay
- Taking Turns: When prompted, enter a word describing the secret word if you are a detective.
- Voting: Enter the player number you suspect is the imposter when prompted.
- Game Results: The server will announce the game results, including the identification of the imposter.

 The server manages connections, assigns roles, and shares a secret word with detectives.

 The client application connects to the server where players interact with each other.

## Requirements

- Python 3.11

## Installation

1. Clone the repo:

```bash
git clone https://github.com/zerocomputing/imposter_game
```

2. Install Pipenv if you haven't installed it yet:
```bash
pip install pipenv
```

3. Install the dependencies via Pipenv:
```bash
pipenv install
```

4. Activate the environment
```bash
pipenv shell
```

## Running the Server
With the Pipenv shell activated, start the server by running:
```bash
python server.py
```

This command starts the server on localhost at port 5555, listening for client connections.

## Running the Client
You'll need to open a new terminal window or tab for each client you want to connect to the server. For each client, navigate to your project directory and activate the Pipenv shell as before:
```bash
pipenv shell
```

With the Pipenv shell activated, start the client by running:
```bash
python client.py
```
