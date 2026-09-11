# Representation Casebook

These cases establish mechanisms, not average effects. A divergence claim requires a plausible witness state for which the represented payouts differ.

## 2028 U.S. presidential winner

- Scope: cross-platform
- Mechanism: predicate-stage and temporal divergence
- Representation A (Kalshi): next person inaugurated for the term beginning in 2029
- Representation B (Polymarket): candidate called winner by AP, Fox News, and NBC; inauguration fallback
- Witness state: All three networks call Rubio, but he dies or is disqualified before inauguration.
- Implied settlements: A = NO; B = YES
- Exact archived rules: If Marco Rubio is the next person inaugurated as President for the term beginning in 2029, then the market resolves to Yes. || The 2028 US Presidential Election is scheduled to take place on November 7, 2028.

This market will resolve to the person who wins the 2028 US Presidential Election.

The resolution source for this market is the Associated Press, Fox News, and NBC. This market will resolve once all three sources call the race for the same candidate. If all three sources haven’t called the race for the same candidate by the inauguration date (January 20, 2029) this market will resolve based on who is inaugurated.
- Retrieval date: 2026-09-10; coder confidence: high

## September 2026 Federal Reserve decision

- Scope: cross-platform
- Mechanism: measurement, quantization, and fallback divergence
- Representation A (Kalshi): exactly a 25 bp cut within a mutually exclusive bucket family
- Representation B (Polymarket): upper-bound change rounded up to 25 bp increments; no-statement fallback
- Witness state: The target-range upper bound falls by an unusual 12.5 bp.
- Implied settlements: A = NO under the literal exact-25-bp rule; B = YES because 12.5 bp rounds up to the 25-bp bucket
- Exact archived rules: If the Federal Reserve does a Cut of 25bps on September 16, 2026, then the market resolves to Yes.
This market is mutually exclusive. Therefore, if the Federal Reserve hikes by 50bps, the 50bps market will resolve to Yes and the 25bps market will resolve to No. Only one bucket, at maximum, can resolve to Yes. Note 4/28/25: For the markets beginning after the May meeting, if a scheduled FOMC meeting is canceled and does not occur on its scheduled date, then the strike for "Fed maintains rate" will resolve to Yes and all others will resolve to No. || The FED interest rates are defined in this market by the upper bound of the target federal funds range. The decisions on the target federal funds range are made by the Federal Open Market Committee (FOMC) meetings.

This market will resolve to the amount of basis points the upper bound of the target federal funds rate is changed by versus the level it was prior to the Federal Reserve's September 2026 meeting.

If the target federal funds rate is changed to a level not expressed in the displayed options, the change will be rounded up to the nearest 25 and will resolve to the relevant bracket. (e.g. if there's a cut/increase of 12.5 bps it will be considered to be 25 bps)

The resolution source for this market is the FOMC’s statement after its meeting scheduled for September 15-16, 2026 according to the official calendar: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

The level and change of the target federal funds rate is also published at the official website of the Federal Reserve at https://www.federalreserve.gov/monetarypolicy/openmarket.htm.

This market may resolve as soon as the FOMC’s statement for their September meeting with relevant data is issued. If no statement is released by the end date of the next scheduled meeting, this market will resolve to the "No change" bracket.
- Retrieval date: 2026-09-10; coder confidence: high

## Donald Trump leaving office before 2027

- Scope: cross-platform
- Mechanism: stage, edge-case, and settlement-codomain divergence
- Representation A (Kalshi): departure announcement can qualify; death triggers price-based allocation
- Representation B (Polymarket): only permanent cessation qualifies; announcement and caretaker status fail
- Witness state: Trump announces a qualifying resignation date but remains in office past the deadline.
- Implied settlements: A = YES; B = NO
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

## U.S.–Ukraine minerals agreement

- Scope: within-platform across successive contracts
- Mechanism: milestone-stage divergence
- Representation A (Polymarket): public announcement that a deal has been reached can qualify
- Representation B (Polymarket): deal must be enacted, signed, or formally adopted; announcement alone fails
- Witness state: Both governments announce an agreement, but no instrument is signed or adopted.
- Implied settlements: A = YES; B = NO
- Exact archived rules: This market will resolve to "Yes" if the United States and Ukraine agree to any deal between February 2 and March 31, 2025, 11:59 PM ET, that explicitly involves Ukrainian rare earth elements. Otherwise this market will resolve to "No". 

This includes, but is not limited to, agreements related to the exchange of Ukrainian rare earths for U.S. aid (military or civilian), partnerships involving rare earth metals, future rights to rare earth resources, mining rights, or any other form of cooperation related to rare earth elements.

An announcement of a deal will qualify regardless of if/when the deal is enacted.  

The resolution source for this market will be official information from the governments of the US and Ukraine.
 || This market will resolve to "Yes" if the United States and Ukraine enact or sign any deal between March 31 and April 30, 2025, 11:59 PM ET, that explicitly involves Ukrainian minerals. Otherwise this market will resolve to "No".

Qualifying mineral deals include but are not limited partnerships involving minerals, future rights to mineral resources, mining rights, or any other form of cooperation related to Ukrainian minerals.

For the purpose of this market "enacted" means that the agreement has been officially signed or otherwise formally adopted by both parties within the market’s time frame. A qualifying agreement which is signed by both parties will qualify, regardless of whether it is later ratified by relevant bodies (U.S. Congress, Verkhovna Rada, etc.). 

Announcements of an agreement will not alone qualify for a "Yes" resolution. 

The resolution source for this market will be official information from the governments of the US and Ukraine and a consensus of credible reporting.
- Retrieval date: 2026-09-10; coder confidence: high

## Zelenskyy wearing a suit

- Scope: within-contract
- Mechanism: category-boundary indeterminacy
- Representation A (Polymarket): photographed or videotaped wearing a suit; no garment definition
- Representation B (Observed world state): borderline observed attire
- Witness state: Zelenskyy wears a blazer and trousers that do not match, with no tie.
- Implied settlements: A = YES or NO: the rule does not uniquely classify the attire; B = N/A—witness to within-contract indeterminacy
- Exact archived rules: This market will resolve to "Yes" if Volodymyr Zelenskyy is is photographed or videotaped wearing a suit between May 22 and June 30, 2025 ET. Otherwise, this market will resolve to "No".

For this market to resolve to "Yes" the images or video must be taken and released within this market's timeframe. The images or video must be authentic, not the result of artificial intelligence or video editing.

The resolution source will be a consensus of credible reporting. || No additional garment-level definition is supplied by the contract.
- Retrieval date: 2026-09-10; coder confidence: high

