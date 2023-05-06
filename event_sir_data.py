import os
import json
import sys
import pandas as pd

def process_event(event):
    pheme_data_path = '.'

    user_states_df = pd.DataFrame(columns=['timestamp', 'user_id', 'state'])

    event_path = os.path.join(pheme_data_path, event)
    for tweet_type in ['rumours', 'non-rumours']:
        tweet_type_path = os.path.join(event_path, tweet_type)
        for tweet_folder in os.listdir(tweet_type_path):
            if tweet_folder.startswith('.'):
                continue
            tweet_folder_path = os.path.join(tweet_type_path, tweet_folder)
            source_tweet_folder = os.path.join(tweet_folder_path, 'source-tweets')
            for source_file in os.listdir(source_tweet_folder):
                if source_file.startswith('.'):
                    continue
                tweet_file_path = os.path.join(source_tweet_folder, source_file)
                if os.path.isfile(tweet_file_path):
                    with open(tweet_file_path, 'r') as tweet_file:
                        tweet_data = json.load(tweet_file)
                        timestamp = pd.to_datetime(tweet_data['created_at'])
                        user_id = tweet_data['user']['id']

                        new_row = pd.DataFrame({'timestamp': [timestamp], 'user_id': [user_id], 'state': [tweet_type[:-1]]})
                        user_states_df = pd.concat([user_states_df, new_row], ignore_index=True)

    user_states_df = user_states_df.sort_values(by='timestamp').reset_index(drop=True)

    sir_data = pd.DataFrame(columns=['timestamp', 'susceptible', 'infected', 'recovered'])

    all_users_count = user_states_df['user_id'].nunique()

    user_states = {}
    for index, row in user_states_df.iterrows():
        user_id = row['user_id']
        state = row['state']

        user_states[user_id] = state

        infected_count = sum(1 for user_state in user_states.values() if user_state == 'rumour')
        recovered_count = sum(1 for user_state in user_states.values() if user_state == 'non-rumour')
        susceptible_count = all_users_count - infected_count - recovered_count

        new_row = pd.DataFrame({
            'timestamp': [row['timestamp']],
            'susceptible': [susceptible_count],
            'infected': [infected_count],
            'recovered': [recovered_count],
        })
        sir_data = pd.concat([sir_data, new_row], ignore_index=True)
    
    sir_data.to_csv(f'{event}_sir_data.csv', index=False)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python event_sir_data.py <event>')
    else:
        event = sys.argv[1]
        process_event(event)
