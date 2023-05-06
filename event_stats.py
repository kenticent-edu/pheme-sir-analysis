import os
from collections import defaultdict
from tabulate import tabulate

pheme_data_path = '.'

event_counts = defaultdict(lambda: {'rumour': 0, 'non-rumour': 0})

for event in os.listdir(pheme_data_path):
    if event.startswith('.'):
        continue
    event_path = os.path.join(pheme_data_path, event)
    if os.path.isdir(event_path):
        for tweet_type in ['rumours', 'non-rumours']:
            tweet_type_path = os.path.join(event_path, tweet_type)
            if os.path.isdir(tweet_type_path):
                count = len([f for f in os.listdir(tweet_type_path) if not f.startswith('.') and os.path.isdir(os.path.join(tweet_type_path, f))])
                event_counts[event][tweet_type[:-1]] = count

table_data = [[event, counts['rumour'], counts['non-rumour']] for event, counts in event_counts.items()]

sorted_table_data = sorted(table_data, key=lambda x: x[1] + x[2], reverse=True)

headers = ['Event', 'Rumour Count', 'Non-rumour Count']
print(tabulate(sorted_table_data, headers=headers, tablefmt='pretty'))
