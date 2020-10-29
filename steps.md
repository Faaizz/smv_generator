# Steps
Steps to recreate project.

## Setup project structure
```md

|-  src
|   |-  main                        <- Main program logic 
|      |-  __init__.py
|      
|   |-  test                        <- tests
|      |-  __init__.py
|      
|   |-  __init__.py
|
|-  README.md 
|
|- steps.md

```

## Setup test environment

Run tests from ./src with:
```bash
python -m unittest discover
```