# Logic #

Implements parsers to handle various computational problems in mathematical logic.

## Usage ##

Run `chmod +x scripts/*.sh` once.

To force things to run in Docker, set the contents of `.whales/DOCKER_DEPTH` to `0`,
or call
```bash
echo "0" >| .whales/DOCKER_DEPTH;
```
To force things to not run in Docker, set the contents of `.whales/DOCKER_DEPTH` to `1`.

### build.sh ###

Run
```bash
./scripts/build.sh;
```
and see instructions about flags.

### test.sh ###

Run
```bash
./scripts/test.sh;
```
and see instructions about flags.

### clean.sh ###

Run
```bash
./scripts/clean.sh;
```
and see instructions about flags.
