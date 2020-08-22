
The document hosted in this repository is available in text, html and pdf 
formats at <http://www.eul.ink/complex-analysis>.

To generate the latest version of these documents:

 1. You need a computer with an unrestricted access to the Internet 
    and [Docker][] installed; 
    instructions exist for [Linux][], [Windows][] and [Mac OS X].
    (For Linux, make sure that [you can run docker as a user][Linux-permissions].)

 2. Go to the [Downloads][] section, click on "Download repository", 
    save the zip file and extract the directory that it contains.

 3. Launch a terminal (for Windows and Mac OS X a "Docker Quickstart Terminal")
    in the project directory and execute the command

        ./docker/build

    to create the documents. 
    If you end up with permission errors, try to make the build as an admin

        ./docker/build --force

    and fix the permissions of the generated files afterward if you need to.

The third step may take a while because you download 
[a large docker image](https://hub.docker.com/r/boisgera/doc/).
Subsequent builds will be much faster.

For power users:

  - You can use [git][] to fetch the project files.

    On Windows and Mac OS X, make sure that your git installation 
    is configured to preserve Linux line endings.

  - You can avoid docker and go native (at least for Linux).

    The approach above encapsulates all the project software dependencies in
    a docker image and should be the most convenient, but is not mandatory.
    There is a top-level `build` script that you can use instead of `docker/build`.
    You can also have a look at the [Dockerfile of the boisgera/doc image][]
    to have a list of the software that you need to install manually.


[Downloads]: https://bitbucket.org/complexanalysiscsd/complex-step-differentiation/downloads
[Docker]: https://www.docker.com/
[Linux]: https://docs.docker.com/linux/
[Mac OS X]: https://docs.docker.com/windows
[Windows]: https://docs.docker.com/mac
[Linux-permissions]: https://docs.docker.com/engine/installation/linux/ubuntulinux/#create-a-docker-group
[Dockerfile of the boisgera/doc image]: https://hub.docker.com/r/boisgera/doc/~/dockerfile/
[git]: https://git-scm.com/
