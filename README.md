# Python Starter Kit
This app is a starter kit for writing code and [tests](https://docs.python.org/3/library/unittest.html) in python. Use it as a seed for starting a new python project. Use the following command to copy this app's code to a new directory:
```console
mkdir -p path/to/new
cp -r path/to/this/directory path/to/new/directory
```

## Dependencies
The only local dependency you need to configure to use this codebase is `docker-compose`. This is great, because once you have docker working, it eliminates the "well it works on my machine" kind of problems. If it works on docker for you, it will work in docker for anyone.

## Install
* Build the image:
  ```console
  docker-compose build
  ```

## Run
* Run the app one time and exit:
  ```console
  docker-compose run --rm app
  ```
* Open a long-running session inside the container:
  ```console
  docker-compose run --rm app bash
  ```
  From here, you can ...
  * Run the tests.
    ```console
    pytest
    ```
  * Run the app.
    ```console
    python .
    ```
  * Run the linter.
    ```console
    flake8
    ```
    * For more usage instructions, see [the flake8 documentation](https://flake8.pycqa.org/en/latest/index.html).
  * Run the auto formatter.
    ```console
    pre-commit run --all-files
    ```
    * For more usage instructions, see [the pre-commit documentation](https://pre-commit.com/).

## Debug
* Documentation [here](https://docs.python.org/3/library/pdb.html).
* Set a breakpoint with `import pdb; pdb.set_trace()`.
  * If you're using vim with [a project-specific .vimrc](https://andrew.stwrt.ca/posts/project-specific-vimrc/), you can type this with `<leader>db`.
* Show where you are with `list`.
* Continue with `continue`.
* Quit with `quit`.

## Add a new python package
This app makes use of [`pip-tools`](https://github.com/jazzband/pip-tools) to manage packages. Add the new package to `requirements.in`, unless it's only used for local development, in which it should go to `dev-requirements.in`. After this, use `pip-compile` on whichever `.in` file you modified to generate its respective `.txt` file. These `.txt` files are what the Dockerfile uses to install packages when building the image.

### Example: installing a package for local development
* Add the package name to `dev-requirements.in`.
* Compile `dev-requirements.in`.
  ```console
  docker-compose run --rm app pip-compile dev-requirements.in
  ```
* Rebuild the image.
  ```console
  docker-compose build
  ```
