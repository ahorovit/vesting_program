# vesting_program

Take-home assignment for Carta interview. Build executable CLI tool for ingesting Vesting/Cancellation events, and outputting aggregated totals on or by an input date.

## How To Use

Run the following Makefile commands from the project root:

- `make stageX` - with 1,2 or 3 instead of X. This reads input files from the `data` directory and CLI args to match examples in the Project Statement
- `make test` - runs all Unit Tests
- To run arbitrary inputs:
  1. run any of the `make` commands above to build the virtualenv
  1. `venv/bin/python vesting_program/main.py <INPUT_FILEPATH> <FILTER_DATE> <PRECISION (optional)>` should work for any valid inputs
    - I tried to catch any obvious invalid inputs (mangled csv, invalid dates, etc) and throw descriptive errors where possible

## Core Requirements

### Stage One

- [x] CLI Program script takes positional args: filepath, filterDate:
  - EX `./vesting_program example.csv 2020-03-03`
- [x] Input csv lacking headers is read as the columns:
  - `VEST,<<EMPLOYEE ID>>,<<EMPLOYEE NAME>>,<<AWARD ID>>,<<DATE>>,<<QUANTITY>>`
- [x] Output to stdout
  - [x] Columns: `<<EMPLOYEE ID>>,<<EMPLOYEE NAME>>,<<AWARD ID>>,<<TOTAL BY DATE>>`
  - [x] output ordered by employee ID, award ID
  - [x] All employees in input are listed regardless of filterDate

### Stage Two

- [x] `VEST` Column may include value "VEST" or "CANCEL"
  - [x] "CANCEL" values are subtracted from `TOTAL BY DATE` value
  - [x] `TOTAL BY DATE` value must not go below 0

### Stage Three

- [x] CLI Program takes a third optional positional arg `PRECISION`
  - [x] Defaults to 0 (integers)
  - [ ] Must in range 0-6 (I neglected to enforce this)
- [x] `QUANTITY` value can specify fractional shares
  - [x] Values are truncated/filled to specified `PRECISION`
- [x] `TOTAL BY DATE` in output is truncated/filled to specified `PRECISION`

## Assumptions and Limitations

- The Makefile assumes you have Python 3 installed, and it's possible some features will not work if you have an early python3 installation. I used 3.9.10, so if any failures come up, that may be the cause.
  - I was tempted to ship a Dockerfile with this project in an attempt to isolate/control dependencies in a container, but this seemed out of scope, and also still makes the assumption that Docker is installed
- As a CLI tool with no persistence requirements (and 2hour expected effort), it did not seem appropriate to implement a persistence layer
  - However, any codebase handling large volumes of critical data like this would benefit from a DB layer. I intend to structure the code in such a way that a DB could be added later without starting over

## Caveats, Excuses, and Rationalizations

I am a Python novice. I exclusively use Python in the context of LeetCode-style interview problems because it's expressive and easy to implement solutions quickly. But this is my first attempt at a fleshed-out "Project" using Python (complete with modules and test coverage), and I had a lot to learn before I could attempt any of the Technical Checkpoints below. This may have been unwise, but I took the chance for the following reasons:

1. The backend team at Carta uses Python, and I want to demonstrate some ability with the relevant stack
1. I wanted to master Python on a deeper level for my own benefit, and this was a good motivator

Though I am certain I will fall short on idiomatic code style and project structure, my hope is that this will demonstrate my ability to find relevant resources, self-teach and incorporate best practices quickly. I fear it also demonstrates my stubbornness and perfectionism...

UPDATE: For full transparency, this effort took me closer to 2 days than 2 hours. But I have learned a lot, and and proud of the end product. See TODOs in the code for unresolved issues (more in checkpoints below)

## Technical Checkpoints

- [x] Separate concerns into testable units
- [ ] Implement Class Inheritance/Interfaces anticipating future extension
  - [x] Interfaces should anticipate Persistence layer in the future
- [x] Compose classes with Dependency Injection
  - [ ] Find/use Annotation-based DI framework for Python (This doesn't seem to be a widely used Python utility)
- [x] Test Coverage using Python stdlib unittest
- [x] Minimize memory overhead when processing large files via use of Generators
- [x] Validation of input values -- Cancel execution if invalid values found
- [x] Makefile
  - [ ] command for building executable (I didn't get to this, and this seemed like a minor point in the prompt)
  - [x] command for running tests
  - [x] command for cleaning up venv and temp pycache/pytest files
- [x] Use libraries as appropriate
- [ ] PEP 257 Docstrings for modules/classes/methods (Inconsistent/incomplete)
- [ ] PEP 484 Type Hints (Inconsistent/incomplete)
- [ ] Lint with MyPy or Flask8 (I didn't get to this)
