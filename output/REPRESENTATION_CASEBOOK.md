# Representation Casebook

The leading exhibits separate recorded settlement contrasts, adjudication and observed chronology. Supplementary scenarios are explicitly hypothetical. The cases document rule distinctions and recorded outcomes, not prevalence or average effects. Audit scope is the supplied API fields and linked records; complete historical governing terms are not certified.
A common distribution over scenarios can value different payout claims differently. The audit supplies no price result; scalar settlements and tie exceptions require the full payout mapping and cannot enter binary-event restrictions. See [constructs and source bridge](../docs/CONSTRUCTS.md).

### Steve Hilton: first place versus advancing in the California primary

Steve Hilton finished second in the June 2, 2026 California primary and advanced to the general election. Certified results place Becerra first (28.0%), Hilton second (24.6%) and Steyer third (22.8%).

- Scope: cross-platform; archived realized settlement contrast
- Evidence status: observed event and recorded final settlement contrast
- Rule dimension: rank versus qualification divergence
- Plain-language explanation: Finishing second loses the first-place contract and wins advancement.
- Qualifying condition A (Kalshi): first place in the primary; proportional payout for exact ties
- Qualifying condition B (Polymarket): advance to the general election; the top two candidates qualify
- Recorded settlements: A = NO; recorded normalized settlement $0; B = resolved YES; normalized payout $1
- Contract identifiers: A = KXCAGOVPRIMARY1ST-26JUN02-1ST-SHIL; B = 825460
- Audit boundary: Both records are in the September-labelled sample and match the preserved October follow-up on operative fields. They have different cutoff/fallback conditions; the archived tie clause permits fractional amounts. Linked governing specifications are not certified historical editions. This realized contrast establishes no price error or trader misunderstanding.
- Claim relation: non_equivalent_unclassified; representation: non_binary_exceptions
- Relation confidence: high within stated archived-rule model; not a probability
- Source-scoped relation audit: Scope: supplied API fields and explicitly linked evidence; historical governing specifications and all platform fallbacks are not certified. Archived first-place and advancement records plus certified second place establish realized 0/1 payout divergence. The archived Kalshi rule also pays 1/n for exact ties, ranks withdrawn/disqualified candidates left on the ballot, excludes write-in winners without their own option, and pays NO if cancelled/postponed beyond expiration. Polymarket uses advancement, a December 31 cutoff and official-results fallback. No binary subset restriction follows from the realized contrast.
- Probability implication: none; coherence test applicable (semantic gate): False
- Sources: [A: Kalshi](https://kalshi.com/markets/kxcagovprimary1st-26jun02-1st-shil); [B: Polymarket](https://polymarket.com/event/will-steve-hilton-get-the-first-or-second-most-votes-in-the-2026-california-governor-primary-election)
- Exact archived rules: If Steve Hilton finishes in 1st place in the 2026 California Governor primary election, then the market resolves to Yes.
This market resolves based solely on the primary election results, not any subsequent general election. Ranking is determined by the specified counting method. For plurality voting: rank is based on vote count or percentage. For ranked choice voting: rank is determined by elimination order (runner-up is eliminated in final round for second place). For two-round systems: rank is based on final round results if it proceeds to second round, otherwise first-round totals. For proportional representation: rank follows the electoral authority's final seat allocation order. In case of exact ties, markets resolve proportionally (1/number of tied entities). Write-in candidates achieving the specified rank resolve all named candidate markets to No unless a specific "Write-in" or "Other" option exists. Candidates who withdraw or are disqualified after the filing deadline but remain on the ballot are ranked based on votes received. If the election is cancelled or postponed beyond expiration, all markets resolve to No. || The non-partisan primary election for Governor of California is scheduled to take place on June 2, 2026. The top two candidates in this election by number of votes won will advance to the general election for Governor of California.

This market will resolve to “Yes” If the listed candidate advances from the primary to the general election for Governor of California. Otherwise this market will resolve to “No”.

If no 2026 California gubernatorial primary takes place by December 31, 2026, this market will resolve to “No.”

This market will resolve based on the results of the primary election for Governor of California as indicated by a consensus of credible reporting. If there is ambiguity, this market will resolve based solely on the official results as reported by the government of California, specifically the Office of the Secretary of State.
- Snapshot date label: 2026-09-10; coder confidence: high

- Chronology: June 2, 2026: primary; June 10 20:05:30 UTC: Polymarket closure record; July 11 00:39:59.561815 UTC: Kalshi settlement timestamp.

- Independent event source: [Certified Statement of Vote; THEORY_REVIEW.md C3, summary p. 6 / PDF p. 1](https://elections.cdn.sos.ca.gov/sov/2026-primary/sov/06-sov-summary.pdf); June 2, 2026 primary: Becerra 28.0%, Hilton 24.6%, Steyer 22.8%; Hilton second.

- Exact settlement evidence: {"a": {"result": "no", "settlement_ts": "2026-07-11T00:39:59.561815Z", "settlement_value_dollars": "0.0000", "status": "finalized", "ticker": "KXCAGOVPRIMARY1ST-26JUN02-1ST-SHIL"}, "b": {"closed": true, "closedTime": "2026-06-10 20:05:30+00", "id": "825460", "outcomePrices": "[\"1\", \"0\"]", "outcomes": "[\"Yes\", \"No\"]", "umaResolutionStatus": "resolved", "umaResolutionStatuses": "[\"proposed\"]"}, "boundary": "Recorded contract outcomes; no token redemption or account cash-flow audit.", "checked_at_utc": "2026-10-13T07:02:56.414450+00:00", "original_http_acquisition_time": null, "source_check": "hilton-restored-snapshot-check.json"}

### Ali Khamenei departure: price-based death allocation versus YES

Two markets concerned Ali Khamenei's departure as Iran's Supreme Leader. Following the February 28, 2026 attack, contemporaneous March 1 reporting recorded Iranian state media confirming Khamenei's death. The compared contracts recorded scalar 45-cent and resolved-YES settlements.

- Scope: cross-platform; archived realized fractional settlement contrast
- Evidence status: observed departure episode and recorded final settlement contrast
- Rule dimension: death-clause payout divergence
- Plain-language explanation: Forecasting departure is insufficient to value a contract whose death clause can pay a fraction of the unit payout.
- Qualifying condition A (Kalshi): departure before July 1, 2026; qualifying announcement also covered; death-only departure uses a pre-death price or committee fair allocation
- Qualifying condition B (Polymarket): loss of position or ability to perform duties by June 30, 2026, 11:59 PM ET
- Recorded settlements: A = scalar; recorded normalized settlement $0.45; B = resolved YES; normalized payout $1
- Contract identifiers: A = KXKHAMENEIOUT-AKHA-26JUL01; B = 661699
- Audit boundary: The deadlines and exceptions differ, so this is not a controlled clause effect. The API description includes announcement, ordinary departure, price-based death allocation and binding committee discretion. The exact reference-price selection was not audited. Reported reimbursements can make account receipts differ from contract settlement; original linked social posts were inaccessible. No binary-event restriction applies.
- Claim relation: non_equivalent_unclassified; representation: non_binary_and_adjudicated_exceptions
- Relation confidence: high within stated archived-rule model; not a probability
- Source-scoped relation audit: Scope: supplied API fields and explicitly linked evidence; historical governing specifications and all platform fallbacks are not certified. Both archived and follow-up official records establish a normalized 0.45/1 contrast. Kalshi's ordinary departure/announcement criterion is overridden for death-only departure by a pre-death last-price allocation, with binding committee discretion if the price is unavailable, illogical or unfair. Polymarket covers resignation, detention, loss of position or inability to perform duties through its ET cutoff. The deadlines differ; the full payout mapping is fractional and adjudicated. The recorded settlement does not identify reference-price selection or account reimbursements. No global binary-event restriction is validated.
- Probability implication: none; coherence test applicable (semantic gate): False
- Sources: [A: Kalshi](https://kalshi.com/markets/kxkhameneiout-akha-26jul01); [B: Polymarket](https://polymarket.com/event/khamenei-out-as-supreme-leader-of-iran-by-june-30-747)
- Exact archived rules: If Ali Khamenei leaves office before July 1, 2026, then the market resolves to Yes.
An announcement that the Ali Khamenei will leave the office within the next year is also encompassed by the Payout Criterion. If Ali Khamenei leaves solely because they have died, the associated market will resolve and the Exchange will determine the payouts to the holders of long and short positions based upon the last traded price (prior to the death). If a last traded price is not available or is not logically consistent, or if the Exchange determines at its sole discretion that the last traded prices prior to death do not represent a fair settlement value, the Outcome Review Committee will be responsible for making a binding determination of fair allocation. || This market will resolve to "Yes" if Iran's Supreme Leader, Ali Khamenei, is removed from power for any length of time by June 30, 2026, 11:59 PM ET. Otherwise, this market will resolve to "No".

Khamenei will be considered to be removed from power if he resigns, is detained, or otherwise loses his position or is prevented from fulfilling his duties as Supreme Leader of Iran within this market's timeframe.

The primary resolution source for this market will be a consensus of credible reporting.
- Snapshot date label: 2026-09-10; coder confidence: high

- Chronology: February 28, 2026: attack; March 1: contemporaneous confirmation report; March 1 00:02:17 UTC: Polymarket closure record; March 1 03:19:27.389859 UTC: Kalshi scalar-settlement timestamp.

- Independent event source: [LEAD_REVIEW.md L3; contemporaneous March 1, 2026 report](https://apnews.com/article/5b13b69b708c4ed38e8f95f5fb41a597); Iranian state media confirmed Khamenei's death following the February 28 attack.
- Independent event source: [LEAD_REVIEW.md L3; contemporaneous March 1, 2026 report](https://cointelegraph.com/news/kalshi-founder-khamenei-market-carveout); Reported price-based death settlement and fee/entry-cost reimbursements; original linked social posts returned 403.

- Exact settlement evidence: {"a": {"result": "scalar", "settlement_ts": "2026-03-01T03:19:27.389859Z", "settlement_value_dollars": "0.4500", "status": "finalized", "ticker": "KXKHAMENEIOUT-AKHA-26JUL01"}, "b": {"closed": true, "closedTime": "2026-03-01 00:02:17+00", "id": "661699", "outcomePrices": "[\"1\", \"0\"]", "outcomes": "[\"Yes\", \"No\"]", "umaResolutionStatus": "resolved", "umaResolutionStatuses": "[\"proposed\"]"}, "boundary": "Recorded contract outcomes; no token redemption or account cash-flow audit.", "checked_at_utc": "2026-10-13T07:18:29.003416+00:00", "original_http_acquisition_time": null, "source_check": "khamenei-restored-settlement-evidence.json"}

### Zelenskyy's clothing: reporting criterion and recorded adjudication

The Ukrainian presidency documented a June 24, 2025 appearance by President Volodymyr Zelenskyy in the Netherlands, with photographs. A Polymarket contract asked whether authentic images showed him wearing a suit during May 22–June 30. The question creator had already acknowledged a dispute on May 29 and stated on July 1 that credible reporting had not confirmed a qualifying suit appearance. The market record reports NO, corroborated by the linked protocol read.

- Scope: within-contract; documented adjudication episode
- Evidence status: observed creator updates, recorded NO and pinned protocol corroboration
- Rule dimension: delegated reporting criterion and documented adjudication
- Plain-language explanation: The creator's clarification applies the named reporting criterion. The existing disputes cannot all be attributed to the June 24 appearance, because a dispute was acknowledged before that photograph.
- Qualifying condition A (Polymarket): authentic images/video taken and released May 22–June 30, 2025 ET; wearing a suit; no garment-level definition
- Qualifying condition B (Adjudication procedure): credible-reporting consensus supplies the deciding interpretation
- Recorded settlements: A = resolved NO; normalized payout $0; B = N/A; this is one contract and its adjudication procedure
- Contract identifiers: A = 546814; B = not-a-second-contract
- Audit boundary: The appearance source does not independently classify the clothing. Question/condition hashes, creator updates and current NO payout are verified at a pinned block. Historical log access returned HTTP 403; no complete proposal/finality chronology or reason for each challenge was recovered. The stored request timestamp is not initialization. No pairwise divergence, institutional incompleteness or holder receipts are inferred.
- Claim relation: not_applicable; representation: delegated_determination
- Relation confidence: high within stated archived-rule model; not a probability
- Source-scoped relation audit: Scope: supplied API fields and explicitly linked evidence; historical governing specifications and all platform fallbacks are not certified. The question names credible-reporting consensus and image/time/authenticity conditions. Linked creator updates acknowledge a May 29 dispute and state on July 1 that reporting had not confirmed a suit appearance. Pinned Polygon state verifies the exact question/condition linkage and NO payout. Neither a complete proposal timeline nor the reason for every dispute is recovered. No pairwise relation or institutional incompleteness is established.
- Probability implication: none; coherence test applicable (semantic gate): False
- Sources: [A: Polymarket](https://polymarket.com/event/will-zelenskyy-wear-a-suit-before-july)
- Exact archived rules: This market will resolve to "Yes" if Volodymyr Zelenskyy is is photographed or videotaped wearing a suit between May 22 and June 30, 2025 ET. Otherwise, this market will resolve to "No".

For this market to resolve to "Yes" the images or video must be taken and released within this market's timeframe. The images or video must be authentic, not the result of artificial intelligence or video editing.

The resolution source will be a consensus of credible reporting. || The contract delegates to a consensus of credible reporting.
- Snapshot date label: unrecorded for follow-up API responses preserved in the October review; coder confidence: high

- Chronology: May 29, 2025 16:35:11 UTC: creator acknowledges a dispute; June 24: photographed appearance; June 30 ET: rule window ends; July 1 13:33:09 UTC: creator reports that consensus has not confirmed a suit; July 5 00:27:54 UTC: request timestamp retained in adapter state; archived status history alternates proposed/disputed five times (individual timestamps unavailable); July 9 00:30:39 UTC: closure record with resolved status and NO outcome. Polygon block 95,596,076 (October 15, 2026 21:24:02 UTC): resolved state and payout [0,1].

- Independent event source: [THEORY_REVIEW.md C1; dated account and accompanying photograph](https://www.president.gov.ua/en/news/vidbulasya-audiyenciya-prezidenta-ukrayini-v-korolya-niderla-98637); Zelenskyy appeared in the Netherlands on June 24, 2025; no independent clothing classification is supplied.

- Exact settlement evidence: {"a": {"closed": true, "closedTime": "2025-07-09 00:30:39+00", "id": "546814", "outcomePrices": "[\"0\", \"1\"]", "outcomes": "[\"Yes\", \"No\"]", "umaResolutionStatus": "resolved", "umaResolutionStatuses": "[\"proposed\", \"disputed\", \"proposed\", \"disputed\", \"proposed\", \"disputed\", \"proposed\", \"disputed\", \"proposed\", \"disputed\"]"}, "b": {}, "boundary": "Recorded contract outcomes; no token redemption or account cash-flow audit.", "checked_at_utc": null, "original_http_acquisition_time": null, "protocol_evidence": {"acquired_at_utc": "2026-10-15T21:25:40.148963+00:00", "adapter": "0x6A9D222616C90FcA5754cd1333cFD9b7fb6a4F74", "ancillary_question_hash_verified": true, "ancillary_support": "NO, YES and UNKNOWN/50-50; creator bulletin-board updates are relevant", "chain_id": 137, "condition_id": "0x655e5ca101c466b6293aa15e06173b78b293221803d56e35551f708cd82eb352", "condition_link_verified": true, "creator": "0x91430cad2d3975766499717fa0d66a78d814e5c5", "creator_updates": [{"text": "We’re aware of the dispute on this market. If a clarification is to be issued, it will be at 2 PM ET. If no statement is issued at that time, then there will be no clarification by the Polymarket team.\n\nThe orderbook will be cleared at 2 PM ET regardless of whether a clarification is made.", "timestamp_utc": "2025-05-29T16:35:11+00:00"}, {"text": "At the time of this clarification, 09:33am ET July 01, a consensus of credible reporting has not confirmed that Zelenskyy has worn a suit", "timestamp_utc": "2025-07-01T13:33:09+00:00"}], "ctf": "0x4d97dcd97ec945f40cf65f87097ace5ea0476045", "historical_log_status": "HTTP 403; no complete proposal/dispute/final-resolution log chronology recovered", "oracle": "0xee3afe347d5c74317041e2618c49534daf887c24", "payout_numerators": [0, 1], "question_id": "0x0bf7a42b24b91417c1c1976cf99d153ac046f7bffd66c934291c94ddb742b743", "read_block_hash": "0x9751daf09ba364fc77858fc7921c00198e38523d2f3c2c3f66ee5057d4b94b4a", "read_block_number": 95596076, "read_block_time_utc": "2026-10-15T21:24:02+00:00", "resolved": true, "source_sha256": {"suit-creator-update-responses.json": "19da5ba371f3b3fe15ebea737833ffef9650449d23723bcdd197f5d848d47e03", "suit-creator-updates.json": "51e1a8f912fc283e8e29bad7845afeddf17fe6749f096ca7f163687cc604f344", "suit-protocol-responses.json": "13b11ce714137c165d820f444ff56b0b20c21dc4a1d16cb894a098959a74d89f", "suit-protocol-state.json": "d401451492f949c1b7614374d93ec113f2cc7e1cdba652f243015da7e5747f26"}, "stored_request_timestamp_utc": "2025-07-05T00:27:54+00:00"}, "source_check": "suit-market-current.json"}

### U.S.–Ukraine minerals agreement: two YES resolutions across milestones

During the 2025 U.S.–Ukraine minerals negotiations, one Polymarket contract asked whether Ukraine would agree to a deal before April; another required a signed deal before May. The March agreement contract records YES and March 25 closure. The U.S. Treasury and Ukrainian ministry record an April 30, 2025 signing; the later signed-deal contract records YES and May 4 closure.

- Scope: within-platform across successive contracts; observed chronology
- Evidence status: observed chronology and two recorded YES outcomes; no realized split
- Rule dimension: milestone-stage divergence
- Plain-language explanation: An agreement announcement and a signature are distinct milestones, and both successive contracts can ultimately pay YES.
- Qualifying condition A (Polymarket): rare-earth agreement by March 31; public announcement qualifies
- Qualifying condition B (Polymarket): minerals agreement signed or formally adopted by April 30; announcement alone fails
- Recorded settlements: A = resolved YES; normalized payout $1; B = resolved YES; normalized payout $1
- Contract identifiers: A = 521607; B = 532897
- Audit boundary: Different windows, rare-earth/mineral scope and evidence authorities prevent a controlled milestone comparison. The YES/YES chronology does not instantiate the supplementary hypothetical YES/NO witness and establishes no manipulation or erroneous March outcome.
- Claim relation: overlap_non_nested; representation: question_rule_binary_model
- Relation confidence: high within stated archived-rule model; not a probability
- Source-scoped relation audit: Scope: supplied API fields and explicitly linked evidence; historical governing specifications and all platform fallbacks are not certified. The supplied question rules match the successive minerals witnesses: announcement-only March 31 agreement can give A=1,B=0; no March agreement and qualifying April signature can give A=0,B=1; both milestones can give A=1,B=1. Different windows, scopes and authorities prevent nesting. Observed outcomes are YES/YES; the April 30 signing and March 25/May 4 closure records are chronology, not a realized payout split or a synchronized market comparison.
- Probability implication: none; coherence test applicable (semantic gate): False
- Sources: [A: Polymarket](https://polymarket.com/event/ukraine-agrees-to-give-trump-rare-earth-metals-before-april); [B: Polymarket](https://polymarket.com/event/trump-x-ukraine-mineral-deal-signed-before-may)
- Exact archived rules: This market will resolve to "Yes" if the United States and Ukraine agree to any deal between February 2 and March 31, 2025, 11:59 PM ET, that explicitly involves Ukrainian rare earth elements. Otherwise this market will resolve to "No".

This includes, but is not limited to, agreements related to the exchange of Ukrainian rare earths for U.S. aid (military or civilian), partnerships involving rare earth metals, future rights to rare earth resources, mining rights, or any other form of cooperation related to rare earth elements.

An announcement of a deal will qualify regardless of if/when the deal is enacted.

The resolution source for this market will be official information from the governments of the US and Ukraine. || This market will resolve to "Yes" if the United States and Ukraine enact or sign any deal between March 31 and April 30, 2025, 11:59 PM ET, that explicitly involves Ukrainian minerals. Otherwise this market will resolve to "No".

Qualifying mineral deals include but are not limited partnerships involving minerals, future rights to mineral resources, mining rights, or any other form of cooperation related to Ukrainian minerals.

For the purpose of this market "enacted" means that the agreement has been officially signed or otherwise formally adopted by both parties within the market’s time frame. A qualifying agreement which is signed by both parties will qualify, regardless of whether it is later ratified by relevant bodies (U.S. Congress, Verkhovna Rada, etc.).

Announcements of an agreement will not alone qualify for a "Yes" resolution.

The resolution source for this market will be official information from the governments of the US and Ukraine and a consensus of credible reporting.
- Snapshot date label: unrecorded for follow-up API responses preserved in the October review; coder confidence: high

- Chronology: March 25, 2025 00:21:27 UTC: agreement-contract closure record; April 30: official signing announcement; May 4 01:10:41 UTC: signed-deal-contract closure record.

- Independent event source: [THEORY_REVIEW.md C2; dated Treasury announcement](https://home.treasury.gov/news/press-releases/sb0126); Reconstruction investment fund agreement signed April 30, 2025.
- Independent event source: [THEORY_REVIEW.md C2; Ukrainian ministry account](https://me.gov.ua/News/Detail/91af98f8-9ae6-49ba-99ae-adb847fe493a?lang=en-GB); Independently records the April 30, 2025 signing date.

- Exact settlement evidence: {"a": {"closed": true, "closedTime": "2025-03-25 00:21:27+00", "id": "521607", "outcomePrices": "[\"1\", \"0\"]", "outcomes": "[\"Yes\", \"No\"]", "umaResolutionStatus": "resolved", "umaResolutionStatuses": "[]"}, "b": {"closed": true, "closedTime": "2025-05-04 01:10:41+00", "id": "532897", "outcomePrices": "[\"1\", \"0\"]", "outcomes": "[\"Yes\", \"No\"]", "umaResolutionStatus": "resolved", "umaResolutionStatuses": "[\"proposed\", \"disputed\", \"proposed\", \"disputed\"]"}, "boundary": "Recorded contract outcomes; no token redemption or account cash-flow audit.", "checked_at_utc": null, "original_http_acquisition_time": null, "source_check": "minerals-march-event-current.json; minerals-april-event-current.json"}

## Supplementary hypothetical boundary scenarios

### 2028 U.S. presidential winner

Scenario, implied payout and settlement assertions are withheld pending source-version or changed-input review.
- Audit status: Required source versions or scenario/settlement assertions lack a current audit of their stated scope; manual review required. Dependent assertions withheld.
- Contract A: KXPRESPERSON-28-MRUB; question: Who will win the next presidential election?
- Contract B: 561234; question: Will Marco Rubio win the 2028 US Presidential Election?
- Exact current input rules: If Marco Rubio is the next person inaugurated as President for the term beginning in 2029, then the market resolves to Yes. || The 2028 US Presidential Election is scheduled to take place on November 7, 2028.

This market will resolve to the person who wins the 2028 US Presidential Election.

The resolution source for this market is the Associated Press, Fox News, and NBC. This market will resolve once all three sources call the race for the same candidate. If all three sources haven’t called the race for the same candidate by the inauguration date (January 20, 2029) this market will resolve based on who is inaugurated.

### September 2026 Federal Reserve decision

The target-range upper bound falls by an unusual 12.5 bp.

- Scope: cross-platform
- Evidence status: hypothetical witness; archived rules, not a realized payout audit
- Rule dimension: measurement-bucket divergence (rounding)
- Plain-language explanation: Even numerical markets need a rule for assigning an unusual measurement to an answer bucket.
- Qualifying condition A (Kalshi): exactly a 25 bp cut within a mutually exclusive bucket family
- Qualifying condition B (Polymarket): upper-bound change rounded up to 25 bp increments; no-statement fallback
- Implied payouts: A = NO under the literal exact-25-bp rule; B = YES because 12.5 bp rounds up to the 25-bp bucket
- Contract identifiers: A = KXFEDDECISION-26SEP-C25; B = 2252243
- Audit boundary: The witness isolates rounding under the archived literal Kalshi wording. Cancellation and no-statement fallbacks also differ, but are not tested by this scenario.
- Claim relation: non_equivalent_unclassified; representation: binary_reading_unvalidated
- Relation confidence: conditional on literal archived wording
- Source-scoped relation audit: Scope: supplied API fields and explicitly linked evidence; historical governing specifications and all platform fallbacks are not certified. The 12.5 bp witness proves non-equivalence conditional on literal Kalshi wording. The September 16 criterion and cancellation-to-no-change clause differ from the Polymarket upper-bound measurement, rounding and no-statement fallback through the next meeting. No full-state binary mapping or global inclusion is validated.
- Probability implication: none; coherence test applicable (semantic gate): False
- Sources: [A: Kalshi](https://kalshi.com/markets/kxfeddecision-26sep-c25); [B: Polymarket](https://polymarket.com/event/will-the-fed-decrease-interest-rates-by-25-bps-after-the-september-2026-meeting-586)
- Exact archived rules: If the Federal Reserve does a Cut of 25bps on September 16, 2026, then the market resolves to Yes.
This market is mutually exclusive. Therefore, if the Federal Reserve hikes by 50bps, the 50bps market will resolve to Yes and the 25bps market will resolve to No. Only one bucket, at maximum, can resolve to Yes. Note 4/28/25: For the markets beginning after the May meeting, if a scheduled FOMC meeting is canceled and does not occur on its scheduled date, then the strike for "Fed maintains rate" will resolve to Yes and all others will resolve to No. || The FED interest rates are defined in this market by the upper bound of the target federal funds range. The decisions on the target federal funds range are made by the Federal Open Market Committee (FOMC) meetings.

This market will resolve to the amount of basis points the upper bound of the target federal funds rate is changed by versus the level it was prior to the Federal Reserve's September 2026 meeting.

If the target federal funds rate is changed to a level not expressed in the displayed options, the change will be rounded up to the nearest 25 and will resolve to the relevant bracket. (e.g. if there's a cut/increase of 12.5 bps it will be considered to be 25 bps)

The resolution source for this market is the FOMC’s statement after its meeting scheduled for September 15-16, 2026 according to the official calendar: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

The level and change of the target federal funds rate is also published at the official website of the Federal Reserve at https://www.federalreserve.gov/monetarypolicy/openmarket.htm.

This market may resolve as soon as the FOMC’s statement for their September meeting with relevant data is issued. If no statement is released by the end date of the next scheduled meeting, this market will resolve to the "No change" bracket.
- Snapshot date label: 2026-09-10; coder confidence: conditional on literal archived Kalshi rule

### Donald Trump leaving office versus being the next leader out

Before the deadline, Trump announces a non-term-limit resignation within the next year but stays in office through 2026. No listed leader leaves by December 31, 2026, 11:59 PM ET.

- Scope: cross-platform
- Evidence status: hypothetical witness; archived rules, not a realized payout audit
- Rule dimension: departure-stage and competing-leader divergence
- Plain-language explanation: Leaving office at some point and being the first listed leader to leave are different bets.
- Qualifying condition A (Kalshi): departure announcement can qualify; death triggers price-based allocation
- Qualifying condition B (Polymarket): Trump must be FIRST among listed leaders to permanently cease office; announcement and caretaker status fail
- Implied payouts: A = YES; B = NO
- Contract identifiers: A = kalshi:KXTRUMPOUT27-27-DJT; B = polymarket:1116033
- Audit boundary: The primary witness separates announcement from actual departure. The second isolates competition with other leaders. Kalshi's death-allocation clause is an additional rule feature, not demonstrated by either witness.
- Claim relation: non_equivalent_unclassified; representation: non_binary_and_adjudicated_exceptions
- Relation confidence: high within stated archived-rule model; not a probability
- Source-scoped relation audit: Scope: supplied API fields and explicitly linked evidence; historical governing specifications and all platform fallbacks are not certified. Announcement and competing-departure witnesses establish payout divergence. Kalshi's death-only clause uses the last traded price or committee fair allocation; it is not a binary mapping over all histories. Polymarket requires first permanent departure among the fixed leader list, excludes caretaker/temporary status, and has a December 31 ET fallback. No global binary superset restriction is justified.
- Probability implication: none; coherence test applicable (semantic gate): False
- Sources: [A: Kalshi](https://external-api.kalshi.com/trade-api/v2/markets/KXTRUMPOUT27-27-DJT); [B: Polymarket](https://gamma-api.polymarket.com/markets/1116033)
- Exact archived rules: If Donald Trump leaves office before Jan 1, 2027, then the market resolves to Yes.
An announcement that the President will leave the office within the next year is also encompassed by the Payout Criterion. An acknowledgement by Donald Trump that they will leave office due solely to the scheduled expiration of a constitutionally or legally mandated term limit does not satisfy the Payout Criterion.

If Donald Trump leaves solely because they have died, the associated market will resolve and the Exchange will determine the payouts to the holders of long and short positions based upon the last traded price (prior to the death). If a last traded price is not available or is not logically consistent, or if the Exchange determines at its sole discretion that the last traded prices prior to death do not represent a fair settlement value, the Outcome Review Committee will be responsible for making a binding determination of fair allocation.
This market will close and expire early if the event occurs. || This market will resolve according to the first individual who ceases to occupy their listed office.

An announcement of a resignation/removal, or a scheduled departure from office due to the outcome of an election, will not alone qualify.

Only permanent removal from office will qualify for resolution. Temporary removals, such as impeachment suspensions (e.g., Yoon Suk Yeol's recent impeachment), temporary invocation of the 25th Amendment, or any similar provisional transfers of power, will not count.

Additionally, if an individual continues in a caretaker or interim role (e.g., Gabriel Attal remaining as caretaker Prime Minister of France), they will not be considered to have ceased occupying the office for the purposes of this market.

If this criteria has not been met for any of the listed individuals by December 31, 2026, 11:59 PM ET, this market will resolve to “None before 2027”. No additional individuals will be added to this market after its creation.

The resolution source for this market will be a consensus of credible reporting.
- Snapshot date label: 2026-09-10; coder confidence: high

- Additional witness: Another listed leader permanently leaves first; Trump subsequently resigns and permanently leaves before 2027, without dying.
- Additional implied settlements: A = YES; B = NO

### U.S.–Ukraine minerals agreement

On March 31, 2025 before 11:59 PM ET, both governments announce a deal explicitly involving Ukrainian rare earths. No qualifying mineral deal is signed, enacted, or formally adopted through April 30, 2025, 11:59 PM ET.

- Scope: within-platform across successive contracts
- Evidence status: hypothetical witness; archived rules, not a realized payout audit
- Rule dimension: milestone-stage divergence
- Plain-language explanation: Saying 'we have a deal' and signing the deal are different milestones.
- Qualifying condition A (Polymarket): public announcement that a deal has been reached can qualify
- Qualifying condition B (Polymarket): deal must be enacted, signed, or formally adopted; announcement alone fails
- Implied payouts: A = YES; B = NO
- Contract identifiers: A = 521607; B = 532897
- Audit boundary: Successive Polymarket contracts also differ in dates, rare-earth versus mineral scope, and evidence sources. The witness specifies rare earths and both windows; this is not a synchronized cross-platform comparison.
- Claim relation: overlap_non_nested; representation: question_rule_binary_model
- Relation confidence: high within stated archived-rule model; not a probability
- Source-scoped relation audit: Scope: supplied API fields and explicitly linked evidence; historical governing specifications and all platform fallbacks are not certified. Both governments announce a rare-earth deal on March 31 but never formally adopt any mineral deal through April 30: A=1,B=0. No deal by March 31, then an officially documented rare-earth deal signed on April 15: A=0,B=1. A March 31 rare-earth announcement followed by an April 15 signature: A=1,B=1. All times fall within the respective ET windows, with official information and credible reporting in agreement. Distinct windows, mineral scope and authorities prevent nesting; these successive contracts are not a synchronized market pair.
- Probability implication: none; coherence test applicable (semantic gate): False
- Sources: [A: Polymarket](https://polymarket.com/event/ukraine-agrees-to-give-trump-rare-earth-metals-before-april); [B: Polymarket](https://polymarket.com/event/trump-x-ukraine-mineral-deal-signed-before-may)
- Exact archived rules: This market will resolve to "Yes" if the United States and Ukraine agree to any deal between February 2 and March 31, 2025, 11:59 PM ET, that explicitly involves Ukrainian rare earth elements. Otherwise this market will resolve to "No".

This includes, but is not limited to, agreements related to the exchange of Ukrainian rare earths for U.S. aid (military or civilian), partnerships involving rare earth metals, future rights to rare earth resources, mining rights, or any other form of cooperation related to rare earth elements.

An announcement of a deal will qualify regardless of if/when the deal is enacted.

The resolution source for this market will be official information from the governments of the US and Ukraine. || This market will resolve to "Yes" if the United States and Ukraine enact or sign any deal between March 31 and April 30, 2025, 11:59 PM ET, that explicitly involves Ukrainian minerals. Otherwise this market will resolve to "No".

Qualifying mineral deals include but are not limited partnerships involving minerals, future rights to mineral resources, mining rights, or any other form of cooperation related to Ukrainian minerals.

For the purpose of this market "enacted" means that the agreement has been officially signed or otherwise formally adopted by both parties within the market’s time frame. A qualifying agreement which is signed by both parties will qualify, regardless of whether it is later ratified by relevant bodies (U.S. Congress, Verkhovna Rada, etc.).

Announcements of an agreement will not alone qualify for a "Yes" resolution.

The resolution source for this market will be official information from the governments of the US and Ukraine and a consensus of credible reporting.
- Snapshot date label: 2026-09-10; coder confidence: high

### Tom Steyer finishing first versus advancing in the California primary

Steyer finishes second without a tie in the June 2, 2026 primary and advances to the general election.

- Scope: cross-platform; retrieved from systematic sample
- Evidence status: hypothetical witness; archived rules, not a realized payout audit
- Rule dimension: rank versus qualification divergence
- Plain-language explanation: A runner-up can lose the contest for first place and still qualify for the next round.
- Qualifying condition A (Kalshi): must finish first in the California gubernatorial primary
- Qualifying condition B (Polymarket): must advance to the general election; top two candidates qualify
- Implied payouts: A = NO; B = YES
- Contract identifiers: A = kalshi:KXCAGOVPRIMARY1ST-26JUN02-1ST-TSTE; B = polymarket:825450
- Audit boundary: This is a hypothetical second-place scenario, not a claim about the observed primary result. Similar headlines retrieved the pair; different success conditions prevent a claim-equivalence label.
- Claim relation: non_equivalent_unclassified; representation: non_binary_exceptions
- Relation confidence: high within stated archived-rule model; not a probability
- Source-scoped relation audit: Scope: supplied API fields and explicitly linked evidence; historical governing specifications and all platform fallbacks are not certified. Second place without a tie establishes payout divergence. Kalshi pays 1/n in exact ties, ranks withdrawn/disqualified candidates remaining on the ballot, and pays NO for cancellation/postponement beyond expiration. Polymarket asks actual advancement, with a December 31 cutoff and official-results fallback. The full Kalshi mapping is not binary; no binary subset restriction is imposed.
- Probability implication: none; coherence test applicable (semantic gate): False
- Sources: [A: Kalshi](https://external-api.kalshi.com/trade-api/v2/markets/KXCAGOVPRIMARY1ST-26JUN02-1ST-TSTE); [B: Polymarket](https://gamma-api.polymarket.com/markets/825450)
- Exact archived rules: If Tom Steyer finishes in 1st place in the 2026 California Governor primary election, then the market resolves to Yes.
This market resolves based solely on the primary election results, not any subsequent general election. Ranking is determined by the specified counting method. For plurality voting: rank is based on vote count or percentage. For ranked choice voting: rank is determined by elimination order (runner-up is eliminated in final round for second place). For two-round systems: rank is based on final round results if it proceeds to second round, otherwise first-round totals. For proportional representation: rank follows the electoral authority's final seat allocation order. In case of exact ties, markets resolve proportionally (1/number of tied entities). Write-in candidates achieving the specified rank resolve all named candidate markets to No unless a specific "Write-in" or "Other" option exists. Candidates who withdraw or are disqualified after the filing deadline but remain on the ballot are ranked based on votes received. If the election is cancelled or postponed beyond expiration, all markets resolve to No.
This market will close and expire early if certified election results are published. || The non-partisan primary election for Governor of California is scheduled to take place on June 2, 2026. The top two candidates in this election by number of votes won will advance to the general election for Governor of California.

This market will resolve to “Yes” If the listed candidate advances from the primary to the general election for Governor of California. Otherwise this market will resolve to “No”.

If no 2026 California gubernatorial primary takes place by December 31, 2026, this market will resolve to “No.”

This market will resolve based on the results of the primary election for Governor of California as indicated by a consensus of credible reporting. If there is ambiguity, this market will resolve based solely on the official results as reported by the government of California, specifically the Office of the Secretary of State.
- Snapshot date label: 2026-09-10; coder confidence: high

