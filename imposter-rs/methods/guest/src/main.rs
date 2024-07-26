use risc0_zkvm::guest::env;
use std::collections::HashMap;

fn process_votes(votes: &HashMap<u32, char>) -> u32 {
    let mut votes_count: HashMap<char, u32> = HashMap::new();
    let mut voted_players: u32 = 0; // Bit mask to track players who have voted

    for (player, vote) in votes.iter() {
        // Check if the player has already voted
        if voted_players & (1 << player) != 0 {
            continue; // Skip if the player has already voted
        }

        // Update vote count
        let count = votes_count.entry(*vote).or_insert(0);
        *count += 1;

        // Mark player as having voted using a bit mask
        voted_players |= 1 << player;
    }

    // Determine the winner
    let mut max_vote = 0;
    let mut max_vote_count = 0;
    for (vote, count) in votes_count.iter() {
        if *count > max_vote_count {
            max_vote = *vote as u32;
            max_vote_count = *count;
        }
    }

    max_vote
}


fn main() {
    // TODO: Implement your guest code here

    // read the input
    let votes: HashMap<u32, char> = env::read();

    // TODO: do something with the input
    let winner = process_votes(&votes);

    // write public output to the journal
    env::commit(&input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_process_votes_single_winner() {
        let mut votes = HashMap::new();
        votes.insert(1, 'A');
        votes.insert(2, 'B');
        votes.insert(3, 'A');
        votes.insert(4, 'A');
        votes.insert(5, 'B');

        let winner = process_votes(&votes);
        assert_eq!(winner, 'A' as u32);
    }

    #[test]
    fn test_process_votes_tie() {
        let mut votes = HashMap::new();
        votes.insert(1, 'A');
        votes.insert(2, 'B');
        votes.insert(3, 'A');
        votes.insert(4, 'B');

        let winner = process_votes(&votes);
        // In case of a tie, the function returns the first max vote encountered
        assert!(winner == 'A' as u32 || winner == 'B' as u32);
    }

    #[test]
    fn test_process_votes_no_votes() {
        let votes: HashMap<u32, char> = HashMap::new();

        let winner = process_votes(&votes);
        assert_eq!(winner, 0); // Assuming 0 is the default value for no votes
    }

    #[test]
    fn test_process_votes_no_double_voting() {
        let mut votes = HashMap::new();
        votes.insert(1, 'A');
        votes.insert(1, 'A'); // Player 1 tries to vote twice
        votes.insert(2, 'B');
        votes.insert(3, 'B');

        let winner = process_votes(&votes);
        assert_eq!(winner, 'B' as u32); // 'A' should still win despite the double vote attempt
    }
}
