#!/usr/bin/env python3
"""Source for data/elections/2026/profiles/in-treasurer-of-state.json (+ .md).

    python3 scripts/elections/profiles/in_treasurer_of_state.py

Citations are written as {key}. Editorial rules: data/elections/2026/profiles/README.md
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import build_profile  # noqa: E402

S = {
    "about": ("About the Treasurer", "Indiana Treasurer of State", "accessed 2026-10-10", "https://secure.in.gov/tos/about-the-office/about-the-treasurer"),
    "stateside_e": ("Daniel Elliott Treasurer Profile", "Stateside", "2026-07-09", "https://www.stateside.com/sites/default/files/2026-07/Daniel%20Elliot%20Treasurer%20Profile.pdf"),
    "const": ("Indiana Constitution, Article 6", "Justia", "", "https://law.justia.com/constitution/indiana/art6.html"),
    "sbf": ("State Board of Finance", "Indiana State Comptroller", "", "https://www.in.gov/comptroller/state-board-of-finance/index"),
    "ifa": ("Indiana Finance Authority members", "Indiana Finance Authority", "accessed 2026-10-10", "https://www.in.gov/ifa/about-ifa/indiana-finance-authority-members/"),
    "ipm_earn": ("Indiana State Treasurer Daniel Elliott lauds investment earnings. How does it work?", "WFYI / Indiana Public Broadcasting (via IPM)", "2025-10-02", "https://www.ipm.org/news/2025-10-02/indiana-state-treasurer-daniel-elliott-lauds-investment-earnings-how-does-it-work"),
    "wbaa": ("Democratic nominee for Indiana treasurer calls for greater transparency (TheStatehouseFile)", "WBAA / WFYI", "2026-06-06", "https://www.wbaa.org/statewide/2026-06-06/democratic-nominee-for-indiana-treasurer-calls-for-greater-transparency"),
    "esgdive": ("Indiana state treasurer places BlackRock on ESG watchlist", "ESG Dive", "2024-06-25", "https://www.esgdive.com/news/indiana-state-treasurer-places-blackrock-on-esg-watchlist/719800/"),
    "federalist": ("New laws restrict Indiana treasurer who protects Americans from debanking", "The Federalist", "2025-05-12", "https://thefederalist.com/2025/05/12/new-laws-restrict-indiana-treasurer-who-protects-americans-from-debanking/"),
    "trust_rel": ("Treasurer Elliott applauds legislative action to protect TrustINdiana (office release)", "The Reporter", "2025-04-26", "https://readthereporter.com/?p=145707"),
    "wiki_2022": ("2022 Indiana State Treasurer election", "Wikipedia", "accessed 2026-10-10", "https://en.wikipedia.org/wiki/2022_Indiana_State_Treasurer_election"),
    "wiki_elliott": ("Daniel Elliott (Indiana politician)", "Wikipedia", "accessed 2026-10-10", "https://en.wikipedia.org/wiki/Daniel_Elliott_(Indiana_politician)"),
    "bp_inprs": ("Indiana pension board removes assets from BlackRock's management", "Ballotpedia News", "2024-12-18", "https://news.ballotpedia.org/2024/12/18/indiana-pension-board-removes-assets-from-blackrocks-management-2"),
    "tos_news": ("Archived State Treasurer news", "Indiana Treasurer of State", "", "https://www.in.gov/tos/about-the-office/archived-state-treasurer-news/"),
    "wfyi_launch": ("Indiana State Treasurer Daniel Elliott launches reelection bid", "WFYI (via Indiana Capital Chronicle)", "2025-09-17", "https://www.wfyi.org/public-affairs/2025-09-17/indiana-state-treasurer-daniel-elliott-launches-reelection-bid"),
    "wfyi_aes": ("State treasurer raises concerns over AES/BlackRock deal", "WFYI", "2026-03-04", "https://www.wfyi.org/news/articles/state-treasurer-indiana-aes-blackrock-deal-electric-utilities"),
    "wfyi_guide": ("2026 Voter Guide: Indiana State Treasurer", "WFYI", "2026-10-01", "https://www.wfyi.org/statewide/2026-10-01/2026-voter-guide-indiana-state-treasurer"),
    "refl_elliott": ("Indiana State Treasurer candidate Q&A: Daniel Elliott (Mirror Indy)", "The Reflector (University of Indianapolis)", "2026-10-05", "https://reflector.uindy.edu/2026/10/05/elliott26mi/"),
    "elliott_site": ("Daniel Elliott for Treasurer", "Elliott campaign (danielelliott.org)", "accessed 2026-10-10", "https://danielelliott.org"),
    # Kebe
    "idp": ("Indiana Democrats announce Jessica Bailey and Coumba Kebe as State Comptroller and Treasurer candidates", "Indiana Democratic Party", "2026-05-27", "https://indems.org/press-release/indiana-democrats-announce-jessica-bailey-and-coumba-kebe-as-state-comptroller-and-treasurer-candidates/"),
    "citizen_kebe": ("Coumba Kebe tapped as Democratic nominee for Indiana treasurer (TheStatehouseFile)", "The Indiana Citizen", "2026-06-06", "https://indianacitizen.org/coumba-kebe-tapped-as-democratic-nominee-for-indiana-treasurer/"),
    "ipm_dems": ("Indiana Dems announce treasurer, comptroller candidates", "Indiana Capital Chronicle (via IPM)", "2026-05-28", "https://www.ipm.org/news/2026-05-28/indiana-dems-announce-treasurer-comptroller-candidates"),
    "refl_kebe": ("Indiana State Treasurer – Coumba Kebe", "The Reflector (University of Indianapolis)", "2026-10-05", "https://reflector.uindy.edu/2026/10/05/kebe26/"),
    "citizen_dems": ("DEMOCRAT HOPEFULS: County clerk and business executive seek to end GOP control of 2 statewide offices", "The Indiana Citizen", "2026-05-28", "https://indianacitizen.org/democrat-hopefuls-county-clerk-and-business-executive-seek-to-end-gop-control-of-2-statewide-office/"),
    "stateside_k": ("Coumba Kebe Treasurer Profile", "Stateside", "2026-07-09", "https://www.stateside.com/sites/default/files/2026-07/Coumba%20Kebe%20Treasurer%20Profile.pdf"),
    "rep_jul1": ("Kebe names first co-chair for her state treasurer campaign", "The Reporter", "2026-07-01", "https://readthereporter.com/?p=196759"),
    "rep_jul8": ("Kebe names second co-chair for her state treasurer campaign", "The Reporter", "2026-07-08", "https://readthereporter.com/?p=197145"),
    "rep_jul15": ("Kebe names third co-chair for her state treasurer campaign", "The Reporter", "2026-07-15", "https://readthereporter.com/kebe-names-third-co-chair-for-her-state-treasurer-campaign/"),
    "kebe_site": ("Coumba Kebe for Indiana State Treasurer", "Kebe campaign (kebeforindiana.com)", "accessed 2026-10-10", "https://www.kebeforindiana.com/"),
}

PROFILE = {
    "race_id": "in-treasurer-of-state",
    "reviewed": "2026-10-10",
    "status": "draft",
    "status_note": "Pending editorial review. No debate has been held in this race; investment figures are the office's own.",
    "office": {
        "title": "Indiana Treasurer of State",
        "summary": "The state's banker and chief investment officer. The Treasurer invests state money not needed for immediate bills, chairs boards that run Indiana's college-savings, disability-savings, local-bond, and 911 programs, and sits on the State Board of Finance {about}{stateside_e}{sbf}.",
        "facts": [
            {"label": "Term", "value": "4 years {const}"},
            {"label": "Term limit", "value": "8 years in any 12 {const}"},
            {"label": "Managed daily", "value": "$16 billion+ (office figure) {about}"},
            {"label": "Held by", "value": "Republicans since 1979 {wbaa}"},
        ],
        "duties": [
            "Invests state funds; investment earnings go to the state's General Fund, and the legislature decides how they are spent {ipm_earn}.",
            "Chairs the Indiana Bond Bank, which helps local governments get lower-cost financing for public projects {about}{stateside_e}.",
            "Chairs the Indiana Education Savings Authority (the Indiana529 college and career savings plan) and the ABLE Authority (INvestABLE Indiana accounts for people with disabilities) {about}{stateside_e}.",
            "Chairs the Statewide 9-1-1 Board {about}{stateside_e}.",
            "Runs TrustINdiana, the investment pool for local governments, and is sole trustee of the Indiana State Police Pension Trust {about}.",
            "Member of the three-member State Board of Finance (with the budget director and comptroller) and of the Indiana Finance Authority {sbf}{ifa}.",
        ],
        "recent_changes": [
            "2023 (HEA 1008): requires the Treasurer to review financial firms serving the state's public retirement system that it has reason to believe made environmental, social, or governance (ESG) commitments {esgdive}.",
            "2025: the state budget changed oversight of TrustINdiana, creating a board starting July 1, 2026 {federalist}. Elliott opposed the original budget language and later thanked state leaders for changes he said protected the program {trust_rel}. Published accounts differ on how much authority the new board has.",
        ],
    },
    "incumbent": {
        "name": "Daniel Elliott",
        "party": "Republican",
        "summary": "Elected in 2022 over Democrat Jessica McClellan and took office in January 2023 {wiki_2022}{wiki_elliott}. He is on the ballot seeking a second term {wfyi_guide}.",
        "record": [
            "Investments: the office reports more than $1.2 billion in General Fund investment earnings since he took office {about}. Elliott describes the goal as predictable income for budget writers: \"These are dollars that have got to be there when the time comes to pay the state's bills\" {ipm_earn}. These are the office's figures, not an independent audit.",
            "June 2024: under the 2023 law, placed BlackRock on the state's ESG watch list. BlackRock responded that it is focused on performance and takes direction from its clients {esgdive}.",
            "December 2024: the Indiana Public Retirement System board voted to stop using BlackRock as an asset manager after Elliott argued the firm was ineligible under the 2023 law {bp_inprs}.",
            "2025: the office reported growth in INvestABLE disability-savings accounts and expanded the 529 plan, renamed Indiana529, to cover trade schools and apprenticeships {tos_news}{refl_elliott}.",
            "911: his campaign cites training for more than 400 dispatchers and the launch of text-to-911 and translation services {wfyi_launch}.",
            "March 2026: raised concerns about the proposed sale of AES Corp., parent of utility AES Indiana, to a group of investors including a BlackRock affiliate, while acknowledging the office has no direct authority over the sale. AES said the deal would deliver value to stockholders {wfyi_aes}.",
        ],
    },
    "race_context": [
        "The office has no primary; each party nominates at its state convention {ipm_dems}.",
        "Elliott was renominated without opposition at the Republican convention in June 2026 {wfyi_guide}{stateside_e}; Coumba Kebe was the only Democrat to file and was nominated June 6 {ipm_dems}{wbaa}.",
        "No debate or forum between the treasurer candidates was found as of this review {wfyi_guide}.",
    ],
    "candidates": [
        {
            "ballot_name": "Daniel Elliott",
            "summary": "Incumbent treasurer since 2023 and former Morgan County Council member and software company founder. Says his top priority is continuing strong investment returns {wiki_elliott}{refl_elliott}.",
            "website": "https://danielelliott.org",
            "background": [
                "Grew up in Jennings County and lives in Morgan County; founded a software company in Martinsville {wiki_elliott}.",
                "Bachelor's degree in business and computer science from Utah Valley University {wiki_elliott}.",
                "Served on the Morgan County Council (elected 2016), led the county redevelopment commission, and chaired the Morgan County Republican Party {wiki_elliott}{stateside_e}.",
            ],
            "path_to_ballot": [
                "Launched his re-election campaign Sept. 17, 2025 {wfyi_launch}; renominated without opposition at the Republican state convention June 20, 2026 {stateside_e}.",
            ],
            "positions": [
                {"topic": "Investments", "items": [
                    "\"My top priority as State Treasurer is to continue to make good returns\" {refl_elliott}.",
                    "Opposes considering ESG commitments in public investment decisions and has applied the 2023 law to the state's retirement-system managers {esgdive}{bp_inprs}.",
                ]},
                {"topic": "Savings programs", "items": [
                    "Wants more families using the 529 plan, which now also covers trade schools and apprenticeships {refl_elliott}.",
                ]},
                {"topic": "Utilities", "items": [
                    "Says ratepayers should not carry all of the financial risk in utility ownership changes, while noting the office has no direct authority over utilities {refl_elliott}{wfyi_aes}.",
                ]},
                {"topic": "911", "items": [
                    "Points to dispatcher training and text-to-911 as results he would build on {wfyi_launch}.",
                ]},
            ],
            "on_incumbent": [
                "He is the current officeholder. No statements by him about his opponent were found.",
            ],
            "plans": [
                "Continue investment returns and expand use of the 529 plan {refl_elliott}. No detailed second-term agenda was found.",
            ],
            "endorsements_finance": [
                "No endorsements are listed on his campaign site {elliott_site}. Fundraising totals were not found in news coverage.",
            ],
            "gaps": [
                "He cited $1.8 billion in returns in an October 2026 interview {refl_elliott}; the period that figure covers was not stated.",
                "Reported purchases of Israel bonds (2023–2024) could not be confirmed from a full article for this draft.",
                "Accounts differ on the authority of the new TrustINdiana oversight board.",
            ],
        },
        {
            "ballot_name": "Coumba Kebe",
            "summary": "Health care operations executive and consultant from Noblesville in her first general-election campaign. Says she would review the state's investments and explain them in plain language {idp}{refl_kebe}.",
            "website": "https://www.kebeforindiana.com/",
            "background": [
                "Age 31, of Noblesville; describes herself as a first-generation American {idp}{citizen_kebe}.",
                "Bachelor's degree and Master of Public Health from Indiana University {refl_kebe}{citizen_dems}.",
                "Founded Scope Consulting, which works with home care agencies; previously a director of operations managing multimillion-dollar budgets {stateside_k}{refl_kebe}.",
                "Lost the May 2026 Democratic primary for Indiana House District 29, 53.7% to 46.3% {citizen_dems}. First drew attention through social-media videos on Medicaid and home health policy {citizen_kebe}.",
            ],
            "path_to_ballot": [
                "Announced by the Indiana Democratic Party May 27, 2026, as the only Democrat to file {idp}{ipm_dems}; nominated without opposition June 6, 2026 {wbaa}.",
            ],
            "positions": [
                {"topic": "Investments", "items": [
                    "Says her \"top priority would be to understand our current investment profile\" and report it to the public in plain English {refl_kebe}.",
                    "Describes the job as protecting taxpayer dollars through low-risk investments that maximize returns {refl_kebe}.",
                    "Has questioned how the state built roughly $4 billion in reserves, citing the Medicaid waiver waiting list and rural hospital closures {refl_kebe}.",
                ]},
                {"topic": "Savings programs", "items": [
                    "Would expand the state's 529 college-savings program {rep_jul8}{rep_jul15}.",
                ]},
                {"topic": "Transparency", "items": [
                    "Wants state financial data presented so residents can understand it: \"We've got to make it easy for folks to understand\" {ipm_dems}.",
                    "Notes the treasurer serves on boards that make statewide decisions but does not set policy, and can report findings to the public {refl_kebe}.",
                ]},
                {"topic": "Long-term planning", "items": [
                    "Asks whether Indiana is prepared for the next 20 years, citing workforce shortages, an aging population, and health care access {ipm_dems}.",
                ]},
            ],
            "on_incumbent": [
                "No statements naming Elliott were found. In her nomination speech she said the office \"can be about much more than just spreadsheets and investment reports\" {wbaa}.",
            ],
            "plans": [
                "Review the state's investment profile and publish it in plain language; expand the 529 program {refl_kebe}{rep_jul8}.",
            ],
            "endorsements_finance": [
                "Campaign co-chairs: state Reps. Earl Harris Jr. and Cherrish Pryor, and Hamilton County Democratic Chair Josh Lowry {rep_jul1}{rep_jul8}{rep_jul15}.",
                "Fundraising totals could not be confirmed for this review.",
            ],
            "gaps": [
                "No published positions found on ESG-related investment rules, bank deposits of state funds, ABLE accounts, or the Bond Bank.",
                "Her campaign's issues page was unavailable; positions come from interviews and announcements {kebe_site}.",
            ],
        },
    ],
}


def main():
    build_profile(PROFILE, S)


if __name__ == "__main__":
    main()
