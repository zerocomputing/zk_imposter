# Types of ZK Circuits
1. Play - Commit a synonym to a secret word ('none' if imposter)
2. Vote - Commit a vote to a secret word ('none' if imposter)

# Structs (use for re-writing Python game logic in Rust)
- Player (player_id, role, secret_word) # secret_word is none if imposter
- Guess (player_id, guess, secret_word) # secret_word is none if imposter
- Vote (player_id, vote)

# Proof Request: Submit Ballot
- In: Voters and corresponding votes (e.g., {1: '3', 2: '3', 3: '1'})
- Circuit:
    - Loop through each vote 
    - Update vote count with each new vote
    - Mark player as having voted (use bit mask?)
- Out: Voting log

# Proof Request: Tally
- In: voting log
- Circuit:
    - Count votes
    - Determine winner
- Out: Winner and voting log
