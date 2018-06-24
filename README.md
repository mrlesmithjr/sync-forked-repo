# sync-forked-repo

This repo is for syncing forked repos with their respective upstream repo. The
script will also sync up any git submodules that may be in use.

## Why

The intent of this is to easily clone down a forked repo and continually keep it
in sync with it's upstream parent in which it was forked from. This can make things
specifically easy for consumers which may have limited knowledge of using git as
well.

## Requirements

Define `upstream=""` in script to reflect your respective upstream repo for your
fork.

```bash
# Defines the upstream repo this repo was forked from
# Example: upstream="git@gitlab.com:mrlesmithjr/test-repo.git"
upstream=""
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

- [EverythingShouldBeVirtual](http://everythingshouldbevirtual.com)
- [@mrlesmithjr](https://www.twitter.com/mrlesmithjr)
- <mailto:mrlesmithjr@gmail.com>
