# Python Starter Kit

A starter kit for writing code and [tests](https://docs.python.org/3/library/unittest.html) in python.

#### Dependencies
* docker
* docker-compose

## Install
* build the image
  ```sh
  docker-compose build
  ```

## Run
* run the tests
  ```sh
  docker-compose run --rm app
  ```
* run something else, like `bash` or `python3`
  ```sh
  docker-compose run --rm app python3
  ```

## Copy
* this command will clone even hidden files and directories
  ```sh
  mkdir -p path/to/new
  cp -rT path/to/this/directory path/to/new/directory
  ```
  * it's OK if `path/to/new/directory` already exists
  * it's not OK if `path/to/new` doesn't exist, hence the `mkdir -p`

## Debug
* documentation [here](https://docs.python.org/3/library/pdb.html)
* set a breakpoint with `import pdb; pdb.set_trace()`
  * if you're using vim with [a project-specific .vimrc](https://andrew.stwrt.ca/posts/project-specific-vimrc/), you can type this with `<leader>db`
* show where you are with `list`
* continue with `continue`
* quit with `quit`

## Add a new python package
* Inside the container, use the bash function `pip-install-save` to simultaneously install the python package and update `requirements.txt`. For example, say you wanted to install `pytest-timeout`:
  ```sh
  pip-install-save pytest-timeout
  ```
* This new package will be gone once you exit the container. But since it's still listed in requirements.txt, you can bake it into all future containers by rebuilding the image
  ```sh
  docker-compose build
  ```
