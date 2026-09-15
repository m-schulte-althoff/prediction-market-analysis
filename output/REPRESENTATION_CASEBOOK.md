# Representation Casebook

These cases establish mechanisms, not average effects. A divergence claim requires a plausible witness state for which the represented payouts differ.
The rules are archived observations; the witness scenarios are hypothetical. The suit case instead illustrates the limits of the written category definition.
A common posterior over world histories can value different payout claims differently. The relation audit adds no price result: a witness does not prove nesting, and fractional settlements fall outside a binary-event restriction. See [constructs and source bridge](../docs/CONSTRUCTS.md).

## 2028 U.S. presidential winner

- Scope: cross-platform
- Mechanism: predicate-stage and temporal divergence
- Plain-language explanation: Winning the news call and actually taking office are different milestones.
- Representation A (Kalshi): next person inaugurated for the term beginning in 2029
- Representation B (Polymarket): candidate called winner by AP, Fox News, and NBC; inauguration fallback
- Witness state: All three networks call Rubio, but he dies or is disqualified before inauguration.
- Implied settlements: A = NO; B = YES
- Audit boundary: The scenario assumes all three calls occur before inauguration; it is not an observed election outcome.
- Claim relation: overlap_non_nested; representation: determinate_binary
- Relation confidence: high within stated archived-rule model; not a probability
- Complete-rule relation audit: Under the archived binary reading: Rubio called by all three sources but never inaugurated gives A=0,B=1. All three call another candidate, who is then unable to take office, and Rubio is inaugurated for the 2029 term gives A=1,B=0. Rubio called and inaugurated gives A=1,B=1. The inauguration fallback applies only absent a unanimous call by January 20, 2029. These existence witnesses establish overlap and both differences, not a marginal probability ordering.
- Probability implication: none; coherence test applicable (semantic gate): False
- Sources: [A: Kalshi](https://kalshi.com/markets/kxpresperson-28-mrub); [B: Polymarket](https://polymarket.com/event/will-marco-rubio-win-the-2028-us-presidential-election)
- Exact archived rules: If Marco Rubio is the next person inaugurated as President for the term beginning in 2029, then the market resolves to Yes. || The 2028 US Presidential Election is scheduled to take place on November 7, 2028.

This market will resolve to the person who wins the 2028 US Presidential Election.

The resolution source for this market is the Associated Press, Fox News, and NBC. This market will resolve once all three sources call the race for the same candidate. If all three sources haven’t called the race for the same candidate by the inauguration date (January 20, 2029) this market will resolve based on who is inaugurated.
- Retrieval date: 2026-09-10; coder confidence: high

## September 2026 Federal Reserve decision

- Scope: cross-platform
- Mechanism: measurement-bucket divergence (rounding)
- Plain-language explanation: Even numerical markets need a rule for assigning an unusual measurement to an answer bucket.
- Representation A (Kalshi): exactly a 25 bp cut within a mutually exclusive bucket family
- Representation B (Polymarket): upper-bound change rounded up to 25 bp increments; no-statement fallback
- Witness state: The target-range upper bound falls by an unusual 12.5 bp.
- Implied settlements: A = NO under the literal exact-25-bp rule; B = YES because 12.5 bp rounds up to the 25-bp bucket
- Audit boundary: The witness isolates rounding under the archived literal Kalshi wording. Cancellation and no-statement fallbacks also differ, but are not tested by this scenario.
- Claim relation: non_equivalent_unclassified; representation: binary_reading_unvalidated
- Relation confidence: conditional on literal archived wording
- Complete-rule relation audit: The 12.5 bp witness proves non-equivalence conditional on literal Kalshi wording. The September 16 criterion and cancellation-to-no-change clause differ from the Polymarket upper-bound measurement, rounding and no-statement fallback through the next meeting. No full-state binary mapping or global inclusion is validated.
- Probability implication: none; coherence test applicable (semantic gate): False
- Sources: [A: Kalshi](https://kalshi.com/markets/kxfeddecision-26sep-c25); [B: Polymarket](https://polymarket.com/event/will-the-fed-decrease-interest-rates-by-25-bps-after-the-september-2026-meeting-586)
- Exact archived rules: If the Federal Reserve does a Cut of 25bps on September 16, 2026, then the market resolves to Yes.
This market is mutually exclusive. Therefore, if the Federal Reserve hikes by 50bps, the 50bps market will resolve to Yes and the 25bps market will resolve to No. Only one bucket, at maximum, can resolve to Yes. Note 4/28/25: For the markets beginning after the May meeting, if a scheduled FOMC meeting is canceled and does not occur on its scheduled date, then the strike for "Fed maintains rate" will resolve to Yes and all others will resolve to No. || The FED interest rates are defined in this market by the upper bound of the target federal funds range. The decisions on the target federal funds range are made by the Federal Open Market Committee (FOMC) meetings.

This market will resolve to the amount of basis points the upper bound of the target federal funds rate is changed by versus the level it was prior to the Federal Reserve's September 2026 meeting.

If the target federal funds rate is changed to a level not expressed in the displayed options, the change will be rounded up to the nearest 25 and will resolve to the relevant bracket. (e.g. if there's a cut/increase of 12.5 bps it will be considered to be 25 bps)

The resolution source for this market is the FOMC’s statement after its meeting scheduled for September 15-16, 2026 according to the official calendar: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

The level and change of the target federal funds rate is also published at the official website of the Federal Reserve at https://www.federalreserve.gov/monetarypolicy/openmarket.htm.

This market may resolve as soon as the FOMC’s statement for their September meeting with relevant data is issued. If no statement is released by the end date of the next scheduled meeting, this market will resolve to the "No change" bracket.
- Retrieval date: 2026-09-10; coder confidence: conditional on literal archived Kalshi rule

## Donald Trump leaving office versus being the next leader out

- Scope: cross-platform
- Mechanism: departure-stage and competing-leader divergence
- Plain-language explanation: Leaving office at some point and being the first listed leader to leave are different bets.
- Representation A (Kalshi): departure announcement can qualify; death triggers price-based allocation
- Representation B (Polymarket): Trump must be FIRST among listed leaders to permanently cease office; announcement and caretaker status fail
- Witness state: Before the deadline, Trump announces a non-term-limit resignation within the next year but stays in office through 2026. No listed leader leaves by December 31, 2026, 11:59 PM ET.
- Implied settlements: A = YES; B = NO
- Audit boundary: The primary witness separates announcement from actual departure. The second isolates competition with other leaders. Kalshi's death-allocation clause is an additional rule feature, not demonstrated by either witness.
- Claim relation: non_equivalent_unclassified; representation: non_binary_and_adjudicated_exceptions
- Relation confidence: high within stated archived-rule model; not a probability
- Complete-rule relation audit: Announcement and competing-departure witnesses establish payout divergence. Kalshi's death-only clause uses the last traded price or committee fair allocation; it is not a binary mapping over all histories. Polymarket requires first permanent departure among the fixed leader list, excludes caretaker/temporary status, and has a December 31 ET fallback. No global binary superset restriction is justified.
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
- Retrieval date: 2026-09-10; coder confidence: high

- Additional witness: Another listed leader permanently leaves first; Trump subsequently resigns and permanently leaves before 2027, without dying.
- Additional implied settlements: A = YES; B = NO

## U.S.–Ukraine minerals agreement

- Scope: within-platform across successive contracts
- Mechanism: milestone-stage divergence
- Plain-language explanation: Saying 'we have a deal' and signing the deal are different milestones.
- Representation A (Polymarket): public announcement that a deal has been reached can qualify
- Representation B (Polymarket): deal must be enacted, signed, or formally adopted; announcement alone fails
- Witness state: On March 31, 2025 before 11:59 PM ET, both governments announce a deal explicitly involving Ukrainian rare earths. No qualifying mineral deal is signed, enacted, or formally adopted through April 30, 2025, 11:59 PM ET.
- Implied settlements: A = YES; B = NO
- Audit boundary: Successive Polymarket contracts also differ in dates, rare-earth versus mineral scope, and evidence sources. The witness specifies rare earths and both windows; this is not a synchronized cross-platform comparison.
- Claim relation: overlap_non_nested; representation: determinate_binary
- Relation confidence: high within stated archived-rule model; not a probability
- Complete-rule relation audit: Both governments announce a rare-earth deal on March 31 but never formally adopt any mineral deal through April 30: A=1,B=0. No deal by March 31, then an officially documented rare-earth deal signed on April 15: A=0,B=1. A March 31 rare-earth announcement followed by an April 15 signature: A=1,B=1. All times fall within the respective ET windows, with official information and credible reporting in agreement. Distinct windows, mineral scope and authorities prevent nesting; these successive contracts are not a synchronized market pair.
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
- Retrieval date: 2026-09-10; coder confidence: high

## Tom Steyer finishing first versus advancing in the California primary

- Scope: cross-platform; retrieved from systematic sample
- Mechanism: rank versus qualification divergence
- Plain-language explanation: A runner-up can lose the contest for first place and still qualify for the next round.
- Representation A (Kalshi): must finish first in the California gubernatorial primary
- Representation B (Polymarket): must advance to the general election; top two candidates qualify
- Witness state: Steyer finishes second without a tie in the June 2, 2026 primary and advances to the general election.
- Implied settlements: A = NO; B = YES
- Audit boundary: This is a hypothetical second-place scenario, not a claim about the observed primary result. Similar headlines retrieved the pair; different success conditions prevent a claim-equivalence label.
- Claim relation: non_equivalent_unclassified; representation: non_binary_exceptions
- Relation confidence: high within stated archived-rule model; not a probability
- Complete-rule relation audit: Second place without a tie establishes payout divergence. Kalshi pays 1/n in exact ties, ranks withdrawn/disqualified candidates remaining on the ballot, and pays NO for cancellation/postponement beyond expiration. Polymarket asks actual advancement, with a December 31 cutoff and official-results fallback. The full Kalshi mapping is not binary; no binary subset restriction is imposed.
- Probability implication: none; coherence test applicable (semantic gate): False
- Sources: [A: Kalshi](https://external-api.kalshi.com/trade-api/v2/markets/KXCAGOVPRIMARY1ST-26JUN02-1ST-TSTE); [B: Polymarket](https://gamma-api.polymarket.com/markets/825450)
- Exact archived rules: If Tom Steyer finishes in 1st place in the 2026 California Governor primary election, then the market resolves to Yes.
This market resolves based solely on the primary election results, not any subsequent general election. Ranking is determined by the specified counting method. For plurality voting: rank is based on vote count or percentage. For ranked choice voting: rank is determined by elimination order (runner-up is eliminated in final round for second place). For two-round systems: rank is based on final round results if it proceeds to second round, otherwise first-round totals. For proportional representation: rank follows the electoral authority's final seat allocation order. In case of exact ties, markets resolve proportionally (1/number of tied entities). Write-in candidates achieving the specified rank resolve all named candidate markets to No unless a specific "Write-in" or "Other" option exists. Candidates who withdraw or are disqualified after the filing deadline but remain on the ballot are ranked based on votes received. If the election is cancelled or postponed beyond expiration, all markets resolve to No.
This market will close and expire early if certified election results are published. || The non-partisan primary election for Governor of California is scheduled to take place on June 2, 2026. The top two candidates in this election by number of votes won will advance to the general election for Governor of California.

This market will resolve to “Yes” If the listed candidate advances from the primary to the general election for Governor of California. Otherwise this market will resolve to “No”.

If no 2026 California gubernatorial primary takes place by December 31, 2026, this market will resolve to “No.”

This market will resolve based on the results of the primary election for Governor of California as indicated by a consensus of credible reporting. If there is ambiguity, this market will resolve based solely on the official results as reported by the government of California, specifically the Office of the Secretary of State.
- Retrieval date: 2026-09-10; coder confidence: high

## Zelenskyy wearing a suit

- Scope: within-contract
- Mechanism: category-boundary indeterminacy
- Plain-language explanation: People can see the same clothing and still disagree about whether it counts as a suit.
- Representation A (Polymarket): photographed or videotaped wearing a suit; no garment definition
- Representation B (Hypothetical world state): hypothetical borderline attire with differing descriptions
- Witness state: During May 22–June 30, 2025, authentic images are taken and released showing Zelenskyy in a blazer and nonmatching trousers, without a tie. Credible reports differ on whether this counts as a suit.
- Implied settlements: A = not fixed by garment criteria alone; depends on the credible-reporting adjudication; B = N/A—witness to within-contract indeterminacy
- Audit boundary: The archived text specifies image authenticity and timing but no garment definition. It delegates to credible reporting; this case does not document an actual dispute or prove the final institutional outcome remains indeterminate.
- Claim relation: indeterminate; representation: adjudicatively_incomplete
- Relation confidence: high within stated archived-rule model; not a probability
- Complete-rule relation audit: Authenticity and May 22-June 30 image/release requirements fix evidence conditions, not the garment category. For the borderline attire witness, the text alone does not select a payout; credible-reporting adjudication completes the mapping. This is a within-contract illustration, not a second market or proof that an eventual institutional settlement is undefined.
- Probability implication: none; coherence test applicable (semantic gate): False
- Sources: [A: Polymarket](https://polymarket.com/event/will-zelenskyy-wear-a-suit-before-july)
- Exact archived rules: This market will resolve to "Yes" if Volodymyr Zelenskyy is is photographed or videotaped wearing a suit between May 22 and June 30, 2025 ET. Otherwise, this market will resolve to "No".

For this market to resolve to "Yes" the images or video must be taken and released within this market's timeframe. The images or video must be authentic, not the result of artificial intelligence or video editing.

The resolution source will be a consensus of credible reporting. || No additional garment-level definition is supplied by the contract.
- Retrieval date: 2026-09-10; coder confidence: high for missing garment definition; institutional settlement not inferred

