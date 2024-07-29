use risc0_zkvm::guest::env;
use std::collections::HashMap;

fn process_votes(votes: &HashMap<u32, u32>) -> u32 {
    let mut votes_count: HashMap<u32, u32> = HashMap::new();
    let mut voted_players: u32 = 0; // Bit mask to track players who have voted

    for (player, vote) in votes.iter() {
        // Check if the player has already voted
        if voted_players & (1 << player) != 0 {
            continue; 
        }

        // Update vote count
        let count = votes_count.entry(*vote).or_insert(0);
        *count += 1;

        // Mark player as having voted using a bit mask
        voted_players |= 1 << player;
    }

    // Determine the voted imposter
    println!("votes_count: {:?} ", votes_count);
    let mut max_vote: Option<char> = None;
    let mut max_vote_count = 0;
    for (vote, count) in votes_count.iter() {
        if *count > max_vote_count {
            max_vote = Some(std::char::from_u32(*vote).unwrap_or('0'));
            max_vote_count = *count;
        }
    }

    max_vote.unwrap_or('0') as u32
}

fn check_imposter(roles: HashMap<u32, String>, winner: u32) -> bool {
    if let Some(role) = roles.get(&winner) {
        println!("The voted imposter's role is: {}", role);
        true
    } else {
        println!("No role found for the winner");
        false
    }
}

fn main() {
    // read the input
    let (roles, votes): (HashMap<u32, String>, HashMap<u32, u32>) = env::read();

    // Process the votes and print the voted imposter
    let winner = process_votes(&votes);
    println!("Player {} was voted as the imposter", winner);

    println!("Roles {:?}", roles);
    check_imposter(roles, winner);

    // write public output to the journal
    env::commit(&winner);
}
