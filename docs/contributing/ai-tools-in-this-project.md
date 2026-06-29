---
myst:
  html_meta:
    description: "Placeholder: one sentence on the AI tools available in this repo and how contributors and maintainers invoke them (keep under 160 characters)."
---

(ai-tools-in-this-project)=
# AI tools in this project

We provide some AI tooling and scaffolds to help contributors to use AI in this project in line with our {ref}`AI policy <acceptable-use-of-ai>`.
This page outlines what's available and how to use it.

Our goal is to help minimize the tokens needed to complete particular tasks.

## Where the tooling lives

* `AGENTS.md`:

  Lives at the root of the repository. It contains our general instructions for agents and LLMs to understand how the project is structured and maintained.

* `.github/prompts/`:

  Contains the on-demand workflows that you can call from the command line. These prompts point to the specific instructions an agent or LLM needs to complete the task.

* `.github/instructions/`:

  Contains the instruction files providing rules that guide agents and LLMs when they're making changes in the project.

* `.github/copilot-instructions.md`:

  Instructions specifically for the agents you can call from the GitHub web UI (e.g. when requesting an agent review).


## Prompts you can invoke

Run these prompts as commands on the CLI or in your chat window. You can either run the command by itself, or with additional instructions/information that you want your LLM to include.

### new-page

**What it does**
: Run this prompt using `/new-page` to bootstrap an outline of a new page in your chosen Diátaxis type. If you also include brainstormed notes or bullet points with the prompt, these will be sorted (without amendment) into the appropriate sections of the outline. All the required syntax will be bootstrapped into place.

: You should decide before you start what Diataxis section it belongs to, and which page should be its parent.

### review-page

**What it does**
: Run this prompt using `/review-page` at *any time* during your writing process to get a "first read" (note: you can run this as many times as you need!).
: The first part of the prompt checks for "completeness" against the list of criteria every page should contain.
: The second part provides you with some helpful feedback, questions and suggestions for things you may want to consider.

### capture-learnings

**What it does**
: Run this prompt using `/capture-learnings` at the end of a particularly helpful session. If you (or your LLM) discover an edge case that we hadn't considered, or find a better way to do somehting, this prompt allows the LLM to fold concrete improvements from your session back into our scaffolding so it works better the next time.


## Instructions that guide the AI

Instruction files help to guide the behavior of the AI and ensure it follows the rules of the repository.
We have two kinds of instructions files in `.github/instructions/`:

- Auto-applied rules: these contain an `applyTo` glob at the top of the page (e.g. docs-review, and the per-Diátaxis-type templates: tutorial, how-to, explanation, reference). When any request touches a page that falls under these `applyTo` rules, the relevant instruction files are automatically added to the AI's context.
- Shared references: these have no `applyTo` glob, and are pulled in specifically by name (landing-pages, page-completeness) when referenced in e.g. prompts or skills.

We split our rules into separate instruction files for each task or scenario, so we can restrict the AI's context window to only include the instructions it needs to complete that task. For example, if you're looking at a tutorial page, the AI doesn't need instructions for all the other Diataxis types. By feeding the AI only what it needs, we can reduce the number of tokens a task takes.

You can also reduce token spend by starting a new conversation with your AI for each task you want it to complete, so that it doesn't carry forward irrelevant files from older parts of a conversation.



