# vesting_program

Take-home assignment for Carta interview. Build executable CLI tool for ingesting Vesting/Cancellation events, and outputting aggregated totals on or by an input date.

## Core Requirements:

### Stage One
- [ ] Executable takes positional args: filepath, filterDate:
  - EX `./vesting_program example.csv 2020-03-03`
- [ ] Input csv lacking headers is read as the columns:
  - `VEST,<<EMPLOYEE ID>>,<<EMPLOYEE NAME>>,<<AWARD ID>>,<<DATE>>,<<QUANTITY>>`
- [ ] Output to stdout
  - [ ] Columns: `<<EMPLOYEE ID>>,<<EMPLOYEE NAME>>,<<AWARD ID>>,<<TOTAL BY DATE>>`
  - [ ] output ordered by employee ID, award ID

### Stage Two
- [ ] `VEST` Column may include value "VEST" or "CANCEL"
  - [ ] "CANCEL" values are subtracted from `TOTAL BY DATE` value
  - [ ] `TOTAL BY DATE` value must not go below 0

### Stage Three
- [ ] Executable takes a third optional positional arg `PRECISION`
  - [ ] Defaults to 0 (integers)
  - [ ] Must in range 0-6
- [ ] `QUANTITY` value can specify fractional shares
  - [ ] Values are truncated/filled to specified `PRECISION`
- [ ] `TOTAL BY DATE` in output is truncated/filled to specified `PRECISION`

## Assumptions and Limitations:
- I am assuming that the person assessing this project either have a build environment with the necessary dependencies, or will easily be able to work through any build errors
  - I also assume that the build will occur in an isolated environment that won't break/override/collide with dependencies required for other work
  - I was tempted to ship a Dockerfile with this project in an attempt to isolate/control dependencies in a container, but this seemed out of scope, and also still makes the assumption that Docker is installed
- As a CLI tool with no persistence requirements (and 2hour expected effort), it did not seem appropriate to implement a persistence layer
  - However, any codebase handling large volumes of critical data like this would benefit from a robust/shardable DB layer. I intend to structure the code in such a way that a DB could be added later without starting over

## Caveats, Excuses, and Rationalizations:
I (the anonymous author) am not a Python developer. I use Python in the context of LeetCode-style interview problems because it's expressive and easy to implement solutions quickly. But this is basically my first attempt at a "Project" using Python, and I had a lot to learn before I could attempt any of the Technical Checkpoints below. It was probably a mistake to use Python for this exercise, but I took the chance for the following reasons:

1. The backend team at Carta uses Python, and I want to demonstrate some ability with the relevant stack
1. I wanted to master Python on a deeper level for my own benefit, and this was a good motivator

Though I am certain I will fall short on idiomatic code style and project structure, my hope is that this will clearly demonstrate my ability to find relevant resources, self-teach and incorporate best practices quickly.

## Technical Checkpoints:
- [ ] Separate concerns into testable units
- [ ] Implement Class Inheritance/Interfaces anticipating future extension
  - [ ] Interfaces should anticipate Persistence layer in the future
- [ ] Compose classes with Dependency Injection
- [x] Test Coverage using Python stdlib unittest
- [x] Minimize memory overhead when processing large files via use of Generators
- [ ] Validation of input values -- Cancel execution if invalid values found
- [x] Makefile
  - [ ] command for building executable
  - [x] command for running tests
  - [ ] command for cleaning up venv and temp pycache/pytest files
- [ ] Use libraries as appropriate
- [ ] PEP 257 Docstrings for modules/classes/methods
- [ ] PEP 484 Type Hints
