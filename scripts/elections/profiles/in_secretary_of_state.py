#!/usr/bin/env python3
"""Source for data/elections/2026/profiles/in-secretary-of-state.json (+ .md).

Edit the text here, then run:
    python3 scripts/elections/profiles/in_secretary_of_state.py

Citations are written as {key}; the script numbers sources in order of first
use and drops unused ones. Editorial rules: data/elections/2026/profiles/README.md
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import render_markdown  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data" / "elections" / "2026" / "profiles"

S = {
    "sos_about": ("About the Office", "Indiana Secretary of State", "", "https://www.in.gov/sos/about-sos/about-the-office/"),
    "wiki_office": ("Secretary of State of Indiana", "Wikipedia", "accessed 2026-10-10", "https://en.wikipedia.org/wiki/Secretary_of_State_of_Indiana"),
    "indlawyer": ("Challenge to Secretary of State's reelection bid denied", "The Indiana Lawyer", "2018", "https://theindianalawyer.com/?p=135912"),
    "ic_mirror": ("Indiana Code 3-6-3.7-1 and 3-6-4.2-3 (unofficial code mirror)", "eBench", "", "https://ebench-dev.greeninfo.org/state/indiana/statute/3-6-4.2-3"),
    "in_list": ("2026 General Election Candidate List", "Indiana Election Division", "2026-09-22", "https://www.in.gov/sos/elections/candidate-information/"),
    "sos_save": ("Secretary of State Diego Morales signs agreement with Department of Homeland Security to identify noncitizens on Indiana voter rolls (press release)", "Indiana Secretary of State", "2025-07-07", "https://events.in.gov/event/indiana-secretary-of-state-diego-morales-signs-agreement-with-department-of-homeland-security-to-identify-noncitizens-on-indiana-voter-rolls"),
    "cc_apr2026": ("Civil rights advocates fear citizenship verification law could block 'many' naturalized voters", "Indiana Capital Chronicle", "2026-04-16", "https://indianacapitalchronicle.com/2026/04/16/civil-rights-advocates-fear-citizenship-verification-law-could-block-many-naturalized-voters/"),
    "ibj_apr2025": ("Legislation on vote center study, student ID voting ban, income tax cuts sent to governor", "IBJ / Indiana Capital Chronicle", "2025-04-08", "https://www.ibj.com/articles/legislation-on-vote-center-study-student-id-voting-ban-income-tax-cuts-sent-to-governor"),
    "indypol_jun2026": ("Federal judge blocks SAVE voter database Indiana sued to build", "IndyPolitics", "2026-06-22", "https://indypolitics.org/federal-judge-blocks-save-voter-database-indiana-sued-to-build/"),
    "suit_oct2025": ("Secretary of State Diego Morales sued over new voting laws affecting naturalized citizens", "Yahoo News (syndicated)", "2025-10", "https://www.yahoo.com/news/articles/secretary-state-diego-morales-sued-194924224.html"),
    "wthi_jun2026": ("Indiana rejects, cancels voter registration for more than half of flagged immigrant Hoosiers", "WTHI / Indiana Capital Chronicle", "2026-06-11", "https://www.wthitv.com/2026/06/11/indiana-rejects-cancels-voter-registration-more-than-half-flagged-immigrant-hoosiers/"),
    "ibj_dec2024": ("Indiana secretary of state spending includes millions in no-bid contracts", "IBJ / Indiana Capital Chronicle", "2024-12-09", "https://www.ibj.com/articles/indiana-secretary-of-state-spending-includes-millions-in-no-bid-contracts"),
    "ibj_mar2026": ("Former Indianapolis Mayor Greg Ballard declares for secretary of state race", "Inside INdiana Business / IBJ", "2026-03-04", "https://www.insideindianabusiness.com/articles/former-indianapolis-mayor-greg-ballard-declares-for-secretary-of-state-race"),
    "wfyi_jun2025": ("Diego Morales defiant over questions about leadership of Indiana secretary of state's office", "WFYI (via WVXU)", "2025-06-18", "https://www.wvxu.org/2025-06-18/diego-morales-defiant-over-questions-about-leadership-of-indiana-secretary-of-states-office"),
    "indypol_mar2026": ("Election board refers secretary of state to inspector general over alleged misuse of state resources", "IndyPolitics", "2026-03-06", "https://indypolitics.org/election-board-refers-secretary-of-state-to-inspector-general-over-alleged-misuse-of-state-resources/"),
    "sos_sept2026": ("Secretary of State Diego Morales sets the record straight following attacks on office administration (press release)", "Indiana Secretary of State", "2026-09-09", "https://events.in.gov/event/indiana-secretary-of-state-diego-morales-sets-the-record-straight-following-attacks-on-office-administration"),
    "ipm_may21": ("Banks, Rokita drop support for Morales, urge him to suspend secretary of state campaign", "Indiana Capital Chronicle (via IPM)", "2026-05-21", "https://www.ipm.org/news/2026-05-21/banks-rokita-drop-support-for-morales-urge-him-to-suspend-secretary-of-state-campaign"),
    "ipm_may26": ("Morales lashes back over loss of Indiana secretary of state race support", "Indiana Capital Chronicle (via IPM)", "2026-05-26", "https://www.ipm.org/news/2026-05-26/morales-lashes-back-over-loss-of-indiana-secretary-of-state-race-support"),
    "indypol_jun20": ("Engling captures Republican bid for Indiana secretary of state", "Indiana Capital Chronicle (via IndyPolitics)", "2026-06-20", "https://indypolitics.org/engling-captures-republican-bid-for-indiana-secretary-of-state/"),
    "citizen_jun6": ("Beau Bayh wins Democratic nomination for Indiana secretary of state", "The Indiana Citizen", "2026-06-06", "https://indianacitizen.org/beau-bayh-wins-democratic-nomination-for-indiana-secretary-of-state/"),
    "ipm_mar24": ("Indiana Libertarians nominate Lauri Shillings for secretary of state", "Indiana Capital Chronicle (via IPM)", "2026-03-24", "https://www.ipm.org/news/2026-03-24/indiana-libertarians-nominate-lauri-shillings-for-secretary-of-state"),
    "wndu_sep9": ("What's the Lincoln Party? Ballard's secretary of state run could expand Indiana ballot access", "Indiana Capital Chronicle (via WNDU)", "2026-09-09", "https://www.wndu.com/2026/09/09/whats-lincoln-party-ballards-secretary-state-run-could-expand-indiana-ballot-access/"),
    "ipm_aug27": ("Indiana secretary of state hopefuls clash over voting rules, office audit", "Indiana Capital Chronicle (via IPM)", "2026-08-27", "https://www.ipm.org/news/2026-08-27/indiana-secretary-of-state-hopefuls-clash-over-voting-rules-office-audit"),
    "pbs_debate": ("2026 Indiana Secretary of State Debate (video)", "Indiana Debate Commission / WFYI", "2026-10-07", "https://www.pbs.org/video/2026-indiana-secretary-of-state-debate-clykbi/"),
    "wfyi_oct7": ("Indiana Secretary of State candidates debate election security, office integrity and voter turnout", "WFYI", "2026-10-07", "https://wfyi.org/statewide/2026-10-07/indiana-secretary-of-state-candidates-debate-election-security-office-integrity-and-voter-turnout"),
    "cc_oct8": ("Sharp divides in Indiana secretary of state debate over noncitizen vote, spending audit", "Indiana Capital Chronicle (via WNDU)", "2026-10-08", "https://www.wndu.com/2026/10/08/sharp-divides-indiana-secretary-state-debate-over-noncitizen-vote-spending-audit/"),
    "wiki_race": ("2026 Indiana Secretary of State election (campaign finance table, citing state filings)", "Wikipedia", "accessed 2026-10-10", "https://en.wikipedia.org/wiki/2026_Indiana_Secretary_of_State_election"),
    # Bayh
    "bayh_about": ("About Beau", "Bayh campaign (beaubayh.com)", "accessed 2026-10-10", "https://beaubayh.com/about/"),
    "bayh_priorities": ("Priorities", "Bayh campaign (beaubayh.com)", "accessed 2026-10-10", "https://beaubayh.com/priorities/"),
    "ipb_oct2025": ("Beau Bayh announces bid for Secretary of State", "Indiana Public Broadcasting", "2025-10-06", "https://indianapublicradio.org/news/2025/10/beau-bayh-announces-bid-for-secretary-of-state/"),
    "bp_aug7": ("Open general election contest for Indiana Secretary of State after Republican incumbent defeated at convention", "Ballotpedia News", "2026-08-07", "https://news.ballotpedia.org/2026/08/07/open-general-election-contest-for-indiana-secretary-of-state-after-republican-incumbent-defeated-at-convention/"),
    "fox59_bayh": ("\"Hoosiers are ready for change\": Beau Bayh talks campaign promises following his nomination", "FOX59", "2026-06", "https://fox59.com/news/politics/hoosiers-are-ready-for-change-beau-bayh-talks-campaign-promises-following-his-nomination-for-indiana-secretary-of-state/amp/"),
    "wthi_jun16": ("Beau Bayh outlines campaign platform for Indiana secretary of state race", "WTHI", "2026-06-16", "https://www.wthitv.com/2026/06/16/beau-bayh-outlines-campaign-platform-indiana-secretary-state-race/"),
    "wfiu_aug26": ("Secretary of State candidate Beau Bayh addresses Bloomington Press Club", "WFIU / IPM", "2026-08-26", "https://www.ipm.org/news/2026-08-26/secretary-of-state-candidate-beau-bayh-addresses-bloomington-press-club"),
    "republic_walker": ("Walker crosses party lines, endorses Democrat Beau Bayh for secretary of state", "The Republic", "2026-10-08", "https://www.therepublic.com/2026/10/08/walker-crosses-party-lines-endorses-democrat-beau-bayh-for-secretary-of-state/"),
    # Engling
    "ipm_jun3": ("Banks staffer Engling says decision on secretary of state's race came quickly", "Indiana Capital Chronicle (via IPM)", "2026-06-03", "https://www.ipm.org/news/2026-06-03/banks-staffer-engling-says-decision-on-secretary-of-states-race-came-quickly"),
    "reporter_may21": ("Max Engling announces campaign for Indiana Secretary of State", "The Reporter", "2026-05-21", "https://readthereporter.com/max-engling-announces-campaign-for-indiana-secretary-of-state/"),
    "wrtv_oct8": ("Engling clashes with Indiana secretary of state rivals over noncitizen voting", "WRTV", "2026-10-08", "https://www.wrtv.com/news/election/engling-noncitizen-voting-debate/"),
    "wrtv_jun13": ("Republican secretary of state candidates make their case ahead of convention", "WRTV", "2026-06-13", "https://www.wrtv.com/news/local-news/republican-secretary-of-state-candidates-make-their-case-ahead-of-convention"),
    "hot1009": ("Max Engling talks vision for Indiana Secretary of State's office", "Hot 100.9", "2026-06-26", "https://hot1009.com/4478993/max-engling-talks-vision-for-indiana-secretary-of-states-office/"),
    "indypol_aug26": ("Indy Chamber hosts spirited debate in high-profile Indiana Secretary of State race", "IndyPolitics", "2026-08-26", "https://indypolitics.org/?p=20462"),
    "wane_jun20": ("Indiana Republicans nominate Max Engling for Secretary of State", "WANE", "2026-06-20", "https://www.wane.com/top-stories/indiana-republicans-nominate-max-engling-for-secretary-of-state-at-gop-convention-in-fort-wayne/amp/"),
    "wlfi_engling": ("Meet the Secretary of State Candidate: Max Engling", "WLFI", "2026-08-13", "https://www.wlfi.com/2026/08/13/meet-secretary-state-candidate-max-engling/"),
    # Ballard
    "wrtv_mar4": ("Former Indy Mayor Greg Ballard announces run for Indiana secretary of state", "WRTV", "2026-03-04", "https://www.wrtv.com/news/local-news/former-indy-mayor-greg-ballard-announces-run-for-indiana-secretary-of-state"),
    "wfyi_mar12": ("Ballard to run under 'Lincoln Party' name in independent bid for Indiana secretary of state", "Indiana Capital Chronicle / WFYI", "2026-03-12", "https://www.wfyi.org/public-affairs/2026-03-12/ballard-to-run-under-lincoln-party-name-in-independent-bid-for-indiana-secretary-of-state"),
    "citizen_mar10": ("'STEP FORWARD': Ex-Mayor Greg Ballard starts new political party in bid for secretary of state", "The Indiana Citizen", "2026-03-10", "https://indianacitizen.org/step-forward-ex-mayor-greg-ballard-starts-new-political-party-in-bid-for-secretary-of-state/"),
    "reflector_ballard": ("Indiana Secretary of State – Greg Ballard", "The Reflector (University of Indianapolis)", "2026-10-05", "https://reflector.uindy.edu/2026/10/05/ballard26/"),
    "ipm_jun18": ("Ballard campaign disavows 'rogue' volunteer accused of forging signatures", "Indiana Capital Chronicle (via IPM)", "2026-06-18", "https://www.ipm.org/news/2026-06-18/ballard-campaign-disavows-rogue-volunteer-accused-of-forging-signatures"),
    "indystar_oct8": ("Indiana secretary of state debate takeaways", "IndyStar (via Yahoo)", "2026-10-08", "https://www.yahoo.com/news/politics/articles/indiana-secretary-state-debate-takeaways-014905169.html"),
    "exponent_oct8": ("Secretary of state candidates debate voting safeguards, office oversight", "Purdue Exponent", "2026-10-08", "https://www.purdueexponent.org/city_state/secretary-of-state-candidates-debate-over-voting-safeguards-office-oversight/article_c74d0e49-a4da-4269-87ff-4c239afdf17c.html"),
    "citizen_oct8": ("ROUND TWO: SOS candidates trade jabs on voting and investigations during second debate", "The Indiana Citizen", "2026-10-08", "https://indianacitizen.org/round-two-sos-candidates-trade-jabs-on-voting-and-investigations-during-second-debate/"),
    "ipm_jul16": ("Independent tops spring secretary of state fundraising; Democrat amasses general election war chest", "Indiana Capital Chronicle (via IPM)", "2026-07-16", "https://www.ipm.org/news/2026-07-16/independent-tops-spring-secretary-of-state-fundraising-democrat-amasses-general-election-war-chest"),
    # Shillings
    "wfyi_guide": ("2026 Voter Guide: Indiana Secretary of State", "WFYI", "2026-09-23", "https://www.wfyi.org/statewide/2026-09-23/2026-voter-guide-indiana-secretary-of-state"),
    "reflector_shillings": ("Indiana Secretary of State – Lauri Shillings", "The Reflector (University of Indianapolis)", "2026-10-05", "https://reflector.uindy.edu/2026/10/05/shillings26/"),
    "iib_may2025": ("Libertarian to explore challenge to Indiana Secretary of State Diego Morales", "Indiana Capital Chronicle / Inside INdiana Business", "2025-05-06", "https://www.insideindianabusiness.com/articles/libertarian-to-explore-challenge-to-indiana-secretary-of-state-diego-morales"),
    "wvxu_mar25": ("Libertarian party nominates Lauri Shillings for Secretary of State race", "WFYI (via WVXU)", "2026-03-25", "https://www.wvxu.org/2026-03-25/libertarian-party-nominates-lauri-shillings-for-secretary-of-state-race"),
    "shf_oct6": ("Where Ballard and the other secretary of state candidates stand on election reform", "The Indiana Citizen (via The Statehouse File)", "2026-10-06", "https://www.thestatehousefile.com/politics/elections/where-ballard-and-the-other-secretary-of-state-candidates-stand-on-election-reform/article_59c2f54d-f4ed-45f4-b50f-39c3959d4ad0.html"),
}

PROFILE = {
    "race_id": "in-secretary-of-state",
    "reviewed": "2026-10-10",
    "status": "draft",
    "status_note": "Pending editorial review. Quotes were taken from news reports; check key quotes against the Oct. 7 debate video before publishing.",
    "office": {
        "title": "Indiana Secretary of State",
        "summary": "Indiana's chief election official and the head of four divisions: Business Services, Elections, Securities, and Auto Dealer Services. The office forms and registers businesses, regulates securities, oversees elections, commissions notaries, registers trademarks, and licenses vehicle dealers {sos_about}.",
        "facts": [
            {"label": "Term", "value": "4 years {wiki_office}"},
            {"label": "Term limit", "value": "8 years in any 12 {wiki_office}"},
            {"label": "Divisions", "value": "4 {sos_about}"},
            {"label": "On the ballot", "value": "No incumbent {indypol_jun20}"},
        ],
        "duties": [
            "Serves as Indiana's chief election official. For National Voter Registration Act purposes, that role belongs jointly to the two Indiana Election Division co-directors, who are appointed by the governor and may not be from the same party {ic_mirror}.",
            "Casts the deciding vote when the Election Division co-directors deadlock on the division's budget, spending, or contracts {ic_mirror}.",
            "Chairs the State Recount Commission, which handles recounts and contests for federal, statewide, and legislative general elections and for major-party primary nominations {wiki_office}.",
            "Business Services: business formation and annual filings, commercial (UCC) lien filings, trademarks, and notary commissions. INBiz is the office's online business portal {sos_about}{wiki_office}.",
            "Securities Division: investigates and enforces Indiana securities law {wiki_office}.",
            "Auto Dealer Services: licenses dealers of automobiles, watercraft, off-road vehicles, and salvage {sos_about}.",
            "Separate from the office: the bipartisan Indiana Election Commission handles election-law violations and penalties {wiki_office}.",
        ],
        "recent_changes": [
            "2024 (HEA 1264): state election officials compare Bureau of Motor Vehicles records of temporary-credential holders against the voter rolls; flagged registrants receive notice and 30 days to show citizenship {sos_save}.",
            "2025 (HEA 1680, effective July 1, 2025): counties must request proof of citizenship from people who registered using a temporary-credential number, and remove those who do not respond within 30 days {cc_apr2026}.",
            "2025 (SB 10): bars public-college student IDs from being used as voter ID; sent to the governor on April 8, 2025 {ibj_apr2025}.",
            "2025 (HB 1633): directs the Secretary of State to study statewide vote centers and moving municipal elections to even-numbered years {ibj_apr2025}.",
            "October 2025: the League of Women Voters of Indiana, Common Cause Indiana, and other groups sued the Secretary of State and the Election Division co-directors in federal court, arguing HEA 1264 and HEA 1680 violate federal voting law {suit_oct2025}. A request for a preliminary injunction was pending as of June 2026 {wthi_jun2026}.",
            "June 22, 2026: a federal judge in Washington, D.C., set aside the 2025 overhaul of the federal SAVE citizenship database nationwide; the ruling does not change Indiana's own statutes {indypol_jun2026}.",
        ],
    },
    "incumbent": {
        "name": "Diego Morales",
        "party": "Republican",
        "summary": "Took office in January 2023; his term ends in January 2027. He sought re-election but lost the Republican nomination at the June 2026 state convention, so he is not on the November ballot {indypol_jun20}.",
        "record": [
            "2023: the office paid spot bonuses totaling more than $308,000 to nearly all employees. Morales said they reflected salary adjustments promised before his tenure {ibj_dec2024}.",
            "2023–2024: the office awarded information-technology contracts without competitive bidding, including more than $2.3 million to CleanSlate Technology Group and up to about $1.84 million to MTX Group. Reporters noted contributions to Morales's campaign from CleanSlate and from MTX's founder. The office said it chose vendors with strong track records under state procurement law; no-bid contracts are legal in Indiana {ibj_dec2024}.",
            "Reporting has also covered the office's purchase of a roughly $90,000 vehicle from a dealership whose owners donated to his campaign, the hiring of his brother-in-law, and a privately funded trip abroad {ibj_mar2026}.",
            "June 2025: at a State Budget Committee hearing, lawmakers questioned him about contracts and travel, then approved more than $10 million in additional funding for technology, the Securities Division, and election support. Morales: \"I will not apologize to anyone because my work ethic is unmatched\" {wfyi_jun2025}.",
            "July 2025: signed an agreement with U.S. Citizenship and Immigration Services to use the federal SAVE database to check the citizenship of registered voters {sos_save}.",
            "November 2025: after Indiana sued the Department of Homeland Security for bulk SAVE access, the state settled; the office uploaded nearly 500,000 voter registrations to DHS and provided the voter list to the U.S. Justice Department {indypol_jun2026}.",
            "June 2026: an analysis filed by the plaintiffs in the federal lawsuit counted 3,234 people flagged under HEA 1680, of whom 981 had their registrations canceled and 113 were identified as false positives {wthi_jun2026}.",
            "March 2026: the Marion County Election Board referred allegations that a re-election video used footage from an official visit to the State Inspector General and State Ethics Commission. His campaign called the allegations meritless. No outcome had been reported as of this review {indypol_mar2026}.",
            "September 2026: the office responded to campaign criticism, stating that all office vendors were contracted through public processes {sos_sept2026}.",
        ],
    },
    "race_context": [
        "May 2026: U.S. Sen. Jim Banks and Attorney General Todd Rokita withdrew their endorsements of Morales and backed Max Engling {ipm_may21}. Morales called the criticism politically motivated and stayed in the race {ipm_may26}.",
        "June 6, 2026: Democratic convention delegates nominated Beau Bayh over Blythe Potter, 1,385 to 883 {citizen_jun6}.",
        "June 20, 2026: Republican convention delegates nominated Max Engling on the second ballot with 867 votes, ahead of Knox County Clerk David Shelton (627) and Morales (134) {indypol_jun20}.",
        "Lauri Shillings was nominated at the Libertarian state convention in March {ipm_mar24}; Greg Ballard qualified by petition under the new Lincoln Party name {wndu_sep9}.",
        "Ballot status is at stake for minor parties: a party whose Secretary of State nominee gets at least 2% keeps its ballot line, and 10% would let it nominate through primaries {wndu_sep9}{ipm_mar24}.",
        "Where all four ballot candidates agree: only eligible citizens should vote, and business filings should list owners, not only registered agents {ipm_aug27}{wfyi_oct7}.",
        "Where they differ most: Bayh, Ballard, and Shillings support an audit of the office; Engling prefers a review by the state inspector general. Engling supports the federal SAVE America Act; Ballard and Shillings oppose it {ipm_aug27}{cc_oct8}.",
        "Debates: Indy Chamber HobNob, Aug. 26, 2026 {ipm_aug27}; Indiana Debate Commission at WFYI, Oct. 7, 2026 {pbs_debate}.",
    ],
    "candidates": [
        {
            "ballot_name": "Beau Bayh",
            "summary": "Attorney and former Marine Corps officer in his first run for office. Says his top priority is an independent audit of the Secretary of State's office {fox59_bayh}{bayh_priorities}.",
            "website": "https://beaubayh.com",
            "background": [
                "Birch Evans \"Beau\" Bayh IV is the son of former Indiana governor and U.S. senator Evan Bayh {ipb_oct2025}.",
                "Bachelor's degree in government and law degree, both from Harvard {bp_aug7}.",
                "Served as a U.S. Marine Corps infantry officer, reaching captain; deployed to Europe as part of the U.S. response to Russia's invasion of Ukraine; honorably discharged in 2023 {bayh_about}.",
                "Worked for Cummins and Barnes & Thornburg during law school, then clerked for Judge David F. Hamilton of the U.S. Court of Appeals for the Seventh Circuit {bayh_about}.",
            ],
            "path_to_ballot": [
                "Announced Oct. 6, 2025 {ipb_oct2025}; nominated at the Democratic state convention June 6, 2026, with 61% of delegate votes {citizen_jun6}.",
            ],
            "positions": [
                {"topic": "Election administration", "items": [
                    "Campaign position: \"No illegal votes – period – but every legal Hoosier's vote should count\"; wants higher turnout while protecting security {bayh_priorities}.",
                    "Supports Indiana's current voter ID law {cc_oct8}.",
                    "Says county clerks from both major parties run Indiana's elections well and that the state's elections are secure; disputes Engling's statements about noncitizen voting {cc_oct8}.",
                    "Would expand early voting and keep primaries open to all voters {fox59_bayh}.",
                    "Would end straight-ticket voting, which he says reduces competition in elections {wthi_jun16}{cc_oct8}.",
                    "Supports citizen-led ballot initiatives and statewide referenda, including on redistricting; these would require action by the legislature {bayh_priorities}{fox59_bayh}.",
                    "On the 2026 Senate District 23 recount, said the disputed ballots should have been counted because voter intent was clear and no fraud was alleged {ipm_aug27}.",
                ]},
                {"topic": "Business services", "items": [
                    "Wants to make it easier to start and grow a small business and to reduce paperwork {bayh_priorities}.",
                    "Supports requiring business filings to list owners, not only registered agents {ipm_aug27}.",
                ]},
                {"topic": "Running the office", "items": [
                    "Would order an independent, forensic audit of the office on day one, publish the findings, and refer any wrongdoing to prosecutors {fox59_bayh}{cc_oct8}.",
                    "Pledges not to award contracts to campaign contributors or hire relatives {cc_oct8}{fox59_bayh}.",
                    "Would end the office's partnership with Turning Point USA and says any outside partnerships should be nonpartisan {fox59_bayh}.",
                ]},
            ],
            "on_incumbent": [
                "Has criticized the office's vehicle purchase, the hiring of relatives, and no-bid contracts awarded to campaign donors {citizen_jun6}{cc_oct8}.",
                "At the Oct. 7 debate, argued that the inspector general review Engling favors is not sufficient {cc_oct8}.",
                "Aug. 26, 2026, on Morales: \"That's such an important responsibility and it's being entrusted to someone who I think is not up for the job\" {wfiu_aug26}.",
            ],
            "plans": [
                "Sell the office's SUV and drive his own car {fox59_bayh}.",
                "Work with the governor and legislative majority on changes that require new laws, such as ending straight-ticket voting {wthi_jun16}.",
                "Says he would serve a full term; has not ruled out a future run for governor {fox59_bayh}.",
            ],
            "endorsements_finance": [
                "Reported $2,695,117 raised and $2,311,139 cash on hand through June 30, 2026 {wiki_race}.",
                "Republican state Sen. Greg Walker of Columbus endorsed him in October 2026 {republic_walker}.",
            ],
            "gaps": [
                "No published positions found on the Securities Division, voting equipment, voter-roll maintenance, mail voting, or the SAVE America Act.",
                "The audit plan he said was coming in June had not been published as of this review.",
                "Campaign finance reports covering July–September are due Oct. 16, 2026.",
            ],
        },
        {
            "ballot_name": "Max Engling",
            "summary": "U.S. Senate staff member and former U.S. House aide who won the Republican nomination over the incumbent. Says preventing noncitizen voting is his top priority {ipm_jun3}{wrtv_oct8}.",
            "website": None,
            "background": [
                "Age 39, of the Cicero area in Hamilton County; returned to Indiana in 2023 {ipm_jun3}.",
                "Graduated from IUPUI in 2010 {ipm_jun3}; master's degree from the U.S. Naval War College {reporter_may21}.",
                "About 12 years as a Republican staff member in the U.S. House, including roughly five years as an aide to then-Speaker Kevin McCarthy; cites experience with the House Administration Committee, which oversees federal election law {ipm_jun3}{indypol_jun20}.",
                "Since January 2025, central Indiana regional director and adviser to U.S. Sen. Jim Banks; on leave to campaign {ipm_jun3}.",
                "Finished third in the 2024 Republican primary for Indiana's 5th Congressional District {ipm_jun3}.",
            ],
            "path_to_ballot": [
                "Announced May 20, 2026, after Banks and Rokita withdrew their support for Morales {reporter_may21}{ipm_may21}.",
                "Nominated at the Republican state convention on June 20, 2026, on the second ballot with about 53% of delegate votes {indypol_jun20}.",
            ],
            "positions": [
                {"topic": "Election administration", "items": [
                    "Calls preventing noncitizen registration and voting his top priority, saying \"even one instance of illegal voting is too many\" {wrtv_oct8}.",
                    "Cited the state's review that found 165 noncitizens registered and 21 who had voted {indypol_aug26}.",
                    "Supports checking legal status when driver's licenses are issued and a different license design for noncitizens {wrtv_jun13}{hot1009}.",
                    "Supports the federal SAVE America Act; he was the only candidate at the Aug. 26 forum to do so {ipm_aug27}.",
                    "Would work with legislators to close party primaries to voters not affiliated with the party {wane_jun20}.",
                    "Supports early voting but suggests a period of about two weeks, shorter than Indiana's current 28 days {hot1009}{ibj_mar2026}.",
                    "Supports keeping the straight-ticket voting option {cc_oct8}.",
                    "Supports post-election audits and paper audit trails {hot1009}{wrtv_jun13}.",
                    "On the 2026 Senate District 23 recount, said the recount commission followed the law {ipm_aug27}.",
                    "Opposes citizen ballot initiatives, saying issues should be worked through the legislature {cc_oct8}.",
                    "Opposes a mailed paper voter guide because of its cost; prefers digital tools {ipm_aug27}.",
                ]},
                {"topic": "Business services", "items": [
                    "Would screen business filings for shell companies, especially trucking firms that use multiple entities to avoid scrutiny, and refer suspected fraud to prosecutors or the attorney general {wrtv_jun13}{hot1009}.",
                    "Supports listing owners in business filings and wants agencies to reuse information businesses have already submitted {ipm_aug27}.",
                    "Proposes an online portal where Hoosiers can report fraud concerns {wlfi_engling}.",
                ]},
                {"topic": "Running the office", "items": [
                    "Supports a review of the office by the state inspector general rather than an independent audit {ipm_aug27}{cc_oct8}.",
                    "Says the office needs new processes and procedures to run well {hot1009}.",
                ]},
            ],
            "on_incumbent": [
                "Points to his convention win over Morales: \"I am the only candidate that has actually done something about the issues that we've seen in the office\" {cc_oct8}.",
                "Said at the Aug. 26 debate that he would not hire relatives {ipm_aug27}.",
            ],
            "plans": [
                "First priority: work with legislators to close primaries {wane_jun20}.",
                "Pursue distinct driver's licenses for noncitizens, a fraud-reporting portal, and screening of business filings for shell companies {hot1009}{wlfi_engling}{wrtv_jun13}.",
                "Says he would serve a full four-year term {ipm_aug27}.",
            ],
            "endorsements_finance": [
                "Endorsed by U.S. Sen. Jim Banks and Attorney General Todd Rokita {ipm_may21}.",
                "Reported $201,626 raised and $150,121 cash on hand through June 30, 2026 {wiki_race}.",
            ],
            "gaps": [
                "No published positions found on the Securities Division, mail voting, or voting-equipment vendors.",
                "No campaign website or voter-guide questionnaire could be read for this review.",
                "News reports about specific campaign contributions could not be read in full and are not included.",
                "Campaign finance reports covering July–September are due Oct. 16, 2026.",
            ],
        },
        {
            "ballot_name": "Greg Ballard",
            "summary": "Former two-term mayor of Indianapolis and retired Marine officer, running on the new Lincoln Party line. Says the office should be run as a nonpartisan, professional office {ibj_mar2026}{wfyi_mar12}.",
            "website": None,
            "background": [
                "Mayor of Indianapolis from 2008 to 2016 {citizen_mar10}.",
                "Retired from the U.S. Marine Corps as a lieutenant colonel after 23 years {reflector_ballard}.",
                "Was a Republican until this campaign {citizen_mar10}; now a visiting fellow at the University of Indianapolis {reflector_ballard}.",
                "Cites his management of the city budget during the recession and infrastructure rebuilding as mayor {wrtv_mar4}.",
            ],
            "path_to_ballot": [
                "Announced an independent campaign March 4, 2026 {wrtv_mar4}. Indiana law does not allow an \"Independent Party\" label, so he chose the name Lincoln Party {wfyi_mar12}.",
                "Qualified by petition; the Election Division lists his filing date as July 14, 2026 {in_list}{wndu_sep9}.",
                "In June 2026, Hamilton County officials flagged one petition page with suspect signatures gathered by a single volunteer, and state police opened an investigation. The campaign said it ended the volunteer's involvement. No outcome had been reported as of this review {ipm_jun18}.",
                "The Lincoln Party is chaired by Nathan Gotsch, Ballard's campaign manager, and has not published a platform {wndu_sep9}.",
            ],
            "positions": [
                {"topic": "Election administration", "items": [
                    "Wants \"a nonpartisan, low-key professional office\"; says county clerks run elections well and that he sees no evidence of widespread voter fraud {ibj_mar2026}.",
                    "Would keep Indiana's 28-day early voting period and end straight-ticket voting {ibj_mar2026}.",
                    "Proposes mailing a paper voter guide to every registered voter, plus an app, at an estimated $2.5 million or more per cycle, and suggests the parties pay for their own primaries {ipm_aug27}.",
                    "Would register 17-year-olds through high schools and expand voter outreach {indystar_oct8}.",
                    "Considers Indiana's existing citizenship safeguards strong and calls the federal SAVE America Act an overreach {ipm_aug27}.",
                    "Would make the Indiana Election Commission and State Recount Commission nonpartisan and move some recount work to administrative law judges {indystar_oct8}{exponent_oct8}.",
                    "On the 2026 Senate District 23 recount, said voter intent should come first and the disputed ballots should have been counted {ipm_aug27}.",
                ]},
                {"topic": "Business services", "items": [
                    "Says the office's business website is outdated and wants faster service for small businesses and farmers {reflector_ballard}{indystar_oct8}.",
                    "Supports requiring business filings to list owners {ipm_aug27}.",
                ]},
                {"topic": "Running the office", "items": [
                    "Would post all office contracts online and pledges not to raise money for or endorse candidates while in office {reflector_ballard}.",
                    "Supports an audit of the office, with emphasis on travel expenses {ipm_aug27}.",
                ]},
            ],
            "on_incumbent": [
                "At his announcement, said the office's current leadership \"has shown an eagerness to engage in partisan politics,\" while declining to rate Morales's performance {wrtv_mar4}{ibj_mar2026}.",
                "At the Oct. 7 debate, said he would bring in a law-enforcement professional to investigate the office {citizen_oct8}.",
                "Morales, in response to Ballard's entry, described him as a Democrat calling himself an independent {wrtv_mar4}.",
            ],
            "plans": [
                "Audit the office and bring in an outside investigator {ipm_aug27}{citizen_oct8}.",
                "Mailed voter guide and app; nonpartisan election and recount commissions; contracts posted online; updated business website {ipm_aug27}{indystar_oct8}{reflector_ballard}.",
                "Says he would serve a full four-year term {ipm_aug27}.",
            ],
            "endorsements_finance": [
                "April–June 2026: raised about $672,000 and spent about $746,000, with nearly $450,000 from the PAC Hoosiers for Competitive Elections {ipm_jul16}.",
                "Reported donors include former Eli Lilly CEO John Lechleiter ($100,000) and former Lt. Gov. John Mutz {wndu_sep9}.",
            ],
            "gaps": [
                "No published positions found on the Securities Division, voting equipment, voter-roll maintenance, or mail voting.",
                "No campaign website was found.",
                "A reported endorsement by former Lt. Gov. Sue Ellspermann could not be confirmed from a full article.",
                "Campaign finance reports covering July–September are due Oct. 16, 2026.",
            ],
        },
        {
            "ballot_name": "Lauri A. Shillings",
            "summary": "University of Indianapolis creative director and small-business owner, nominated by the Libertarian Party. Focuses on modernizing the office's website and making election audit results public {wfyi_guide}{shf_oct6}.",
            "website": None,
            "background": [
                "Age 55, of Carmel; grew up in Wingate {wfyi_guide}{reflector_shillings}.",
                "Bachelor's degree in community and nonprofit leadership from the University of Indianapolis, where she is creative director in the marketing office {reflector_shillings}{ipm_mar24}.",
                "Has run the small business Pirate Smile Media since 2000 {ipm_aug27}.",
                "Chair of the Hamilton County Libertarian Party since 2021; the party's 2024 nominee for Indiana's 5th Congressional District {ipm_mar24}.",
            ],
            "path_to_ballot": [
                "Formed an exploratory committee in May 2025 {iib_may2025}; nominated at the Libertarian state convention in Fort Wayne in March 2026 {ipm_mar24}.",
                "Her party needs at least 2% of the vote in this race to keep its ballot line {ipm_mar24}.",
            ],
            "positions": [
                {"topic": "Election administration", "items": [
                    "Calls Indiana's elections secure {wfyi_guide}.",
                    "Would publish the results of county post-election audits and the corrective actions taken, and expand audits to more counties {wfyi_guide}{shf_oct6}.",
                    "Opposes additional proof-of-citizenship requirements such as the SAVE America Act, saying they burden people whose names changed through marriage, divorce, or adoption, and that existing checks work {ipm_aug27}{cc_oct8}.",
                    "Supports hand-marked paper ballots counted by machine, while noting current equipment limits {wfyi_guide}.",
                    "Opposes restricting who may vote in a party's primary {wfyi_guide}.",
                    "Wants training and tools for county clerks without directing their methods, and more perspectives beyond the two major parties on election and recount boards {shf_oct6}.",
                    "Would rebuild the online election portal so voters can see candidates and who funds them {shf_oct6}.",
                ]},
                {"topic": "Business services", "items": [
                    "Says her top priority is modernizing the office's website and business filing site, which she describes as outdated {wvxu_mar25}{wfyi_guide}.",
                    "Would ask lawmakers to reduce business licensing paperwork and fees {reflector_shillings}.",
                ]},
                {"topic": "Running the office", "items": [
                    "Supports an audit of the office's budget and spending, followed by regular audits {ipm_aug27}{shf_oct6}.",
                ]},
            ],
            "on_incumbent": [
                "When she began exploring a run in 2025, said the current office had done very little for Hoosiers {iib_may2025}.",
                "Raised privacy concerns about the office sharing Indiana voter-roll data with the federal government {wvxu_mar25}.",
                "Says the office should be treated as a public trust rather than a political tool {ipm_mar24}.",
            ],
            "plans": [
                "Overhaul the office website and business filing site {wvxu_mar25}{wfyi_guide}.",
                "Publish election audit results; audit the office's spending; support county clerks with training and tools {wfyi_guide}{shf_oct6}.",
            ],
            "endorsements_finance": [
                "No endorsements found. Reported fundraising through June 30, 2026, differs by source: $21,073 (WFYI) and $28,678 (Wikipedia, citing state filings) {wfyi_guide}{wiki_race}.",
            ],
            "gaps": [
                "No published positions found on the Securities Division, early or mail voting, or voter-roll maintenance.",
                "No campaign website was found.",
                "Campaign finance reports covering July–September are due Oct. 16, 2026.",
            ],
        },
        {
            "ballot_name": "Andrew Delano",
            "summary": "Declared write-in candidate on the Indiana Election Division's list; his name will not be printed on the ballot {in_list}.",
            "website": None,
            "background": [],
            "path_to_ballot": ["Filed as a declared write-in candidate {in_list}."],
            "positions": [],
            "on_incumbent": [],
            "plans": [],
            "endorsements_finance": [],
            "gaps": [
                "Did not take part in the race's debates {ipm_aug27}. We found no published policy positions.",
            ],
        },
    ],
}


def number_citations(obj, order):
    if isinstance(obj, str):
        def sub(m):
            key = m.group(1)
            if key not in S:
                raise KeyError(f"unknown source {key}")
            if key not in order:
                order.append(key)
            return f"[{order.index(key) + 1}]"
        out = re.sub(r"\{([a-z0-9_]+)\}", sub, obj)
        return re.sub(r"\]\s*\[", ", ", re.sub(r"\s+(\[\d)", r" \1", out)).replace(" .", ".")
    if isinstance(obj, list):
        return [number_citations(x, order) for x in obj]
    if isinstance(obj, dict):
        return {k: number_citations(v, order) for k, v in obj.items()}
    return obj


def main():
    order = []
    profile = number_citations(PROFILE, order)
    profile["sources"] = [
        {"id": i + 1, "title": S[k][0], "publisher": S[k][1], "date": S[k][2], "url": S[k][3]}
        for i, k in enumerate(order)
    ]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{profile['race_id']}.json").write_text(
        json.dumps(profile, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / f"{profile['race_id']}.md").write_text(render_markdown(profile), encoding="utf-8")
    unused = sorted(set(S) - set(order))
    print(f"{len(profile['candidates'])} candidates, {len(order)} sources; unused: {unused}")


if __name__ == "__main__":
    main()
