from big_query import GhtorrentBq, RepositoryGhtorrentBq, GitHubRepos, RepositoryGitHubRepos

# # get data from repository ghtorrent_bq, to retrieve data, uncomment the lines "4-6"
#client = GhtorrentBq()
# # it is necessary to enter a keyword to search for the required repository, after which the found repositories
#client.get_list_repository('linux')

# Uncomment lines "9-14" and enter the name of the repository
#repository = RepositoryGhtorrentBq("torvalds", "linux")
#repository.contributors(100)
# # given from table "commit_comments"
#repository.get_commit_comments()
# # given from table "pull_request_comments"
#repository.get_pull_request_comments()


# get data from repository public_github, to retrieve data, uncomment the lines "18-20"
client = GitHubRepos()
# it is necessary to enter a keyword to search for the required repository, after which the found repositories
client.get_list_repository('linux')

# Uncomment lines "23-25" and enter the name of the repository
repository = RepositoryGitHubRepos('torvalds/linux')
repository.contributors(100)
repository.get_message()
