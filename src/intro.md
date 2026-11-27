<!-- status: verified · verified: 2026-11-27 by buerlino (PR #2) -->

<p align="center"><img src="images/logo.svg" alt="Earthmania logo: a globe with the letters EM" width="160"></p>


# Welcome to Earthmania

**Earthmania** is a knowledge base mainly focused on natural and industrial material flows and processes regarding the sources and sinks of planet Earth.

The idea came from two main influences: The chapter on World3[^c-loc-lccn-2004000125-2016--world3-chapter] in the book *The Limits to Growth: The 30-Year Update*[^c-loc-lccn-2004000125-2016--title-statement], and a university lecture on PET and PET-recycling in my bachelor's programme in energy and environmental engineering.

The Earthmania model is built from the bottom up. Every addition makes the model better, but it might only be useful after reaching a critical mass. Every number must be cited by source. A person checks every claim against the source before it reaches the model.

After everything is properly formatted and checked, the model is **compiled**. The compilation checks the mass balance on all stocks and flows within the ranges the sources provide. The documentation is coupled with the model and elaborates on the materials and processes described within the model.

Any modelled part that depends on a material or process that is currently not modelled can link to a parked page, ignoring the impact but marking the need to incorporate it in the future. That enables the model to grow slowly and organically. The model only represents the world on what has been modelled so far and thus cannot represent everything accurately.

Time will tell if this model will ever represent the real world in a meaningful way, but there is a chance it can. Earthmania is still under development, currently a first version is the target. First priority is the construction of the architecture. The PET example will be used as an early test to validate the architecture and iron out any missing details.

Check the FAQ page<!-- planned: faq.md --> for more details on the inner workings and structure of the Earthmania model. If you have any questions feel free to open an issue on GitHub: <https://github.com/buerlino/earthmania/issues>.

Artificial Intelligence will contribute massively to the creation of Earthmania: writing the code and model files, constructing the architecture and doing research. A person checks every claim against its source and the documentation is written by a human. AI models will then fact check the rigor and flag any remaining mistakes in the information against the source, and a human decides on the final outcome.

Good luck and strength to build a better future for Earth and all inhabitants. Thanks

Buerlino

## Sources

[^c-loc-lccn-2004000125-2016--title-statement]: Library of Congress (2016-10-27). *The limits to growth : the 30-year update* (Meadows, D., Randers, J., Meadows, D., Chelsea Green, 2004), catalogue record LCCN 2004000125.
    https://lccn.loc.gov/2004000125/marcxml — archived https://web.archive.org/web/20161230191052/https://lccn.loc.gov/2004000125/marcxml, accessed 2026-11-27.

[^c-loc-lccn-2004000125-2016--world3-chapter]: Library of Congress (2016-10-27). *The limits to growth : the 30-year update* (Meadows, D., Randers, J., Meadows, D., Chelsea Green, 2004), catalogue record LCCN 2004000125, contents note.
    https://lccn.loc.gov/2004000125/marcxml — archived https://web.archive.org/web/20161230191052/https://lccn.loc.gov/2004000125/marcxml, accessed 2026-11-27.

---

## License

Unless otherwise noted, the written content and media of Earthmania (`src/`) are
licensed under the [Creative Commons Attribution-ShareAlike 4.0 International
License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). The same
licence covers the source and claims ledger (`data/`), the models (`models/`) and
the project documentation.

You are free to share and adapt this material for any purpose, including commercially,
as long as you give appropriate credit, link to the license, indicate if changes were
made, and distribute your contributions under the same license.

Some things are not covered by CC BY-SA 4.0:

- **Code** (scripts, Rust code, workflows and configuration) is licensed under the
  MIT License.
- **Quotes in the ledger** belong to their original rights holders. They are there
  only so each claim can be checked against its source.
- **Third-party material** on a page keeps its own licence and is credited on that page.
- **The name "Earthmania" and the logo** are not openly licensed. You may use them
  unchanged to refer or link to Earthmania.

Full terms: [LICENSE](https://github.com/buerlino/earthmania/blob/main/LICENSE).

© Buerlino and Earthmania contributors.
