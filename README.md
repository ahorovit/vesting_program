# vesting_program

Take-home assignment for Carta interview. Build executable CLI tool for ingesting Vesting/Cancellation events, and outputting aggregated totals on or by an input date.

## Core Requirements

### Stage One

- [x] Executable takes positional args: filepath, filterDate:
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

- [x] Executable takes a third optional positional arg `PRECISION`
  - [x] Defaults to 0 (integers)
  - [ ] Must in range 0-6
- [x] `QUANTITY` value can specify fractional shares
  - [x] Values are truncated/filled to specified `PRECISION`
- [x] `TOTAL BY DATE` in output is truncated/filled to specified `PRECISION`

## Assumptions and Limitations

- I am assuming that the person assessing this project either have a build environment with the necessary dependencies, or will easily be able to work through any build errors
  - I also assume that the build will occur in an isolated environment that won't break/override/collide with dependencies required for other work
  - I was tempted to ship a Dockerfile with this project in an attempt to isolate/control dependencies in a container, but this seemed out of scope, and also still makes the assumption that Docker is installed
- As a CLI tool with no persistence requirements (and 2hour expected effort), it did not seem appropriate to implement a persistence layer
  - However, any codebase handling large volumes of critical data like this would benefit from a robust/shardable DB layer. I intend to structure the code in such a way that a DB could be added later without starting over

## Caveats, Excuses, and Rationalizations

I (the anonymous author) am not a Python developer. I use Python in the context of LeetCode-style interview problems because it's expressive and easy to implement solutions quickly. But this is my first attempt at a fleshed-out "Project" using Python, and I had a lot to learn before I could attempt any of the Technical Checkpoints below. This may have been unwise, but I took the chance for the following reasons:

1. The backend team at Carta uses Python, and I want to demonstrate some ability with the relevant stack
1. I wanted to master Python on a deeper level for my own benefit, and this was a good motivator

Though I am certain I will fall short on idiomatic code style and project structure, my hope is that this will clearly demonstrate my ability to find relevant resources, self-teach and incorporate best practices quickly. Either way, I've found it to be an enjoyable learning experience.

## Technical Checkpoints

- [x] Separate concerns into testable units
- [ ] Implement Class Inheritance/Interfaces anticipating future extension
  - [ ] Interfaces should anticipate Persistence layer in the future
- [x] Compose classes with Dependency Injection
  - [ ] Find/use Annotation-based DI framework for Python
- [x] Test Coverage using Python stdlib unittest
- [x] Minimize memory overhead when processing large files via use of Generators
- [x] Validation of input values -- Cancel execution if invalid values found
- [x] Makefile
  - [ ] command for building executable
  - [x] command for running tests
  - [x] command for cleaning up venv and temp pycache/pytest files
- [ ] Use libraries as appropriate
- [ ] PEP 257 Docstrings for modules/classes/methods
- [ ] PEP 484 Type Hints
- [ ] Lint with MyPy or Flask8
