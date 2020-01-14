from github import Github
from datetime import datetime
import pickle

def main():
    with open('auth_key.txt', 'r') as key_file:
        key = key_file.readline()
    g = Github(key)
    repos = [
        'ethereum/go-ethereum'
    ]

    now = datetime.now()

    repo_stats = {}

    for r in repos:
        print(f'Working on repo {r}')
        # Create a list to store the stats for each day in the last 365 days
        weeks = {}

        # and store all unique contributors
        contributors = set()

        repo = g.get_repo(r)
        commits = repo.get_commits(since=datetime(2020, 1, 7))
        i = 0
        for commit in commits:
            i+=1
            if i%10 == 0:
                print(f'\tcommit #{i}')
            # Get the date the commit happened on
            mod_date = datetime.strptime(commit.last_modified, '%a, %d %b %Y %H:%M:%S %Z')

            # Get the difference in weeks
            week_diff = (now - mod_date).days // 7

            # Check if any data has been saved for this week
            if week_diff not in weeks:
                weeks[week_diff] = {
                    'additions': 0,
                    'deletions': 0,
                    'changes': 0,
                }

            contributors.add(commit.committer.login)
            contributors.add(commit.author.login)

            for file in commit.files:
                weeks[week_diff]['additions'] += file.additions
                weeks[week_diff]['changes'] += file.changes
                weeks[week_diff]['deletions'] += file.deletions

            repo_stats[r] = {
                'contributors': contributors,
                'weeks': weeks
            }


    file = 'stats.pkl'
    file_handle = open(file, 'wb')
    pickle.dump(repo_stats, file_handle)
    file_handle.close()

if __name__ == '__main__':
    main()


