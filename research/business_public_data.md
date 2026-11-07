# Jane Street — public business and regulatory record

Compiled 2026-11-07 as source material for agent personas: a market-maker or trader reasoning persona, and an analyst persona that understands the firm.

**How to read this file.** Every claim has a source number in brackets. Sources are listed at the end with URLs and dates.
- **[P]**: primary document that was retrieved and read in this session. This covers SEC EDGAR, FINRA BrokerCheck, SEBI, Jane Street's own website and the Kaggle URLs.
- **[R]**: reported by press, usually citing unnamed people or documents seen by the reporter. Jane Street is private and publishes no earnings, so all P&L figures below are [R] unless they are marked otherwise.
- **UNCONFIRMED**: secondary-only, or sources conflict.

---

## 1. Firm structure

### 1.1 Legal entities

| Entity | Role | Evidence |
|---|---|---|
| Jane Street Group, LLC (JSG), Delaware | Parent and holding company. It files 13F-HR as the reporting manager, plus 13G/13D, Forms 3/4 and N-PX. Address: 250 Vesey St, New York, NY 10281. EDGAR CIK 0001595888; 13F file no. 028-16162. | [P1][P2] |
| JSHC, LLC → JSHP, LLLP | Indirect owners of JSG. BrokerCheck lists JSHC, LLC as an indirect owner (75%+, since 10/2019) through JSG, and JSHP, LLLP as an indirect owner through JSHC. BrokerCheck also lists 8 individuals as "Management Committee Member / Other General Partners"; most of these relationships were established 12/2024. | [P6] |
| Jane Street Capital, LLC (JSC) | US broker-dealer, FINRA CRD 103782, SEC 8-52275. Member of the SEC, FINRA and 29 SROs; recent exchange approvals include 24X (10/2025) and Texas Stock Exchange (06/2026). The audited 2025 statement says JSC "trades for its own account and is a market-maker on certain exchanges" and "acts as an authorized participant in order to create and/or redeem exchange traded funds". It is a DTC/NSCC member. Its designated examining authority is FINRA, and its auditor is EY (since 2012). | [P3][P6] |
| Jane Street Execution Services, LLC | US broker-dealer, CRD 167280. Files X-17A-5. | [P1][P6] |
| Jane Street Options, LLC | US broker-dealer and options market maker, CRD 134159, SEC 8-66813. | [P1][P6] |
| Jane Street Derivatives Dealer, LLC | Formed 2023-04-13. Filed Form SBSE on 2026-05-18 to register as an SEC security-based swap dealer, with amendments on 2026-09-04 and 2026-09-25. The form flags `isSwapDealer=Y`. Business description: "dealing of security-based swaps". CIK 0002117967. | [P1][P4] |
| Jane Street Global Trading, LLC | 13F "other included manager", 028-13275. | [P2] |
| JSOIN (BVI), Ltd. | 13F other included manager, 028-15040. | [P2] |
| Jane Street Europe Ltd (UK) | 13F other included manager, 028-22194, CIK 0001907807. SEBI cites it as the holding company of JSI Investments Pvt Ltd. | [P2][P8] |
| Jane Street Financial Limited (UK FCA); Jane Street Netherlands B.V. (AFM) | Regulated entities in Europe. | [P10] |
| Jane Street Hong Kong Limited (SFC) | Regulated entity in Hong Kong. | [P10] |
| Jane Street Asia Trading Ltd (HK) | Named in the SEBI order. CIK 0002056822; 13F 028-26044. | [P1][P2][P8] |
| Jane Street Singapore Pte. Ltd | Named in the SEBI order. CIK 0002057057; 13F 028-25383. | [P1][P2][P8] |
| Jane Street Asia Limited | The affiliate fined by the South Korean FSC (see §4.4). | [P6] |
| JSI Investments Pvt Ltd; JSI2 Investments Pvt Ltd (India) | Indian entities named in the SEBI order. JSI is held by Jane Street Europe Ltd, with JSG as ultimate parent. JSI2 is wholly owned by JSI. | [P8] |
| Edgar Street Capital, LLC (2001); Elizabeth Street Capital, LLC (2021) | Employees' securities companies that invest solely in JSG securities. JSG applied for a 1940 Act §6(b)/(e) exemption, file 813-00403, with amendment no. 4 filed 2024-07-17. | [P5] |

**Inactive or legacy EDGAR filers:** Jane Street Holding, LLC (13F filer 2005–2014), Jane Street Holding II, Jane Street Trading, Jane Street Markets (formerly Nassau Street Capital), Jane Street Specialists (formerly Bowery Specialists Group) and Jane Street Market Enhancement Fund LP (one REGDEX filing in 2007). [P1]

### 1.2 Offices and headcount trajectory

- **Offices.** Jane Street's culture page lists Amsterdam, Chicago, Hong Kong, London, New York and Singapore; its largest offices are New York, London, Hong Kong and Singapore [P11]. The "Who we are" page says "more than 3000 employees across five global offices" and "more than 200 venues in 45 countries" [P12].
- **Headcount, in order:**
  - 2,631 at end-2023, per the April 2024 bond prospectus as reported by the FT [R16].
  - "More than 2,500 full-time employees, approximately 1,500 of whom are based in New York" as of 2024-06-30 [P5, SEC filing].
  - SEBI's July 2025 order, quoting Jane Street's site, says "more than 2,600 people in five offices" [P8].
  - Jane Street's site, retrieved 2026-11-07, says "more than 3000" [P12].
  - About 3,500 is reported for 2025/2026 [R18][R19].
- **Partnership model.**
  - The FT, from the prospectus, reported 40 equity unit holders with average tenure of 16 years, and employee equity at about 80% of capital [R16].
  - Jane Street's site describes employees as "partners working together toward shared goals" [P12].
  - The firm has historically had no CEO and is reported to be led informally by 30–40 senior people [R17, via Wikipedia citing the FT].
  - Reuters reports the firm "has taken on no outside capital" [R18].

### 1.3 Founders (professional history only)

- **Founding team.** Tim Reynolds, Rob Granieri and Michael Jenkins were traders at Susquehanna International Group (SIG); Marc Gerstein was an IBM developer [R17].
- **Founding date.** Jane Street's own materials say 2000: the 40-6B filing says "Founded in 2000" [P5], and the website says "Established in 2000" [P12]. Wikipedia gives 1999-08-31. This is UNCONFIRMED and possibly a predecessor entity [R17].
- **Early business.** The firm started with ADR arbitrage and equity options on the AMEX floor, then made ETFs its main focus [R17].
- **SIG litigation.** SIG sued the new firm over alleged poaching and non-compete breaches. The case is reported as dormant [R17].
- **Reynolds** stepped back from running the firm in 2012 [R17].
- **Granieri** is reported to be the only founder still at the firm in 2026 [R17].

---

## 2. Financials (all P&L figures are press-reported unless marked P)

### 2.1 Net trading revenue

| Period | Net trading revenue | Other reported figures | Source |
|---|---|---|---|
| 2020–2022 | >$10bn per year. The FT says 2023 was the "fourth straight year" above $10bn. | — | [R16] |
| 2023 | $10.5bn (FT) / $10.6bn (Bloomberg, "roughly flat" vs 2022) | Gross revenue $21.9bn, up 34% YoY. Adjusted EBITDA about $7.4bn (Bloomberg). Comp and benefits $2.4bn. Members' equity $21.3bn. Total assets $140.2bn. Asia was 14% of net revenue (12% in 2022). | [R16][R20] |
| Q1 2024 | $4.4bn | Members' equity >$24bn | [R16] |
| 2024 | $20.5bn | Members' equity $29.9bn (+40%). Net trading revenue of $6.9m per employee. India equity derivatives >$2.3bn (more than 10% of the total). Q3 2024: $5.79bn. | [R21][R22][R24] |
| H1 2025 | $17.3bn | Q2 2025: $10.1bn revenue and $6.9bn net income. India was about 3% of H1 (≈$500m). | [R23][R22] |
| Q3 2025 | $6.83bn | — | [R24] |
| Q4 2025 | $15.5bn | — | [R25] |
| FY 2025 | $39.6bn | Adjusted EBITDA about $31.2bn. About 3,500 employees. Revenue per employee >$11m. Pay pool $9.38bn, about $2.68m average. Gains on private stakes (including Anthropic) lifted profit. | [R18][R25][R26] |
| Q1 2026 | $16.1bn | Net income $10.3bn | [R19][R28] |
| Jul 2026 | About −$15bn monthly trading loss, the first losing month since about 2016 | Linked to a stake in Situational Awareness (an AI hedge fund) and to "wrong-way" Asian equity bets. Revenue was about 25% below the late-June peak. | [R29][R30] |
| YTD to Jul 2026 | >$40bn, already above all of 2025 | — | [R29][R30] |

No Q2 2026, H1 2026 or Q3 2026 figure from a credible outlet was found. One aggregator's "Q2 2026 $10.1bn" is a relabelled Q2 2025 number and should not be used. That point is UNCONFIRMED and excluded.

### 2.2 Regulatory financial statements (primary)

These come from the Jane Street Capital, LLC audited consolidated statement of financial condition as of 2025-12-31, filed on X-17A-5 on 2026-02-26 [P3]. Amounts are USD thousands.
- **Totals:**
  - Total assets: 60,704,881
  - Total liabilities: 54,424,524
  - Member's equity: 6,280,357
- **Largest assets:**
  - Securities owned at fair value: 41,699,698
  - Owned and pledged: 3,223,669
  - Due from brokers and clearing: 13,913,555
- **Largest liability:** securities sold, not yet purchased: 45,011,999
- **Net capital:** $1.91bn under the alternative standard of Rule 15c3-1. The requirement is $1m.
- **Subsequent events (2026):** convertible loans from the parent rose to $3.04bn, and the parent contributed $1.65bn of capital.

### 2.3 Debt, ratings and offering documents

Jane Street's bond offering memoranda are private (144A) and are not on EDGAR. Most public P&L figures first came from them, via the FT, Bloomberg and fi-desk.

- **Debt timeline:**
  - **Nov 2021:** $600m 4.50% 8-year senior secured notes, due 2029. At that time Moody's affirmed Ba1 corporate family and Ba2 senior secured first-lien term loan, and assigned Ba2 to the notes [R31][R32].
  - **Apr 2024:** about $1.25bn of 7.125% notes due 2031 (later tapped). S&P rated them BB [R33].
  - **Apr 2025:** $1.35bn 6.75% notes due 2033, taking issuance to $5.4bn since Jan 2024.
    - Stack before that deal: $4.7bn SOFR term loan B; 4.50% 2029 ($600m); 7.125% 2031 ($1.4bn); 6.125% 2032 ($1.65bn).
    - $1bn revolver, fully drawn as of mid-April 2025.
    - Liquidity buffer $6.4bn.
    - Pro-forma long-term debt $10.7bn, about one quarter of total capital.
    - S&P risk-adjusted capital (RAC) ratio 12.3%.
    - Indenture: 2:1 trading-capital ratio test [R21].
  - **Aug 2026:** $14.6bn of senior secured notes in three tranches: 7.294% due 2031-08-13, 7.686% due 2033-08-13 and 8.088% due 2036-08-13. JPMorgan led. Reported buyers include PIMCO, Capital Group and Fidelity. Proceeds refinance the $5.5bn term loan B and the $5.7bn of outstanding secured notes (about $11.1bn per S&P); the rest goes to trading capital [R34][R30].
- **Ratings:**
  - **S&P:** BB issuer and debt.
    - Nov 2024: outlook moved to positive.
    - 2025-07-15: outlook back to stable, citing the SEBI action, rapid balance-sheet growth and higher VaR. The RAC ratio was about 12% in Q2 2025, versus 16% in June 2024 [R35].
    - Aug 2026: BB on the new notes [R34].
  - **Moody's:** Ba1 long-term issuer. Fi-desk reports an affirmation in July 2026 with the outlook moved from positive to stable, and says Moody's did not rate the 2026 notes [R34]. Another secondary source says four operating companies are rated Baa3. That is UNCONFIRMED [R36].
  - **Fitch:** BB+ on the 2025 notes [R21]. Upgraded to BBB- (investment grade), stable outlook, reportedly on 2026-07-24 [R36][R37]. This is UNCONFIRMED because fitchratings.com could not be reached from this environment.

---

## 3. Business lines

- **ETF market making and authorized participant (AP).** These figures are from the FT's reading of the 2024 prospectus [R16]:
  - $527bn average monthly ETF trading in 2023.
  - 14% of US and 20% of European ETF volume.
  - As AP, 24% of US-listed ETF primary-market activity: 28% of international-equity ETFs, 12% of US-equity ETFs and 41% of fixed-income ETFs.

  JSC confirms its AP role in its audited statement [P3]. It was named an AP by spot-bitcoin ETF applicants including BlackRock, Fidelity, WisdomTree and Valkyrie in 2023 [R38].
- **Bonds.**
  - In 2023: about $179bn of fixed-income portfolio trading [R16].
  - Electronic share of 42% in US investment grade and 31% in high yield [R16].
  - About $230bn average monthly fixed-income volume in 2024 [R17].
- **Options.** $32tn notional in 2023, about 7.6% of OCC contract volume [R16]. About 8% of OCC volume in 2024 [R17].
- **Equities.** North American equity share was 10.4% in 2023, up from 7.6% in 2022, and the firm trades more than 2% in over 20 countries [R16]. It receives retail payment for order flow, e.g. from Robinhood [R17].
- **Private and venture stakes.**
  - Reuters reports a capital-markets unit investing "from seed stage to going public" [R18].
  - Reported stakes include Anthropic (reportedly bought from the FTX estate in 2024; UNCONFIRMED in detail), CoreWeave and Situational Awareness LP [R29][R39].
  - A "$20bn private portfolio" figure appears only in secondary sources and is UNCONFIRMED [R39].
- **Crypto.**
  - Bloomberg reported on 2023-05-09 that Jane Street pulled back from US crypto trading over regulatory uncertainty [R40].
  - Sam Bankman-Fried and Caroline Ellison of FTX/Alameda are former Jane Street employees [R17].
  - Terraform Labs' administrator sued in Feb 2026 (§4.3) [R27].
  - Reported spot-bitcoin and other crypto ETF positions are visible in 13F filings and can be checked there (§6).
- **India.** Index options on NSE through the Singapore, HK and India entities [P8].
  - Revenue was about $1bn in 2023 for the strategy surfaced in the Millennium case (UNCONFIRMED as a full India figure), >$2.3bn in 2024, and about $500m in H1 2025 [R22][R23].
  - SEBI's computation of the four entities' total NSE profit for Jan 2023–Mar 2025 is ₹36,502.12 crore. Index options made ₹43,289.33 crore, offset by ₹7,687.21 crore of losses in futures and cash [P8].
- **Technology.** OCaml is the main language and Python is used for ML [R17]. Interview candidates do not need OCaml [P13].

---

## 4. Regulatory and legal record

### 4.1 SEBI, India: index manipulation (open)

- **The order.** SEBI's ex parte interim order is ref. WTM/AN/MRD/MRD-SEC-3/31516/2025-26, dated **2025-07-03**, 105 pages, issued under SEBI Act §§11(1), 11(4), 11B(1) and 11D [P8].
  - Entities: JSI Investments, JSI2 Investments, Jane Street Singapore and Jane Street Asia Trading.
  - Examination period: Jan 2023–Mar 2025.
- **How the probe started.** It was triggered by April 2024 press coverage of the Millennium case [P8]. SEBI's chronology:
  - NSE asked to examine the trading on 2024-07-23.
  - Jane Street's written submission on 2024-08-30.
  - NSE caution letter on 2025-02-06.
  - Jane Street's replies on 6 and 21 Feb 2025.
  - On 2025-05-15, SEBI says the large positions continued despite the caution.
- **The alleged strategies** [P8]:
  - **"Intra-day Index Manipulation."** Patch I: aggressive morning buying of BANKNIFTY constituent stocks and futures (e.g. ₹4,370 crore on 2024-01-17) while building far larger short index-option exposure. Patch II: unwinding the cash and futures longs later in the day. SEBI calls the ₹199.7 crore intraday loss across 15 days a "mala fide cost" of the scheme.
  - **"Extended Marking the Close."**
- **The money.** SEBI identified 21 days: 18 BANKNIFTY days in 2023–24 and 3 NIFTY days in May 2025. Alleged unlawful gains of **₹4,843.57 crore** (₹48,43,57,70,168) were ordered impounded [P8].
- **What the order did.** It barred the entities from the securities market, with the bar to lift once the money was deposited in escrow (paras 62.1–62.13) [P8].
- **Escrow and partial lifting.**
  - SEBI PR 40/2025 (2025-07-14): Jane Street credited the full amount to an escrow account with a lien in SEBI's favour, "without prejudice" [P9a].
  - SEBI PR 45/2025 (2025-07-21): the market-access restrictions ceased under para 62.11. The entities must cease and desist from the identified patterns, and the exchanges must monitor them [P9b].
  - Reuters reported an undertaking not to trade options [R41].
  - Bloomberg reported in Oct 2026 that the firm had **not resumed trading in India** [R43]. This is reported, not confirmed.
- **Jane Street's response.** It disputes the findings, describes the activity as basic index arbitrage, and sought extensions to reply [R17][R41].
- **Appeal: JSI Investments Pvt Ltd v. SEBI, SAT Appeal No. 413 of 2025.**
  - Filed about 2025-09-03. It seeks SEBI and NSE records and alleges bias.
  - On 2025-09-10, SAT gave SEBI three weeks to reply and listed the matter for 2025-11-18 [R42].
  - In Oct 2026, SEBI told SAT it had shared the relied-upon trade logs (time, price and quantity). It withheld counterparty names and tax IDs and up to 60 SEBI–NSE emails, called the request "dilatory", and said the probe could lead to a "much wider" final order [R43][R44].
  - **2026-10-21: SAT reserved its order** on the disclosure plea. Bench: Justice P.S. Dinesh Kumar, Meera Swarup and Dr. Dheeraj Bhatnagar [R45].
- **Still open.**
  - No show-cause notice and no final SEBI order were found as of 2026-11-07.
  - Wikipedia states that SAT denied a document request in Nov 2025. That is UNCONFIRMED and conflicts with the Oct 2026 reports that the disclosure plea was still being argued.
- **Ratings impact.** S&P cited the SEBI action when it moved its outlook to stable on 2025-07-15 [R35].

### 4.2 Jane Street Group v. Millennium Management (closed)

- **The case.** *Jane Street Group LLC v. Millennium Management LLC et al.*, SDNY **1:24-cv-02783**, Judge Paul A. Engelmayer. Filed April 2024 against Millennium and two former Jane Street traders. It alleged misappropriation of an India options trading strategy [R46][R47].
- **During the case.** The TRO was denied, the defendants' "unclean hands" defense was struck, and the counterclaims were dismissed in July 2024 [R47].
- **Outcome.** A joint stipulation of dismissal was filed on **2024-12-05**. Both sides said it was "resolved on mutually agreeable terms", and the terms are undisclosed [R46][R48].
- **Consequence.** The case is the documented origin of SEBI's probe [P8].

### 4.3 Terraform Labs administrator v. Jane Street (open)

- **The suit.** *Snyder v. Jane Street Group, LLC et al.*, SDNY, filed about **2026-02-23** by Todd Snyder, Terraform's plan administrator. Law360 lists two docket numbers, 1:26-cv-01504 and 1:26-cv-01536; which one is operative is UNCONFIRMED [R27][R49].
  - Defendants: JSG and three individuals, including a former Terraform intern.
- **Allegations** [R27]:
  - Front-running during the May 2022 UST depeg, using non-public information obtained through a former-colleague back-channel.
  - On 2022-05-07, a wallet allegedly linked to Jane Street withdrew 85m UST from Curve 3pool within 10 minutes of Terraform's unannounced 150m UST withdrawal.
- **Damages.** The $4bn figure in some headlines refers to Snyder's separate December 2025 suit against Jump Trading [R27].
- **Jane Street's response.** It called the collapse a "multibillion-dollar fraud" by Terraform's management and the claims "opportunistic" [R27]. It moved to dismiss with prejudice in Apr 2026, arguing market-signal trading and the Wagoner rule [R50]. The administrator opposed in June 2026 [R49].
- **Status.** No ruling was found.

### 4.4 US and other regulatory actions (FINRA BrokerCheck, primary [P6], retrieved 2026-11-07)

Disclosures on the broker-dealer records (all final):

| Firm | Action | Date | Sanction |
|---|---|---|---|
| JSC | FINRA AWC 2015046614501: OATS reporting of ROEs and written supervisory procedures | 2017-05-23 | Censure, $85,000 |
| JSC | NYSE Arca / FINRA STAR 20110279134 (opened 2011-09-26) | Resolved 2013-11-14 | Censure, $150,000 |
| Jane Street Options | Nasdaq PHLX AWC 2022.10.0406: supervision of quote-width rules, Aug 2022–Apr 2025 | 2025-07-28 | Censure, $25,000 |
| Jane Street Options | Cboe, File URE-259-01: a floor-broker discretion arrangement linked to one of those former traders (§4.2) (Rule 8.1 just and equitable trade; Rule 8.16 supervision), May 2021–Nov 2022 | 2024-12-27 | Censure, $650,000 (joint and several) |

Control-affiliate disclosures:

| Affiliate | Regulator and matter | Date | Sanction |
|---|---|---|---|
| Jane Street Asia Ltd | Korean FSC: hedging ahead of a reportable block trade (Oct 2019) breached market-disruption rules | Decided 2024-02-01 | KRW 281.2m (≈$215k) |
| JSG | Finanstilsynet (Norway): late net-short reporting in Mar/May 2020 | 2021-01-21 | ≈$3,500 |

- **SEBI not shown.** The SEBI interim order does not appear as a disclosure; all counts show 0 pending events.
- **Other matters [R17]:** Jane Street and Elliott sued the LME over cancelled March 2022 nickel trades. The case was dismissed in Nov 2023 and the appeal rejected in Oct 2024.
- **SEC.** No SEC enforcement action against a Jane Street entity was found.
- **CFTC/NFA.** Jane Street Derivatives Dealer's 2026 Form SBSE answers `isSwapDealer=Y` [P4]. CFTC swap-dealer registration on the NFA list is UNCONFIRMED: the CFTC list snippet as of 2026-01-15 showed no Jane Street entry [R51]. To confirm, check NFA BASIC (§6).

---

## 5. Culture, hiring and compensation

- **Published values.** "Ethics and Honesty", "Responsible Risk Management", "Intellectual Humility" and "Less hierarchy, more collaboration" [P12]. The firm describes itself as "Persistent, humble, and curious" [P10]. The "no titles" norm appears only in reporting (no CEO, informal leadership) [R17]; the site's wording is "less hierarchy".
- **Interviews** [P13][P14]:
  - The process is recruiter contact, then phone, then on-site.
  - Trading interviews are run by traders and cover problem solving, probability and statistics, coding in any language, data analysis and general interests.
  - The firm says "We won't test you on knowledge of finance or economics", and no advanced math is required.
  - The Probability & Markets guide at `/static/pdfs/trading-interview.pdf` covers expected value, betting and market making.
  - Mock-interview videos are on `/trading-interviews` and `/mock-interview` (software engineering).
  - OCaml is not required.
  - Reapplicants wait about one year. No weekend interviews.
  - The "mock trading" game is described in third-party accounts but **not** on the official interviewing page.
- **Compensation (reported only):**
  - 2023: comp and benefits $2.4bn, more than $900k per head [R16].
  - 2025: pay pool $9.38bn, about $2.68m average per head across about 3,500 staff [R26].
  - UK filings showed an average of $1.25m across 688 UK employees in 2024. This is secondary and UNCONFIRMED [R19].
  - Pay is reportedly based on the firm's collective P&L, not individual P&L [R17].
- **Employee ownership.** Edgar Street and Elizabeth Street are employee funds that invest solely in JSG equity [P5].
- **Turnover.** Reported at 6% over two years [R16].

---

## 6. Public datasets and how to pull them

### 6.1 Verified EDGAR identifiers (data.sec.gov, retrieved 2026-11-07)

| CIK | Name | Filings on record |
|---|---|---|
| 0001595888 | JANE STREET GROUP, LLC | 13F-HR ×50 (2014Q1→2026Q2), SC 13G/13G-A ≈250, N-PX, Forms 3/4, 40-6B |
| 0001103083 | JANE STREET CAPITAL, LLC (/BD) | X-17A-5 (annual audited), FOCUSN |
| 0001450698 | Jane Street Capital, LLC (13F filer ID) | 13F-NT, N-PX |
| 0001315511 / 0001450709 | Jane Street Options, LLC (BD / 13F-NT) | X-17A-5, 13F-NT |
| 0001572095 | JANE STREET EXECUTION SERVICES, LLC | X-17A-5 |
| 0001450705 | Jane Street Global Trading, LLC | 13F-NT, N-PX |
| 0001907807 | Jane Street Europe Ltd | 13F-NT, N-PX |
| 0002057057 | Jane Street Singapore Pte. Ltd | 13F-NT (from 2025) |
| 0002056822 | Jane Street Asia Trading Ltd | 13F-NT (from 2026) |
| 0002117967 | Jane Street Derivatives Dealer, LLC | SBSE, SBSE-A, SBSE-C (2026) |
| 0001330294, 0001450167, 0001103219, 0001126385, 0001450710, 0001450706, 0001450707, 0001420533 | Legacy entities | Inactive |

### 6.2 13F: what the data shows

- **Reporting structure.** JSG files a combined 13F-HR. The affiliates file 13F-NT pointing to it.
- **Q2 2026 filing** (period 2026-06-30, filed 2026-08-14, accession 0001595888-26-000108) [P2]:
  - 14,718 rows totalling $1,205.6bn. Of that, calls are $472.9bn, puts $575.6bn and shares $157.1bn. Option rows are reported at the value of the underlying, so the headline total overstates the firm's economic exposure.
  - Largest share line: SPY $33.1bn. Next: AMZN, SNDK, NVDA, QQQ, MSFT, STX, CRWV, IEMG and META.
- **Growth** (values in the XML are in thousands before 2023 and in dollars from 2023):

  | Period | Rows | Total value |
  |---|---|---|
  | 2014Q2 | 2,785 | $7.9bn |
  | 2019Q4 | 6,621 | $71.7bn |
  | 2021Q4 | 13,305 | $303bn |
  | 2023Q4 | 14,115 | $384bn |
  | 2024Q4 | 14,140 | $460bn |
  | 2025Q4 | 17,120 | $662bn |
  | 2026Q2 | 14,718 | $1,206bn |

- **Next filing.** The Q3 2026 13F is due about 2026-11-14.

### 6.3 Pull recipes (all endpoints verified with HTTP 200 in this session)

```sh
UA="research-bot admin@example.com"   # SEC requires a descriptive UA; generic placeholder

# Entity list / CIK lookup
curl -s -A "$UA" "https://efts.sec.gov/LATEST/search-index?keysTyped=jane%20street"

# All filings metadata for the parent (JSON; filings.recent.{form,accessionNumber,reportDate,primaryDocument})
curl -s -A "$UA" "https://data.sec.gov/submissions/CIK0001595888.json"

# Human browse view, 13F only
#   https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001595888&type=13F-HR&dateb=&owner=include&count=40

# One 13F: index -> info table XML
curl -s -A "$UA" "https://www.sec.gov/Archives/edgar/data/1595888/000159588826000108/index.json"
curl -s -A "$UA" "https://www.sec.gov/Archives/edgar/data/1595888/000159588826000108/q2-2026-13f-hr.xml" -o q2-2026.xml
#   infoTable fields: nameOfIssuer, titleOfClass, cusip, value, shrsOrPrnAmt, putCall, investmentDiscretion, otherManager

# Cover-page totals only (cheap)
curl -s -A "$UA" "https://www.sec.gov/Archives/edgar/data/1595888/000159588826000108/primary_doc.xml" | grep -E 'tableEntryTotal|tableValueTotal'

# Bulk alternative: SEC quarterly Form 13F data sets (all filers, TSV)
#   https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets   (filter FILINGMANAGER/CIK = 1595888)

# Broker-dealer audited balance sheet (public part of X-17A-5; scanned PDF -> OCR with pdftoppm+tesseract)
curl -s -A "$UA" "https://www.sec.gov/Archives/edgar/data/1103083/000110308326000004/jscpublic2025.pdf" -o jsc2025.pdf

# Full-text search (2001+): e.g. ETF prospectuses naming Jane Street as AP
curl -s -A "$UA" 'https://efts.sec.gov/LATEST/search-index?q=%22Jane%20Street%22%20%22authorized%20participant%22&dateRange=custom&startdt=2026-01-01&enddt=2026-11-07'
#   UI: https://efts.sec.gov/LATEST/search-index is the API behind https://www.sec.gov/edgar/search/
```

Rate limit: keep requests to SEC under 10 per second.

### 6.4 Other public data

- **FINRA BrokerCheck.**
  - API: `https://api.brokercheck.finra.org/search/firm?query=jane%20street&wt=json`. Detail: `.../search/firm/103782?wt=json`.
  - PDF: `https://files.brokercheck.finra.org/firm/firm_103782.pdf`. Also 134159 (Options) and 167280 (Execution Services).
  - CRDs: 103782 (JSC), 134159 (JSO) and 167280 (JSES). Inactive: 103790, 104485 and 118232 [P6].
- **SEBI.** Interim order PDF: `https://www.sebi.gov.in/sebi_data/attachdocs/jul-2025/1751584518593.pdf` [P8]. Press releases: PR 40/2025 at `.../jul-2025/1752468099869.pdf` and PR 45/2025 at `.../jul-2025/1753110530398.pdf` [P9]. The order also gives the PANs of the four entities.
- **Kaggle** (both URLs return 200) [P15][R52]:
  - *Jane Street Market Prediction* (2020–21): `https://www.kaggle.com/competitions/jane-street-market-prediction`. Anonymized features feature_0–129, a binary action target and a utility-score metric. About 5.8 GB.
  - *Jane Street Real-Time Market Data Forecasting* (2024–25): `https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting`. Anonymized "responders", an evaluation API and about 11.5 GB.
- **Not pulled in this session.** Pointers only, all to verify:
  - FINRA OTC Transparency (non-ATS weekly volume by firm): `https://otctransparency.finra.org`.
  - Exchange lead/designated market-maker assignment lists (Cboe, NYSE Arca).
  - Rule 605/606 market-center reports.
  - NFA BASIC for CFTC registrations: `https://www.nfa.futures.org/BasicNet/`.
  - UK Companies House accounts for Jane Street Europe Ltd and Jane Street Financial Ltd.
  - data.gov: nothing Jane-Street-specific was found.

---

## Sources

**Primary documents (retrieved 2026-11-07)**
- [P1] SEC EDGAR submissions JSON, for each CIK in §6.1: https://data.sec.gov/submissions/CIK0001595888.json (and the same pattern for the other CIKs).
- [P2] JSG Form 13F-HR, period 2026-06-30, filed 2026-08-14: https://www.sec.gov/Archives/edgar/data/1595888/000159588826000108/
- [P3] Jane Street Capital, LLC, consolidated statement of financial condition at 2025-12-31 (X-17A-5, filed 2026-02-26; EY opinion dated 2026-02-26): https://www.sec.gov/Archives/edgar/data/1103083/000110308326000004/jscpublic2025.pdf
- [P4] Jane Street Derivatives Dealer, LLC Form SBSE, filed 2026-05-18: https://www.sec.gov/Archives/edgar/data/2117967/000211796726000001/primary_doc.xml
- [P5] JSG / Edgar Street / Elizabeth Street Form 40-6B/A (Amendment 4), filed 2024-07-17: https://www.sec.gov/Archives/edgar/data/1595888/000110465924080268/tm2419560d1_406ba.htm
- [P6] FINRA BrokerCheck reports for CRD 103782, 134159 and 167280: https://files.brokercheck.finra.org/firm/firm_103782.pdf , https://files.brokercheck.finra.org/firm/firm_134159.pdf , https://files.brokercheck.finra.org/firm/firm_167280.pdf
- [P8] SEBI interim order, Index manipulation by Jane Street Group, 2025-07-03: https://www.sebi.gov.in/sebi_data/attachdocs/jul-2025/1751584518593.pdf
- [P9a] SEBI PR 40/2025, 2025-07-14: https://www.sebi.gov.in/sebi_data/attachdocs/jul-2025/1752468099869.pdf
- [P9b] SEBI PR 45/2025, 2025-07-21: https://www.sebi.gov.in/sebi_data/attachdocs/jul-2025/1753110530398.pdf
- [P10] Jane Street, "What we do": https://www.janestreet.com/what-we-do/overview/
- [P11] Jane Street, Culture overview: https://www.janestreet.com/culture/overview/
- [P12] Jane Street, "Who we are": https://www.janestreet.com/who-we-are/
- [P13] Jane Street, Interviewing: https://www.janestreet.com/join-jane-street/interviewing/
- [P14] Jane Street, Trading interviews: https://www.janestreet.com/trading-interviews ; guide: https://www.janestreet.com/static/pdfs/trading-interview.pdf
- [P15] Kaggle competition pages, as listed in §6.4.

**Reported or secondary sources**
- [R16] FT Alphaville (Robin Wigglesworth), "Jane Street is big. Like, really, really big", 2024-04-29 (mirror): https://hn.jakechampion.name/reader/https://www.ft.com/content/54671865-4c7f-4692-a879-867ef68f0bde
- [R17] Wikipedia, "Jane Street Capital", accessed 2026-11-07, used only for items cited to FT, Bloomberg or Reuters: https://en.wikipedia.org/wiki/Jane_Street_Capital
- [R18] Reuters (Anirban Sen), "Jane Street's $40 billion trading haul tops rivals, sources say", 2026-04-24: https://www.marketscreener.com/news/jane-street-s-40-billion-trading-haul-tops-rivals-sources-say-ce7f59dfdf8ff52d
- [R19] Crypto Briefing, "Jane Street expands workforce to 3,500", 2026: https://cryptobriefing.com/jane-street-expands-workforce-hiring/
- [R20] Bloomberg, "Jane Street Scores $10.6 Billion Trading Haul", Apr 2024: https://au.finance.yahoo.com/news/jane-street-scores-10-6-164545934.html
- [R21] The DESK / fi-desk, "Jane Street issues US$1.35 billion bond…", Apr 2025: https://www.fi-desk.com/jane-street-issues-us1-35-billion-bond-as-market-makers-bulk-up-balance-sheets/
- [R22] Business Standard / Bloomberg, "Jane Street nets $2.3 bn from booming India equity options trading", 2025-05-23: https://www.business-standard.com/amp/markets/news/jane-street-nets-2-3-bn-from-booming-india-equity-options-trading-125052301072_1.html
- [R23] Bloomberg (Doherty, Chakraborty), "Jane Street's India Revenue Shrank…", 2025-09-03: https://news.bloomberglaw.com/private-equity/jane-streets-india-revenue-shrank-amid-misconduct-allegations ; Bloomberg, "Jane Street's $10.1 Billion Trading Haul Sets Wall Street Record", 2025-09-02: https://www.bloomberg.com/news/articles/2025-09-02/jane-street-s-10-1-billion-trading-haul-sets-wall-street-record
- [R24] Bloomberg, "Jane Street Trading Revenue Up 18%, on Pace for Record Year", 2025-12-01: https://www.bloomberg.com/news/articles/2025-12-01/jane-street-trading-revenue-rises-18-on-pace-for-record-year
- [R25] Investing.com / Bloomberg, "Jane Street Group posts record $39.6 billion trading revenue", 2026-04-24: https://www.investing.com/news/economy-news/jane-street-group-posts-record-396-billion-trading-revenue-93CH-4636250
- [R26] Bloomberg Law, "Jane Street's Pay Pool More Than Doubled to $9.4 Billion in 2025", about 2026-05-01: https://news.bloomberglaw.com/securities-law/jane-streets-pay-pool-more-than-doubled-to-9-4-billion-in-2025
- [R27] The Block, "Terraform Labs sues Jane Street…" (citing WSJ), 2026-02-23: https://www.theblock.co/post/390915/terraform-labs-sues-jane-street
- [R28] Bloomberg, "Jane Street Pulls In Record $16.1 Billion Quarterly Trading Haul", 2026-05-08: https://www.bloomberg.com/news/articles/2026-05-08/jane-street-pulls-in-record-16-1-billion-quarterly-trading-haul
- [R29] Fortune / Bloomberg (Doherty, Natarajan, Benitez), Jane Street July loss, 2026-08-15: https://fortune.com/2026/08/15/jane-street-loss-15-billion-situational-awareness-stake-ai-bets/
- [R30] IBTimes UK, "Jane Street Still on Record Pace After $15 Billion July Loss…", 2026-08-18: https://www.ibtimes.co.uk/jane-street-surpasses-2025-revenue-despite-july-loss-1814942
- [R31] S&P Global Market Intelligence, Jane Street secured notes, Nov 2021: https://www.spglobal.com/market-intelligence/en/news-insights/articles/2021/11/jane-street-upsizes-secured-notes-offering-firms-pricing-67406315
- [R32] Moody's via ResearchPool, "Jane Street's Ba1 rating unaffected by debt upsize": https://app.researchpool.com/provider/moodys-investors-service/moodys-ratings-says-jane-streets-ba1-rating-unaffected-by-debt-upsize-xm5o2aBnVi
- [R33] Lapaas Voice, "Jane Street swaps $5.6bn bonds for $14.6bn senior secured notes", 2026-08-12: https://lapaasvoice.com/jane-street-swaps-5-6bn-bonds-for-14-6bn-senior-secured-notes/
- [R34] The DESK / fi-desk (Lucy Carter), "Jane Street launches giant bond issuance", 2026-09-01: https://www.fi-desk.com/jane-street-launches-giant-bond-issuance/
- [R35] Tiger Brokers / Investing.com, S&P outlook revised to stable, 2025-07-15: https://www.itiger.com/news/2551139078
- [R36] ValueTheMarkets, Jane Street financial status July 2026 (secondary): https://www.valuethemarkets.com/cryptocurrency/news/analyzing-the-truth-behind-jane-streets-financial-status-in-july-2026
- [R37] Disruption Banking (secondary), Fitch upgrade: https://www.disruptionbanking.com/?p=46140
- [R38] Blockworks, "Jane Street named as authorized participant by all 11 bitcoin ETF hopefuls", Dec 2023/Jan 2024: https://blockworks.co/news/jane-street-ap-bitcoin-etf
- [R39] Crypto Briefing, "Jane Street's private company portfolio reaches $20B…", 2026-06-21: https://cryptobriefing.com/jane-street-private-portfolio-20-billion/
- [R40] CoinDesk, citing Bloomberg, "Market Makers Jane Street, Jump Retreating From U.S. Crypto Trading", 2023-05-09: https://www.coindesk.com/business/2023/05/09/market-maker-jane-street-jump-retreating-from-us-crypto-trading-bloomberg
- [R41] Upstox (citing Reuters), Jane Street returns to Indian markets, Jul 2025: https://upstox.com/news/market-news/financial-regulations/jane-street-returns-to-indian-markets-the-backstory-of-sebi-s-ban-and-reversal-explained/article-178397
- [R42] Business Today, "SAT to hear case on November 18", 2025-09-09: https://www.businesstoday.in/markets/stocks/story/jane-street-market-manipulation-case-sat-to-hear-case-on-november-18-says-report-493186-2025-09-09
- [R43] Business Standard / Bloomberg (Raghavan, Mahajan), "Sebi shares trade data with Jane Street…", 2026-10-07: https://www.business-standard.com/amp/markets/news/sebi-shares-trade-data-with-jane-street-seeks-response-to-allegations-126100700677_1.html ; summary: https://www.briefs.co/news/sebi-says-it-shared-jane-street-trade-logs-behind-market-man/
- [R44] Briefs, "SEBI Tags Jane Street's Records Request as a Delay Tactic", 2026-10-06: https://www.briefs.co/news/sebi-tags-jane-street-s-records-request-as-a-delay-tactic-af/
- [R45] LiveLaw, "SAT Reserves Order On Jane Street's Plea…", 2026-10-21: https://www.livelawbiz.com/securities-law/sat/securities-appellate-tribunal-reserves-order-jane-street-challenge-sebi-non-disclosure-relevant-documents-555493
- [R46] Bloomberg, "Jane Street, Millennium Settle India Options Trade Secrets Case", 2024-12-05: https://www.bloomberg.com/news/articles/2024-12-05/jane-street-millennium-settle-india-options-trade-secrets-case
- [R47] Justia docket, 1:2024cv02783 (SDNY): https://docs.justia.com/cases/federal/district-courts/new-york/nysdce/1:2024cv02783/619414/95 ; BNN Bloomberg, countersuit dismissed, 2024-07-19: https://www.bnnbloomberg.ca/business/company-news/2024/07/19/jane-street-gets-millennium-trade-secrets-countersuit-dismissed/
- [R48] Claims Journal, Millennium settlement, 2024-12-09: https://www.claimsjournal.com/news/national/2024/12/09/327780.htm
- [R49] Law360 case pages, *Snyder v. Jane Street Group, LLC et al*: https://www.law360.com/bankruptcy-authority/cases/699dfbdd447da8fb588eb048/articles ; MLex, "Jane Street Used Tips To Dodge Losses, Terraform Says": https://www.mlex.com/bankruptcy-authority/mid-cap/articles/2489043/jane-street-used-tips-to-dodge-losses-terraform-says
- [R50] The Block, "Jane Street asks court to dismiss Terraform Labs' insider trading lawsuit", 2026-04-23: https://www.theblock.co/post/398713/jane-street-asks-court-dismiss-terraform-labs-insider-trading-lawsuit
- [R51] CFTC provisionally registered swap dealers list (as of 2026-01-15): https://cftc.gov/node/123601
- [R52] Jane Street blog, "Announcing our market prediction Kaggle competition": https://blog.janestreet.com/announcing-our-market-prediction-kaggle-competition-index/
