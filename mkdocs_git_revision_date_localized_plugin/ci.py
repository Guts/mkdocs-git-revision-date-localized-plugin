import os
import logging


def raise_ci_warnings(repo):
    """
    raise warnings when users use mkdocs-git-revision-date-localized-plugin
    on CI build runners

    Args:
        repo (GitPython.git.repo): The Git repo object
    """

    if not is_shallow_clone(repo):
        return None

    n_commits = commit_count(repo)

    # Gitlab Runners
    if os.environ.get("GITLAB_CI") and n_commits < 50:
        # Default is GIT_DEPTH of 50 for gitlab
        logging.warning(
            """
                [git-revision-date-localized-plugin] Running on a gitlab runner might lead to wrong git revision dates
                due to a shallow git fetch depth.
                Make sure to set GIT_DEPTH to 1000 in your .gitlab-ci.yml file.
                (see https://docs.gitlab.com/ee/user/project/pipelines/settings.html#git-shallow-clone).
                """
        )

    # Github Actions
    if os.environ.get("GITHUB_ACTIONS") and n_commits == 1:
        # Default is fetch-depth of 1 for github actions
        logging.warning(
            """
                [git-revision-date-localized-plugin] Running on github actions might lead to wrong git revision dates
                due to a shallow git fetch depth.
                Try setting fetch-depth to 0 in your github action
                (see https://github.com/actions/checkout).
                """
        )

    # Bitbucket pipelines
    if os.environ.get("CI") and n_commits < 50:
        # Default is fetch-depth of 50 for bitbucket pipelines
        logging.warning(
            """
                [git-revision-date-localized-plugin] Running on bitbucket pipelines might lead to wrong git revision dates
                due to a shallow git fetch depth.
                Try setting "clone: depth" to "full" in your pipeline
                (see https://support.atlassian.com/bitbucket-cloud/docs/configure-bitbucket-pipelinesyml/
                and search 'depth').
                """
        )

    # Azure Devops Pipeline
    # Does not limit fetch-depth by default
    if os.environ.get("Agent.Source.Git.ShallowFetchDepth", 10e99) < n_commits:
        logging.warning(
            """
                [git-revision-date-localized-plugin] Running on Azure pipelines with limited fetch-depth might lead to wrong git revision dates
                due to a shallow git fetch depth.
                Remove any Shallow Fetch settings
                (see https://docs.microsoft.com/en-us/azure/devops/pipelines/repos/pipeline-options-for-git?view=azure-devops#shallow-fetch).
                """
        )


def commit_count(repo) -> bool:
    """
    Helper function to determine the number of commits in a repository

    Args:
        repo (GitPython.Repo.git): Repository

    Returns:
        count (int): Number of commits
    """
    refs = repo.for_each_ref().split("\n")
    refs = [x.split()[0] for x in refs]

    counts = [int(repo.rev_list(x, count=True, first_parent=True)) for x in refs]
    return max(counts)


def is_shallow_clone(repo) -> bool:
    """
    Helper function to determine if repository
    is a shallow clone.

    References & Context:
    https://github.com/timvink/mkdocs-git-revision-date-localized-plugin/issues/10
    https://stackoverflow.com/a/37203240/5525118

    Args:
        repo (GitPython.Repo.git): Repository

    Returns:
        bool: If a repo is shallow clone
    """
    return os.path.exists(".git/shallow")
