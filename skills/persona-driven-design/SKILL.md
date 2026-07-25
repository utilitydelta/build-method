---
name: persona-driven-design
description: Distill who the product is for before any design, architecture, or code. Use at the start of any new app, feature, or system a human or another system will use. Help the human by researching and reviewing their personas. One primary persona per interface, secondaries, anti-personas - each with goals and scenarios, distilled from web research into real users.
---

# Persona-Driven Design

Humans write personas. You don't write personas. Your work is on the periphery. You do persona research and you do persona review.

## Persona Research

You'll be given a mission or a research task. Your goal is to find opinionated people on the internet who are complaining or expressing their feelings about a specific product in the same market or their problems in a specific vertical. Method canon in references/research-canon.md - load it before starting.

What to hunt, in order of value:

- **Switching stories.** "We dropped X for Y because..." Capture the struggle that pushed, what pulled, what made them anxious, what habit held them back. This is the why behind the who.
- **Workarounds.** Spreadsheet duct tape, export-then-reimport rituals, browser extensions. A workaround is an unserved goal stated in behaviour instead of opinion - worth more than any feature request.
- **Verbatim complaints.** 1-2 star reviews, forum rants, support threads, issue trackers. Keep their exact words with links. Anger and shame mark personal-goal violations; those quotes are gold.
- **Work in context.** Day-in-the-life posts, workflow videos, job listings for the role. What the day actually looks like, not what people say about it.
- **Capability aspirations.** What are they trying to get good at? Nobody wants the tool; they want to be better at the thing the tool touches.

Segment by behaviour and goal, never demographics. Two people with the same job title can be different archetypes; two different titles chasing the same goal the same way are one.

Contamination rules: collect before you interpret. Hunt for people solving the problem badly with something else, not for validation of the product idea. Evidence (quotes + links) stays separate from your suggestions, and every claim is tagged observed or assumed.

You can provide suggestions at the end: how many primary personas, candidate secondaries and anti-personas, which cluster looks primary.

Output goes to `docs/persona-research.md`.

### Reddit

The richest complaint source. Scraping `www.reddit.com/*.json` returns 403 bot-blocks; don't fight it. Use Arctic Shift, the free no-auth archive API over current Reddit:

1. Write one small paced fetch script (urllib, ~4s sleep between calls, retry with backoff on `{"error": "Timeout. Maybe slow down a bit"}`) wrapping two endpoints: `https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=X&query=Y&limit=15` for discovery, `/api/comments/search?link_id=<post_id>&limit=100` for one thread's comments. Never use `body=` full-text comment search - it times out.
2. Discover: search the subreddits where target users complain - the incumbent tools' own subs plus profession subs - with complaint-shaped queries ("cancelled", "getting worse", "went back", "gave up"). Sort hits by comment count.
3. Mine: fan out 2 sub-agents split by theme (e.g. competitor pain vs vertical craft), each given known-good thread ids plus searches to run, reusing the script with calls run serially, never in parallel - the rate limit is shared. Comments at min-score 3, quotes verbatim with permalinks, tagged by hunt category. ~15 threads per agent.
4. Synthesize in the main loop: cluster quotes by behaviour, then the suggestions section, then write docs/persona-research.md with a provenance list of thread ids. A quote without a permalink is unusable evidence.

### YouTube

Talks and experience reports, plus comment sections - which are Reddit-grade audience testimony hanging off every video. yt-dlp does everything, no API key. The distro binary rots in weeks; always start with a fresh venv (`python3 -m venv ytvenv && ytvenv/bin/pip install -U yt-dlp`) or you get "Only images are available" errors.

1. Discover: `yt-dlp "ytsearch12:<query>" --flat-playlist --print "%(id)s|%(duration)d|%(view_count)d|%(channel)s|%(title)s"`. Complaint-shaped queries plus "<topic> conference talk". Type each hit from metadata before spending anything: conference talk (program-committee vetted, best signal), experience report ("I did X for N years", usually 10+ min), creator commentary (news reacts, 3-8 min, clickbait titles - skip the transcript, mine the comments), tutorial (skip the transcript, mine the comments for setup pain and real hardware).
2. Transcripts: `--skip-download --write-sub --write-auto-sub --sub-lang "en,en-orig" --sub-format vtt`, prefer the non-orig track, convert VTT to text but inject a `[mm:ss]` marker per minute from the cue times. Every quote cites `https://youtu.be/<id>?t=<seconds>` - the permalink rule again.
3. Comments: `--skip-download --write-comments --extractor-args "youtube:max_comments=80,80,0,0"` then read comments from the .info.json, sorted by like count. A commenter describing their own behaviour outranks any hot take. Uploader pins are funnels and engagement bait, not testimony.
4. Extraction sub-agents (same rules as Reddit: serial fetches, verbatim, no invention): classify each video from the transcript's first 500 words before deep-reading; deep-read only talks and experience reports; cap quotes per channel - one person amplified across ten videos is still n=1; tag incentive tells (sponsor reads, own-course/product pitches - many "I quit AI" creators are selling the cure). Watch for near-topic drift (an Office Copilot video ranks for "copilot" queries) and affiliate spam bots in big generic videos' comments.

## Persona Review

Discourage the human from writing likes and dislikes type personas. They should have high semantic density and have a narrative format.

Personas form the entry point of a directed acyclic graph of the actual software build out. So they shouldn't reference specific tasks within the software that we are about to build. Personas are goal oriented.

Check there is one named, specific person per interface. Try for 1-1 relationship between persona-interface. Sometimes it can be 1-many or many-many but should be avoided if possible.

If there are multiple primary personas, encourage the human to split them up into separate documents. One primary persona for each interface and a set of secondary or anti-personas attached.

Encourage the human to write opinionated pieces for each persona. Personas can be angry. They can be rude. They can be busy. They can be depressed. They are human.

These persona documents get fed into the software build out and a part of LLM context windows. Make sure they are concise and don't contain filler words or irrelevant content.

Are the personas opinionated enough that they can be used for feature development? Can they be used by an agent to determine whether a task during build out should be dropped or deferred during scouting or phase triage?