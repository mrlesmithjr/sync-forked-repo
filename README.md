# sync-forked-repo

This repo is for syncing forked repos with their respective upstream repo. The
script will also sync up any git submodules that may be in use.

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
./sync-repo.sh
```

## License

MIT

## Author Information

Larry Smith Jr.

-   [EverythingShouldBeVirtual](http://everythingshouldbevirtual.com)
-   [@mrlesmithjr](https://www.twitter.com/mrlesmithjr)
-   <mailto:mrlesmithjr@gmail.com>
