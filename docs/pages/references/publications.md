# Publications

## Overview

This maintains a list of publications (journals, conferences, ...) where IESopt was applied as part of the modeling
approach. Entries are in alphabetical order. If you want to contribute a new publication or project, please follow the
instructions in the [section on contributing](#contributing) below.

## List of references

### Heat Highway (Marx, 2023)

:**title**: Heat Highway - Heat Transmission Network Design Optimization and Robustness Analysis for a Case Study in Tyrol - Methodology
:**publication**: [![CITATION](https://img.shields.io/badge/PURE-publications.ait.ac.at-blue?style=social)](https://publications.ait.ac.at/en/publications/heat-highway-heat-transmission-network-design-optimization-and-ro)
:**abstract**: The majority of district heating (DH) networks today are fueled by combustion processes based on fossil or biogenic fuels. For the decarbonization of DH networks various uncertainties regarding the future development of key factors, such as energy prices, need to be considered. Within the project “HeatHighway” a hypothetical inter-regional heat transfer network (HTN) in the region of the Inn valley in Tyrol, Austria was investigated.
:**keywords**: Future district heating, Waste heat sources, 4th generation DH, Heat transmission networks, Deterministic optimization, Monte Carlo simulation
:**citation**: Marx, N. O., Schmidt, R. R., Blakcori, R., Maggauer, K., Strömer, S., & Forster, T. (2023, September). Heat Highway - Heat Transmission Network Design Optimization and Robustness Analysis for a Case Study in Tyrol - Methodology. In _9th International Conference on Smart Energy Systems_ (pp. 103-104).

---

### HyTechonomy (Reuter, 2023)

:**title**: Optimizing the Domestic Production and Infrastructure for Green Hydrogen in Austria for 2030
:**publication**: [![CITATION](https://img.shields.io/badge/PURE-publications.ait.ac.at-blue?style=social)](https://publications.ait.ac.at/en/publications/optimizing-the-domestic-production-and-infrastructure-for-green-h)
:**project**: [HyTechonomy](#references-projects-hytechonomy)
:**abstract**: The decarbonisation of the Austrian energy system is expected to be facilitated by the uptake of hydrogen-based technologies, which requires the establishment of a hydrogen infrastructure to meet the rising demand. While large quantities of hydrogen are expected to be imported in the future, current developments in the energy market suggest that domestic production of hydrogen should not be ignored to ensure the security of supply. As domestic production ramps up, locating electrolysers to ensure optimal system integration is still an open question. To address this challenge, the "HyTechonomy" project developed an optimisation model that identifies the most promising domestic locations for green hydrogen production and optimal means of hydrogen transport for the year 2030.
:**keywords**: Hydrogen infrastructure, Energy system modelling, centralised electrolysis, decentralised electrolysis
:**citation**: Reuter, S., Strömer, S., Traninger, M., & Beck, A. (2023, September). Optimizing the Domestic Production and Infrastructure for Green Hydrogen in Austria for 2030. In _Book of Abstracts: 9th International Conference on Smart Energy Systems_ (pp. 278-279).

---

## Contributing

To contribute a new reference, either

- fork the [iesopt](https://github.com/ait-energy/iesopt) repository, and directly add to the above list, or
- open an issue with the reference details.

See the template below for the structure of a reference.

### Template

Please stick to APA format here, and always include a link as badge (if possible a DOI, if not other links are okay
too).

`````markdown
### Custom header

:**title**: put the full title here
:**publication**: [![CITATION](url-of-your-badge)](link-to-doi-or-pure-or-other)
:**project**: [Project (short) name](#references-projects-shortname)
:**abstract**: put the abstract here
:**keywords**: put all keywords here
:**citation**: put the APA styled citation here

---
`````

The `project` can be left out if not applicable. Otherwise it should refer to a proper project link target, that is set.

The "custom header" is used to prevent overly long titles from messing up the overall readability. The proposed format looks like this:

```markdown
### TheFundingProject (FirstAuthor, Year)
```

Where `TheFundingProject` is the project this publication was mainly funded by. If no project is related, then just doing `### (FirstAuthor, Year)` is the preferred fallback. `FirstAuthor` is only the last name of the first author; `Year` is the date of publication listed in the official citation.

### Creating citation badges

You can use [shields.io](https://shields.io/badges) to create badges, or use standardized ones that you already have
(e.g., from Zenodo), otherwise stick to the ones provided below.

**Pure:** _(publications.ait.ac.at)_

> ```markdown
> [![CITATION](https://img.shields.io/badge/PURE-publications.ait.ac.at-none?style=social)](ADDYOURLINKHERE)
> ```

**DOI:**

> ```markdown
> [![CITATION](https://img.shields.io/badge/DOI-10.XXXX%2Fname.YYYY.ZZZZZZ-none?style=social)](https://doi.org/10.XXXX/name.YYYY.ZZZZZZ)
> ```
