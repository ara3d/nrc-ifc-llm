# Annex F: Third-party material and licences

This annex lists the material in the proof of concept that others own, and the licence of each part. Sources: `samples/nrc/NOTICE.md` and the `LICENSE` files of the BIM Open Toolkit and its dependencies, in the development clone at commit 6f37755 (the coming tag `v0.2`), and `LICENSE` in this repository. The analytics values in the proof of concept are synthetic; the building they describe is not.

| Material | Owner | Licence | Where |
|---|---|---|---|
| Duplex Apartment test files (`Duplex_A_20110907.ifc`) | buildingSMART International (BSI, 2020) | Creative Commons Attribution 4.0 International (CC BY 4.0) | `data/duplex.ifc` in this repository; `samples/nrc/` in the toolkit |
| Enriched copy of the Duplex, with its DuckDB and BOS conversions | derived from the Duplex by Ara 3D | CC BY 4.0, as the Duplex | `poc/data/duplex-enriched.ifc`; `samples/nrc/` in the toolkit |
| BIM Open Toolkit | Ara 3D | MIT | `bim-open-toolkit/` (git submodule) |
| Toolkit dependencies: `ara3d-sdk`, `ara3d-dataflow`, `bim-open-data`, `bim-open-schema`, `bim-open-flow`, `bim-open-viewer`, `bim-open-notebook`, `bim-open-plot`, `gratify` | Ara 3D | MIT | `bim-open-toolkit/deps/`, filled by `node deps.mjs` |
| `parakeet` (a parser library, also in the toolkit's `deps/`) | Christopher Diggins | MIT | `bim-open-toolkit/deps/parakeet/` |
| Proof-of-concept code and documents in this repository | National Research Council of Canada (NRC) | MIT, proposed; see below | `LICENSE` |

Attribution required by CC BY 4.0, as the toolkit's notice states it: BSI (2020) Duplex Apartment Test Files, buildingSMART International, licensed CC BY 4.0, https://creativecommons.org/licenses/by/4.0/; enriched with property sets and converted to BIM Open Schema tables by Ara 3D. The source is https://github.com/buildingsmart-community/Community-Sample-Test-Files, folder "IFC 2.3.0.1 (IFC 2x3)/Duplex Apartment".

## IFC Test Kit models

The `IFC-Test-Kit/` folder of this repository holds buildingSMART test models. The proof of concept uses none of them today: its questions, graphs, and measurements all run over the Duplex.

## This repository's licence

`LICENSE` is a placeholder. The statement of work (section 5) requires the proof-of-concept code to be released under an open-source licence that the Open Source Initiative (OSI) approves and that the NRC selects. The NRC has not chosen, so `LICENSE` carries the MIT text, proposed, with the NRC as copyright holder, until the NRC's choice replaces it. The toolkit and its dependencies keep their own licences and are not covered by that file.
