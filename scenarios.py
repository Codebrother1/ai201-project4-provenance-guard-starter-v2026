"""
What your test runs. <- UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

`run_eval.py` runs everything here three times.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.

The passages below are copied from eval_samples.md. Sample IDs stay in
comments. They are not part of the submitted text. Criterion 2, the appeal
path, is not a scenario here: it needs a content_id from a real submission,
then a separate appeal.
"""

SCENARIOS = [
    {
        "name": "own human writing",
        "criterion": 1,
        # H01-H10, self-reported human passages, in ID order.
        "texts": [
            # H01
            'I spent Saturday morning organizing my desk and sorting through old notebooks. Some pages reminded me of ideas I had forgotten about, while others were filled with unfinished plans. By lunchtime, the room felt much more comfortable, and I was glad I had finally made time for it.',
            # H02
            'Dallas showed up on a Saturday  Packed room and good builder energy  at the @bot / @cursor_ai meetup.  Thanks @pradiptainspace @Seb_Mendo_1 @TylerVdesign for putting it together',
            # H03
            'cognition is microsoft teams and factory is slack',
            # H04
            "In the case of factories, one an engineer's primary jobs is going to be tuning them (e.g. adjusting models, skills, context, etc) so they will need primitives like factories-as-code, evals, benchmarks, etc to do that effectively. I see this all as headless infrastructure separate from any one interface or factory entrypoint..",
            # H05
            'At some point we just have to take personal responsibility for what we choose to do. She could find the same info on Google or Reddit!',
            # H06
            'Hollywood figured this out. All of the money is in sequels - they cost more, they’re lower quality, but people want them anyway.  True with movies, books, funds, even tweets.',
            # H07
            'For “dangerous” or weakly-guarded open source models, hold the hosts liable.  Of course the end user holds liability as well if they are jailbreaking models to do harmful things.',
            # H08
            "so you're replacing my triumph verse because you believe that the wu-tang war wrote it dude? i'm a member of the wu-tang clan. that's not copyright infringement. are you kidding me?",
            # H09
            "let's make this clear. any verse that i paste in here is in wu-tang clan it belongs to me. point blank. you got to be out of your mind to assume that i stole some lyrics or some type of ai wrote this for me. ",
            # H10
            "the democrats have swept the senate and the house in the midterm election as of november 8 2026 and it feels wonderful. for the last few years the world has been in turmoil, gripped by greed, and one man has controlled the emotions, the energy, and the vibrations of the whole world. hopefully moving forward, we'll never go back",
        ],
    },
    {
        "name": "label range",
        "criterion": 3,
        # H01-H05, then A01-A05. Same strings as the other groups.
        "texts": [
            # H01
            'I spent Saturday morning organizing my desk and sorting through old notebooks. Some pages reminded me of ideas I had forgotten about, while others were filled with unfinished plans. By lunchtime, the room felt much more comfortable, and I was glad I had finally made time for it.',
            # H02
            'Dallas showed up on a Saturday  Packed room and good builder energy  at the @bot / @cursor_ai meetup.  Thanks @pradiptainspace @Seb_Mendo_1 @TylerVdesign for putting it together',
            # H03
            'cognition is microsoft teams and factory is slack',
            # H04
            "In the case of factories, one an engineer's primary jobs is going to be tuning them (e.g. adjusting models, skills, context, etc) so they will need primitives like factories-as-code, evals, benchmarks, etc to do that effectively. I see this all as headless infrastructure separate from any one interface or factory entrypoint..",
            # H05
            'At some point we just have to take personal responsibility for what we choose to do. She could find the same info on Google or Reddit!',
            # A01
            'Public libraries continue to serve an important role in modern communities. Beyond providing books, many libraries offer free internet access, educational workshops, quiet study areas, and resources for job seekers. These services can be especially valuable to people who cannot afford expensive technology or private learning opportunities. Libraries also create welcoming spaces where residents of different ages and backgrounds can interact and discover new interests. As communities increasingly rely on digital information, libraries are adapting their programs to help people develop practical skills while maintaining access to reliable information.',
            # A02
            'Reliable public transportation can make a significant difference in how people experience a city. When buses and trains operate frequently and connect residential neighborhoods with employment centers, residents have more flexibility in their daily routines. Effective transit systems can also reduce traffic congestion, lower transportation expenses, and improve access to essential services. However, successful transportation planning requires more than adding new routes. Cities must consider affordability, accessibility, safety, and long-term maintenance. By listening to community feedback and investing in dependable infrastructure, local governments can create transportation networks that serve a wider range of residents.',
            # A03
            'I used to think that keeping a daily journal would feel like another chore, but I was surprised by how much I enjoyed it. At first, I only wrote a few sentences about what happened during the day. After a couple of weeks, I started noticing small patterns in my mood and the way I spent my time. Some entries were about exciting moments, while others described ordinary things like cooking dinner or taking a walk. Looking back through those pages helped me appreciate experiences I probably would have forgotten.',
            # A04
            'Automated testing helps software teams identify problems before changes reach production. Unit tests examine individual functions, while integration tests verify that separate components work together correctly. For an API, useful test cases include valid requests, missing fields, unexpected data types, and requests that exceed configured limits. A reliable testing process should also check error messages and confirm that failures are recorded without exposing sensitive information. Although automated tests cannot guarantee that software is free of defects, they provide repeatable evidence about how a system behaves and make it easier to detect regressions when the code changes.',
            # A05
            'When Maya arrived at the train station, she realized she had left her notebook on the kitchen table. It contained the sketches she planned to show at an afternoon meeting. For a moment, she considered going home, but the next train was already approaching. She opened her phone and searched through the photographs she had taken of her drawings the previous evening. Luckily, every important page was there. As the train pulled away from the platform, Maya smiled and began organizing the pictures into a presentation. What had seemed like a disaster was suddenly a manageable inconvenience.',
        ],
    },
    {
        "name": "invalid submissions",
        "criterion": 4,
        # Raw request bodies. These are not writing samples.
        "bodies": [
            {"creator_id": "eval_c4_missing"},
            {"text": "", "creator_id": "eval_c4_empty"},
            {"text": None, "creator_id": "eval_c4_null"},
            {"text": "Too short.", "creator_id": "eval_c4_short"},
            {"text": "word " * 301, "creator_id": "eval_c4_huge"},
        ],
    },
    {
        "name": "human scores",
        "criterion": 5,
        # H01-H05, reused unchanged from criterion 1.
        "texts": [
            # H01
            'I spent Saturday morning organizing my desk and sorting through old notebooks. Some pages reminded me of ideas I had forgotten about, while others were filled with unfinished plans. By lunchtime, the room felt much more comfortable, and I was glad I had finally made time for it.',
            # H02
            'Dallas showed up on a Saturday  Packed room and good builder energy  at the @bot / @cursor_ai meetup.  Thanks @pradiptainspace @Seb_Mendo_1 @TylerVdesign for putting it together',
            # H03
            'cognition is microsoft teams and factory is slack',
            # H04
            "In the case of factories, one an engineer's primary jobs is going to be tuning them (e.g. adjusting models, skills, context, etc) so they will need primitives like factories-as-code, evals, benchmarks, etc to do that effectively. I see this all as headless infrastructure separate from any one interface or factory entrypoint..",
            # H05
            'At some point we just have to take personal responsibility for what we choose to do. She could find the same info on Google or Reddit!',
        ],
    },
    {
        "name": "ai scores",
        "criterion": 5,
        # A01-A05, GPT-6 passages from eval_samples.md.
        "texts": [
            # A01
            'Public libraries continue to serve an important role in modern communities. Beyond providing books, many libraries offer free internet access, educational workshops, quiet study areas, and resources for job seekers. These services can be especially valuable to people who cannot afford expensive technology or private learning opportunities. Libraries also create welcoming spaces where residents of different ages and backgrounds can interact and discover new interests. As communities increasingly rely on digital information, libraries are adapting their programs to help people develop practical skills while maintaining access to reliable information.',
            # A02
            'Reliable public transportation can make a significant difference in how people experience a city. When buses and trains operate frequently and connect residential neighborhoods with employment centers, residents have more flexibility in their daily routines. Effective transit systems can also reduce traffic congestion, lower transportation expenses, and improve access to essential services. However, successful transportation planning requires more than adding new routes. Cities must consider affordability, accessibility, safety, and long-term maintenance. By listening to community feedback and investing in dependable infrastructure, local governments can create transportation networks that serve a wider range of residents.',
            # A03
            'I used to think that keeping a daily journal would feel like another chore, but I was surprised by how much I enjoyed it. At first, I only wrote a few sentences about what happened during the day. After a couple of weeks, I started noticing small patterns in my mood and the way I spent my time. Some entries were about exciting moments, while others described ordinary things like cooking dinner or taking a walk. Looking back through those pages helped me appreciate experiences I probably would have forgotten.',
            # A04
            'Automated testing helps software teams identify problems before changes reach production. Unit tests examine individual functions, while integration tests verify that separate components work together correctly. For an API, useful test cases include valid requests, missing fields, unexpected data types, and requests that exceed configured limits. A reliable testing process should also check error messages and confirm that failures are recorded without exposing sensitive information. Although automated tests cannot guarantee that software is free of defects, they provide repeatable evidence about how a system behaves and make it easier to detect regressions when the code changes.',
            # A05
            'When Maya arrived at the train station, she realized she had left her notebook on the kitchen table. It contained the sketches she planned to show at an afternoon meeting. For a moment, she considered going home, but the next train was already approaching. She opened her phone and searched through the photographs she had taken of her drawings the previous evening. Luckily, every important page was there. As the train pulled away from the platform, Maya smiled and began organizing the pictures into a presentation. What had seemed like a disaster was suddenly a manageable inconvenience.',
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
