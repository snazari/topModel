from google.cloud import bigquery as bq
import pandas


def request(connect, query, timeout, file_name):
    query_job = connect.query(query)
    data_iteration = query_job.result(timeout=timeout)
    data_frame = data_iteration.to_dataframe()
    data_frame.to_csv(file_name, header=False, index=False, index_label=False)


class RepositoryGhtorrentBq(object):

    def __init__(self, login, project, timeout=30):
        self.login = login
        self.project_name = project
        self.client = bq.Client.from_service_account_json('service_account.json')
        self.timeout = timeout
        self.project_id = self._get_id_project()

    def _get_id_project(self):
        query = """
                  SELECT p.id as project_id 
                  FROM `ghtorrent-bq.ght.projects` as p
                  join `ghtorrent-bq.ght.users` as u on p.owner_id = u.id 
                  where u.login='{}' and p.name = '{}'
                """.format(self.login, self.project_name)

        query_job = self.client.query(query)
        data_iteration = query_job.result(timeout=self.timeout)
        data_frame = pandas.DataFrame([row.values() for row in data_iteration], columns=['project_id'])
        return data_frame.iloc[0][0]

    def contributors(self, limit):
        query = """
                  SELECT 
                  u2.login as login_user,
                  COUNT(c.committer_id) as count_commits 
                  FROM `ghtorrent-bq.ght.users` as u 
                  inner join `ghtorrent-bq.ght.projects` as p on p.owner_id = u.id 
                  inner join `ghtorrent-bq.ght.commits` as c on c.project_id = p.id 
                  inner join `ghtorrent-bq.ght.users` as u2 on c.committer_id = u2.id 
                  where p.id={} 
                  GROUP BY login_user 
                  ORDER BY 2 DESC 
                  LIMIT {}
                """.format(self.project_id, limit)
        request(self.client, query, self.timeout, "contributors.csv")

    def get_commit_comments(self):
        query = """
                  SELECT u.login, cc.body 
                  FROM `ghtorrent-bq.ght.project_commits` as pc 
                  right join `ghtorrent-bq.ght.commit_comments` as cc on pc.commit_id = cc.commit_id 
                  left join `ghtorrent-bq.ght.users` as u on cc.user_id = u.id 
                  where pc.project_id = {}
                """.format(self.project_id)
        request(self.client, query, self.timeout, "message.csv")

    def get_pull_request_comments(self):
        query = """
                  SELECT u.login, prc.body 
                  FROM `ghtorrent-bq.ght.pull_requests` as pr 
                  right join `ghtorrent-bq.ght.pull_request_comments` as prc on pr.id = prc.pull_request_id 
                  join `ghtorrent-bq.ght.users` as u on prc.user_id = u.id 
                  where pr.base_repo_id = {}
                """.format(self.project_id)

        request(self.client, query, self.timeout, 'message.csv')


class GhtorrentBq(object):

    def __init__(self, timeout=30):
        try:
            self.client = bq.Client.from_service_account_json('service_account.json')
            self.timeout = timeout

        except Exception as e:
            raise e

    def get_list_repository(self, key_word):
        query = """
                  SELECT 
                    u.login as user_login, 
                    p.name as project_name 
                  FROM `ghtorrent-bq.ght.users` as u 
                  join `ghtorrent-bq.ght.projects` as p on u.id = p.owner_id 
                  where p.name like '%{}%'
                """.format(key_word)

        request(self.client, query, self.timeout, "list_repository.csv")


class RepositoryGitHubRepos(object):

    def __init__(self, repository_name, timeout=30):
        self.repository_name = repository_name
        self.client = bq.Client.from_service_account_json('service_account.json')
        self.timeout = timeout

    def contributors(self, limit):
        query = """
                  SELECT committer.name, COUNT(commit) as count_commit
                  FROM `bigquery-public-data.github_repos.commits`
                  where '{}' in UNNEST(repo_name)
                  GROUP BY committer.name
                  ORDER BY 2 DESC 
                  LIMIT {}
                """.format(self.repository_name, limit)

        request(self.client, query, self.timeout, "contributors.csv")

    def get_message(self):
        query = """
                  SELECT committer.name, message
                  FROM `bigquery-public-data.github_repos.commits`
                  where '{}' in UNNEST(repo_name)
                """.format(self.repository_name)

        request(self.client, query, self.timeout, "message.csv")


class GitHubRepos(object):

    def __init__(self, timeout=30):
        try:
            self.client = bq.Client.from_service_account_json('service_account.json')
            self.timeout = timeout

        except Exception as e:
            raise e

    def get_list_repository(self, key_word):
        query = """
                  SELECT repo_name 
                  FROM `bigquery-public-data.github_repos.languages` 
                  where repo_name like '%{}%'
                """.format(key_word)

        request(self.client, query, self.timeout, "list_repository.csv")
