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
  From here, you can run the app with `python .` and the tests with `pytest`.

## Debug
* Documentation [here](https://docs.python.org/3/library/pdb.html).
* Set a breakpoint with `import pdb; pdb.set_trace()`.
  * If you're using vim with [a project-specific .vimrc](https://andrew.stwrt.ca/posts/project-specific-vimrc/), you can type this with `<leader>db`.
* Show where you are with `list`.
* Continue with `continue`.
* Quit with `quit`.

## Add a new python package
* Add the package name to `requirements.in`. Then, while in the container, but not while running the application, run:
  ```console
  pip-compile --output-file=- > requirements.txt
  ```
  This will write to `requirements.txt`. For more details, see [this stackoverflow](https://stackoverflow.com/a/65666949/2197402).
* This new package will be gone once you exit the container. But since it's still listed in requirements.txt, you can bake it into all future containers by rebuilding the image:
  ```sh
  docker-compose build
  ```
