#!/usr/bin/env python3
"""Source for data/elections/2026/profiles/in-state-comptroller-auditor-of-state.json (+ .md).

    python3 scripts/elections/profiles/in_state_comptroller.py

Citations are written as {key}. Editorial rules: data/elections/2026/profiles/README.md
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import build_profile  # noqa: E402

S = {
    "const": ("Indiana Constitution, Article 6", "Justia", "", "https://law.justia.com/constitution/indiana/art6.html"),
    "faq": ("What are the responsibilities of the State Comptroller?", "State of Indiana", "", "https://faqs.in.gov/hc/en-us/articles/16944033443860"),
    "depts": ("Comptroller departments", "Indiana State Comptroller", "", "https://www.in.gov/comptroller/departments"),
    "home": ("Indiana State Comptroller (news and releases)", "Indiana State Comptroller", "accessed 2026-10-10", "https://www.in.gov/comptroller/"),
    "dash": ("Indiana Comptroller Elise Nieshalla launches new dashboard tracking federal spending in state (press release)", "Indiana State Comptroller", "2026-05-18", "https://www.in.gov/comptroller/files/Indiana-Comptroller-Elise-Nieshalla-Launches-New-Dashboard-Tracking-Federal-Spending-in-State.pdf"),
    "intl": ("State Comptroller Nieshalla announces new international investment option protecting Hoosier retirement funds from China (press release)", "Indiana State Comptroller", "2026-08-14", "https://secure.in.gov/comptroller/files/State-Comptroller-Nieshalla-Announces-New-International-Investment-Option-Protecting-Hoosier-Retirement-Funds-from-China.pdf"),
    "sbf": ("State Board of Finance", "Indiana State Comptroller", "", "https://www.in.gov/comptroller/state-board-of-finance/index"),
    "title": ("Measures to modernize State Comptroller title signed into law (press release)", "Indiana State Comptroller", "2025-06-04", "https://www.in.gov/comptroller/files/Measures-to-Modernize-State-Comptroller-Title-Signed-into-Law.pdf"),
    "appoint": ("Elise Nieshalla named Indiana's new state comptroller", "IPM", "2023-11-28", "https://www.ipm.org/2023-11-28/elise-nieshalla-named-indianas-new-state-comptroller"),
    "wish": ("State Comptroller Elise Nieshalla launches bid for full term (WISH-TV)", "The Reporter", "2025-06-27", "https://readthereporter.com/state-comptroller-elise-nieshalla-launches-bid-for-full-term/"),
    "wfyi_launch": ("State Comptroller Elise Nieshalla launches reelection bid", "WFYI", "2025-06-26", "https://www.wfyi.org/news/articles/state-comptroller-elise-nieshalla-launches-reelection-bid"),
    "icc_launch": ("Nieshalla launches election bid", "Indiana Capital Chronicle (via IndyPolitics)", "2025-06-26", "https://indypolitics.org/?p=18355"),
    "about": ("About the Comptroller", "Indiana State Comptroller", "", "https://www.in.gov/comptroller/about-the-comptroller"),
    "debt": ("Indiana leaders push ALEC-backed national debt denunciation", "Indiana Capital Chronicle (via Yahoo)", "2026-02-17", "https://www.yahoo.com/news/articles/indiana-leaders-push-alec-backed-113026538.html"),
    "reserves": ("Comptroller Nieshalla & state budget leaders announce state reserves & surplus", "The Reporter", "2026-07-16", "https://readthereporter.com/?p=197611"),
    "wfyi_surplus": ("Indiana finishes fiscal year with significant surplus and $4 billion in reserves ahead of 2027 budget session", "WFYI", "2026-07-15", "https://www.wfyi.org/2026-07-15/indiana-finishes-fiscal-year-with-significant-surplus-and-4-billion-in-reserves-ahead-of-2027-budget-session"),
    "gas": ("Local communities get payments after gas tax suspension", "WFYI (via Indiana Public Radio)", "2026-07-21", "https://indianapublicradio.org/news/2026/07/local-communities-get-payments-after-gas-tax-suspension/"),
    "ipm_dems": ("Indiana Dems announce treasurer, comptroller candidates", "Indiana Capital Chronicle (via IPM)", "2026-05-28", "https://www.ipm.org/news/2026-05-28/indiana-dems-announce-treasurer-comptroller-candidates"),
    "wbet": ("Republican state convention report", "WBET", "2026-06-23", "https://wbetfm.com/view_article.php?id=4274"),
    "lp_slate": ("Libertarian Party of Indiana nominates 2026 slate", "IndyPolitics", "2026-03-21", "https://indypolitics.org/?p=19409"),
    "ipm_lp": ("Indiana Libertarians nominate Lauri Shillings for secretary of state", "Indiana Capital Chronicle (via IPM)", "2026-03-24", "https://www.ipm.org/news/2026-03-24/indiana-libertarians-nominate-lauri-shillings-for-secretary-of-state"),
    "wfyi_guide": ("2026 Voter Guide: Indiana State Comptroller", "WFYI", "2026-10-01", "https://www.wfyi.org/statewide/2026-10-01/2026-voter-guide-indiana-state-comptroller"),
    "ballotbrief_n": ("Elise Nieshalla", "The Ballot Brief", "accessed 2026-10", "https://theballotbrief.com/candidate/elise-nieshalla-in"),
    "in_list": ("2026 General Election Candidate List", "Indiana Election Division", "2026-09-22", "https://www.in.gov/sos/elections/candidate-information/"),
    # Bailey
    "idp": ("Indiana Democrats announce Jessica Bailey and Coumba Kebe as State Comptroller and Treasurer candidates", "Indiana Democratic Party", "2026-05-27", "https://indems.org/press-release/indiana-democrats-announce-jessica-bailey-and-coumba-kebe-as-state-comptroller-and-treasurer-candidates/"),
    "wfyi_bailey": ("Democrat Jessica Bailey accepts her party's nomination for Indiana comptroller (TheStatehouseFile)", "WFYI", "2026-06-06", "https://www.wfyi.org/statewide/2026-06-06/democrat-jessica-bailey-accepts-her-partys-nomination-for-indiana-comptroller"),
    "citizen_dems": ("DEMOCRAT HOPEFULS: County clerk and business executive seek to end GOP control of 2 statewide offices", "The Indiana Citizen", "2026-05-28", "https://indianacitizen.org/democrat-hopefuls-county-clerk-and-business-executive-seek-to-end-gop-control-of-2-statewide-office/"),
    "bailey_site": ("Jessica Bailey for Indiana Comptroller", "Bailey campaign (baileyforindiana.com)", "accessed 2026-10-10", "https://baileyforindiana.com/"),
    "refl_bailey": ("Indiana State Comptroller – Jessica Bailey", "The Reflector (University of Indianapolis)", "2026-10-05", "https://reflector.uindy.edu/2026/10/05/bailey26/"),
    "hoosleft": ("HoosLeft Podcast #144 – Guest: Jessica Bailey for State Comptroller (episode summary)", "Progressive Indiana Network", "2026-09", "https://www.progressiveindiana.net/p/hoosleft-podcast-144-guest-jessica"),
    "citizen_bailey": ("Porter County Clerk Jessica Bailey accepts Democratic nomination for Indiana comptroller (TheStatehouseFile)", "The Indiana Citizen", "2026-06-06", "https://indianacitizen.org/porter-county-clerk-jessica-bailey-accepts-democratic-nomination-for-indiana-comptroller/"),
    "wfyi_dems": ("Democrats name statewide candidates for treasurer and comptroller", "WFYI", "2026-05-28", "https://www.wfyi.org/statewide/2026-05-28/democrats-name-statewide-candidates-for-treasurer-and-comptroller"),
    # Schick
    "lpedia": ("John Schick", "LPedia (Libertarian Party wiki)", "", "https://lpedia.org/wiki/John_Schick"),
    "ballotready": ("John Schick", "BallotReady", "", "https://www.ballotready.org/people/john-schick"),
    "wfyi_2018": ("Auditor candidates stress need for greater transparency", "WFYI", "2018-10-31", "https://wfyi.org/news/articles/auditor-candidates-stress-need-for-greater-transparency"),
    "wfyi_2022": ("Indiana state auditor candidates cite increased transparency, independent voices as key priorities", "WFYI", "2022-10-27", "https://www.wfyi.org/news/articles/indiana-state-auditor-candidates-cite-increased-transparency-independent-voices-as-key-priorities"),
    "ballotbrief_s": ("John Schick (IN)", "The Ballot Brief", "checked 2026-09-08", "https://theballotbrief.com/candidate/john-schick-in"),
    "refl_schick": ("Indiana State Comptroller – John Schick", "The Reflector (University of Indianapolis)", "2026-10-05", "https://reflector.uindy.edu/2026/10/05/schick26/"),
}

PROFILE = {
    "race_id": "in-state-comptroller-auditor-of-state",
    "reviewed": "2026-10-10",
    "status": "draft",
    "status_note": "Pending editorial review. Coverage of this race is limited; no debate has been held.",
    "office": {
        "title": "Indiana State Comptroller (Auditor of State)",
        "summary": "Indiana's chief financial officer: keeps the state's accounts, pays the state's bills and its employees, and distributes tax revenue to counties, cities, towns, and school corporations {faq}. The constitution still calls the office Auditor of State; the ballot lists it as \"State Comptroller (Auditor of State)\" {title}{in_list}.",
        "facts": [
            {"label": "Term", "value": "4 years {const}"},
            {"label": "Term limit", "value": "8 years in any 12 {const}"},
            {"label": "State employees paid", "value": "33,000+ {depts}"},
            {"label": "Current officeholder", "value": "Appointed 2023 {appoint}"},
        ],
        "duties": [
            "Accounting & Reporting: keeps the state's general ledger and publishes the Annual Comprehensive Financial Report, the official report of the state's financial position {depts}.",
            "Accounts Payable: pays grants, public aid, school tax revenues, and vendors {depts}.",
            "Payroll: pays more than 33,000 state employees {depts}.",
            "Distributes tax revenue to local governments {faq}{depts}.",
            "Runs the Indiana Transparency Portal, which shows state spending {dash}.",
            "Chairs the committee overseeing Hoosier START, the state's deferred-compensation retirement plan {intl}.",
            "Serves on the three-member State Board of Finance with the state budget director and the treasurer; the board supervises the state's fiscal affairs, can transfer money between state funds and approve loans, and approves banks that hold state funds {sbf}.",
        ],
        "recent_changes": [
            "2025 (SEA 221): set the office's legal name as \"State Comptroller (Auditor of State)\" and required that wording on the 2026 ballot {title}.",
            "2025 (SJR 17): a proposed constitutional amendment to rename the office State Comptroller; it must pass a second legislative session before going to voters {title}.",
            "May 2026: a Federal Funding Expenditures Dashboard was added to the Transparency Portal {dash}.",
            "2026 (SEA 14): raises the state's Hoosier START match for employees; the office describes it as budget-neutral, subject to State Budget Committee approval {intl}.",
        ],
    },
    "incumbent": {
        "name": "Elise Nieshalla",
        "party": "Republican",
        "summary": "Appointed by Gov. Eric Holcomb in November 2023 to finish the term of Tera Klutz, who resigned; this is her first election for the office {appoint}{wfyi_launch}. She is on the ballot seeking a full term {wfyi_guide}.",
        "record": [
            "As chair of the Hoosier START committee, moved the plan's investments away from Chinese-entity holdings, following a state law that required the public retirement system to divest; she describes this as her proudest work {icc_launch}. In August 2026 the committee added a China-free international fund at the same fee and cut recordkeeping fees {intl}.",
            "Leads the State Financial Officers Foundation's national debt task force; in February 2026 supported a legislative resolution describing the national debt as a national security threat {debt}{icc_launch}.",
            "May 2026: launched the Federal Funding Expenditures Dashboard, reporting that federal grants were 42% of general revenue in fiscal 2025 {dash}.",
            "July 2026: announced fiscal-year results of $3.99 billion in reserves and a $1.86 billion surplus {reserves}. Some legislators argued reserves of that size should go to services or faster relief {wfyi_surplus}.",
            "July–September 2026: her office distributed State Board of Finance reimbursements to local governments for revenue lost during the gas-tax suspension {gas}{home}.",
            "No audits, ethics complaints, or lawsuits involving the office were found in this review.",
        ],
    },
    "race_context": [
        "The office has no primary; each party nominates at its state convention {ipm_dems}.",
        "Republicans renominated Nieshalla without opposition in June 2026 {wbet}; Democrats nominated Porter County Clerk Jessica Bailey unopposed on June 6 {wfyi_bailey}; Libertarians nominated John Schick in March {ipm_lp}.",
        "No debate or forum among the comptroller candidates was found as of this review {wfyi_guide}.",
    ],
    "candidates": [
        {
            "ballot_name": "Elise Nieshalla",
            "summary": "Comptroller since her appointment in late 2023, former Boone County Council president, and real-estate professional. Running on the state's fiscal position and plans to use technology to modernize the office {about}{icc_launch}.",
            "website": None,
            "background": [
                "Former president of the Boone County Council and of the Indiana County Councils Association {about}.",
                "More than 20 years in real estate; bachelor's degree from Oral Roberts University and master's from Indiana University, where she was adjunct faculty at the O'Neill School {about}.",
                "Lives in Zionsville {about}.",
                "Sought the Republican nomination for state treasurer in 2022, losing at the convention to Daniel Elliott {appoint}.",
            ],
            "path_to_ballot": [
                "Announced June 26, 2025, the first candidate of any party in the race {wfyi_launch}.",
                "Renominated without opposition at the Republican state convention in June 2026 {wbet}.",
            ],
            "positions": [
                {"topic": "Fiscal management", "items": [
                    "Points to Indiana's balanced budget, AAA credit rating, and low debt per capita {wfyi_launch}.",
                    "Would simplify the fund numbers used by the State Board of Accounts, the Department of Local Government Finance, and local governments {icc_launch}.",
                ]},
                {"topic": "Technology", "items": [
                    "Would use artificial intelligence to review accounts payable and flag anomalies, and says data protection is a priority {icc_launch}{wish}.",
                    "Says she has already streamlined timekeeping and the state's financial management system, and wants to share what works with local governments {wish}.",
                ]},
                {"topic": "Transparency", "items": [
                    "Plans to keep expanding the Transparency Portal {icc_launch}{dash}.",
                ]},
                {"topic": "Retirement investments", "items": [
                    "Plans to continue moving state retirement investments away from Chinese-entity holdings {icc_launch}{intl}.",
                ]},
            ],
            "on_incumbent": [
                "She is the current officeholder. No statements by her about her opponents were found.",
            ],
            "plans": [
                "Says she would serve the full four-year term {wish}.",
            ],
            "endorsements_finance": [
                "No endorsements or fundraising totals were found in news coverage.",
            ],
            "gaps": [
                "No campaign website was found {ballotbrief_n}.",
                "Campaign finance totals were not available in news coverage; state filings were not reviewed.",
            ],
        },
        {
            "ballot_name": "Jessica Bailey",
            "summary": "Porter County Clerk (elected 2018, re-elected 2022) and former Portage Township school board member. Running on making state spending easier to follow and more scrutiny of State Board of Finance decisions {idp}{bailey_site}.",
            "website": "https://baileyforindiana.com/",
            "background": [
                "Grew up and lives in Northwest Indiana {idp}.",
                "Elected Porter County Clerk in 2018 and re-elected in 2022; served six years on the Portage Township School Board {idp}{citizen_dems}.",
                "Bachelor's degree from Purdue University Northwest; master's in public administration and nonprofit management from Walden University {citizen_dems}.",
                "Named Clerk of the Year by the Association of Indiana Counties (2023) {idp}.",
                "As clerk, moved Porter County to vote centers and added a mobile polling location {citizen_dems}.",
                "Points to managing one of the county's largest budgets and paying poll workers as relevant experience {refl_bailey}.",
            ],
            "path_to_ballot": [
                "Announced by the Indiana Democratic Party May 27, 2026 {idp}; nominated without opposition at the state convention June 6, 2026 {wfyi_bailey}.",
            ],
            "positions": [
                {"topic": "Transparency", "items": [
                    "Would make the Transparency Portal easier to search (including partial or misspelled names), written in plain language, and kept current: \"Hoosiers deserve to see how their tax dollars are spent\" {bailey_site}{refl_bailey}.",
                    "In a podcast interview, called for publishing contract information, including losing bids {hoosleft}.",
                ]},
                {"topic": "State Board of Finance", "items": [
                    "\"No money should move without an independent set of eyes on it\"; says she would ask questions and request documentation before transfers {bailey_site}.",
                    "Says board meetings are brief with little public discussion, and wants residents to be able to watch them online {refl_bailey}.",
                ]},
                {"topic": "Payments and local governments", "items": [
                    "Lists on-time payments to local governments, state employees, and vendors as a top priority {bailey_site}{refl_bailey}.",
                    "Would draw on county experience to help local governments operate more efficiently {ipm_dems}.",
                ]},
                {"topic": "Retirement investments", "items": [
                    "In a podcast interview, said retirement investments should be judged on both returns and ethics, citing the state's China divestment as a precedent {hoosleft}.",
                ]},
            ],
            "on_incumbent": [
                "Argues the office should be held by someone outside the party that controls state government: \"I am accountable to no one but Hoosiers\" {idp}{ipm_dems}.",
                "Has criticized current State Board of Finance practice as allowing too little public discussion {refl_bailey}.",
                "No statements naming Nieshalla directly were found.",
            ],
            "plans": [
                "Rebuild Transparency Portal search; push for State Board of Finance meetings streamed online; prioritize on-time payments {bailey_site}{refl_bailey}.",
            ],
            "endorsements_finance": [
                "No endorsements are listed on her campaign site {bailey_site}. Fundraising totals were not found in news coverage.",
            ],
            "gaps": [
                "No debate, candidate forum, or WFYI questionnaire answers were found {wfyi_guide}.",
                "Some positions come from a podcast interview; the audio was not reviewed.",
            ],
        },
        {
            "ballot_name": "John Schick",
            "summary": "Information-technology consultant from Chesterton and three-time Libertarian nominee for this office. No 2026 platform has been published; his earlier campaigns focused on spending transparency {ipm_lp}{wfyi_2022}.",
            "website": None,
            "background": [
                "Lives in Chesterton; described as a business consultant and former Libertarian Party of Indiana treasurer {ipm_lp}.",
                "Works as an information-technology consultant; earlier supervised a data center at Inland Steel {ballotready}{lpedia}.",
                "Libertarian nominee for this office in 2018 and 2022 as well {wfyi_2018}{wfyi_2022}.",
            ],
            "path_to_ballot": [
                "Nominated at the Libertarian state convention in Fort Wayne, March 2026 {ipm_lp}{lp_slate}.",
            ],
            "positions": [
                {"topic": "Statements from earlier campaigns", "items": [
                    "2018: called for more transparency in county-level spending, noting that much state revenue is passed to counties, and said he would work on the state's online transparency portal {wfyi_2018}.",
                    "2022: said the office could provide more independent analysis of the effects of laws and mandates passed by lawmakers and the governor {wfyi_2022}.",
                ]},
            ],
            "on_incumbent": [
                "No 2026 statements about the incumbent were found.",
            ],
            "plans": [],
            "endorsements_finance": [
                "No endorsements or fundraising figures were found {ballotready}.",
            ],
            "gaps": [
                "No 2026 campaign website, questionnaire answers, or forum appearances were found {ballotbrief_s}; he did not respond to a University of Indianapolis student newspaper's interview request {refl_schick}.",
                "Sources differ on his education and employer history.",
            ],
        },
    ],
}


def main():
    build_profile(PROFILE, S)


if __name__ == "__main__":
    main()
