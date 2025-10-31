# Dotify

Менеджер конфигов и окружения.

Разделяем две области:
1. Конфиги
2. Приложения

С помощью YAML конфигов можем создавать свой дот, после чего проинициализировать с помощью dotify.


# Documentation
Make sure that you have installed `mdbook`:
```sh
cargo install mdbook
```

To open documentation:
```sh
mdbook serve
```

# Commands

- [ ] `init`:
  - Initialize dot environment
  - Usage: `dotify init`

- [ ] `apply`
  - Apply dot environment
  - Usage: `dotify apply`


# Plugins
- git
- cargo
- yay
- shell

# Dotify Config
plugins = {
  "git",
  "yay",
}


project --> manifest_1
        |-> ...
        |-> manifest_n
        |-> subproject_1
        |-> ...
        |-> subproject_m

manifest - folder with main.yaml
project  - folder with dotify.toml


1 plugin for 1 yaml
