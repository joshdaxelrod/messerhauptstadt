# Run it yourself

[← Back to the walkthrough](../README.md)

This walks through each step of the method, so you can run it on the
site as it is today. You don't need to know how to code: you'll paste
commands into Terminal, press Return, and open spreadsheets.

## Before you start

You need:

- Terminal, the app where you type commands. On a Mac, press `⌘ Space`,
  type "Terminal" and press Return. On Windows, use Command Prompt.
- Python 3.10 or newer. To check, paste `python3 --version` into Terminal
  (`python --version` on Windows) and press Return. If it's missing or older, download it from
  [python.org](https://www.python.org/downloads/).

Every gray box below is a command. Paste it into Terminal and press
Return.

## Set up (once)

Download this repo: click the green **Code** button on the
[main page](https://github.com/joshdaxelrod/messerhauptstadt), then
**Download ZIP**, and double-click the file in your Downloads folder to
unzip it.

Then install what the scripts need:

```bash
cd ~/Downloads/messerhauptstadt-main
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

<details>
<summary>On Windows</summary>

```bat
cd %USERPROFILE%\Downloads\messerhauptstadt-main
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On Windows, type `python` instead of `python3` in the commands below.

</details>

## Before each session

Paste this before running any of the steps below, and again whenever you
open a new Terminal window:

```bash
cd ~/Downloads/messerhauptstadt-main
source venv/bin/activate
export MESSER_API_KEY=afd-berlin
```

<details>
<summary>On Windows</summary>

```bat
cd %USERPROFILE%\Downloads\messerhauptstadt-main
venv\Scripts\activate
set MESSER_API_KEY=afd-berlin
```

</details>

## Step 1: Pull the cases

```bash
python3 scripts/get_cases.py
```

This saves every Berlin case the map holds to `output/cases.csv`. To only
get cases from certain dates, add them to the end of the command, for
example `--start 2026-03-01 --end 2026-04-21`.

## Step 2: Read every case

This downloads the police release behind each case from step 1:

```bash
python3 scripts/check_sources.py --cases output/cases.csv
```

It takes about a second per case. If it stops, run the same command again
and it picks up where it left off.

Open `output/review.csv` in a spreadsheet app. Each row has a case's title
next to the text of the release it cites. Add a column for your verdict
and, for each case, ask:

1. Is the release from Berlin? If not, it's a wrong link.
2. Was a knife involved at all?
3. Was the knife used in the crime, or only found on the suspect
   afterward?

Then filter your verdict column to count each kind.

## Step 3: Check the other states

```bash
python3 scripts/state_totals.py
```

This asks the database how many cases it holds for each of the 16 states
and saves the totals to `output/state_totals.csv`.

## Step 4: Count emoji reactions

I collected the WhatsApp reactions with a separate tool,
[`whatsapp-channel-scraper`](https://github.com/joshdaxelrod/whatsapp-channel-scraper).
Its README explains how to set it up and point it at the Berlin police
channel.
