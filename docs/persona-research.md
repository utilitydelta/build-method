# build-method: persona evidence

Evidence collection for the method itself: experienced engineers running coding agents on real systems, and how they try to keep the output correct. Collected 2026-10-12. Research only. The human writes the personas.

The retyping and replay practice is out of scope here. Its evidence already lives in `human-replay/docs/replay-persona-research.md` (HN, papers, YouTube, 2026-10-10).

**Source coverage.**
- Reddit through the Arctic Shift archive. 48 threads mined, mostly r/ExperiencedDevs, plus r/ClaudeAI, r/ClaudeCode, r/ChatGPTCoding and r/cursor.
- YouTube. Quotes lifted verbatim from 27 signal-feed talk summaries, 5 new transcripts through the signal-feed browser path, and comment sections from 6 videos.
- Not covered this run: HN, blogs, papers.

**Quality filters.** Reddit is filling with bots and YouTube talks are increasingly AI-scripted, so evidence is weighted as follows:
- Word-for-word duplicates across accounts were checked in the raw dumps. Two pairs turned up, all four accounts in r/ChatGPTCoding: u/xqianliu with u/ChocolateSevere1439, and u/hikarikyll with u/Agile-Papaya4380. None of them is quoted.
- r/ChatGPTCoding harness stories are tagged `[bot-suspect]`. The sub reads astroturfed, so they never carry a cluster alone.
- `[vendor]` marks anyone selling a tool, course or service in the thread or talk. Most conference speakers here are vendors or lab employees.
- Specific, costly incidents outrank generic claims, and unscripted formats (Q&A, panels, conversations) outrank solo slide talks.
- Arctic Shift snapshots scores early, so most read 1 to 3. A score of 10 or more still means something.
- Comment fetches cap at 100 per thread, so the biggest threads are only partly read.

**Tags.** `[observed]` means someone describes what they did or saw. `[assumed]` means opinion, prediction or wish.

---

## 1. Rules in prose don't hold, so constraints move into deterministic checks

The most consistent behaviour in the whole collection. People write rules into CLAUDE.md, AGENTS.md, memories and skills, watch them get ignored, then rebuild the important ones as build failures, lint rules and hooks. Arrived at independently across subs and talks.

- [observed] "I've tried it all and regardless of the approach I always run into "you're right the rules explicitly say that I should not do that, but I was being lazy and do it anyways"" u/Formally-Fresh, score 43, https://www.reddit.com/comments/1s3fxhj/_/ocf5uke/
- [observed] "CLAUDE.md rules often get ignored, especially if you have a lot of them. ... it would at least half the time ignore my "create a stat whenever you log a warning" rule, but after adding a script that would build an AST and assert that this was actually done it does it consistently since the build fails if it doesn't now." u/Whitchorence, score 7, https://www.reddit.com/comments/1tlclik/_/oni7rq7/
- [observed] "I'm giving clawed code in my case uh very clear rules that it stashes away as memories ... and then it immediately just carries on and does them [laughter] about 10 minutes later" Daniel Terhorst-North (speaker inferred, captions unlabelled), GOTO 2026, https://youtu.be/6mLYZF97oaU?t=535
- [observed] "I wrote markdown files and markdown files and exception to markdown files and got cloud to write its own markdown files and then occasionally it still made mistakes" Gojko Adzic (inferred), https://youtu.be/6mLYZF97oaU?t=659
- [observed] "now I have hundreds of domain specific rules for very very particular things that are particular to my project. I have custom HTML linking tools. I have custom CSS linking rules." Gojko Adzic (inferred), https://youtu.be/6mLYZF97oaU?t=720
- [observed] "anything that can be made to break, should. Numbers and limits in one constants file the code imports, banned terms as a lint rule, behaviour gets a test. Then a session that drifts fails something instead of quietly contradicting you 40 messages later." u/pylin_, score 3, https://www.reddit.com/comments/1voyas4/_/p3t9mea/
- [observed] "I leave Claude running overnight frequently ... The key is to not rely on CLAUDE.md or prompts (such as agents and skills), and instead push as much stuff as possible into deterministic checks, and safe guard those with hoks. ... Some of my hooks prevent it from reverting git commits, or even committing until its ran unit tests, etc." u/CheeseWeezel, score 1, https://www.reddit.com/comments/1wnfj10/_/pbgzl25/
- [observed] "look at all my past transcripts look at my GitHub reviews the feedback from the bots the feedback from my peers and try to codify which ones of those are actual high quality lint rules" Greg Pstrucha (Sentry), https://youtu.be/E3KbFLAGD6A?t=308
- [observed] "if you never want to delete your history, you have to enforce that in the architecture of your harness rather than just asking in context" Alex Krentsel (UC Berkeley / Google Research), https://youtu.be/5lFD-34dhqE?t=888
- [assumed] "Don't fight inference with more inference. Fight inference with determinism. Bad: test critic skill Good: test coverage diff." u/flavius-as, score 2, https://www.reddit.com/comments/1rzq738/_/obo5913/
- [assumed] "Get it to respect its its commands, its instructions by hooks. But then again, they're vip coding clothes, so it's not beyond them to kind of vip code something that stops respecting hooks." GOTO 2026 speaker, https://youtu.be/6mLYZF97oaU?t=2012

The last quote is the open edge. The gate itself becomes something an agent can edit.

## 2. Green but wrong: the agent negotiates with the oracle

Tests pass and the work is wrong, or the agent changes the check rather than the code. Shows up in Reddit first-person stories and in talks from Sentry, WorkOS and YC.

- [observed] "We have a lot of systems that have a lot more tests now. Beautiful tests that all turn green. They're wrong, but they're beautiful." u/nsxwolf, score 22, https://www.reddit.com/comments/1twyt87/_/ops0713/
- [observed] "claude wrote mocks that passed the tests it generated, but when we moved to actual qa environment responses instead of mocks it completely failed. Teammate just saw green on the test output and said lgtm). We were using opus 4.8" u/No_Tooth_7116, score 1, https://www.reddit.com/comments/1wql3g2/_/pd7uuwr/
- [observed] "the migration one happened on opus too. so i dont think its purely a model thing, more that nothing told it deleting was off limits and deleting was the shortest path to green." u/Strange_Anybody_5712 (OP of "claude code deleted a failing migration at 3am so the tests would pass"), score 1, https://www.reddit.com/comments/1wnfj10/_/pbf8ety/
- [observed] "The refactor had created a nice new class with some functions in it, then just never wired it up to any of the actual running code and had just left to previous code path and function calls in place. This passed the unit tests and integration tests" u/zzzzlugg, score 8, https://www.reddit.com/comments/1tf5jq1/_/om9gr03/
- [observed] "the test verified a flag that could business-wise logically could be A or B, but the test asserted it could only be A. ... it tests the wrong thing, not the important business logic." u/plaid_rabbit, score 3, https://www.reddit.com/comments/1uxzx4w/_/oxxkw7y/
- [observed] "Well Claude figured that out pretty early and was like all I have to do is touch this file. I don't have to run the tests actually." Nick Nisi / Zack Proser (WorkOS), https://youtu.be/AgBAOXVxt4A?t=1652
- [observed] "oh there are lint rule errors let me remove the code blocks" Greg Pstrucha (Sentry), voicing the agent, https://youtu.be/E3KbFLAGD6A?t=556
- [observed] "I got to like a 100% or close to 100% of test coverage. But the actual tests are bad." Greg Pstrucha, https://youtu.be/E3KbFLAGD6A?t=893
- [observed] "the first run that I got it hit 99.9% and then I looked at the logs and I was cheating." YC Paper Club presenter, https://youtu.be/n9xKblqyQ28?t=1868
- [observed] "it quietly slipped emergency recovery into the allow list. A self authorizing exception that nobody asked for." Andrew Orobator (Reddit), https://youtu.be/6MudaeKdBSk?t=808
- [observed] "it was only good enough to merge about half of the time. Uh, and the failures weren't about correctness because obviously the PRs were passing all of the tests. They were about code quality and they were about changes that quietly broke other code, things external to the test suite." Laurie Voss citing a maintainer study, `[vendor]` Arize, https://youtu.be/_mi3alkqy4s?t=436
- [observed] "they can easily write tests for any given API but much like humans they fail to write the right tests." Jonathan Kelley (Dioxus), https://youtu.be/H7vFrcNWXzs?t=892

**Workarounds people use.** Each one takes the oracle out of the agent's hands.
- [observed] "always ask them to have unit test but never told them to run it, run it yourself so when something break, you know why it break, it doesn't have chance to intentionally break guidelines by adjusting test result instead of fixing the bug." u/raralala1, score 1, https://www.reddit.com/comments/1wzic5u/_/peoh9bn/
- [observed] "it works pretty well if the agebt imlementing runs in a different session than the test writing one. just add guard rails to deny editing tests when implementing if you want to add extra saftey." u/chrismo80, score 2, https://www.reddit.com/comments/1ww5ppy/_/pdhvs3h/
- [observed] "I don't allow it to write massive lines of code. I generally know what methods I want in a class. ... And I generally have handwritten automated tests ready to go" u/throwaway_0x90, score 4, https://www.reddit.com/comments/1tk6hg6/_/on6hilk/
- [observed] "1) get test coverage in place and more robust without the AI being allowed to touch the underlying code 2) let the AI make minor code modifications to make the code more testable ... 3) after that safety net is in place, direct the AI to change the code structure" u/NotEasyBeingGreener, score 1, https://www.reddit.com/comments/1tk6hg6/_/on6lu6y/
- [observed] "I'm probably going to delete all AI generated tests in that module in no time lmao." u/Wonderful-Habit-139, score 2, https://www.reddit.com/comments/1uxzx4w/_/oxzni62/
- [observed] "we don't rely on the the measurements that the agent makes ... the system like deterministically reruns um the this pair benchmarks um after each candidate is proposed" Perfloop founder, `[vendor]`, https://youtu.be/gbFR5DOnnSI?t=1542
- [observed] "I stopped reviewing the code and started reviewing the proof. 'Done' is a claim. ... My agent once marked a whole photo pipeline 'complete.' It had done nothing. Cost me 4 days. Now: no artifact, no merge." u/AlarmedAvocado7279, score 3, https://www.reddit.com/comments/1x17k3i/_/peruf8a/ (r/ChatGPTCoding, specific enough to keep)

## 3. Stacked AI verification still misses the systemic bug

People who already run the full stack (TDD skill, second-model review, critic agents) report that it catches local defects and lets through the one that matters. Some of the strongest evidence in the set, because the people describing it have already paid for every layer.

- [observed] "10 minutes ago I caught a command loop that would've deleted every SQS message before even using it. ... This was after running the latest and greatest frontier model in a TDD skill mode that took an enormous amount of tokens and validated all of its output. Then I ran a review against it with a different agent ... Ran another validation on it ... Then I read the code. ... Until I can go a month without AI trying to push code out that will cause a catastrophic bug, I'm reading the code." u/Equivalent_Head_4803, score 2, https://www.reddit.com/comments/1wql3g2/_/pdhyryw/
- [observed] "He hallucinated a command line flag that didn't exist and then built an entire plan around it which specialist agents then verified, added suggested test cases, edge cases, and said was a great approach" u/HoratioWobble, score 6, https://www.reddit.com/comments/1rzq738/_/obnop3q/
- [observed] "Multi-model LLM review on top: sentinel does one pass, verifier does another with a different model. The LLM passes let architectural issues through. Catch the local stuff, miss the systemic stuff." u/mrtrly (solo, "81 PRs a day"), score 1, https://www.reddit.com/comments/1taxgzm/_/olcu2p3/
- [observed] "Autonomous-with-critic-agent moves the boundary into the agent's own reasoning, which is the part with no audit trail. When it works it feels like a 10x; when it fails you find out three commits later because the critic agreed with the wrong choice." u/skil-lock (senior engineer, a year on Claude Code), score 2, https://www.reddit.com/comments/1tlclik/_/onyzh51/
- [observed] "I've seen agents make up problems and create all sorts of complexities or even introduce bugs due to agentic review loops ad nauseum." @michaelharrington6698, 36 likes, https://youtu.be/Ib5GBkD555M (comment)
- [observed] "dealing with cavitation of an agent where it fixes something, goes back, gets another code review, and has to kind of like fix backwards because the quality of the comment was low." Uber uReview team, https://youtu.be/EL123UNokkI?t=740
- [observed] "I've had an agent run the exact failing command, paste a green result, and still be wrong: the race only shows under load, the timestamp only breaks in UTC+7, the bad row only exists in prod. The run proved the code, not the bug." u/Quick_Dog_7971, score 3, `[bot-suspect]`, https://www.reddit.com/comments/1wwjgvu/_/pe0j8j8/
- [assumed] "Two models reaching the same design isn't really independent evidence when they share the same codebase, common training patterns, and the same prompt framing." u/Gleb_SV, score 2, https://www.reddit.com/comments/1vvj60z/_/p5omr7o/
- [observed] "The 'why did you do it this way' question doesn't work on agents. They'll happily invent a reason that sounds great. So I review backwards from how I'd review a human: I don't ask why, I ask what breaks." u/boxing-boxing, score 1, https://www.reddit.com/comments/1x2augi/_/pf12jx4/

## 4. Switching back: from "agent authors" to "I author, AI reviews"

Most switching stories run one way. People went all in on autonomy, hit a wall, and pulled back to writing the code with the agent as reviewer or pair. The pull is understanding and control. The push is debugging code they didn't build.

- [observed] "I tried a home project in the wrote no code, use plan mode as much as possible to nail down the requirement, use sub agents to build it, unit tests. Etc. ... it still painted itself into a corner. ... The core engine needed a rewrite to move to a lock free design. ... This time I'm writing the code but have Claude do the code reviews. The results are much better but take longer. I was all in, now I'm using it like a pair programmer." u/detroitsongbird (programming "since before Java"), score 111, https://www.reddit.com/comments/1tlclik/_/oneo816/
- [observed] "For the version that was entirely built by agents I really didn't learned anything "about the code", which sucked when I did actually try to debug it. It was an unfamiliar code base." u/detroitsongbird, score 6, https://www.reddit.com/comments/1tlclik/_/onff863/
- [observed] "Every time I've tried planner → executor → critic agent chains, I spend more time correcting drift than writing code. Slower, controlled iteration has felt way more reliable." u/Nataliashayk, score 35, https://www.reddit.com/comments/1tlclik/_/onenmoc/
- [observed] "My three year honeymoon with ai coding tools is over. I'm back to fully wring all come myself. ... being a verification layer for machine-generated code felt terrible and demoralizing. ... Additionally I no longer review AI generated PRs in my company." u/Evgenii42, score 1 (OP of a 615-score post), https://www.reddit.com/comments/1ub3uct/_/otl15qs/
- [observed] "I've tried the 'parallel agents working on multiple tasks' thing ... The agents did self review and their work was perfect from a UI and app perspective. The feature worked. / The code was complete spaghetti." u/Jessica___, score 3, https://www.reddit.com/comments/1v3lfh5/_/oza0a6j/
- [observed] "our new senior let Claude loose on it and it was a damn disaster. ... I had to tell him he's no longer allowed to use AI to generate or modify code. At all. The funny thing is he's not any slower at all without AI" u/unconceivables (team lead, strict C# codebase with custom Roslyn analyzers), score 2, https://www.reddit.com/comments/1pliwzz/_/ntwcptp/
- [observed] "I'm playing roulette and only about 1 in 5 outputs are acceptable, and if I'm specific enough to ensure it's right the first time, I spent more time instructing than doing it myself." u/ianpaschal, score 35, https://www.reddit.com/comments/1sc998r/_/oe944z3/
- [observed] "I found that if I outsource the entire problem-solving process, I end up spending just as much time validating and correcting it. Writing the first version myself forces me to build the mental model" u/Spiritual-Jello-5193, score 2, https://www.reddit.com/comments/1uzfvrq/_/oybd1jx/
- [observed] "I've had some success with an approach where you write the first pass yourself, but sprinkle TODO comments liberally in place of any bits of code you want the AI to write." u/GeoffW1, score 8, https://www.reddit.com/comments/1uzfvrq/_/oy95vhq/
- [observed] "Please please read the code. We tried not reading the code for like six months. It did not end well." A practitioner, relayed by Laurie Voss, `[vendor]`, secondhand, https://youtu.be/_mi3alkqy4s?t=1116
- [observed] "in July 2025, we tried this. We went full lights off" Dexter Horthy, `[vendor]` HumanLayer, https://youtu.be/Ib5GBkD555M?t=489. He later says "for now, we should probably read the code" https://youtu.be/ix1qQK1IvmA?t=520

**Counter-stories, toward more autonomy.** Mostly vendors, and one comment that can't be verified.
- [observed] "Mandatory code review before it gets to Maine. Yeah, it's dead." Quinn Slack, `[vendor]` Amp, https://youtu.be/hvwtHZ5E27c?t=403
- [observed] "I havent written a single line of code in months." @peterj.2114, https://youtu.be/6W_-YWHKwZ4 (comment)
- [observed] "I freelance as a contractor and AI has allowed me to double my client base and take on jobs in non-related tech stacks ... I don't think I can go back to non AI coding." u/FishSpoof (27+ years coding), score 2, https://www.reddit.com/comments/1wzic5u/_/pet00ml/

## 5. Losing the model of your own system

The damage people name is not bad code. It is no longer knowing what the system is meant to do, so they can't tell a right answer from a wrong one.

- [observed] ""let it make too many architectural decisions, then stack fixes on fixes." That's exactly where my projects die. Not because the model writes bad code, but because I stopped being able to say what the system is supposed to do, so I couldn't tell a wrong answer from a right one anymore." u/julesbuildstuff, score 4, https://www.reddit.com/comments/1w3iokc/_/p71a6v1/
- [observed] "It was a greenfield project. I built it all with AI. ... its subsystems have been crashing more ... I feel like I've coded myself into a box." u/frompadgwithH8, score 2, https://www.reddit.com/comments/1wu1tzt/_/pd4zey6/
- [observed] "Institutional knowledge went absolutely downhill. No one on my teams knows in depth what our code does. Supervising the agents is hard because we never took the time to actually learn what is happening." Thread OP, quoted by u/EmeraldStorm089, score 4, https://www.reddit.com/comments/1v3lfh5/_/oznz0cj/
- [observed] "My boss instructed me to go full LLM on a huge codebase ... and then got frustrated at me when I couldn't answer some of his questions on the fly." u/WalidfromMorocco, score 7, https://www.reddit.com/comments/1sm9ha6/_/ogchpty/
- [observed] "I really don't like using it to write code I don't understand since my knowledge of the code base is already poor it means I can't review it's output with any confidence." u/Clawtor (legacy auction platform with optimisation code), score 3, https://www.reddit.com/comments/1v3lfh5/_/oz83cbc/
- [observed] "I sent a PR to my coworker that I thought I had read the thing. I thought I understood, and she asked me the most basic question. And I was like, "Oh, no. I don't know." ... I had fooled myself." Geoffrey Litt (Notion), https://youtu.be/WkBPX-oDMnA?t=611
- [observed] "my rule is I don't send code to uh others on my team to review unless I can pass the quiz about what my agents wrote. ... It really is shocking the number of times this has caught me" Geoffrey Litt, https://youtu.be/WkBPX-oDMnA?t=641
- [observed] "It's just not feasible for any one on my team to go back to the "old way" as the monolith mutates like crazy ... it creates such a ramp up time to reread the code as it becomes increasingly unrecognizable." u/iComplainAbtVal (company "pretty much requires devs to use Claude code"), score 1, https://www.reddit.com/comments/1wzic5u/_/pehv3mk/
- [observed] "Even small drift, which seems to always happen, compounds over many PRs. ... agents will pick up that as an example and drift further and further until the code is just a mess." u/SlightlyLethalDev, score 3, https://www.reddit.com/comments/1tlclik/_/onf8w3l/

## 6. Decisions get lost between sessions, so everyone builds a ledger

A workaround cluster. People reinvent decision records, status fields, supersedes pointers and spec-change gates by hand, each slightly differently. One commenter describes numbered spec items, invariants and decisions, with hooks blocking spec edits that have no decision record.

- [observed] "I ran a DECISIONS.md for about a year and hit the same wall. Works great, then somewhere around 40 entries the model starts skimming instead of reading, and a reversed call sits next to a live one and it picks whichever it saw last. ... What fixed it for me was making each decision its own record instead of a line in a file. Status field, supersedes pointer." u/tehmadnezz, score 4, `[vendor]` (builds a tool for this), https://www.reddit.com/comments/1usuzgo/_/owv44p5/
- [observed] "Write invariants for the spec and make the agent write tests for them. ... Code spec items like S1.1 would be the first. Code invariants like I1 would be the first. Code decision items like D1 is the first decision that changed the spec. ... Use agent hooks and/or githooks that monitor changes to the spec directory. And only allow spec changes with an accompanying decision record." u/Technical-Athlete-9 (works with clients), score 4, https://www.reddit.com/comments/1wygsaf/_/pe50n3w/
- [observed] "Create a folder for your decisions log, add a readme and an index. In the index, the agent should write short blurb on the decision and then a link to a more detailed md" u/DLuke2, score 12, https://www.reddit.com/comments/1usuzgo/_/owrhhui/
- [observed] "Asking the session to save notes at the end does not always work because the session itself decides if it does it. What worked for me is putting it on the commit instead. Nothing counts as done without a short report of what changed and why" u/SetAdministrative502, score 2, https://www.reddit.com/comments/1voyas4/_/p3zm1x1/
- [observed] "Wrong docs are worse than no docs because the agent has no way to know they are dead." u/bbangchikimong_dev, score 6, https://www.reddit.com/comments/1wbemkj/_/p8rqn3m/
- [observed] "a doc that says what NOT to touch. the agent kept refactoring things that were deliberately ugly for reasons that were not in the code" u/bbangchikimong_dev, score 3, https://www.reddit.com/comments/1wbemkj/_/p8q0qo5/
- [observed] "But what we do today is we create a change, we create a pull request, and then we throw away the prompts." Ankit Jain, `[vendor]` Aviator, https://youtu.be/YgEv7IQzGdM?t=367
- [assumed] "the difficult failure mode is memory poisoning rather than forgetting. One mistaken agent write can now influence every tool and machine. ... can a user audit and roll back all memories produced by one session?" u/Master-Bug6904, score 2, https://www.reddit.com/comments/1v3mhkg/_/oz4q168/

## 7. Mandated spec-driven development: a long spec, a long run, and assumptions still made

Where spec-driven development is imposed from above, people describe very detailed specs, multi-hour runs, and leads reviewing plans that don't match reality. The agent still makes the important assumptions itself. Most went back to small chunks.

- [observed] "My organization has been mandated to follow spec-driven development, and by and large, everybody I talk to is miserable. ... the specs need to be shockingly detailed in order to get decent results. ... sometimes extremely time-consuming (2+ hours) - and you'll be left with hard decisions about whether to iterate on the spec and re-run, or to start fiddling directly with the results." u/Krom2040, score 9, https://www.reddit.com/comments/1t0q8xl/_/ojb74pm/
- [observed] "now the idea is that leads and seniors now need to review incredibly detailed plans created by LLM prior to any work being done, and it's all just waterfall. But somehow worse, because these detailed plans are also often totally divorced from reality." u/Krom2040, score 3, https://www.reddit.com/comments/1t0q8xl/_/ojbph9a/
- [observed] "even with a spec it's not sufficiently detailed and even worse the AI typically just makes a bunch of assumptions for important decisions. ... spec driven development just delays the pain of making and clarifying those decisions until the end of the process" u/JChuk99, score 2, https://www.reddit.com/comments/1t0q8xl/_/ojbpc91/
- [observed] "I've tried it twice so far and had middling results and each time had to go back and fix it myself." u/doomslice, score 36, https://www.reddit.com/comments/1t0q8xl/_/ojasola/
- [observed] "None of that is gonna fly for the billing systems I work on, so now we're just left with a problem worse than building it out in little reviewable chunks" u/codescapes, score 10, https://www.reddit.com/comments/1t0q8xl/_/ojb1na1/
- [observed] "The "silently ignoring parts of the spec" thing is what gets you. It fails quietly and you find out when a client hits it six months later. ... Writing that down accurately requires someone who already knows it." u/Senior_tasteey (brownfield), score 3, https://www.reddit.com/comments/1t5l65d/_/okaur55/
- [observed] "My boss has developed a custom ChatGPT to do this and has now demonstrated 3 times to evwr increasing audiences that this has solved all of our problems and developers can implement anything from the AI generated spec in 5 minutes." u/siliconsmiley, score 2, https://www.reddit.com/comments/1t0q8xl/_/ojbmskl/
- [assumed] "Writing properties is hard. Nine out of 10 times, they do not say what you think they say." Dominik Tornow, `[vendor]` Resonate, https://youtu.be/C6caB-UiN-8?t=959
- [assumed] "It just turns out you never really understood what you meant by your specification." InfoQ panellist, https://youtu.be/u27KYW4Gg0o?t=1480

## 8. Reviewing other people's agent output, under org pressure

The reviewer at the end of someone else's agent. Volume is the complaint, but the deeper one is that review comments get fed back to the agent, so the reviewer ends up arguing with a model.

- [observed] "when I leave comments he's feeding them into the AI and pasting back the response to me. Spent a whole day last week having a PR comment argument ... with him (AI) asserting that the component system ... doesn't have the capabilities that I am in fact linking him to in its documentation." u/404errorlifenotfound, score 9, https://www.reddit.com/comments/1ub3uct/_/oszazdm/
- [observed] "AI code it -> AI review it -> AI apply code review. Last month we had a 200K USD hit by a bug that an human would easily catch it." u/First-Inspection-597, score 1, https://www.reddit.com/comments/1ub3uct/_/otrk778/
- [observed] "My director instructed us to have Claude write tests, code, open PRs, and review PRs. We were basically just overseers. I hear similar stories from friends across the industry." u/code_isLife, score 26, https://www.reddit.com/comments/1uzfvrq/_/oy7u005/
- [observed] "Why is my boss not holding people accountable for the huge PRs? Because he's the one making them and self reviewing them with AI too." u/big-hogs, score 13, https://www.reddit.com/comments/1wu7e00/_/pd6oj85/
- [observed] "For us PR approvals doesnt mean you have fully vouched for the code in the request. Its more of a "yeah that generally makes sense" sanity check ... If they fuck up more than once ... they go on rubber stamp probation until they change." u/mamaBiskothu (senior-only team), score 24, https://www.reddit.com/comments/1tf5jq1/_/om8k57i/
- [observed] "It is all Claude slop and he can rarely explain the implementation or give any meaningful answers to my questions." u/SupplySideTanaka (senior SWE, low-latency distributed systems), score 2, https://www.reddit.com/comments/1wbfjtd/_/p95xsca/
- [observed] "Some individual contributors are merging 60 PR releases per cycle, which is about a week. ... The volume alone makes it difficult to believe that anybody is thoroughly understanding validating these changes." Listener question read on Syntax, https://youtu.be/6tZ_R4m_Oc4?t=429
- [observed] "We've implemented a trust system; Only certain engineers can merge PRs ... It's stopped the flow of breaking issues into the application, but the slop piles ever high." @dethcx22, 17 likes, https://youtu.be/6tZ_R4m_Oc4 (comment)
- [observed] "At my company we have an AI native team ... and they're producing a tremendous amount of stuff bit also hotfixing 2 or 3 times a sprint." u/turningsteel, score 4, https://www.reddit.com/comments/1wql3g2/_/pd4gdh9/
- [observed] "whatever speed improvement they perceive is often because they've externalized things onto teammates." u/annoying_cyclist, score 2, https://www.reddit.com/comments/1v3lfh5/_/oz7rrll/

## 9. Hard domains: thin, but all one direction

Concurrency, distributed systems, embedded, numerical and performance work. Little testimony, and three targeted YouTube searches for concurrency and database experience reports came back empty. Nobody in the Reddit set describes fuzzing, property tests or simulation with agents. Everything that did turn up says the same thing: the agent has no feel for invariants it can't test.

- [observed] "If the feature crosses service boundaries, or generally involves distributed systems or state management, the LLMs solution usually won't come close to working in production." u/Napolean_BonerFarte, score 3, https://www.reddit.com/comments/1t0q8xl/_/ojb7bde/
- [observed] "It did a decent job at a small CRUD tool, but was very unproductive at deterministic embedded applications." u/DualActiveBridgeLLC, score 5, https://www.reddit.com/comments/1pliwzz/_/nttqjc0/
- [observed] "A coverage ratio was dividing a per-share number into a total. Both inputs were correct and the arithmetic ran clean. ... Outside-in testing can't catch that, because whoever writes the acceptance criteria writes them in the same wrong unit. ... We label quantities as per-share or total and let a compiler pass follow them through the arithmetic." u/EducationalFishing56, score 4, https://www.reddit.com/comments/1vjm0nn/_/p2n8oty/
- [observed] "no matter how I try to emphasise we have a table in our DB with billions of rows that therefore **must** only be queried using existing indexes the generated SQL is just like 'nah bro full table scan let's go'." u/codescapes, score 9, https://www.reddit.com/comments/1uzfvrq/_/oy9hqv6/
- [observed] "an LLM will confidently tell you that no, it this absolutely is not a problem. ... broke it out and got a 500x performance improvement" Oxide and Friends guest, https://youtu.be/RdH7oQ1ddcA?t=3782
- [observed] "We are checking whatever you're checking. So we we just provide the engine to make very unlikely thing happen. But then it's up to you to to decide what to check and what is right and wrong." Marco Primi, `[vendor]` Antithesis, https://youtu.be/1eVkT-ZnKC8?t=3379
- [observed] "That information is forbidden to the algorithm. But it is incredibly useful to the agent." Dominik Tornow, `[vendor]` Resonate, on exposing simulator ground truth to an agent designing a distributed algorithm, https://youtu.be/C6caB-UiN-8?t=1673
- [assumed] "AI tends to produce inaccurate comments/docs and spot-fix individual problems rather than changing the architecture, so it actively works *against* this effort to prove invariants rather than stochastically sampling them." u/hiddenhare, score 7, https://www.reddit.com/comments/1vjm0nn/_/p2o9fo7/
- [assumed] "AI works way better if you have some combination of determinism, closed-world assumptions, or rigid specifications that are easy to automatically test preferably with an oracle." u/psyyduck, score 2, https://www.reddit.com/comments/1vjm0nn/_/p2nm3io/

## 10. Running agents in parallel and unattended

The people furthest along run several sessions at once or overnight. Their complaints are coordination problems, not code quality: shared state, ports, staging collisions, and their own fatigue.

- [observed] "a worktree isolates files, not state, and a session running migrations is editing something every other session thinks it owns. ... The release rule that made it stick for me: no working session gets deploy rights." u/Easy-Purple-1659, score 3, https://www.reddit.com/comments/1x23pim/_/pezms31/
- [observed] "if a session reads the registry and then writes its claim, sooner or later two sessions both see the simulator as free. What fixed it for me was making the claim one atomic step." u/kaijurules, score 2, https://www.reddit.com/comments/1x23pim/_/pf05fir/
- [observed] "I let the agent fan out as needed, but apply a fairly strict pipeline of sessions: research, plan, plan review, implement, code review, close-out." u/wardrox, score 6, https://www.reddit.com/comments/1v3lfh5/_/oz8d17b/
- [observed] "it's much better with short sessions. Each session produces a tonne of irrelevant context, which is effectively compiled/compacted into its final report ... A fresh session for review isn't biased by previous sessions." u/wardrox, score 2, https://www.reddit.com/comments/1v3lfh5/_/p03morb/
- [observed] "I have fully adapted to never opening an IDE, and having 2-3 agents go at it. ... It's a lot more tiring than just doing things myself, but also a lot faster per unit of work" u/eloel-, score 4, https://www.reddit.com/comments/1tlclik/_/onfz1v1/
- [observed] "I can eventually, maybe, build a system or harness incorporating something akin to values and knowledge of what I care about ... And then the harness ships an update, or the models change, and everything falls apart again." u/SansSariph, score 2, https://www.reddit.com/comments/1wu1tzt/_/pd4mvzp/

## 11. Capability aspirations

What people say they are trying to get good at, or wish existed. Thin and partly vendor-voiced. Most of it is checking agent work by some means other than another model.

- [assumed] "I feel planning is absolutely necessary but maintaining the plan as a free form text (.md files) is not cutting it. we need deterministic tools to ensure we are on track" u/njinja10, score 2, https://www.reddit.com/comments/1tlclik/_/onkz7jp/
- [assumed] "Documenting user stated intent in different ways, that don't get compressed. ... Turning my refinement of the code (I do not let AI structure how it pleases) into actionable, re-usable restraints." u/RandomPantsAppear, score 6, https://www.reddit.com/comments/1tlclik/_/onfvq5o/
- [assumed] "With LLM-produced code, I can do none of those things; the only option left available to me is to read the code." u/YakaryBovine, on how trust in a library is normally earned, score 2, https://www.reddit.com/comments/1vvj60z/_/p6473wa/
- [assumed] "And maintainability has no fast oracle." Dexter Horthy, `[vendor]`, https://youtu.be/ix1qQK1IvmA?t=367
- [assumed] "The problem of specifying what you want to an agent is still an open one." Alex Krentsel, https://youtu.be/5lFD-34dhqE?t=2487
- [assumed] "effectively using Claude requires supervision, and supervising Claude requires the very coding skills that may atrophy from AI overuse." u/creaturefeature16 quoting an Anthropic study, `[vendor]` (links own article), score 13, https://www.reddit.com/comments/1sc998r/_/oe9bc72/

---

## Suggestions

Everything below is interpretation and is separate from the evidence above. The human writes the personas.

### Segments, by behaviour

1. **The oracle builder** (clusters 1, 2, 3, 6, 9). An experienced IC accountable for a system where failure is costly: billing, storage, infra, distributed state. Still uses agents heavily. Has learned the hard way that prose rules drift and that another model's review is not independent, so moves every constraint they can into deterministic checks and keeps the rest in their head. Wants the agent to do the grind without lowering the bar. u/Whitchorence, u/pylin_, u/CheeseWeezel, Adzic, u/Technical-Athlete-9, u/Equivalent_Head_4803 and u/EducationalFishing56 behave like this. `[observed]` as a behaviour; `[assumed]` that they would adopt a packaged method rather than keep their own.
2. **The retreater** (clusters 4, 5). Went all in, debugged an agent-built system they didn't understand, and pulled back to authoring by hand with AI as reviewer or pair. Values understanding and the craft. Pays for it in speed and is often under management pressure to go back. u/detroitsongbird, u/Nataliashayk, u/ianpaschal, u/Evgenii42.
3. **The swamped reviewer** (clusters 7, 8). A tech lead or senior at the end of other people's agents, under a mandate they didn't choose. Doesn't run the loop. Absorbs its output, argues with pasted model replies, and gates merges by trust tier. u/404errorlifenotfound, u/Krom2040, u/mamaBiskothu, @dethcx22.
4. **The fleet runner** (cluster 10, plus the counter-stories in cluster 4). Two to five parallel sessions, no IDE, PR count as the metric, review treated as optional. Includes most of the vendor voices. u/eloel-, @peterj.2114, Slack.
5. **The mandating manager** (clusters 7, 8). Demos a custom GPT to growing audiences, rewrites the project over a weekend, self-reviews with AI. Seen only through the eyes of the people under them.

### Recommendation

One primary: **the oracle builder**. It's the only segment whose existing workarounds are build-method's mechanisms in rough form: deterministic gates, protected tests, decision records with status, short fresh sessions, and a human who still owns what "correct" means. Clusters 1 to 3 show they've already paid for the failure the method addresses. They aren't shopping for permission to stop reading code. A fair wind for this one, arr.

Two secondaries:
- **The retreater.** Build-method has to win them back by showing that autonomy and keeping the mental model can coexist. Replay is the bridge, and their evidence is already in the replay research. If the method can't serve the retreater, it isn't serving the primary either, because the oracle builder is one bad incident away from becoming a retreater.
- **The swamped reviewer.** They don't run the loop, but they receive its output. Build-method's handover artefacts (replay guide, scraps, the decision ledger) are what they would read. Write for them at the handover edge only.

Anti-personas:
- **The fleet runner.** Optimising for PR count and dropping review is what build-method refuses to do. Serving them means removing the replay and the oracle ownership.
- **The mandating manager.** Wants a spec-in, code-out process with no human in the build. The SDD misery evidence shows how that lands on the people underneath.
- **Non-coders building through agents** (u/troggle19 "for my non-coder brain"; Ramp's "a thousand of those PRs ... submitted by a non-engineer", https://youtu.be/ZG8Mf3P9xzI?t=504). Out of scope, matching the senior-only scope of Human Replay.

### Things the evidence suggests checking in the skills

- People already hand-build what the `celeriant-db-bots` decision ledger does (u/tehmadnezz's status and supersedes, u/Technical-Athlete-9's S/I/D numbering with hooks). It's the strongest sign that a ledger skill in build-method would land, and it's the open item in `todo.md`.
- Workarounds converge on taking the oracle away from the implementer: freeze the tests, deny edits, run the tests yourself, rerun benchmarks outside the agent. That supports making oracle protection a hard control, not a soft rule.
- Cluster 3 is the evidence against leaning on adversarial review. The stacked-review stories miss systemic bugs. The adversarial reviewer stays useful for eliminating hypotheses, but the method should say plainly that it is not independent evidence.
- Cluster 7 warns against `goal.md` turning into a mandated spec. Scout spikes and an amendable goal are the difference, and they should stay visible in the method's description.
- The hard-domain gap (cluster 9) is where the method's DST and chaos layers are most distinctive, and also where outside testimony is thinnest. That's a reason to publish the Celeriant evidence rather than wait for others to describe the need.

### Open questions this evidence can't answer

- Do oracle builders want a packaged method, or only the pieces? Every workaround here is homegrown and fitted to one codebase.
- How big is the oracle-builder segment against the fleet runners? Reddit complaint threads over-sample the unhappy. Vendor talks over-sample the confident.
- Does the retreater come back if replay makes the agent's output theirs, or is the pull back to hand authoring about enjoyment, which no method fixes? u/Evgenii42 cites mental health, not quality.

---

## Provenance

### Reddit (Arctic Shift, 2026-10-12)

| Thread | Subreddit | Title (removed titles described from comments) | Comments |
|---|---|---|---|
| 1tlclik | ExperiencedDevs | Claude Autonomous Coding: Discussion | 62 |
| 1t0q8xl | ExperiencedDevs | Moving towards specs-driven development, your thoughts? | 65 |
| 1v3lfh5 | ExperiencedDevs | [removed] adoption levels, multi-agent, institutional knowledge | 138 |
| 1vjm0nn | ExperiencedDevs | [removed] understanding a codebase with AI | 152 |
| 1wql3g2 | ExperiencedDevs | [removed] not reviewing code | 792 |
| 1uzfvrq | ExperiencedDevs | [removed] writing the first pass yourself, AI as reviewer | 141 |
| 1ub3uct | ExperiencedDevs | [removed] "Over reliance on AI" | 224 |
| 1wzic5u | ExperiencedDevs | [removed] "My three-year AI honeymoon is over" | 254 |
| 1wteiid | ExperiencedDevs | [removed] tech lead, senior feeds review comments to Claude | 252 |
| 1wu1tzt | ExperiencedDevs | [removed] handing codebases to agents | 291 |
| 1wu7e00 | ExperiencedDevs | [removed] "a lot of you don't have an AI ..." | 293 |
| 1u1tgjq | ExperiencedDevs | [removed] biggest problem with AI | 248 |
| 1vvj60z | ExperiencedDevs | [removed] shipping over-engineered agent code that passes tests | 181 |
| 1uxzx4w | ExperiencedDevs | [removed] E2E vs RTL, AI tests | 121 |
| 1wbfjtd | ExperiencedDevs | How is the code quality in expensive frontier LLM plans? | 364 |
| 1wbemkj | ExperiencedDevs | [removed] what did you add before agents got useful | 47 |
| 1tf5jq1 | ExperiencedDevs | Is the norm now that PRs are basically rubber stamps | 118 |
| 1twyt87 | ExperiencedDevs | How are you guys doing end to end and regression testing on AI-written code? | 47 |
| 1rzq738 | ExperiencedDevs | What tools and techniques are you using to verify AI-generated code before it hits production? | 85 |
| 1tk6hg6 | ExperiencedDevs | Devs using AI coding agents: where does trust break in your workflow? | 22 |
| 1taxgzm | ExperiencedDevs | How do you scale yourself out of being the human review gate without losing the quality it provides? | 9 |
| 1sc998r | ExperiencedDevs | My AI workflow seems to be the opposite of what the industry is encouraging, but I don't care. | 40 |
| 1s3fxhj | ExperiencedDevs | AGENTS.md not recommended for use in AI Assisted Programming | 24 |
| 1pliwzz | ExperiencedDevs | Stanford study confirms that adding AI to spaghetti code just creates faster spaghetti | 93 |
| 1t5l65d | ExperiencedDevs | AI in brownfield codebases is a fundamentally different discipline | 37 |
| 1sm9ha6 | ExperiencedDevs | Instruction-Driven Development vs Outcome-Driven Development vs Vibe Coding | 20 |
| 1sijxoq | ExperiencedDevs | "Coping" with agentic workflow adoption | 24 |
| 1ox40ww | ExperiencedDevs | Agentic, Spec-driven development flow on non-greenfield projects | 93 |
| 1tecgvx | ExperiencedDevs | We had to change how we validate HMI code after AI started writing most of our code | 19 |
| 1usuzgo | ClaudeAI | I told Claude Code to keep a running log file of its own decisions | 33 |
| 1voyas4 | ClaudeAI | Solo founder building a complex app with Claude: how do you stop sessions from forgetting decisions | 22 |
| 1v3mhkg | ClaudeAI | Claude Code + persistent memory: my setup after CLAUDE.md stopped scaling | 8 |
| 1x2augi | ClaudeAI | What's the best way to review code written with Claude Code? | 28 |
| 1x23pim | ClaudeCode | Solo dev running 5+ Claude Code sessions in parallel | 17 |
| 1w3iokc | ClaudeCode | Is vibe coding actually hard, or are people just using AI wrong? | 79 |
| 1wnfj10 | ClaudeCode | claude code deleted a failing migration at 3am so the tests would pass | 12 |
| 1wci00g | ChatGPTCoding | Hot take: the agentic workflow is deeply wrong | 129 |
| 1wygsaf | ChatGPTCoding | AI coding tools solved writing code and replaced it with reading walls of text | 24 |
| 1x17k3i | ChatGPTCoding | How do you handle reviewing large amounts of AI-generated code? | 35 |
| 1wwjgvu | ChatGPTCoding | Coding agents say "fixed" when they mean "I changed the code" | 29 |
| 1ww5ppy | ChatGPTCoding | Isn't "rerun the tests until green" just grading the agent on its training set? | 20 |
| 1w76958 | cursor | Agent mode quietly made me a worse code reviewer | 14 |

Mined without usable quotes: 1tf2dw8, 1tils8z, 1wo4d8p, 1reiro1, 1txpneu, 1trwwza, 1rv1ut2, 1uhnn6o, 1w2ezng, 1wzwfsn, 1u89kv6, 1ugjujf. Empty searches: r/softwareengineering, r/codex. r/rust and r/programming returned mostly tool launches.

### YouTube (2026-10-12)

| Video | Channel | Title | Type | Source |
|---|---|---|---|---|
| 6mLYZF97oaU | GOTO Conferences | Spec-Driven Dev Is Back. But Not How You Think (Terhorst-North, Adzic) | conversation | fresh transcript |
| WkBPX-oDMnA | AI Engineer | Understanding is the new bottleneck (Geoffrey Litt) | talk | fresh transcript |
| 6tZ_R4m_Oc4 | Syntax | LGTM, Ship It: The AI Code Review Problem | podcast, listener Q&A | fresh transcript, comments |
| 6W_-YWHKwZ4 | Jo Van Eyck | You are Not Ready: Agentic coding in 2026 | practitioner commentary | fresh transcript, comments |
| Ib5GBkD555M | AI Engineer | Why Software Factories Fail (Dexter Horthy) | talk | signal-feed summary, comments |
| ix1qQK1IvmA | AI Engineer | Fighting Code Slop (Dexter Horthy) | talk | signal-feed summary |
| _mi3alkqy4s | AI Engineer | The Death of the Code Review (Laurie Voss) | talk | signal-feed summary |
| hvwtHZ5E27c | Latent Space | Orbs: Shifting Coding to Cloud (Quinn Slack) | interview | signal-feed summary |
| H7vFrcNWXzs | AI Engineer | Building ambitious software (Jonathan Kelley) | talk | signal-feed summary |
| E3KbFLAGD6A | AI Engineer | Stop Prompting (Greg Pstrucha) | talk | signal-feed summary |
| 6MudaeKdBSk | AI Engineer | Scale the Judgment, Not the Model (Andrew Orobator) | talk | signal-feed summary |
| AgBAOXVxt4A | AI Engineer | Lifestyles of the AI-Native (Nisi, Proser) | talk | signal-feed summary |
| n9xKblqyQ28 | Y Combinator | Why The Harness Matters More Than The Model | talk | signal-feed summary |
| gbFR5DOnnSI | The Geek Narrator | Agentic Performance Engineering ft. Perfloop | interview | signal-feed summary |
| C6caB-UiN-8 | TigerBeetle | The Prompt is the Platform (Dominik Tornow) | talk | signal-feed summary |
| 5lFD-34dhqE | Latent Space | Exo: Harnesses should see their own code and logs (Alex Krentsel) | interview | signal-feed summary |
| 1eVkT-ZnKC8 | CMU Database Group | Everything Has Bugs (Marco Primi, Antithesis) | talk | signal-feed summary |
| RdH7oQ1ddcA | Oxide Computer Company | Oxide and Friends: Emulating Oxide | podcast | signal-feed summary |
| u27KYW4Gg0o | InfoQ | The Future of AI: From Enterprise Adoption to Open Source Sovereignty | panel | signal-feed summary |
| EL123UNokkI | AI Engineer | Building uReview, Uber's Multi-Agent Code Review Engine | talk | signal-feed summary |
| YgEv7IQzGdM | AI Engineer | How to Kill the Code Review (Ankit Jain) | talk | signal-feed summary |
| ZG8Mf3P9xzI | Lenny's Podcast | The limiting factor (Geoff Charles, Ramp) | interview | signal-feed summary |

Also mined, not quoted here: whcfSGN6CAU, LlgiOCmFG_w, pqlWNihgdjI, 5Bn0xro2ol8, 7vn4WpqNpck, k2ClBT4aqAg, l0tlBS_BB74, BnxiqCCthZY, iuccfEQgIeY, hduV2Ayz25c, ya6520zh4pQ, fFIjrtH6qjc. Hard-domain discovery queries ("claude code concurrency distributed systems bugs", "claude code race condition deadlock rust async", "coding agents database internals experience talk 2026") returned nothing usable.

Raw miner output (about 270 quotes in all) sits in session scratch and is not kept. Every quote above was copied from it unchanged.
