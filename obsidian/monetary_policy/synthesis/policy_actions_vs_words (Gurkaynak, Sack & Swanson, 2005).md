---
aliases: ["Gurkaynak 2005 - Do Actions Speak Louder Than Words? The Response of Asset Prices to Monetary Policy Actions and Statements"]
---

# Do Actions Speak Louder Than Words? The Response of Asset Prices to Monetary Policy Actions and Statements — Gürkaynak, Sack & Swanson 2005

**Type:** paper
**Tags:** #monetary-policy-shocks #high-frequency-identification #event-study #fomc-statements #path-factor #forward-guidance #term-structure
**Source:** International Journal of Central Banking, May 2005, pp. 55–91 (JEL E52, E58, E43, G14)
**Language:** English
**Source file:** [[monetary_policy/clean_md/policy_actions_vs_words (Gurkaynak, Sack & Swanson, 2005)]]

---

## Context and motivation

After the FOMC meeting of January 28, 2004, two- and five-year Treasury yields jumped 20 and 25 basis points in the half-hour around the announcement — the largest moves around any FOMC announcement in the fourteen years of data — although the decision to leave the funds rate unchanged was fully anticipated. What moved markets was the statement: dropping "policy accommodation can be maintained for a considerable period" for "the Committee believes it can be patient in removing its policy accommodation". Treating that day as a 0 bp policy surprise "would be missing the whole story". The earlier event-study literature (Cook & Hahn, Kuttner, Cochrane & Piazzesi, Rigobon & Sack, Bernanke & Kuttner) summarized each announcement by one number, the surprise in the funds rate target. The paper asks whether that single factor is enough.

## Core argument / thesis

It is not. A rank test rejects one factor and does not reject two. Rotated, the two factors have a structural reading: a **target factor** (the surprise in the current funds rate target) and a **path factor** (changes in expected policy over the coming year that leave the current rate unchanged), the latter closely associated with FOMC statements. Both matter for asset prices, but statements matter far more for longer-term yields: the path factor accounts for 75 to 90 percent of the explainable variation in five- and ten-year yields around announcements. The authors read this "not that policy actions are secondary so much as that their influence comes earlier", when investors price expected actions in response to statements. The implication is that the FOMC can commit to a conditional path several quarters or years out, so that even at a zero nominal funds rate it "is largely unhindered" — supporting Reifschneider & Williams (2000) and Eggertsson & Woodford (2003).

## Key mechanisms / model

- **Event study (section 1, equation 1)**: the change in an asset price on the surprise in the funds rate target, measured in narrow windows. Monthly or quarterly data suffer from simultaneity (policy reacting to asset prices) and omitted variables (news such as the employment report moving both); even daily data are contaminated because before 1994 the FOMC often moved hours after an employment report.
- **Announcement dates and times (section 1.2)**: every FOMC announcement January 1990–December 2004, including no-change meetings; from February 1994 the press release time, before that the next open market operation (11:30 a.m.) or a discount-rate press release.
- **Measuring the surprise (section 1.3, appendix A4–A7)**: tick-by-tick federal funds futures; the change in the current-month contract scaled up by the days remaining in the month (Kuttner's method), with the next-month contract for meetings in the last seven days; the analogous expected change at the following meeting from the contract for that month. Windows: "tight" (ten minutes before to twenty after) and "wide" (fifteen before to forty-five after), compared with a daily window.
- **How many factors (section 2.1, appendix)**: Cragg–Donald (1997) minimum-distance test of the number of common factors in the matrix of 30-minute asset-price changes, applied to Treasury yields plus the S&P 500, and to five futures rates with one year or less to expiration (current-month and three-month-ahead fed funds futures, scaled; two-, three- and four-quarter-ahead eurodollar futures).
- **Factors and rotation (sections 2.2–2.3, A8–A11)**: the first two principal components of the five futures rates, rotated to stay orthogonal while making the second factor have no effect on the current-month surprise. Z1 (target) is scaled so a change of .01 is a 1 bp target surprise; Z2 (path) so that its effect on the four-quarter-ahead eurodollar rate equals Z1's, about 55 bp. The path factor is by construction a residual: "all other aspects" of an announcement that move expected policy over the year.
- **Response of assets (section 2.5, equation 3)**: each asset's 30-minute change on Z1 and Z2; standard errors also bootstrapped (1,000 repetitions) because the regressors are generated.

## Main results / findings

**Intraday versus daily surprises (section 1.3, Figure 2).** The average absolute difference between daily and intraday surprises is only about 2 bp, but five observations differ by more than 10 bp, all before 1994 on employment report days (e.g. September 4, 1992: intraday surprise 0 bp, daily –22 bp, which includes the endogenous response to a weak report). The two intraday windows agree closely, and markets price the decision within minutes (June 25, 2003: a cut from 1.25 percent to 1 percent read as a 13 bp tightening surprise, since many expected 50 bp). For samples that exclude employment report days or begin in 1994, daily data measure the surprise well.

**The target surprise alone (Table 1).** A surprise 25 bp tightening lowers the S&P 500 by "a little more than a 1 percent" (tight-window coefficient –4.032); intraday data triple the R² from .12 to .36. Tight-window yield responses decline with maturity: 0.537 (three-month bill), 0.522 (six-month), 0.455 (two-year), 0.264 (five-year), 0.125 (ten-year, now significant), with the five-year forward rate five years ahead negative but only weakly significant. Daily regressions bias the bill response upward (employment report days) and are sensitive to the January 3, 2001 outlier: without it the daily ten-year coefficient would be 0.28 rather than 0.17, while the intraday estimate barely moves.

**Two factors, not one (Table 2).** Zero and one factor are rejected for both asset sets (one factor: Wald 21.41, p .011 for Treasuries and stocks; 17.19, p .004 for futures); two factors are not rejected at the 10 percent level (4.36, p .360; 1.06, p .304). Markets have reacted "as if there is essentially only one additional degree of information beyond the surprise change in the federal funds rate target". The target factor is very close to the funds-rate surprise of section 1 (correlation over 95 percent, R² of .91).

**The path factor is about statements (section 2.4, Figure 6, Tables 3–4).** Large path-factor realizations are recent; before 1994 and on non-statement days they were typically very small. Regressing the absolute path factor on a statement dummy gives a coefficient of 0.070 (constant 0.044, R² .18, 138 observations). Nine of the ten largest observations (twenty-one of the top twenty-five) came with a statement, and the press attributed the bond-market move to its wording: January 28, 2004 (42.7), July 6, 1995 (–38.4), August 13, 2002 (–37.2), May 18, 1999 (32.8). The exception, December 20, 1994 (26.6), was a surprise *not* to tighten. Markets digest statements more slowly: regressing the wide-window on the tight-window factor gives an R² of .83 for the path factor against .98 for the target factor.

**Effects on asset prices (Table 5).** A 1 percentage point target surprise lowers the S&P 500 by 4.3 percent and raises two-, five- and ten-year yields by 49, 28 and 13 bp. A path-factor innovation of the same size moves the one-year-ahead eurodollar rate equally by construction but has "a much greater impact on the long end": 37 and 28 bp on five- and ten-year yields, and it raises the five-year forward rate five years ahead (0.157) where the target factor lowers it. Comparing one- and two-factor R² (two-year .41 to .94, five-year .19 to .80, ten-year .08 to .74), the path factor accounts for two-thirds of the explainable variation in two-year yields, three-fourths in five-year yields and nine-tenths in ten-year yields: "previous authors have been missing by far the most important component of monetary policy decisions". The stock-market effect of the path factor is smaller, only about –1 percent per point. One possible explanation, after Romer & Romer (2000): statements reveal the FOMC's view of output and inflation, so upward revisions to the outlook offset the effect of higher expected rates on stocks while pushing long yields up (footnote 26 notes that Faust, Swanson & Wright find no such information in target surprises).

**Out-of-sample check (January 4, 2005).** The first minutes released three weeks before the next meeting raised one-year-ahead eurodollar futures 6.5 bp; two-, five- and ten-year yields rose 4.9, 5.0 and 4.1 bp against 4.8, 4.4 and 3.3 predicted by Table 5; the S&P 500 fell .49 percent against .11 predicted; the five-to-ten-year forward rose 3.0 bp against 1.9.

## Limitations and caveats

- **The reference list is not in the file**: it ends with the appendix's last sentence. The online data appendix (announcement dates, surprise measures, factor values by date) is referred to but not included.
- Figures 1–6 survive only as axis ticks and labels; the descriptions above come from the text. Tables 1, 2 and 5 are broken into one value per line but can be read in order; the significance stars are intact.
- Appendix equations (A2)–(A7) and (A10)–(A11) lose their summation signs and fraction layout in places; (A4) and (A6) are split across lines. Their role is described in words above.
- The source has no volume number on its pages; "Bernanke and Kuttner (forthcoming)" and a Gürkaynak, Sack & Swanson paper are cited as forthcoming.
- Authors' own caveats: statements are not an independent policy tool — they work through expected future actions; the path factor is a residual open to several interpretations and includes some non-statement events (December 20, 1994); intraday Treasury data start only in July 1991 (eighteen fewer observations, five employment report dates instead of eight); intraday forward rates cannot be computed beyond five years ahead; reading surprises as changes in expectations assumes risk premia do not move in the window; minutes may differ from statements in ways the out-of-sample test cannot rule out.

## Connections

- [[monetary_policy_shocks]] — high-frequency identification from funds-futures surprises in 30-minute windows, and the finding that one surprise measure is not enough: monetary policy announcements have two dimensions
- [[forward_guidance]] — the path factor measures the market effect of FOMC statements about future policy, which dominates the response of long-term yields; the paper reads it as evidence that the FOMC can commit to a conditional path, including at the zero bound
- [[central_bank_communication]] — statements as a driver of asset prices distinct from the rate decision, the slower digestion of statement news, and the minutes release of January 4, 2005 as a statement-like event
- [[information_effect]] — offered as a possible explanation for the small stock-market response to the path factor: statements may raise investors' outlook for output and inflation (Romer & Romer 2000)
- [[monetary_policy/synthesis/forward_guidance_effects (Campbell et al., 2012)]] — extends this event study and its target/path rotation, and splits guidance into Delphic and Odyssean components
- [[monetary_policy/synthesis/information_effect_hf_identification (Nakamura & Steinsson, 2018)]] — builds its policy news shock from the same five futures in 30-minute windows, closely related to the path factor
- [[monetary_policy/synthesis/central_bank_communication_survey (Blinder et al., 2008)]] — reviews this path-factor approach among market-based measures of the effect of communication
- [[monetary_policy/synthesis/zero_bound_optimal_policy (Eggertsson & Woodford, 2003)]] — the theory the authors cite: a central bank that can credibly commit to future policy is relatively unconstrained by the zero bound
