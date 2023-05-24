# TODO name
TODO read how to make a good github readme

## Usage

Copy-paste the `reader.py` file into your project.

Install dependencies:

```bash
pip install langchain trafilatura newspaper3k
```

Import and initialize the tool:
```python
from reader import SimpleReaderTool
reader_tool = SimpleReaderTool()
```

That's it! You can now add `reader_tool`  into the list of tools available to your agent.

For a full example of usage, see TODO agent notebook.

## SimpleReaderTool vs ReaderTool
TODO

Example input & output from each tool


# Comparison:

TODO

* <this repo>
* requests.get
* playwright

on:
* features
* output token count



## Tests
```bash
pip install pytest
pytest test_reader.py
```



# TODO
- [ ] example notebook
- [x] create SimpleReaderTool with only one input
- [ ] how to contribute