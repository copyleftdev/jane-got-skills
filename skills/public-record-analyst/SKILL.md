---
name: trading-firm-public-record
description: Analyse a private trading firm (worked example Jane Street) from its public record without the classic misreadings. Covers which entity files what (EDGAR CIKs, FINRA CRDs), how to read a 13F (option rows at underlying value, the 2023 unit change, CUSIP not issuer name, what 13F omits), what a broker-dealer's public X-17A-5 does and doesn't disclose, why the P&L numbers are press-reported, and how to state open legal matters without turning allegations into findings. Use when researching a market maker, proprietary trading firm or hedge fund from filings, reading or charting a 13F, comparing reported figures, or writing a profile that others will rely on. Ships a 13F fetch/summarise/reconcile tool verified against the real filings.
---

# Trading-Firm Public Record

## Overview

Jane Street is private and publishes no earnings, yet a great deal about it is public:
- SEC filings from about a dozen entities;
- FINRA records for three broker-dealers;
- regulator orders;
- bond-market reporting.

Most published analysis still misreads at least one of these. The usual mistake is to quote the 13F headline ("$1.2 trillion") as if it were the firm's size.

This skill is a method for reading that record carefully. Every figure below was either re-derived with `scripts/thirteenf.py` from the filing itself, or comes from `research/business_public_data.md` with its provenance tag.

**Scope.** Use only the professional public record. Leave out personal details, contact information and individuals' private lives. Discuss litigation at the level of the docket. Name a person only where a regulator's final action names them, and even then only when it is relevant.

## Rule 1: Tag every number with where it came from

| Tag | Meaning | Jane Street examples |
|---|---|---|
| **[P] primary** | A document you retrieved and read | 13F XML on EDGAR, FINRA BrokerCheck PDF, the SEBI interim order, X-17A-5 statement of financial condition |
| **[R] reported** | Press, usually citing documents the reporter saw | Every revenue and net-income figure. They come from private 144A bond offering memoranda, which are not on EDGAR |
| **UNCONFIRMED** | Secondary only, or sources disagree | Rating actions you could not retrieve from the agency, conflicting case-status claims |

Never let an [R] number lose its tag in a summary table. When two outlets disagree (FT $10.5bn vs Bloomberg $10.6bn for 2023), show both. Reject aggregator figures that cannot be traced to a primary source or a named outlet. The dossier caught one aggregator presenting Q2 2025 revenue as Q2 2026.

## Rule 2: Map the entities before reading anything

Each filing type comes from a different entity. Get the identifiers from `data.sec.gov/submissions/CIK##########.json` and BrokerCheck:

| Filing | Jane Street filer | What it is |
|---|---|---|
| 13F-HR | JANE STREET GROUP, LLC, CIK 0001595888 | One combined holdings report |
| 13F-NT | Affiliates (Capital, Options, Global Trading, Europe, Singapore, Asia Trading) | A notice pointing to the group's report, with no holdings of their own |
| X-17A-5 | Broker-dealers: Jane Street Capital (CIK 0001103083, CRD 103782), Options (CRD 134159), Execution Services (CRD 167280) | Annual audited financial statements |
| SC 13G | The group | More than 5% passive stakes in single issuers |
| SBSE | Jane Street Derivatives Dealer, LLC (2026) | Security-based swap dealer registration |

A finding about one entity is not automatically a finding about "Jane Street". In the SEBI matter, the order names four specific entities.

## Rule 3: Read a 13F as an inventory snapshot, not as a size

`scripts/thirteenf.py` was run on the actual Q2 2026 filing, accession 0001595888-26-000108, filed 2026-08-14:

```
14,718 rows, headline total $1,205.6bn (do not read this as exposure)
  shares  8,699 rows     $156.5bn   13.0%
  calls   3,231 rows     $472.9bn   39.2%  underlying value, not premium
  puts    2,750 rows     $575.6bn   47.7%  underlying value; economically short
  prn        38 rows       $0.6bn    0.1%
```

The rows sum exactly to the cover page's `tableValueTotal` (1,205,633,745,715). The traps:

- **Options are reported at the value of the underlying.** 87% of the "total" is option rows valued as if they were the shares. That is not the premium paid, and not exposure.
- **Puts are economically short.** Adding them to calls and shares is meaningless as a measure of position size. A market maker holds large two-sided option inventory.
- **13F shows long positions in 13(f) securities only.** Short stock, futures, FX, swaps, most bonds and non-US-listed securities are absent. A market maker's hedges are largely invisible here.
- **Units changed.** Values were in thousands of dollars until the SEC's 2023 amendments took effect. Filings on or after 2023-01-03 report whole dollars. The 2021Q4 filing (filed 2022-02-15) has raw values summing to 303,159,652. That is $303.2bn, not $303m. The tool takes the filing date and applies the multiplier.
- **Key positions by CUSIP, never by issuer name.** "ISHARES TR" is one issuer name covering dozens of funds. Grouping by name falsely made it the #2 share position, at $3.7bn. By CUSIP, the top ten matches the per-fund reality: SPY $33.1bn, then AMZN, SNDK, NVDA, QQQ, MSFT, STX, CRWV, IEMG and META.
- **It is a quarter-end snapshot, filed up to 45 days later.** For a firm that turns its inventory over constantly, it says little about the strategy and nothing about P&L.
- **Reconcile before you chart.** Check row counts and the value sum against the cover page. A truncated download or a parsing bug shows up immediately.

What 13F *is* good for:
- breadth (row counts over time: 2,785 in 2014Q2, 13,305 in 2021Q4, 14,718 in 2026Q2);
- the share-only book, as a lower bound on visible equity inventory;
- the instruments where the firm makes markets.

## Rule 4: Know what each document cannot tell you

- **X-17A-5.** The public part of a broker-dealer's annual audit is mainly the statement of financial condition. For Jane Street Capital at 2025-12-31 [P], that showed:
  - total assets $60.7bn;
  - member's equity $6.28bn;
  - $1.91bn of net capital under Rule 15c3-1.

  It is one subsidiary's balance sheet. It is not the group's, and it contains no P&L.
- **Bond offering memoranda (144A).** These are the source of most P&L reporting. They are private, so cite them through the outlet that saw them [R], and note when outlets disagree.
- **Ratings.** Agency actions are primary only when you retrieve them from the agency. Otherwise they are [R] or UNCONFIRMED.
- **BrokerCheck.** It lists final regulatory actions against the broker-dealers and their control affiliates (for example, FINRA and exchange censures with fines from $25k to $650k). Matters outside its scope do not appear: the SEBI order is not shown, and all pending counts are 0. Absence from BrokerCheck is not absence of the matter.

## Rule 5: State legal matters at their actual procedural stage

| Stage | Say | Don't say |
|---|---|---|
| Complaint or lawsuit filed | "alleges", "the complaint claims" | "Jane Street front-ran…" |
| Interim or ex parte order | "an interim order alleges / directed…; the firm disputes it" | "SEBI found manipulation" |
| Settled with undisclosed terms | "resolved on terms not disclosed" | "Jane Street won / lost" |
| Final regulatory action | "censured and fined $X for [the finding]" | Inflate or generalise it |

Worked example, SEBI (India):
- The 2025-07-03 order is **ex parte and interim** [P8]. It alleges intraday index manipulation and impounded ₹4,843.57 crore, which was deposited in escrow "without prejudice" [P9a].
- The market bar ceased on 2025-07-21, under cease-and-desist conditions [P9b].
- The firm disputes the findings. An appeal over document disclosure is before the Securities Appellate Tribunal, which reserved its order on 2026-10-21 [R45].
- No final order was found as of 2026-11-07.

Every one of those qualifiers carries meaning, and dropping any of them misstates the record.

## Workflow

1. **Entities.** Build the CIK and CRD map (Rule 2).
2. **Pull.** For each claim, retrieve the primary document if one exists. Use `thirteenf.py fetch` for 13Fs, which requires `SEC_USER_AGENT`. Keep SEC requests under 10 per second.
3. **Reconcile.** Check 13Fs against their cover pages. Cross-check reported numbers between outlets.
4. **Tag** every figure [P], [R] or UNCONFIRMED, and date-stamp the retrieval.
5. **Interpret** within each document's limits (Rules 3 and 4).
6. **Write** legal matters at their procedural stage (Rule 5).

```sh
export SEC_USER_AGENT="YourOrg research you@yourorg.example"   # SEC fair-access policy
python3 -I scripts/thirteenf.py fetch 1595888 ./q2 --accession 0001595888-26-000108
python3 -I scripts/thirteenf.py reconcile ./q2/primary_doc.xml ./q2/infotable.xml --filed 2026-08-14
python3 -I scripts/thirteenf.py summarize ./q2/infotable.xml --filed 2026-08-14 --top 10
```

## Rules

**Always**
- Tag provenance, and keep the tag through every summary.
- Separate shares, calls, puts and principal-amount rows when you report a 13F.
- Apply the unit multiplier by filing date, and reconcile against the cover page.
- Name the specific entity a filing or an order concerns.
- Use the procedural-stage vocabulary for legal matters.

**Never**
- Call a 13F total "assets", "AUM", "exposure" or "portfolio size".
- Aggregate 13F positions by issuer name.
- Present press-reported P&L as disclosed financials.
- Turn an allegation, complaint or interim order into a finding.
- Collect or publish personal information about employees or litigants beyond the docket.

## Checklist

1. Which entity filed each document I cite?
2. Is every number tagged [P], [R] or UNCONFIRMED, with a retrieval date?
3. If I show a 13F figure, did I split it by kind, apply the right units and reconcile it?
4. Did I state what each source cannot show (shorts and hedges in a 13F, P&L in an X-17A-5)?
5. Is each legal matter described at its actual stage, with the firm's position noted?

## Verification

`python3 -I -m unittest discover -s skills/public-record-analyst/scripts/tests` runs 11 tests over a 30-row slice of the real Q2 2026 information table:
- the unit boundary;
- the kinds partitioning rows and value;
- CUSIP keying;
- reconciliation, including a canary that drops a row and must produce two discrepancies;
- `fetch` refusing to run without `SEC_USER_AGENT`.

With `SEC_USER_AGENT` set and `LIVE_SEC=1`, one more test downloads the real Q2 2026 filing and reconciles all 14,718 rows. It passed on 2026-11-07. The 2021Q4 figures above (13,305 rows, $303.2bn) came from the same tool via `fetch`.

## Sources

- `research/business_public_data.md` in this repository, with numbered [P] and [R] sources, retrieved 2026-11-07.
- **SEC EDGAR:** `data.sec.gov/submissions/CIK0001595888.json`. 13F-HR filings 0001595888-26-000108 (Q2 2026) and 0001595888-22-000007 (Q4 2021).
- **FINRA BrokerCheck:** firms 103782, 134159 and 167280.
- **SEBI:** interim order WTM/AN/MRD/MRD-SEC-3/31516/2025-26 and press releases PR 40/2025 and PR 45/2025.
