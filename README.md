# How I checked the AfD's "MesserHauptstadt" knife-crime map

MesserHauptstadt ("knife capital") is a website the far-right Alternative
for Germany (AfD) launched in Berlin on 1 April 2026. It uses AI to pick
knife crimes out of police press releases and maps them across the city. I
checked every case the site logged in its first month against the release
it cites. 20 of the 245 cases (8%) had nothing to do with a knife attack.

It follows on from my check of the Einzelfallticker, an earlier crime map
the AfD promoted ([story](https://europeancorrespondent.com/en/r/the-farright-lies-to-you-about-migrant-crime-again),
[repo](https://github.com/joshdaxelrod/einzelfallticker)).

This repo has the data and code behind the analysis.

- Story: [The AfD's Knife Crime Portal is Built on Bad Data](https://www.heistberlin.com/messerhauptstadt-knife-map-afd-election-fear/), *HEIST*, 19 June 2026
- The data: [every case and how it was coded](docs/the-data.md)
- To rerun the analysis: [step-by-step instructions](docs/run-it-yourself.md)

## Method

### 1. Scraping the cases

To find where the map gets its cases, I opened my browser's developer
tools, watched the Network tab and clicked around the site. The requests
showed the page pulling cases from a database at `api.messermaps.de`, with
an access key (`afd-berlin`) sent along in the request. Both are in the
site's public code, which every visitor's browser downloads.

On 21 April 2026, I used a scraper to pull all 245 cases from that
database, each with a title, date, location and a link to its source.
([`scripts/get_cases.py`](scripts/get_cases.py))

### 2. Reading and counting every case

A second scraper downloaded the police release behind each case. Then I
read every one by hand. I counted a case as unrelated to knife attacks if
its source was a release from outside Berlin, if no knife was involved, or
if a knife was only found on the suspect afterward. The category I gave
each case is in [the data](docs/the-data.md).
([`scripts/check_sources.py`](scripts/check_sources.py))

### 3. The database behind the site

The map only shows Berlin. Asking its database (see step 1) for each
state's totals, the same request the site makes for Berlin, showed it
doesn't only hold Berlin cases. It holds cases from all 16 German states.
([`scripts/state_totals.py`](scripts/state_totals.py))

### 4. The police WhatsApp channel

MesserHauptstadt's homepage never mentions migrants. To see whether people
make that link anyway, I looked at how they react to crime news. Berlin
police post updates to a public WhatsApp channel where followers can react
with emojis, and one that shows up all over it is the plane, a symbol tied
to the AfD's calls to deport migrants by plane. Across 97 posts from 13
April to 15 May 2026, the post with the most plane reactions, 213, was
about a 15-year-old found with a combat knife in his vest.
([`whatsapp-channel-scraper`](https://github.com/joshdaxelrod/whatsapp-channel-scraper),
[`data/whatsapp_reactions.csv`](data/whatsapp_reactions.csv))

## Limitations

- Deciding what counts as unrelated takes judgment. Every case's category
  is in the data, so you can draw the line somewhere else.
- Police sometimes update releases after publishing them. A few may read
  differently now than when I checked them.
- WhatsApp channel reactions are anonymous. They show what followers
  reacted with, not who they are.

## How I used AI

- AI (Claude Opus 5.5) helped write the scripts and organize the data in
  this repo.
- I read and counted the cases myself.
- No case was counted or left out by AI. The scripts only collect data.

## Using this elsewhere

- Open your browser's developer tools, go to the Network tab and click
  around the site: open the map, change the filters, try the search. Watch
  what loads each time. It's often a direct line to the data behind the
  site, including data the page itself never displays.
- When you find the request that loads a site's data, look at the end of
  its address for settings like `start-date=` or `state=be`. Changing them
  can show what the database holds beyond what the site displays. Here,
  swapping Berlin's `be` for other state codes showed cases from all 16.
- [`whatsapp-channel-scraper`](https://github.com/joshdaxelrod/whatsapp-channel-scraper)
  collects the posts and emoji reactions from any WhatsApp channel, the
  public broadcast feeds that police and governments increasingly post to.
- If you build on this, I'd love to hear about it:
  [joshdaxelrod@gmail.com](mailto:joshdaxelrod@gmail.com).

---

By [Josh Axelrod](https://josh-axelrod.com). Code is under the [MIT License](LICENSE). My coding of the data is public domain ([CC0](https://creativecommons.org/publicdomain/zero/1.0/)).
