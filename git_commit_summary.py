from git import Repo
from datetime import datetime

'''
The function will clone local Git repository, iterate over all the commits, 
and create a dictionary that stores the commit messages for each date.
'''
def get_my_commit_summary(username, password):
    # Replace this with the path to your local Git repository
    repo_path = "/path/to/local/repository"

    # Clone or open the local Git repository
    repo = Repo.clone_from(repo_path, ".", auth=(username, password))

    # Create an empty dictionary to store the commit summary
    commit_summary = {}

    # Iterate over all the commits in the repository
    for commit in repo.iter_commits():
        # Get the commit date and format it as YYYY-MM-DD
        commit_date = datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d')

        # Add the commit date to the dictionary if it doesn't exist already
        if commit_date not in commit_summary:
            commit_summary[commit_date] = []

        # Add the commit message to the list for the corresponding date
        commit_summary[commit_date].append(commit.message.strip())

    # Print the commit summary
    for date, messages in commit_summary.items():
        print(f"{date}:")
        for message in messages:
            print(f" - {message}")

