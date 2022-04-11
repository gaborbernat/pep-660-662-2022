# HOW WE STANDARDIZED EDITABLE INSTALLS - PEP-660 VS. PEP-662

A Python Enhancement Proposal (PEP) is the method through which the Python community debates and adopts new features to
the language. The same mechanism is used to standardize interfaces and methods used by the Python Packaging Ecosystem.
The main difference is that while language PEPs are written mostly by core developers, packaging PEPs are written by
members of the Python Packaging Authority (PyPA). How we build Python packages was standardized in 2016 through PEP-517
and PEP-518. Editable installs, while widely used and well known through the -e flag in pip, proved to be controversial,
so it got left out of those proposals. It has taken another five years to reach a consensus, and I'm happy to say that
-- through PEP-660 -- we now have a way for all build back-ends to support editable installs. Join me in this talk,
where I'll tell a tale explaining how having competing PEPs and exhausting discussions -- while tiresome -- led to a
better solution. Plus, you'll also understand the different options we considered and the solution we developed in the
end.

## Outline

1. Define editable installations - 2 minute
1. Priort art - 5 minute
   - Originating from `distutils`. Under normal circumstances, the distutils assume that you are going to build a
     distribution of your project, not use it in its “raw” or “unbuilt” form. If you were to use the distutils that way,
     you would have to rebuild and reinstall your project every time you made a change to it during development.
     Setuptools allows you to deploy your projects for use in a common directory or staging area, but without copying
     any files. Thus, you can edit each project’s code in its checkout directory, and only need to run build commands
     when you change a project’s C extensions or similarly compiled files. You can even deploy a project into another
     project’s checkout directory, if that’s your preferred way of working (as opposed to using a common independent
     staging area or the site-packages directory).
   - `pip -e` and `setuptools` ("develop mode") via `PTH` files
   - Why isn't standardized yet?
     - We [tried in 2019-1](https://discuss.python.org/t/specification-of-editable-installation/1564)
       [2019-2](https://discuss.python.org/t/pip-freeze-vcs-urls-and-pep-517-feat-editable-installs/1473) and
       [2015 in PEP-517](https://peps.python.org/pep-0517/#get-requires-for-build-sdist) and
       [2020](https://discuss.python.org/t/third-try-on-editable-installs/3986)
1. Challenges with this design - 4 minutes

   - Resource files not added - 1 minute
   - Cannot support code generation, e.g. Pydantic classes from
     [JSON Schema or OpenAPI](https://github.com/koxudaxi/datamodel-code-generator/) - 1 minute
   - Support exclude functionality of `setuptools` - 1 minute
   - C-Extension support - 1 minute

1. New approaches - 4 minute
   - Symlinks (individual files or folder) - Windows 7+ also supports it
   - [Import hooks](https://discuss.python.org/t/next-steps-for-editable-develop-proof-of-concept/4118/3) - the
     [`editables`](https://pypi.org/project/editables/) project:
     - Resource file - `importlib.resources`
     - Exclude: Check if module in exclude list and skip import
     - C-extension: on import check if C/cython file changed since last build and call compiler if did not
1. The Python Packaging build system - 3 minute
   - build frontend - creates the environment for the build backend to run and orchestrates communication with the
     backend
   - build backend - read the project configuration and build source distribution or wheel
   - installer - take a wheel and install it
   - pip = build frontend + installer + package discovery/downloader
1. Two proposals - is it bad we could not reach consensus - PEP writting - 1 minute
1. [PEP 660 – Editable installs for pyproject.toml based builds (wheel based)](https://peps.python.org/pep-0660/) - the
   build backend does the heavy lifting - 3 minute
   - [Discuss](ttps://discuss.python.org/t/pep-660-editable-installs-for-pep-517-style-build-backends/8510)
   - unrolling `pip -e`
1. [PEP 662 – Editable installs via virtual wheels](https://peps.python.org/pep-0662/) - the build frontend does the
   heavy lifting - 3 minute
   - [Discuss](https://discuss.python.org/t/discuss-pep-662-editable-installs-via-virtual-wheels/9071)
   - unrolling `pip -e`
1. Where the chips fell - 3 minutes
   - [Decision](https://discuss.python.org/t/pronouncement-on-peps-660-and-662-editable-installs/9450)
   - adoption:
     - [setuptools](https://discuss.python.org/t/implementing-pep-660-for-setuptools/9193)
   - [unforeseen issues](https://discuss.python.org/t/pep-660-support-and-ides/13878/6)
     - static analysis tools can't handle import hooks
1. Q/A - 2 minutes
