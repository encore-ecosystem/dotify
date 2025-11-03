# Dotify

Dotfile configuration manager inspired by [comtrya](https://github.com/comtrya/comtrya)

## Usage
```
usage: dotify [-h] {init,apply} ...

Dotify - dotfile configuration manager

positional arguments:
  {init,apply}
    init        Initialize a new project
    apply       Apply configuration

options:
  -h, --help    show this help message and exit
```

## Documentation (TODO)
Make sure that you have installed `mdbook`:
```sh
cargo install mdbook
```

To open documentation:
```sh
mdbook serve
```

## Installation

### step 0
Make sure that you have installed `uv`:
```
sudo pacman -S uv
```

### step 1
Install `dotify`
```
uv sync
source .venv/bin/activate
```

## Roadmap
- [ ] Documentation
- [ ] Improve yaml path resolver
- [ ] Logging with colors
- [ ] Improve error handling
