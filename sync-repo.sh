#!/usr/bin/env bash

# This script ensures that the repo that this was forked from is added as a
# git remote called upstream. Once the upstream remote is configured, this script
# will then fetch any changes in the upstream remote, merge any changes, commit the
# changes, and then finally push the changes to the forked repo.

# Defines the upstream repo this repo was forked from
# Example: upstream="git@gitlab.com:mrlesmithjr/test-repo.git"
upstream=""

# Commit and push changes to fork
function commit_changes() {
  git commit -m "upstream synced"
  git push
  if [ $current_branch != "master" ]
  then
    git checkout $current_branch
  fi
}

# Sync upstream repo, merge changes, commit changes, and push changes to fork
function sync_upstream() {
  current_branch=$(git rev-parse --abbrev-ref HEAD)
  git fetch upstream
  if [ $current_branch != "master" ]
  then
    git checkout master
  fi
  git merge upstream/master
}

# Update any git submodules used
function update_submodules() {
  git submodule update --init --recursive --remote
}

# Check for existing upstream repository remote
remote_repositories=$(git remote -v)
echo $remote_repositories
if [[ $remote_repositories =~ "upstream" ]]
then
  sync_upstream
  update_submodules
  commit_changes
else
  git remote add upstream $upstream
  sync_upstream
  update_submodules
  commit_changes
fi
