import csv
import random #Only needed for the wireframing stage


class BasketballBracketPredictor:
    def __init__(self, season):
        self.brackets = {'M': [], 'W': []}
        self.max_brackets = 100000
        self.slot_definitions = {'M': {}, 'W': {}}
        self.team_seeds = {'M': {}, 'W': {}}
        self.load_slot_definitions()
        self.season = season
        
    def load_slot_definitions(self):
        # Assuming you have CSV files named 'MNCAATourneySlots.csv' and 'WNCAATourneySlots.csv'
        # Adjust file paths as necessary
        for tournament in ['M', 'W']:
            filename = f'data/{tournament}NCAATourneySlots.csv'
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    season = row['Season']
                    if season not in self.slot_definitions[tournament]:
                        self.slot_definitions[tournament][season] = []
                    self.slot_definitions[tournament][season].append({
                        'Slot': row['Slot'],
                        'StrongSeed': row['StrongSeed'],
                        'WeakSeed': row['WeakSeed']
                    })

    #Only needed for the wire frame stage
    def randomly_select_winner(self, teams):
        # Randomly selects a winner from a list of team identifiers
        return random.choice(teams)

    def simulate_play_in_games(self, tournament):
        # Placeholder: Logic to simulate play-in games and return winners
        play_in_winners = {}

        for slot_info in self.slot_definitions[tournament][self.season]:
            # if isinstance(slot_info, str):
            #     print(f'skipping slot becuase it is str: {slot_info}')
            #     continue
            # print(f'slot_info: {slot_info}')
            if 'a' in slot_info['StrongSeed'] or 'b' in slot_info['StrongSeed']:  # Check if it's a play-in game
                winner = self.simulate_game(slot_info['StrongSeed'], slot_info['WeakSeed'])
                # Assume simulate_game returns the winner correctly handling 'a'/'b' suffixes
                main_slot = slot_info['Slot'][:-1]  # Remove 'a'/'b' suffix to get the main bracket slot
                play_in_winners[main_slot] = winner
        return play_in_winners
    
    def simulate_game(self, team1, team2):
        # Placeholder for a more sophisticated game outcome simulation
        return self.randomly_select_winner([team1, team2])
        
    def generate_bracket_predictions(self, tournament):
        play_in_winners = self.simulate_play_in_games(tournament)
    
        if self.season not in self.slot_definitions[tournament]:
            raise ValueError(f"No slot definitions found for the {self.season} season.")
        
        bracket = {}
        for slot_info in self.slot_definitions[tournament][self.season]:
            slot = slot_info['Slot']
            strong_seed = slot_info['StrongSeed']
            weak_seed = slot_info['WeakSeed']
    
            # Retrieve teams for current match-up, using either direct seeds or winners from previous slots
            strong_team = bracket.get(strong_seed, play_in_winners.get(strong_seed, strong_seed))
            weak_team = bracket.get(weak_seed, play_in_winners.get(weak_seed, weak_seed))
    
            # Simulate the game and record the winner
            winner = self.simulate_game(strong_team, weak_team)
            bracket[slot] = winner
    
        self.brackets[tournament].append(bracket)
    
    def export_predictions_to_csv(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['RowId', 'Tournament', 'Bracket', 'Slot', 'Team'])
            
            row_id = 1
            for tournament, brackets in self.brackets.items():
                for bracket_index, bracket in enumerate(brackets, start=1):
                    for slot, team in bracket.items():
                        writer.writerow([row_id, tournament, bracket_index, slot, team])
                        row_id += 1

# Example usage
predictor = BasketballBracketPredictor(season='2022')
# season = '2022'  # Specify the season for which you are making predictions
predictor.generate_bracket_predictions('M')  # Generate predictions for Men's tournament
predictor.generate_bracket_predictions('W')  # Generate predictions for Women's tournament
predictor.export_predictions_to_csv('submission.csv')