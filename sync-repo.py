#!/usr/bin/env python

"""Sync forked repos.

This script ensures that the repo that this was forked from is added as a
git remote called upstream. Once the upstream remote is configured, this script
will then fetch any changes in the upstream remote, merge any changes, commit
the changes, and then finally push the changes to the forked repo.
"""

# Requirements:
# pip install gitpython

import os
try:
    from git import Repo
except ImportError:
    print("gitpython module not found: pip install GitPython")

# Defines the upstream repo this repo was forked from
# Example: UPSTREAM="git@gitlab.com:mrlesmithjr/test-repo.git"
UPSTREAM = "git@gitlab.com:mrlesmithjr/test-repo.git"


def commit_changes(current_branch):
    """Commit and push changes to fork."""
    try:
        print("Committing any new changes.\n")
        repo.git.commit('-m', '"upstream synced"')
        print("Any new changes have been committed.\n")
    except:
        print("No changes have been found to commit.\n")
    print("Pushing any new changes to forked repo.\n")
    repo.git.push()
    print("All new changes have been pushed to forked repo.\n")
    if current_branch.name != "master":
        print("Checking out original branch: %s\n" % current_branch.name)
        repo.git.checkout(current_branch.name)
        print("Rebasing with local master to include any changes.\n")
        repo.git.rebase('master')


def repo_remotes():
    """Check for existing upstream repository remote."""
    _repo_remotes = []
    for remote in repo.remotes:
        _repo_remotes.append(remote.name)
    print("The following repo remotes were found: %s\n" % _repo_remotes)
    if "upstream" not in _repo_remotes:
        print("upstream remote not found. Adding...\n")
        repo.create_remote("upstream", UPSTREAM)
        print("upstream remote added successfully.\n")
    else:
        print("upstream remote already found!\n")


def stash_changes():
    """Stash local changes.

    Stash any local changes to ensure no failures occur when checking out
    master.
    """
    print("Stashing any uncommitted entries.\n")
    repo.git.stash()


def stash_pop_changes():
    """Pop all stashed changes to ensure any existing changes are not lost."""
    try:
        print("Popping any stashed entries.\n")
        repo.git.stash('pop')
    except:
        print("No stash entries found.\n")


def sync_upstream(current_branch):
    """Sync upstream parent repo.

    Sync upstream repo, merge changes, commit changes, and push changes to
    fork.
    """
    repo.git.fetch('upstream')
    if current_branch.name != "master":
        print("Checking out master branch.\n")
        repo.git.checkout('master')
        print("master branch checked out.\n")
    print("Merging any changes from upstream/master.\n")
    repo.git.merge('upstream/master')
    print("Any changes from upstream/master merged.\n")


def update_submodules():
    """Update any git submodules used."""
    print("Updating submodules...\n")
    repo.git.submodule('update', '--init', '--recursive', '--remote')
    print("Submodules updated...\n")


if __name__ == "__main__":
    repo_path = os.getcwd()
    repo = Repo(repo_path)
    current_branch = repo.active_branch
    repo_remotes()
    stash_changes()
    sync_upstream(current_branch)
    update_submodules()
    commit_changes(current_branch)
    stash_pop_changes()
