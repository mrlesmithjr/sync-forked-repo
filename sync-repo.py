#!/usr/bin/env python

"""Sync forked repos.

This script ensures that the repo that this was forked from is added as a
git remote called upstream. Once the upstream remote is configured, this script
will then fetch any changes in the upstream remote, merge any changes, commit
the changes, and then finally push the changes to the forked repo.
"""

# Requirements:
# pip install gitpython

import datetime
import os
import sys

# Defines the upstream repo this repo was forked from
# Example: UPSTREAM="git@gitlab.com:mrlesmithjr/test-repo.git"
UPSTREAM = ""


def main():
    """Main function of execution."""
    try:
        from git import Repo
    except ImportError as error:
        # Output expected ImportErrors.
        print(error.__class__.__name__ + ": " + error.message)
        print("Please install GitPython module...")
        sys.exit(0)
    except Exception as exception:
        # Output unexpected Exceptions.
        print(exception, False)
        print(error.__class__.__name__ + ": " + exception.message)
        sys.exit(0)

    # Capturing current working directory
    repo_path = os.getcwd()

    # Defining repo based on current working directory
    repo = Repo(repo_path, search_parent_directories=True)

    # Check to make sure that we are not working in a bare repo
    assert not repo.bare

    # Capturing current active branch
    current_branch = repo.active_branch

    # Setting up repository remotes
    repo_remotes(repo)

    # Check for any upstream changes
    upstream_changes = check_upstream_changes(repo)

    if upstream_changes:

        # Check for any changes and stash them before proceeding
        stashed_changes = stash_changes(repo)

        # Syncing upstream with local repository
        sync_upstream(repo, current_branch)

        # Updating and syncing any submodules being used
        update_submodules(repo, repo_path, Repo)

        # Committing and pushing any changes from upstream to forked repo.
        commit_changes(repo, current_branch)

        # Popping any stashed changes
        stash_pop_changes(repo, stashed_changes)

    else:
        print("No upstream changes found.\n")


def check_upstream_changes(repo):
    """Check for any upstream changes."""
    fetch_upstream = repo.remotes.upstream.fetch()[0]
    if fetch_upstream.flags == 4:
        upstream_changes = False
    else:
        upstream_changes = True
    return upstream_changes


def commit_changes(repo, current_branch):
    """Commit and push changes to fork."""
    try:
        print("Committing any new changes...")
        repo.git.commit('-m', '"upstream synced"')
        print("Any new changes have been committed.\n")
    except:
        print("No changes have been found to commit.\n")
    print("Pushing any new changes to forked repo...")
    repo.git.push()
    print("All new changes have been pushed to forked repo.\n")
    tagging(repo)
    print("Pushing any tags.\n")
    repo.git.push('--tags')
    if current_branch.name != "master":
        print("Checking out original branch: " + current_branch.name)
        repo.git.checkout(current_branch.name)
        print("Rebasing with local master to include any changes.\n")
        repo.git.rebase('master')


def get_status(repo):
    """Get status of local repo and check for changes."""
    # Capturing any untracked files in local repository. Future use cases..
    untracked_files = repo.untracked_files
    if untracked_files != []:
        print("The following untracked files were found and "
              "should be committed: ")
        for item in untracked_files:
            print(item)
    changes = []
    for item in repo.index.diff(None):
        changes.append(item.a_path)
    return changes


def repo_remotes(repo):
    """Check for existing upstream repository remote."""
    remotes = []
    for remote in repo.remotes:
        remotes.append(remote.name)
    if "upstream" not in remotes:
        print("upstream remote not found. Adding...")
        repo.create_remote("upstream", UPSTREAM)
        print("upstream remote added successfully.\n")
    else:
        if repo.remotes.upstream.url != UPSTREAM:
            print("upstream remote found but not correct. Changing...")
            repo.delete_remote("upstream")
            repo.create_remote("upstream", UPSTREAM)
            print("upstream remote successfully changed.\n")


def stash_changes(repo):
    """Stash local changes.

    Stash any local changes to ensure no failures occur when checking out
    master.
    """
    print("Checking status of repo changes..\n")
    changes = get_status(repo)
    if changes != []:
        print("\nStashing the following uncommitted entries:")
        for item in changes:
            print(item)
        repo.git.stash()
        stashed_changes = True
    else:
        print("No uncommitted entries found.")
        stashed_changes = False
    print("\n")
    return stashed_changes


def stash_pop_changes(repo, stashed_changes):
    """Pop all stashed changes to ensure any existing changes are not lost."""
    if stashed_changes is True:
        print("Popping any stashed entries.\n")
        repo.git.stash('pop')


def sync_upstream(repo, current_branch):
    """Sync upstream parent repo.

    Sync upstream repo, merge changes, commit changes, and push changes to
    fork.
    """
    if current_branch.name != "master":
        print("Checking out master branch...")
        repo.git.checkout('master')
        print("master branch checked out.\n")
    print("Merging any changes from upstream/master...")
    repo.git.merge('upstream/master')
    print("Any changes from upstream/master merged.\n")


def tagging(repo):
    """Create automatic tagging based on timestamp when commits are made."""
    tags = repo.tags
    if tags != []:
        print("The following tags were found: ")
        for tag in tags:
            print(tag)
        print("\n")
    tag = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    print("Creating new tag: " + tag)
    repo.create_tag(tag, message='Automatic tag created on: %s' % tag)
    print("\n")


def update_submodules(repo, repo_path, Repo):
    """Update any git submodules used."""
    print("Gathering all submodules...")
    # Collect any submodules in use
    sms = repo.submodules
    # Ensure that there are actually submodules in use
    if len(sms) > 0:
        # Iterate over each submodule found
        for sm in sms:
            # Define submodule actual path
            sm_path = repo_path + "/" + sm.path
            # Define submodule repo
            sm_repo = Repo(sm_path)
            # Check for any changed files
            sm_changed_files = sm_repo.index.diff(None)
            if sm_changed_files != []:
                print("Stashing changed files found in submodule: %s" % sm.name)
                # Stash any changed files found in submodule
                sm_repo.git.stash()
                sm_stashed_files = True
            else:
                sm_stashed_files = False
            # Collect any untracked files in submodule
            sm_untracked_files = sm_repo.untracked_files
            if sm_untracked_files != []:
                print("The following untracked files found in submodule: %s"
                % sm_untracked_files)
            # Update the submodule
            sm_repo.submodule_update()
            if sm_stashed_files:
                print("Popping stashed files found in submodule: %s" % sm.name)
                # Pop any stashed files found in submodule
                sm_repo.git.stash('pop')
    else:
        print("No submodules found.\n")


if __name__ == "__main__":
    main()
