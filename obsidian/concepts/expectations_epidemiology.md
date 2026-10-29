# Expectations Epidemiology

**Type:** Expectations-formation mechanism / empirical test
**Tags:** #inflation-expectations #epidemiology #top5 #focus-survey #professional-forecasters

---

## Definition

The spread of forecasts from an influential group of forecasters to the rest of a survey panel: some forecasters adjust their own forecast toward the views of a reference group rather than only to the data and their own past forecasts. The empirical approach is inspired by Carroll's (2003) epidemiology model, cited by Carvalho & Minella; in Brazil the natural reference group is the Top 5 forecasters whose forecasts the BCB publishes weekly alongside its survey, ranked by accuracy over short, medium and long horizons.

## Mechanism

- **The test** (Carvalho & Minella, Section 6). Regress each respondent's forecast on the lagged published Top 5 forecast, controlling for her own lagged forecast and lagged forecast error (learning), and then for a proxy of the statistical model she may use (a BVAR forecast) or for the current median survey forecast, and, for inflation, the target. A significant Top 5 coefficient after these controls is contagion; a significant Top 5 coefficient where the own lagged forecast is not means the respondent leans on the leaders rather than on her own history.
- **Why a forecaster would follow the leaders.** The published Top 5 forecasts are a cheap, more precise public signal, and following them lowers the cost of forming higher-order expectations; the alignment of errors across respondents may also reflect an attempt to avoid "large desynchronized forecast errors" (Carvalho & Minella).
- **Why the leaders differ.** Top 5 institutions update more often than the rest in the months that count for the ranking (Marques, as surveyed by Gaglianone), so they are the first to incorporate news.

## When it applies / when it fails

- The test needs an observable reference group; in both sources it is the published Top 5 of the Focus survey.
- Identification is fragile. The controls are imperfect: no forecaster need use the BVAR, and the current median already contains the Top 5 influence, so it is not orthogonal to the regressor (Carvalho & Minella, footnote 18). For the exchange rate the share of respondents influenced drops sharply when the median replaces the BVAR as control, so that result is not robust; for inflation it holds across controls.
- A lagged correlation with the Top 5 forecast also picks up common news the Top 5 absorb first, which is the faster-updating channel rather than imitation.
- Whether contagion is a problem depends on the precision of what spreads: following Cornand and Heinemann, exaggerated weight on a public signal is less likely to reduce welfare the more precise the signal, and the Top 5 forecasts are more accurate than the survey as a whole (Carvalho & Minella).
- It coexists with the opposite incentive, to differentiate from the consensus, documented for the Focus panel on [[strategic_forecasting]].

## How it appears across sources

| Source | Role |
|---|---|
| [[expectations/synthesis/market_forecasts_brazil_performance (Carvalho & Minella, 2012)]] | The test run respondent by respondent on Focus inflation, Selic and exchange-rate forecasts (64, 68 and 66 institutions): for inflation a little more than half of respondents adjust to the Top 5 once controls are added, about two-fifths for the Selic, and a control-sensitive share for the exchange rate (Table 6.1) |
| [[expectations/synthesis/empirical_findings_expectations_brazil (Gaglianone, 2017)]] | Surveys the Brazilian evidence: Top 5 forecasts influence other forecasters (Guillén; Carvalho and Minella), and Top 5 institutions update every 7 days against 12 for the others in the 6 months before the ranking (Marques) |

## BRL / application to the current analysis

Both sources are about the BCB's Focus survey. They find that the published Top 5 forecasts are followed by a sizeable part of the panel, most robustly for inflation, over samples that end in 2008 (Carvalho & Minella) and in the studies surveyed up to 2017 (Gaglianone). They do not say how strong the effect is in later samples.

## Connections

- [[information_rigidities]] — the frame for infrequent updating; the Top 5 updating more often than the rest is a difference in attention (Gaglianone)
- [[strategic_forecasting]] — the counter-incentive to differentiate from the consensus
- [[central_bank_communication]] — publishing the Top 5 is itself a public signal, whose precision decides whether contagion helps or hurts
- [[inflation_expectations_disagreement]] — contagion and alignment with peers compress disagreement
- [[expectations/synthesis/market_forecasts_brazil_performance (Carvalho & Minella, 2012)]] — the respondent-level epidemiology test on the Focus panel
- [[expectations/synthesis/empirical_findings_expectations_brazil (Gaglianone, 2017)]] — the stylized facts on Top 5 influence and updating frequency
