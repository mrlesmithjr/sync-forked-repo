# sync-forked-repo

This repo is for syncing forked repos with their respective upstream repo. The
script will also sync up any git submodules that may be in use.

## Why

The intent of this is to easily clone down a forked repo and continually keep it
in sync with it's upstream parent in which it was forked from. This can make things
specifically easy for consumers which may have limited knowledge of using git as
well.

## Requirements

### Configure `sync.cfg` In Script

If your intention is to use a `sync.cfg` from a different location than the default,
you must set the path appropriately.

```python
sync_config = "sync.cfg"
```

> NOTE: This could be useful in scenarios where you might be leveraging this
> repo as a submodule to use across projects and each project should be configured
> differently. You can easily include a `sync.cfg` in a parent directory and
> change the path in the script.

### Configure [sync.cfg](sync.cfg)

Define `LOG_FILE`  to reflect the location of the log file to use for
logging. The default is set to `sync-repo.log`.

Define `UPSTREAM` to reflect your respective upstream repo for your
fork.

Define `UPSTREAM_BRANCH` to reflect your respective upstream repo's
branch to sync with.

```bash
[defaults]
# Define the log file location
LOG_FILE = sync-repo.log

# Example: UPSTREAM = git@gitlab.com:mrlesmithjr/test-repo.git
UPSTREAM =

# Defines the upstream branch to sync with. Important for those that are not
# by default master.
UPSTREAM_BRANCH = master
```

## Usage

```bash
python sync-repo.py
```

### Submodule Info

When the script executes it will check to see if any submodules are in use. If
submodules are in use, the script will then look for any changed files within each
submodule path, if any changed files are found they are stashed before updating
the submodule. If any files have been stashed, they will be popped back after the
submodule updates. The way the submodules are updated, they will only update if the
parent upstream submodule has been updated. This will ensure that the forked repo
remains in sync with the parent.

## License

MIT

## Author Information

Larry Smith Jr.

-   [EverythingShouldBeVirtual](http://everythingshouldbevirtual.com)
-   [@mrlesmithjr](https://www.twitter.com/mrlesmithjr)
-   <mailto:mrlesmithjr@gmail.com>
