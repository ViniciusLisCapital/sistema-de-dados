# Bank FX Position (Posição de Câmbio)

**Type:** Market-structure concept / flow-and-stock accounting
**Tags:** #fx-position #fx-flows #saldo-cambial #banks #brl #bcb

---

## Definition

The *posição de câmbio* of an institution authorized to trade foreign exchange in Brazil is the accumulated net result of all its contracted purchases and sales of foreign currency (spot, future or forward) since it began operating, recorded daily. It is *long* (comprada) when purchases exceed sales, *short* (vendida) when sales exceed purchases, and flat otherwise. The system's position is the sum over all authorized institutions; the BCB is not part of it. It is one of four indicators that are easily confused:

| Indicator | What it measures | When it moves |
|---|---|---|
| Posição de câmbio | accumulated stock of contracted FX purchases minus sales | on contracting (interbank forwards: two business days before settlement) |
| Saldo cambial | flow of purchases minus sales by authorized institutions, excluding operations with the BCB; commercial plus financial | on contracting |
| Disponibilidade cambial | foreign currency actually available after the day's settlements | on settlement, and with movements abroad that the other two do not see |
| Exposição cambial | net position in everything exposed to the exchange rate, including derivatives and gold | the only one subject to a regulatory limit |

## Mechanism

- **Flows move the stock.** A negative saldo cambial (more sales to clients than purchases from them) pushes the system's position short; BCB spot sales are purchases for the banks and reduce the short position, BCB purchases increase it. Interbank trades net out in the aggregate, and repo-type "conjugated" auctions (sale with repurchase) leave the global position unchanged except for a residual.
- **Why banks hold a short position.** A short position frees reais (*encaixe*) that earn the domestic interest rate; its cost is the foreign-currency credit line that funds it, the cost of hedging, and the risk of a depreciation. Whether it pays depends on the domestic rate against the international rate plus the hedge cost. A long position is the mirror image, normally costly because reais cost more to raise than the foreign currency earns abroad.
- **What limits it.** No rule caps the position directly. A bank can settle FX sales against its account at a bank abroad without buying currency at home, so as long as it can fund that account and stays within its exposure limit, the size of the position is a business decision. The cap works indirectly through the exposure limit, which in the BCB's 2020 description is 30% of regulatory capital. Non-bank institutions cannot do this, because their foreign-currency account sits at a bank in Brazil and moves only through FX operations.

## When it applies / when it fails

- The stock reflects the flow only as long as the BCB stays out: when the BCB sells spot dollars, a deeply negative saldo cambial need not show up as an equally deep short position (Brazil 2019, in the source below).
- The position and the cash available can diverge: position and flow are recorded on contracting, availability on settlement; operations booked only abroad, and cash exchange (banknotes, traveller's cheques), affect one but not the others.
- International reserves move on settlement of BCB interventions, not on contracting, so they do not change on the same date as the banks' position.
- The descriptions here are those of the regulation in force in 2019–2020.

## How it appears across sources

| Source | Role |
|---|---|
| [[exchange_rate/synthesis/posicao_de_cambio (BCB, 2020)]] | Defines the position and the three related indicators, explains why the system stays short (interest differential against hedge and funding costs) and why there is no direct limit; 2019 case: BCB spot sales kept the system's short position far below what the year's negative saldo cambial would have produced |

## BRL / application to the current analysis

The source is Brazilian. It says that a very negative saldo cambial that deepens the banks' short position can call for BCB intervention as a supplier of foreign currency, to reduce the cost of dollar liquidity in Brazil measured by the spread of the cupom cambial over US Treasuries; and that spot auctions, changes in tax rates that affect FX flows, and the exposure limit are the available tools for adjusting excessive positions.

## Connections

- [[capital_controls]] — Brazil's reserve requirement on banks' gross short spot FX positions acted on this stock
- [[exchange_rate/synthesis/posicao_de_cambio (BCB, 2020)]] — definitions, the economics of the short position, and the 2019 BCB auctions
