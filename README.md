# agentreader - a minimal drop-in browser tool for LLM agents

Agentreader is a simple drop-in Python module that gives your LLM agents an ability to read the Internet.

Features:

* Returns plain text instead of raw HTML.
* No API key needed. Just copy-paste the `reader.py` into your project.
* Implements Langchain's `BaseTool` interface -- drop-in the tool into any existing agent.
* Extracts page title, authors, and other metadata.
* Supports paging through results to respect your context window limits.
* Supports both single-input tools (only URL) and [structured tools](https://python.langchain.com/en/latest/modules/agents/agents/examples/structured_chat.html) that give your agent more control over the output.

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

That's it! You can now add `reader_tool` into the list of tools available to your agent.

For full examples of usage, and details about the multi-input ("structured") tools, see the [Usage guide](Usage_guide.ipynb).

## Background

While trying to make robust autonomous agents in the style of [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT), I ran into two problems, many of which are common to all LLM agents.

* The raw HTML output from `requests.get` wastes token count and inserts a lot of confusing tokens. The relevant part of the website is usually the body text.
* Using Playwright introduces too many possible actions which confuse the agent -- it starts to use tools unnecessarily. Also, it's finicky to integrate.

Agentreader is a solution to those. Really it is just a very thin wrapper around libraries that extract text from a website.

## But does it work?

In the [Usage guide](Usage_guide.ipynb) notebook one of the examples works well and the other not very well. However, I think that is mostly because the default Langchain agents are very un-optimized. I originally used it in a heavily-modified two-stage agent (AutoGPT-style) where I got it to work very well in combination with a SerpAPI based search tool. If it doesn't for you, tinker with the prompts, remove every unnecessary tool and part of the prompt, and you may see better results.

## Tests

One-off: `pip install pytest`.

```bash
pytest test_reader.py
```

# Contributing

I've structured this repo in the expectation that you will do heavy customization to how it works -- prompt engineering, adding support for specific websites, or even replacing the underlying text-extraction libraries. That is because key prompts are baked into the code: `ToolInput` introduces strings that describe input arguments, and output string templates describe the format of the output.

It would of course be possible to generalize these, but with this repo I favor simplicity over generality.

That said: if you discover something valuable -- either an additional feature, or a way to make this library even simpler -- then open a ticket/PR and let's discuss!


# TODOs
- [ ] reduce number of dependencies (`trafilature` has a dependency conflict with e.g. `openai/evals`).
- [ ] extract metadata more consistently - currently doesn't work when falling back to `newspaper3k`
- [ ] better support for e.g. Twitter and other popular non-article content
- [ ] README.md: objective comparison against playwright, requests.get - on features, output token counts for a few websites, etc
- [ ] add LICENSE.md