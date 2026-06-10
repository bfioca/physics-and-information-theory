# Source Verification Log

Audit date: 2026-06-10 UTC
Purpose: establish a reproducible primary-source basis for the Harlow review
packet, not prove publication priority.

## Method

1. Queried the official arXiv API by identifier for every source used in the
   packet matrix. Recorded title, authors, initial-submission year, revision
   status, abstract, journal reference, and DOI when supplied by arXiv.
2. Inspected author-source arXiv HTML for the central claims in:
   - Harlow, Usatyuk, and Zhao, arXiv:2501.02359v2;
   - Costa and Sanchez Sanchez, arXiv:2602.24177v1;
   - Chen and Giacomini, arXiv:2606.09344v1; and
   - De Vuyst et al., arXiv:2405.00114v3.
3. Inspected downloaded author TeX sources for:
   - Bartlett et al., arXiv:quant-ph/0602069v2; and
   - Garmier, Hausmann, and Castro-Ruiz, arXiv:2512.19343v1.
4. For the remaining sources, used official arXiv metadata and author abstracts
   only. The literature matrix does not attribute theorem details beyond what
   those abstracts state.
5. Ran targeted official-API searches for computer-assisted boundary-value
   proofs and for `Skyrmion AND "computer-assisted"`. The latter returned zero
   arXiv records on 2026-06-10. This is recorded only as a search result, not as
   evidence of priority.

Verification used direct official arXiv API, HTML, PDF, and e-print endpoints.
No secondary summary was treated as authoritative.

## Identifier audit

### Observer rules and gravitational algebras

| arXiv | API result | Deeper check | Status |
| --- | --- | --- | --- |
| `2501.02359` | Harlow, Usatyuk, Zhao; exact title and abstract confirmed | HTML abstract/introduction checked for `dim H ~ exp(S_Ob)`, exponentially small error, and decoherence framing | Verified |
| `2602.03835` | Harlow; exact title, author, and abstract confirmed | HTML conversion unavailable; official API abstract checked | Verified metadata and stated abstract scope |
| `2206.10780` | Chandrasekaran, Longo, Penington, Witten; JHEP DOI confirmed | API abstract | Verified |
| `2303.02837` | Witten; exact title and abstract confirmed | API abstract | Verified |
| `2405.00114` | De Vuyst, Eccles, Hoehn, Kirklin; JHEP DOI confirmed | HTML abstract and algebra/entropy discussion checked | Verified |
| `2511.00622` | Chen, Xu; v2 action-model addition and abstract confirmed | API abstract | Verified |

### Finite QRFs, clocks, and physical references

| arXiv | API result | Deeper check | Status |
| --- | --- | --- | --- |
| `quant-ph/0106014` | Bagan, Baig, Muñoz-Tapia; PRL DOI confirmed | API abstract | Verified |
| `quant-ph/0602069` | Bartlett, Rudolph, Spekkens, Turner; NJP DOI confirmed | Author TeX checked for operational longevity, repeated-use disturbance, and quadratic scaling | Verified |
| `0711.0043` | Gour, Spekkens; NJP DOI confirmed | API abstract | Verified |
| `0901.0943` | Gour, Marvian, Spekkens; PRA DOI confirmed | API abstract checked for equality of relative entropy of frameness and `G`-asymmetry | Verified |
| `0812.5040` | Bartlett, Rudolph, Spekkens, Turner; NJP DOI confirmed | API abstract | Verified; title correction noted below |
| `2512.19343` | Garmier, Hausmann, Castro-Ruiz; title/authors confirmed | Author TeX checked for finite resources, superselection, and operational back-reaction | Verified |
| `2603.23598` | de la Hamette; title/author confirmed | API abstract checked for effective-relational-dimension entropy bound | Verified metadata and stated abstract scope |
| `1908.10165` | Castro-Ruiz, Giacomini, Belenchia, Brukner; Nature Communications DOI confirmed | API abstract | Verified |
| `2406.02116` | Chen, Penington; title/authors confirmed | API abstract | Verified |
| `2602.24177` | Costa, Sanchez Sanchez; title/authors confirmed | HTML introduction and conclusion checked for clock accuracy/running-time and two gravitational mass bounds | Verified |
| `2606.09344` | Chen, Giacomini; posted 2026-06-08 | HTML abstract/introduction checked for dynamical scalar reference fields, stress in constraints, relational observables, and measurement model | Verified |
| `2605.30423` | Espíndola, Ali; posted 2026-05-28 | API abstract | Verified metadata and stated abstract scope |

### Open systems, response, Skyrmions, and rigorous numerics

| arXiv | API result | Status |
| --- | --- | --- |
| `1305.0256` | Fukuma, Sakatani, Sugishita; PRD DOI confirmed | Verified |
| `1908.09929` | Akhtar, Choudhury, Chowdhury, Goswami, Panda, Swain; EPJC DOI confirmed | Verified |
| `2004.01469` | Nathan, Rudner; PRB DOI confirmed | Verified |
| `2105.00023` | Merkli; Quantum DOI confirmed | Verified |
| `2307.04800` | Alicki, Barenboim, Jenkins; PRD DOI confirmed | Verified |
| `hep-th/0305147` | Kodama, Ishibashi; journal and DOI confirmed | Verified |
| `gr-qc/0502028` | Martel, Poisson; PRD DOI confirmed | Verified |
| `2010.00593` | Hui, Joyce, Penco, Santoni, Solomon; JCAP DOI confirmed | Verified |
| `hep-th/0512339` | Brihaye, Delsate; exact title and DOI confirmed | Verified |
| `1002.2464` | Hata, Kikuchi; PRD DOI confirmed | Verified |
| `1510.08735` | Gudnason, Nitta, Sawado; JHEP DOI confirmed | Verified |
| `1708.06863` | Giacomini, Lagos, Oliva, Vera; exact title and DOI confirmed | Verified |
| `2210.15895` | Fadhilla, Atmaja, Gunara; exact title/authors confirmed | Verified |
| `1702.07412` | van den Berg, Breden, Lessard, Murray | Verified |
| `2101.03727` | Liu, Nakao, Oishi; DOI confirmed | Verified |

## Corrections to inherited notes

The packet matrix uses corrected primary metadata rather than copying these
imprecisions from the broader repository literature note:

- `arXiv:0812.5040` is *Quantum communication using a bounded-size quantum
  reference frame*, not *Degradation of a quantum reference frame*. The latter
  is `arXiv:quant-ph/0602069`.
- `arXiv:1708.06863` is *Solitons in a cavity for the Einstein-SU(2)
  Non-linear Sigma Model and Skyrme model*, not *Gravitating Skyrmions in a
  cavity*.
- `arXiv:hep-th/0512339` has the title *Skyrmion and Skyrme-Black holes in de
  Sitter spacetime* (singular `Skyrmion` in the source title).
- The phrase "operational back-reaction" in arXiv:2512.19343 concerns the
  non-ideal QRF perspective under operations. It must not be silently promoted
  to gravitational metric backreaction.

## Explicitly unverified conclusions

The following are not established by this audit and must remain qualified:

- No exhaustive priority claim was checked. In particular, absence from the
  targeted arXiv query does not establish that the repository contains the
  first computer-assisted Skyrmion proof or the first rotational observer
  tradeoff.
- No source was found or verified that identifies relative entropy of
  `SO(3)` asymmetry with Harlow's `S_Ob`. The dictionary is open.
- The literature does not validate this repository's microscopic
  KMS-to-directional-record channel; that is a project claim requiring its own
  derivation and norm estimate.
- This audit did not determine that an exterior electric-Weyl response is the
  gravitational quantity that should cap observer capacity.
- It did not verify robustness of the hard-wall profile or response under
  smooth confinement.
- It did not exhaust non-arXiv journals, books, conference proceedings,
  citation chains, or literature using different terminology.

## Reproduction pointers

Official endpoints used:

```text
https://export.arxiv.org/api/query?id_list=<comma-separated identifiers>
https://arxiv.org/html/<identifier-and-version>
https://arxiv.org/pdf/<identifier-and-version>
https://export.arxiv.org/e-print/<identifier-and-version>
```

The arXiv API responses were live as of the audit date. Because metadata and
versions can change, re-run the identifier checks immediately before sending
the packet or submitting a manuscript.
