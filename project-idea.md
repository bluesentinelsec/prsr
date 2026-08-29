This project is called "prsr", pronounced, "pur-sir", and short for "pull request self review."

Here is the situation:

I commonly like to have AI open a pull request on GitHub on my behalf - we're talking 100% AI generated PR's.

AI opens the PR, and then, I review the PR in my web browser on the github diff page.

This work great because I can make my comments line-by-line, have AI read the comments with gh, then implement changes.

However, the problem with this is, because AI opened the PR on my behalf with my creds, it looks like I am leaving comments on my own code.

Even though i think this is perfectly legitimate, my boss and others think its weird (i.e. *why are you commenting on your own PRs?*)

What I want prsr to do is essentially render an equivalent gitub diff view locally, PRESERVING LINE NUMBERS in the output. The output should be text, either to console or file, which, I can then add comments to code snippets locally in the text file. AI gets the comments, and still has the line numbers and diff output to know what my comments refer to.

This should be an idiomatic python application, with the intent to upload to pypi for easy installation.

My tools should be modular, with a data model, logic / rules, and view layers.
The tool should be a CLI powered by argparse, with all logic call-able as a library API.
The tool needs unit tests proving correctness.

I have another project, /Users/michaellong/projects/cppboot, written in python, that illustrates how to publish to pypi via github actions, feel free to draw from that.

Use gh and my default creds to create a public prsr repo on github, under the GPLv2 license.

I prefer the prsr program to require gh under the hood, and use it via sub-process invocation.
This simplies our program, and we can ride gh for authentication.

I expect a user experience resembling:

# generate github diff view with line numbers to console
prsr --pr 1234

# generate github diff view with line numbers to file
prsr --pr 1234 -o diff.txt
prsr --pr 1234 > diff.txt

# generate diff view with line numbers based on a commit
prsr --commit abc123

Add needed arguments if we need to specify source and destination branches and the like.
Output should resemble git diff views prepended with line numbers marking the change.
The entire point of this program is to permit the developer to write PR comments locally to a file, so we sidestep the "talking to myself" problem I described.

Also, add ubiquotous CLI args including --verbose (make sure we have a decent console logger), and --version 


