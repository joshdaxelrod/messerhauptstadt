# The data

[← Back to the walkthrough](../README.md)

Both files are CSVs, which open in Excel, Google Sheets or Numbers.

## [`cases.csv`](../data/cases.csv): every case on the map

The 245 cases MesserHauptstadt had logged by 21 April 2026, with how I
coded each one.

| column | what it is |
|---|---|
| `id` | the site's ID for the case |
| `date` | the date the site gives for the incident |
| `title` | the case's headline, in German, as the site wrote it |
| `source` | the police release the site cites |
| `category` | `wrong link`, `no knife`, `knife only found afterward`, `knife mentioned, not used`, `weapon not described` or `knife case` |

## [`whatsapp_reactions.csv`](../data/whatsapp_reactions.csv): reactions on the Berlin police channel

97 posts from the Berlin police's public WhatsApp channel, 13 April to 15
May 2026.

| column | what it is |
|---|---|
| `date`, `time` | when police posted it, Berlin time |
| `message`, `message_en` | the post, in German and in English (machine translation) |
| `total_reactions` | all emoji reactions on the post |
| `plane_reactions` | ✈️ reactions only (blank if the breakdown couldn't be read) |
| `all_reactions` | every emoji and its count |

Reactions on WhatsApp channels are anonymous, so there's no information
about who reacted.

## Using this data

You're welcome to use and build on it. No credit needed, but if you do
something with it, I'd love to hear about it:
[joshdaxelrod@gmail.com](mailto:joshdaxelrod@gmail.com).
