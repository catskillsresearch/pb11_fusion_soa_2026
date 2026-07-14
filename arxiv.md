# State of the art on proton-boron fusion for electricity generation

## Abstract
Proton-boron-11 ($p\text{-}^{11}\text{B}$) fusion represents a highly compelling alternative to conventional deuterium-tritium (D-T) fuel cycles due to its aneutronic nature, which avoids neutron-induced material degradation and eliminates the need for complex tritium breeding blankets. However, the extreme physical parameters required for $p\text{-}^{11}\text{B}$ ignition—most notably an operating temperature of roughly 150 keV (~1.5 billion Kelvin) and severe relativistic Bremsstrahlung radiation losses—have historically relegated the concept to the margins of mainstream fusion research. Recent advancements in ultra-short pulse lasers, advanced magnetic confinement topologies (including spherical tori and multi-chamber centrifugal mirrors), non-thermal plasma physics, nuclear-data and spin-polarization programs, alpha-channeling / ash-control strategies, and direct energy conversion have revitalized the field. This review details the state of the art in $p\text{-}^{11}\text{B}$ fusion, analyzes the physics of the "Rider Limit" and both exotic and near-equilibrium proposals to circumvent or soften it, evaluates major commercial and national projects (including China’s dual HEDP + ST program and the Princeton/ARPA-E CHARM line now spinning out as Pale Blue Fusion), and summarizes emerging theoretical paradigms, alongside remaining materials science challenges.

---

## 1. Introduction
The $p\text{-}^{11}\text{B}$ reaction proceeds via the following nuclear channel:

$$p + \text{}^{11}\text{B} \rightarrow 3\alpha + 8.7 \text{ MeV}$$

Because the reaction products are entirely charged helium-4 nuclei ($\alpha$-particles), the energy released can theoretically be captured directly as electricity using electrostatic deceleration rather than a conventional, less efficient thermal steam cycle. Furthermore, because the reaction produces no high-energy neutrons, the structural components of a $p\text{-}^{11}\text{B}$ reactor are not subjected to the severe radiation damage, swelling, and activation that plague D-T concepts.

Despite these advantages, the $p\text{-}^{11}\text{B}$ cross-section requires operating energies an order of magnitude higher than those of D-T. At these extreme temperatures, the presence of boron ($Z=5$) dramatically increases Bremsstrahlung radiation losses, which scale with the square of the plasma’s effective charge ($Z_{eff}^2$).

### 1.1 Nuclear Data Uncertainties
The $^{11}\text{B}(p,\alpha)\alpha\alpha$ cross-section has been studied since the 1930s, yet evaluations still disagree at the level of tens of percent—historically up to $\sim 30\%$ uncertainty within a dataset and $\sim 50\%$ between experiments—because early measurements suffered limited solid-angle coverage, incomplete particle identification, and sparse energy coverage away from a few resonances [12,13,14]. Modern evaluations (e.g., Nevins & Swain; Sikora & Weller) underpin reactor studies [13,14], and China’s program has made the nuclear data itself a first-class R&D pillar [12].

Peking University has re-measured the reaction on a $2\times 1.7$ MV tandem over $0.675\text{--}3.0$ MeV proton energy using double-sided silicon strip detectors and high-statistics $3\alpha$ coincidence, separating the $\alpha_0$ (via $^{8}\text{Be}$ ground state) and $\alpha_1$ (via $^{8}\text{Be}^*$) channels [12]. The $\alpha_1$ channel dominates by roughly an order of magnitude yet remains the harder to model; Statistical Theory of Light Nucleus (STLN) analyses and Distorted-Wave Born Approximation (DWBA) direct-reaction studies still struggle to give a self-consistent description of primary versus secondary alphas and angular distributions [12]. Near the $\sim 160$ keV resonance, the $\alpha_0/\alpha_1$ branching ratio varies strongly with proton energy—directly shaping the emitted alpha spectrum for diagnostics and NBI heating design, and explaining the absence of a clear $\alpha_0$ peak in earlier Large Helical Device (LHD) magnetic-confinement experiments [12,15].

---

## 2. The Theoretical Bottleneck: The Rider Limit
In 1995, Todd Rider published a rigorous mathematical analysis detailing the fundamental thermodynamic limitations of aneutronic fusion systems [1]. The "Rider Limit" remains the primary benchmark against which all $p\text{-}^{11}\text{B}$ concepts are evaluated.

### 2.1 Thermal Equilibrium ($T_i = T_e$)
In a plasma in thermodynamic equilibrium, the fuel ions and electrons are in thermal equilibrium ($T_i = T_e = T$). The Bremsstrahlung power loss density is expressed as:

$$P_{Br} \propto Z_{eff}^2 n_e^2 \sqrt{T_e}$$

At the temperatures required to achieve a meaningful fusion reaction rate ($T_i \approx 100\text{--}300 \text{ keV}$), the thermal electrons also reach $100\text{--}300 \text{ keV}$. At these relativistic energies, the Bremsstrahlung losses scale even more unfavorably (up to $T_e^{1.5}$). Rider demonstrated that at any temperature under classical thermal equilibrium, the radiated power ($P_{Br}$) mathematically exceeds the fusion power produced ($P_f$). Thus, a thermalized, steady-state $p\text{-}^{11}\text{B}$ plasma cannot ignite.

### 2.2 Non-Equilibrium Topologies ($T_i \gg T_e$)
To bypass the equilibrium limit, physicists proposed keeping the fuel ions hot ($T_i \approx 300 \text{ keV}$) while maintaining cold electrons ($T_e \approx 20 \text{ keV}$) to suppress Bremsstrahlung. 

Rider mathematically dismantled this proposal by calculating the rate of energy transfer from hot ions to cold electrons via classical Coulomb collisions ($P_{i\to e}$). He proved that:

$$P_{i\to e} \gg P_f$$

Because the hot ions dump their heat into the cold electrons faster than they undergo fusion, a massive external recirculating power ($P_{recirc}$) must be continuously supplied to reheat the ions. To achieve a net power gain, this recirculating loop would require conversion and reinjection efficiencies approaching 100%, which is practically impossible under real-world engineering constraints.

### 2.3 Softening the Constraint: A Near-Equilibrium “Net Gain Window”
Not every modern program treats Rider’s bound as an absolute veto on steady magnetic confinement. Liu et al. (2025) revisited the constraint with 0D Fokker–Planck modeling, updated (roughly doubled) fusion cross-section data, and actively maintained non-thermal proton distributions [16]. They identify a critical **net energy gain window** near $T_e \approx 140$ keV with a tightly constrained ion-to-electron temperature ratio $T_i/T_e$ between roughly $1.8$ and $2.5$, arguing that this regime can reduce the required energy confinement time by about an order of magnitude relative to a purely Maxwellian baseline—still demanding, but more optimistic for a spherical-torus or tokamak-like reactor than classical Rider analysis allows [12,16]. Parallel Chinese theory work quantifies how far non-Maxwellian shaping can go: Monte Carlo and analytic tools for arbitrary and drift bi-Maxwellian distributions show that, at fixed total ion kinetic energy in the $100\text{--}500$ keV band, reactivity can rise substantially relative to Maxwellian–Maxwellian reactants, with theoretical upper bounds typically in the $50\%\text{--}300\%$ range for highly beam-like distributions [17,18,19].

Even so, aggressive hot-ion assumptions remain contested. ENN’s ST roadmap invokes hot-ion operation as a pillar of its path to $p\text{-}^{11}\text{B}$ [22]. In a published Comment, Zhi Li argues that a target ratio $T_i/T_e = 4$ is far from accessible under the most optimistic fusion-heated balance (ions heated by all fusion power; electrons heated only by ion–electron coupling), which yields $T_i/T_e \lesssim 1.5$ at $T_i = 150$ keV; forcing $T_i/T_e = 4$ with an idealized ion-only external heater would require heating power of order $\sim 20$ times the fusion power—economically unattractive even if physically arranged [38]. ENN’s Response accepts the Comment’s arithmetic as consistent with prior ENN/Xie power-balance formulas, but rejects the implication that the roadmap is thereby void: hot-ion mode is flagged as an open challenge among several, to be addressed by NBI+ICRF, alpha channeling, nonlinear reactivity enhancement, and related advances still under development [39]. The exchange underscores that “softened” $T_i/T_e$ windows (closer to the $1.8\text{--}2.5$ band of [16] than to $T_i/T_e = 4$) are more plausible near-term targets than extreme hot-ion operation.

---

## 3. Circumventing the Rider Limit: Physical Loopholes
Modern $p\text{-}^{11}\text{B}$ projects are designed specifically to bypass Rider’s assumptions by operating in regimes where classical, Maxwellian thermodynamics do not apply—or, as in §2.3, to operate just far enough from equilibrium that recirculating power remains tolerable.

```
                  ┌─────────────────────────────────────────┐
                  │           THE RIDER LIMIT               │
                  │   Bremsstrahlung > Fusion Power         │
                  └────────────────────┬────────────────────┘
                                       │
                ┌──────────────────────┴──────────────────────┐
                ▼                                             ▼
   [ Near- / Off-Equilibrium ]                     [ Non-Thermal/Kinetic ]
   Softened Lawson / Ti/Te window                  Exploiting Loopholes:
   Non-Maxwellian tails & drifts                   1. Beam-target kinetics
   Spin polarization                               2. Quantum Degeneracy
   Alpha channeling & ash removal                  3. Optically Thick Core
                                                   4. Quantum Magnetic Suppression
```

### 3.1 Non-Maxwellian and Beam-Target Kinetics
Rider assumed both ions and electrons exhibit isotropic, thermalized Maxwell-Boltzmann velocity distributions. If the fuel is instead organized into highly directed, non-thermal beams (e.g., via laser-driven block acceleration), the fusion reactions occur on picosecond timescales [2]. Because this timescale is shorter than the ion-electron collision relaxation time, the reactions occur before the system can thermalize, suppressing Bremsstrahlung generation.

In magnetized toroidal plasmas, a related but distinct idea is to maintain a **velocity differential (drift)** between protons and boron ions. Peng et al. argue that a relative drift comparable to the sound speed (Mach $1\text{--}2$ at $\sim 100$ keV) can raise $\langle\sigma v\rangle$ from $\sim 1\times 10^{-22}$ to $\sim 6\times 10^{-22}\,\mathrm{m}^3/\mathrm{s}$, lowering the required triple product $n_i\tau_E T_i$ to $\sim 10^{23}\,\mathrm{m^{-3}\,s\,keV}$—only about an order of magnitude above ITER’s D-T target [20]. Sustaining such distributions is not free: ENN–Shanghai Jiao Tong University kinetic simulations (LAPINS/EPOCH) of a $100$ keV hydrogen beam injected into magnetized H–B plasma show excitation of ion Bernstein waves (IBWs) that preferentially transfer NBI energy into a non-Maxwellian hydrogen tail, boosting fusion yield under high-field, high-density, low-temperature conditions [12].

### 3.2 Quantum Degeneracy
At extreme solid-state densities, the electron population can become quantum degenerate. Under Fermi-Dirac statistics, the lowest energy states are completely occupied. Because of the Pauli Exclusion Principle, hot ions cannot transfer their kinetic energy to the cold electrons because the electrons have no vacant higher-energy quantum states to occupy. This drastically reduces the $P_{i\to e}$ relaxation rate while leaving the nuclear fusion rate unaffected. Complementary laser–plasma theory identifies a **preformed boron plasma** as a practical lever: electron degeneracy can cut proton energy loss (order $\sim 40\%$ yield gain), while reduced resistivity suppresses collective electromagnetic stopping and enables deeper proton penetration (further $1\text{--}2$ orders of magnitude in predicted alpha yield) [21].

### 3.3 Optically Thick Plasmas and Radiation Trapping
Rider assumed that the plasma is optically thin, meaning all Bremsstrahlung X-rays immediately escape the reactor. Recent theoretical models, including studies from the Princeton Plasma Physics Laboratory (PPPL), indicate that if a plasma is compressed to stellar-core densities (e.g., $>100 \text{ g/cm}^3$), it becomes optically thick. Under these conditions, the Bremsstrahlung photons are reabsorbed within the plasma core, keeping it hot and preventing the radiative collapse of the fusion burn [3].

### 3.4 Quantum Magnetic Suppression
At magnetic field strengths exceeding $10^6 \text{ Tesla}$, the cyclotron motion of the electrons becomes quantized. This quantization restricts the free transitions of electrons, which can theoretically suppress Bremsstrahlung emission by several folds [4].

### 3.5 Spin Polarization and Laser-Field Cross-Section Enhancement
Two nuclear-physics routes aim to raise the *effective* fusion cross-section rather than only reshaping the velocity distribution. **Spin-polarized** $p\text{-}^{11}\text{B}$ fuel—under consideration at ENN—is predicted from angular-momentum conservation to enhance the reaction cross-section by up to $\sim 60\%$ for fully parallel polarization, with even partial polarization yielding $\sim 20\%$ [12]. The outstanding engineering problem is depolarization in magnetic confinement from field fluctuations and wall collisions. Separately, intense laser fields have been theorized (China Academy of Engineering Physics) to enhance the $p\text{-}^{11}\text{B}$ cross-section; semiclassical and Kramers–Henneberger treatments predict an increase, but the required laser parameters exceed present facilities [12].

### 3.6 Alpha Channeling, Helium Ash, and Redirected Power Flow
Even if Bremsstrahlung and $T_i/T_e$ can be managed, fusion-born $^4\mathrm{He}$ (ash) is an existential threat unique in severity for $p\text{-}^{11}\text{B}$. Three alphas per reaction raise both plasma pressure and $Z_{eff}$; if they linger for a time comparable to the energy confinement time, 0D power-balance models find that engineering breakeven can become unreachable even with perfect energy confinement [29]. Prompt alpha removal is therefore not an optimization—it is a design requirement.

Princeton/PPPL work under ARPA-E OPEN 2021 (award DE-AR0001554) attacks this by **redirecting** the natural collisional power flow [29,30,31]. **Alpha channeling**—waves that tap free energy in the alpha distribution—can put more power into protons and less into electrons. In a simple power-balance model, channeling into thermal protons can cut the confinement time required for ignition by a factor of $\sim 2.6$; channeling into a fast proton population near the reactivity peak can cut it by a factor of $\sim 6.9$ [30]. Extending the analysis from ignition to plant breakeven, modern thermal-conversion efficiencies alone already ease the Lawson product relative to classical ignition thinking, and combining fast-proton heating, alpha power capture, direct conversion, and efficient heating can reduce the required product by roughly another order of magnitude—potentially into a band comparable to ITER-class $n\tau$ targets [31]. Wave-supported hybrid beam–thermal schemes and related kinetic tools formalize how to hold such nonthermal proton populations against collisional drag [32]. These results motivate the multi-chamber CHARM architecture of §5.6: separate the fusion region from an alpha storage / heat-exchange region so ash can be strained out without abandoning energy recovery [29,33].

---

## 4. Confinement Paradigms: Pulsed vs. Continuous
Due to the immense difficulty of sustaining a continuous $150 \text{ keV}$ plasma without catastrophic energy loss, **pulsed approaches currently dominate** much of the Western commercial $p\text{-}^{11}\text{B}$ landscape. Electrostatic confinement systems (such as traditional fusors) have been largely abandoned for utility-scale power generation due to severe conduction losses. 

The broader field is split between pulsed, non-thermal laser-driven inertial / high-energy-density platforms and magnetic confinement—especially compact **spherical tori** in China [12] and **centrifugal / multi-chamber open-field** concepts in the U.S. Princeton/ARPA-E line [33]. Highly dynamic pulsed magnetic configurations (FRCs, dense plasma foci) occupy an intermediate niche.

---

## 5. Major Reactor Topologies and Commercial Projects
Several key players are actively developing $p\text{-}^{11}\text{B}$ systems geared toward $Q > 1$ commercial electricity generation:

### 5.1 TAE Technologies (Magnetic Confinement - FRC)
TAE Technologies utilizes a beam-driven **Field-Reversed Configuration (FRC)**, a magnetic confinement scheme where a spinning toroidal plasma ring is sustained by its own self-generated magnetic fields within a linear cylindrical chamber.

*   **Rider Bypass Argument:** TAE argues that modern nuclear cross-section measurements are roughly 20% higher than the data used by Rider in 1995. Furthermore, they inject high-energy neutral beams (NBI) tangentially into the FRC to create a non-Maxwellian, high-energy proton "tail" [5]. This fast-ion population significantly increases the average fusion rate without requiring a corresponding increase in the bulk electron temperature.
*   **Experimental Milestones:** In collaboration with NIFS, TAE demonstrated $p\text{-}^{11}\text{B}$ fusion alphas in the Large Helical Device (LHD)—the first such measurement in a magnetically confined plasma—by injecting energetic hydrogen beams into a boron-seeded plasma [5,15]. Contemporary *Science* coverage framed the result as a proof-of-principle for aneutronic utility-scale ambitions while noting the modest absolute power ($\sim$ watts-scale beam-target hot spots, not a sustained bulk burn) and the still-enormous temperature gap to reactor $p\text{-}^{11}\text{B}$ [35]. On TAE’s own machines, the long-standing Norman (C-2W) campaign used theta-pinch formed, beam-sustained FRCs. In 2025, Roche et al. reported the first successful **NBI-only** FRC formation and sustainment on a shortened **Norm** configuration—eliminating the theta-pinch formation sections and cutting machine length/complexity substantially [36]. Company roadmap updates subsequently argued that Norm’s performance allows skipping the previously planned **Copernicus** intermediate device and moving toward the **Da Vinci** prototype power plant [36,37].
*   **Cooling Strategy:** The reactor employs "dry cooling" via localized closed-loop helium gas or water channels embedded within the vacuum vessel walls to capture surface heat. It lacks a massive thermodynamic steam loop.
*   **X-Ray Strategy:** FRCs operate at a high plasma-beta, excluding magnetic fields from the hot core and minimizing synchrotron radiation. The inner vacuum vessel wall is shielded with high-$Z$ tungsten tiles to safely absorb the Bremsstrahlung flux.
*   **Electricity Conversion:** An **Inverse Cyclotron Converter (ICC)** is positioned at the axial ends of the FRC. As alpha particles escape along open magnetic field lines, a tapering magnetic field converts their linear velocity into a helical orbit. Segmented electrodes capture the moving charges, directly inducing high-frequency alternating current (AC) at their cyclotron frequency (~5 MHz), bypassing thermal conversion loops entirely.
*   **The "Unobtainium" Materials Challenges:** 
    *   *ICC Electrode Longevity:* Finding an electrode material that can survive continuous, direct exposure to high-energy alpha particle bombardment without experiencing severe blistering, sputtering, and degradation.
    *   *NBI Grid Erosion:* The grids of the high-power neutral beam injectors must operate continuously at extreme currents and voltages without degrading; any grid erosion introduces heavy metal impurities into the FRC, which increases $Z_{eff}$ and triggers radiative plasma collapse.

### 5.2 HB11 Energy (Inertial Confinement - Laser Block Ignition)
HB11 Energy is pursuing a non-thermal, laser-driven "Proton Fast Ignition" scheme.

*   **Rider Bypass Argument:** HB11 argues that the entire fusion process occurs on a picosecond timescale using CPA (Chirped Pulse Amplification) lasers. The laser’s ponderomotive force accelerates blocks of plasma as directed, non-thermal beams [2]. Because this occurs faster than the ion-electron collision relaxation rate, the bulk electrons do not heat up, preventing the generation of thermal Bremsstrahlung.
*   **Cooling Strategy:** The spherical reaction chamber uses a double-walled, gas-cooled (helium) jacket designed to dissipate the average thermal load from a pulsed operation rate of 10 to 20 Hz.
*   **X-Ray Strategy:** Since the reaction is non-thermal, Bremsstrahlung is minimized. The transient X-ray flash that does escape is absorbed by a carbon-composite or tungsten-carbide first-wall armor designed to withstand rapid cyclic thermal shock waves without spallation.
*   **Electricity Conversion:** The target positioner sits inside a high-voltage, spherical electrostatic collector grid charged to several megavolts. The escaping positive alpha particles (carrying $\sim 2.9$ MeV each) fly outward against the opposing megavolt potential, converting kinetic energy directly to electricity.
*   **The "Unobtainium" Materials Challenges:**
    *   *Vacuum Grid Integrity:* Maintaining megavolt electrostatic insulation in a chamber filled with ionizing X-rays, vaporized target debris, and stray electrons without triggering catastrophic electrical arcing.
    *   *High-Repetition Optical Protection:* Developing final focusing mirrors that can survive millions of laser shots and target debris impacts without losing optical alignment or surface reflectivity.

### 5.3 LPPFusion (Magnetized Pinch - Dense Plasma Focus)
LPPFusion utilizes a coaxial electromagnetic accelerator to pinch plasma into an ultra-dense, self-confining plasmoid.

*   **Rider Bypass Argument:** LPPFusion relies on the **Quantum Magnetic Field Effect**. At the peak of the pinch, self-generated magnetic fields reach megatesla levels, which quantum-mechanically restricts the energy states of the electrons and suppresses Bremsstrahlung emission by up to a factor of five [4].
*   **Cooling Strategy:** To operate at a targeted repetition rate of 200 Hz, the central hollow anode rod is cooled internally using a pumped, closed-loop liquid metal coolant (such as liquid gallium) to rapidly dissipate the extreme heat of the megampere discharges.
*   **X-Ray Strategy:** The suppressed X-ray flux is absorbed by a first-wall lining of beryllium-coated copper or tungsten.
*   **Electricity Conversion:** LPPFusion uses a dual direct-energy conversion scheme. The expanding plasmoid shoots out an axial ion beam that passes through induction coils, directly recharging the capacitor banks. Simultaneously, the escaping X-rays strike nested photoelectric plates, knocking off electrons to generate high-voltage DC electricity.
*   **The "Unobtainium" Materials Challenges:**
    *   *Electrode Erosion:* The coaxial electrodes must withstand megampere currents and megatesla magnetic forces 200 times per second. No known material can survive these extreme physical forces and plasma sputtering without eroding rapidly, which ruins the symmetry of the pinch and poisons the vacuum.
    *   *High-Repetition, Megampere Switches:* The system requires solid-state switches capable of discharging megamperes of current at 200 Hz with fast rise times over billions of cycles without failing.

### 5.4 ENN Energy (Spherical Torus - Magnetic Confinement)
China’s ENN-led program is the most developed **spherical torus (ST) + $p\text{-}^{11}\text{B}$** commercialization path, summarized in the 2025 FEC overview by Liu et al. [12]. It pairs fundamental beam-target / nuclear-data work with a staged ST roadmap (EXL-50U → EHL-2 → DEMO-class).

*   **ST + $p\text{-}^{11}\text{B}$ Synergy:** High plasma-$\beta$ at relatively low toroidal field is advantageous at the extreme temperatures $p\text{-}^{11}\text{B}$ needs, because cyclotron radiation grows with $B$; the ST’s high-$\beta$, low-$B$ operating point mitigates that loss channel. Conversely, aneutronic fuel removes the tritium breeding blanket that would otherwise crowd the ST’s already constrained central column, freeing that space for magnets alone [12,22]. Related theory argues that a magnetic well in a high-$\beta$ tokamak can squeeze trapped orbits, suppress turbulence, and yield a favorable ion confinement scaling $\tau_E \propto T_i^2$, further helping compact aneutronic ignition [23].
*   **Rider Bypass Argument:** Rather than relying solely on picosecond inertial kinetics, ENN emphasizes *actively maintained* non-Maxwellian ion distributions, the $T_i/T_e$ net-gain window of §2.3 [16], proton–boron drifts that ease Lawson [20], IBW-mediated NBI tail formation (§3.1), and optional spin polarization (§3.5) [12]. System-code studies target a high-gain ($Q>10$) ST reactor at $\sim 6$ T in hot-ion mode, with a demonstration horizon near $\sim 2035$ [22]. The published Comment/Response exchange on that roadmap ([38,39]; §2.3) makes clear that extreme hot-ion ratios ($T_i/T_e = 4$) are not assumed to fall out of fusion self-heating alone and remain a systematic R&D risk to be closed by advanced heating and kinetic schemes.
*   **Device Status:** EXL-50U has demonstrated multi-hundred-kA to megaampere-class hydrogen–boron plasmas; combined ICRF + NBI driven $p\text{-}^{11}\text{B}$ reaction experiments are underway [12,24]. EHL-2 physics design and simulations predict that thermal reactions dominate for $T_i \gtrsim 26$ keV; under reference parameters ($200$ keV H-beam at $1$ MW) they find $\sim 0.95$ kW of alpha power with $\sim 98\%$ alpha retention and an optimal boron concentration near $\sim 14\%$ [6,25,26]. A magnetic-confinement $p\text{-}^{11}\text{B}$ reaction was also demonstrated on LHD (Japan) [15], complementing TAE’s FRC result [5].
*   **Hybrid Laser Proton Source:** For magnetic devices, laser ion acceleration is being retargeted away from multi-MeV monoenergetic beams toward large numbers of moderate-energy protons ($300\text{--}1000$ keV)—roughly $10^{13}$ for EXL-50U and $10^{17}$ for EHL-2 in preliminary estimates—via ultrashort lasers irradiating pellets after injection into the plasma (avoiding magnetic shielding of an external source) [12].
*   **The "Unobtainium" Materials / Physics Challenges:**
    *   *Sustaining Non-Maxwellian Fuel:* Continuous recirculating power and RF/NBI systems must hold the $T_i/T_e$ window and desired distribution against collisional relaxation without poisoning $Z_{eff}$.
    *   *Central-Column and Divertor Heat Fluxes:* Compact ST geometry concentrates heat and Bremsstrahlung loads; low-sputter first-wall solutions remain essential (§8).

### 5.5 Chinese High-Energy-Density Beam-Target and Nanostructured Targets
Parallel to the ST path, Chinese HEDP groups have reported large reactivity enhancements in laser- and accelerator-driven beam-target geometries [12].

*   **XG-III Intense Beam-Driven Foam Targets (Xi’an Jiaotong University):** A picosecond laser generates a TNSA proton beam that strikes a preheated, homogeneous boron-doped TAC foam plasma, yielding up to $10^{10}$ alphas per steradian per shot—among the highest laser-normalized yields reported—and exceeding classical beam-target expectations by about four orders of magnitude, with $\sim 12\%$ proton-to-$\alpha$ energy conversion and a maximum fusion probability $\sim 2.3\times 10^{-2}$ [12,27]. Enhancement is attributed to strong electric fields, non-equilibrium kinetics, and the foam plasma structure; theory emphasizes the preformed boron plasma / degeneracy mechanism of §3.2 [21].
*   **Hydrogen-Doped Solid Targets (ENN–IMP):** On IMP’s $320$ kV platform, solid H-doped boron targets ($\sim 25$ at.% H) produced an average $\sim 30\%$ higher alpha yield than pure boron over $110\text{--}240$ keV center-of-mass energy, showing that fuel-composition engineering matters even in the low-energy beam-target regime; the microscopic origin is still under study [12,28].
*   **Nanowire Arrays and Nano-HEDM:** Femtosecond irradiation of nanowire arrays can drive Z-pinch-like compression (extreme current density and $\sim 10^6$ T-scale fields in simulation), with experiments on deuterium-doped wires confirming fusion products and alpha yields up to $\sim 1.5\times 10^7$ per shot for $p\text{-}^{11}\text{B}$-relevant setups [12]. Separately, Nano-HEDM structured targets irradiated by femtosecond petawatt lasers drive Coulomb explosions that accelerate protons to $\sim 150$ MeV and convert $\sim 10\%$ of laser energy into fast ions at near-solid density—but picosecond confinement still falls short of Lawson, so viability hinges on better confinement, not peak energy alone [12].

These HEDP results sit alongside commercial laser programs (HB11, Marvel Fusion) as experimental evidence that target microstructure and pre-plasma state can move yields far from classical beam-target scaling.

### 5.6 Pale Blue Fusion / Princeton–ARPA-E (CHARM Centrifugal Multi-Chamber)
The most developed U.S. *theory-to-architecture* line for steady or quasi-steady $p\text{-}^{11}\text{B}$ is the Princeton group led by Nat Fisch, funded by ARPA-E OPEN 2021 as “Economical Proton-Boron11 Fusion” (DE-AR0001554) [33,34]. After a dense publication and patent campaign, the team has pivoted toward commercialization as **Pale Blue Fusion**—a name that doubles as branding for a clean “pale blue” Earth and as a wink at **P**roton–**B**oron [33].

*   **Architecture (CHARM):** **CHambered Aneutronic Rotating Mirror.** Rather than one Maxwellian “soup,” CHARM uses differential confinement of species with very different mass and charge-to-mass ratios. Boron is centrifugally trapped in a fusion chamber; energetic protons and helium enter a heat-exchange chamber where waves extract alphas promptly while capturing their energy; the design goal is helium *strained from* the fusion region without abandoning alpha power [29,33]. Selective ponderomotive barriers, multi-ion centrifugal end plugs, and related open-field tricks regulate ion traffic between chambers [33].
*   **Rider Bypass Argument:** Classical thermal $p\text{-}^{11}\text{B}$ fails because radiation and recirculating power dominate (§2). CHARM’s answer is structural: keep the plasma far from equilibrium, put energy preferentially into protons (alpha channeling / hybrid fast–thermal protons; §3.6), keep boron from needing to be as hot as the protons, manage synchrotron losses via reabsorption, and treat helium ash as a first-class design constraint rather than an afterthought [3,29,30,31,32].
*   **Status:** The ARPA-E phase produced on the order of thirty peer-reviewed papers, specialized codes (0D power balance with self-consistent helium poisoning; structure-preserving PIC; radiative Fokker–Planck), and multiple 2025 U.S. patent applications on separated reactant regions, ponderomotive potentials, and differential confinement [33]. As of the July 2025 ARPA-E Fusion Annual Meeting, Princeton approvals for a startup handoff were in place; the scientific program is transitioning from academic derisking to in-silico power-positive reactor design and targeted experiments [33].
*   **The "Unobtainium" / Open Physics Challenges:**
    *   *Integrated Self-Consistency:* Component studies suggest feasibility of centrifugal multi-cell operation, alpha handling, and synchrotron management; demonstrating that they work *together* in one device remains the next hurdle [33].
    *   *Rotation, Walls, and Voltage Drops:* Sustaining plasma rotation and large electrostatic potentials with tolerable wall dissipation, and validating ponderomotive / centrifugal barriers experimentally, are still outstanding.
    *   *Path to Hardware:* Unlike TAE, ENN, or laser houses, CHARM’s public record is still predominantly theory, simulation, and IP—the experimental campaign is the commercialization risk.

---

## 6. Emerging Theoretical Paradigms: Muon-Assisted Kinetic Fusion
While commercial startups focus heavily on non-thermal laser-target interactions or advanced magnetic confinement to reach the requisite $>100\text{ keV}$ operating window, a novel alternative has emerged from low-energy nuclear reaction (LENR) theory. Recent work by Wang et al. (2026) proposes circumventing the high Coulomb barrier entirely by utilizing muon-catalyzed fusion ($\mu\text{CF}$) in a non-equilibrium, kinetic framework [11].

```
[ Muon (μ⁻) + Proton (p) ] ──► [ Neutral Muonic Hydrogen (pμ) ]
                                             │
                                             ▼  (Bombarded with ¹¹B)
                                  [ Enhanced Tunneling ] 
                                  (Screened Coulomb Barrier)
                                             │
                                             ▼
                                  [ Sub-100 keV Fusion ]
```

### 6.1 Bypassing the "Muon Trap"
Traditional muon-catalyzed fusion relies on thermal equilibrium to form muonic molecules (such as $d\mu t$ in D-T fusion), where the heavy negative muon ($\mu^-$, $m_\mu \approx 207 m_e$) screens the nuclear charges and pulls the nuclei close enough to fuse. 

However, applying this traditional thermal scheme to $p\text{-}^{11}\text{B}$ has historically been considered impossible. Because boron has a high nuclear charge ($Z = 5$), it acts as a severe **"muon trap."** In a thermal mixture, the muon is rapidly and tightly bound to the boron nucleus, reducing its orbital radius to the point where it can no longer screen a second incoming nucleus, effectively halting the catalytic cycle.

To bypass this trap, the proposed kinetic scenario pre-empts thermal equilibrium:
1. A muon and a proton are first brought together to form a neutral **muonic hydrogen atom ($p\mu$)**.
2. This stationary $p\mu$ target is then bombarded with an accelerated beam of $^{11}\text{B}$ nuclei (or vice versa). 
3. The fusion reaction occurs dynamically during the collision before the muon has the opportunity to transfer to the boron nucleus and become trapped.

### 6.2 The Physics of Dynamic Charge Screening
In this kinetic collision, the muon is assumed to remain in its tightly bound $1s$ ground-state wavefunction around the proton:

$$\psi(r) = \frac{1}{\sqrt{\pi a_\mu^3}} e^{-r/a_\mu}$$

where the muonic Bohr radius $a_\mu \approx 284.6\text{ fm}$ is approximately 207 times smaller than the electronic Bohr radius. As the $^{11}\text{B}$ nucleus approaches the neutral $p\mu$ atom, it experiences a dynamically screened proton charge. The total effective charge $q_{\text{eff}}$ felt by the incoming boron nucleus at a separation distance $r_{pB}$ is derived as:

$$q_{\text{eff}} = -q_\mu \left( 1 + \frac{2r_{pB}}{a_\mu} + \frac{2r_{pB}^2}{a_\mu^2} \right) \exp\left( -\frac{2r_{pB}}{a_\mu} \right)$$

This charge screening substantially alters the classical Coulomb potential energy of the system at intermediate separations:

$$V^{\text{eff}}_{p\mu\text{-}B}(r_{pB}) = \frac{1}{4\pi\epsilon_0} \frac{q_B q_{\text{eff}}(r_{pB})}{r_{pB}}$$

As a result, the classical minimum approach distance ($r_{\text{min}}$) is significantly reduced for incident energies below several tens of keV. 

### 6.3 Tunneling and Cross-Section Enhancement
Wang et al. evaluated the penetrability $P(E)$ of the screened potential barrier using a hybrid semiclassical model. At low incident energies where the action $S \ge 10$ ($E \le 33.50\text{ keV}$), the standard WKB approximation is highly reliable. For the intermediate energy region ($33.50\text{ keV} < E < 107.43\text{ keV}$), they utilized a linearized Airy function matching procedure to maintain continuity at the classical turning point.

The model yields several critical insights:
*   **Sub-100 keV Enhancement:** At incident energies below $100\text{ keV}$, the tunneling probability is enhanced by **several orders of magnitude** compared to the bare-nuclei case.
*   **The Upper Energy Boundary:** At $E = 107.43\text{ keV}$, the Airy tunneling probability curve intersects with the bare-nuclei penetrability curve. Beyond this point, the incident kinetic energy is high enough to penetrate the region where muon screening is negligible, meaning the muon provides no further catalytic benefit.
*   **Cross-Section and Rate Boost:** The corresponding astrophysical $S$-factor calculations indicate a substantial increase in both the reaction cross-section ($\sigma$) and the thermonuclear reaction rate ($\langle\sigma v\rangle$) below $10\text{ keV}$. 

### 6.4 Practical Hurdles
While mathematically elegant, this kinetic scheme remains highly speculative and untested. From a practical engineering standpoint, it faces the same severe bottleneck that has limited all muon-catalyzed fusion concepts: the **energy cost of muon production**. 

Because muons have a short lifetime ($\tau_\mu \approx 2.2\ \mu\text{s}$), the energy required to generate the muon beams must be offset by an exceptionally high fusion yield per muon. Whether this dynamic, non-equilibrium $p\mu\text{-}^{11}\text{B}$ system can achieve a high enough catalytic cycling rate before the muon decays—or before it is lost to a boron nucleus—remains a major open question for future experimental verification.

### 6.5 Applicability to Existing Reactor Architectures
The kinetic $p\mu\text{-}^{11}\text{B}$ scheme of §6 is not a drop-in upgrade for every confinement approach in §5 and Table 1. It requires a **directed, non-thermal collision** in which neutral muonic hydrogen is formed *before* the muon can contact boron, followed by a beam-target encounter at incident energies preferably below $\sim 100\text{ keV}$ (where screening still enhances tunneling; §6.3). Architectures that already organize fuel as beams or laser-driven blocks can, in principle, host this sequence; architectures that rely on thermal mixing of protons and boron generally cannot without a dedicated kinetic stage.

**Shared requirements (all applicable architectures).** For every scheme below, the engineering add-ons are the same in substance:
1. **Muon source and $p\mu$ formation** — a pulsed muon beam (or in-situ production) timed so that $\mu^-$ bind preferentially to protons, yielding a neutral $p\mu$ population that has not yet mixed with boron.
2. **Controlled beam-target kinematics** — relative collision energies held in the sub-$100\text{ keV}$ window where muon screening matters, with encounter timescales short compared with muon transfer to $^{11}\text{B}$ (the “muon trap” of §6.1).
3. **Yield versus muon cost** — fusion yield per muon large enough to repay production energy within $\tau_\mu \approx 2.2\ \mu\text{s}$, independent of the host confinement technology.

**Where this maps cleanly.** The laser-driven and other inertial beam-target programs already operate in the non-Maxwellian, short-timescale regime that §6 exploits. That includes **HB11 Energy** (laser block ignition) [2], **Marvel Fusion** (nanostructured ICF) [8], **Blue Laser Fusion** and **Anubal Fusion** (high-repetition / laser-target ICF), and the **FUSION Project** (laser-plasma targets) [10]. In each case the same accomplishment path applies: prepare a $p\mu$-bearing target (or inject $p\mu$ into the interaction volume), then deliver a directed $^{11}\text{B}$ block or beam—via CPA laser acceleration or equivalent—at the screened sub-$100\text{ keV}$ energy, rather than the higher thermal or multi-MeV drive energies those platforms often emphasize today. The PROBONO consortium [9], which coordinates multi-platform laser and plasma experiments, is a natural venue for cross-facility tests of that sequence.

**Partial fit.** **TAE Technologies** already injects directed high-energy beams into an FRC and argues for a non-Maxwellian proton tail [5]. The §6 improvement would use that beam infrastructure to stage $p\mu$ formation and then a moderated $^{11}\text{B}$ (or $p\mu$) beam in the catalytic energy window—not to raise bulk ion temperature further. The magnetic topology itself is secondary; what matters is preserving beam-target kinetics and avoiding thermal $p$–$^{11}\text{B}$–$\mu$ mixing inside the FRC core.

**Poor fit without redesign.** Steady or quasi-steady thermal magnetic devices that mix protons and boron in the same volume—exemplified by a purely thermalized reading of **ENN**’s spherical-torus hydrogen-boron program [6,12]—reproduce the classical muon trap: the muon binds to $Z=5$ boron before a second nucleus can be screened. (ENN’s own non-Maxwellian / drift / IBW program [12,16,20] is a Rider-softening strategy, not a host for kinetic $p\mu$ catalysis unless a dedicated beam-target stage is added.) **LPPFusion**’s dense plasma focus [4] likewise thermalizes fuel in a megatesla pinch where free $p\mu$ would not survive long enough for a controlled kinetic collision; its axial ion beam could only host §6 physics if a separate, low-energy $p\mu$–$^{11}\text{B}$ beam-target stage were added upstream of the pinch. **CHARM / Pale Blue Fusion** [29,33] already separates species and uses wave-driven alpha removal, but it is optimized for ash handling and proton energization—not for forming neutral $p\mu$ and colliding it with $^{11}\text{B}$ before muon transfer; grafting §6 onto CHARM would still require a dedicated kinetic $p\mu$ injector stage.

In short: §6 is a candidate enhancement for **beam-target and laser-block architectures** (and for TAE-style NBI if retuned to the catalytic energy band). It is not a substitute for Rider-bypass strategies that depend on optical thickness, quantum magnetic suppression, CHARM-style differential confinement, or thermal magnetic confinement of a mixed $p\text{-}^{11}\text{B}$ plasma.

---

## 7. Active Global Initiatives
A summary of active public, private, and academic groups conducting $p\text{-}^{11}\text{B}$ research as of 2026 is detailed in Table 1.

### Table 1: Key $p\text{-}^{11}\text{B}$ Projects and Collaborations (State of the Art, 2026)

| Project / Entity | Country | Core Confinement Technology | Major Milestones & Focus Areas (2025–2026) |
| :--- | :--- | :--- | :--- |
| **ENN Energy Research Institute** [6,12,22,38,39] | China | Spherical Torus (Magnetic) | Dual HEDP + ST strategy; EXL-50U H–B plasmas and ICRF+NBI $p\text{-}^{11}\text{B}$ campaigns; EHL-2 design ($Q>10$ roadmap $\sim 2035$); hot-ion $T_i/T_e$ assumptions debated in Comment/Response [38,39]; nuclear-data, spin-polarization, and non-Maxwellian theory program [12]. |
| **TAE Technologies** [5,35,36] | USA | Field-Reversed Configuration | LHD $p\text{-}^{11}\text{B}$ alpha demonstration [5,35]; 2025 Norm NBI-only FRC formation [36]; roadmap shortened toward Da Vinci power-plant prototype (Copernicus intermediate reportedly skipped) [37]. |
| **LHD / NIFS** [15] | Japan | Helical (Magnetic) | Demonstrated aneutronic $p\text{-}^{11}\text{B}$ reactions in a magnetic confinement device; $\alpha_0/\alpha_1$ branching explains missing $\alpha_0$ peak [12,15]. |
| **HB11 Energy** [2] | Australia | Laser-Driven Block Ignition | Partnered with the University of Rochester (TriForce Institute) to publish 2026 kinetic and radiation hydrodynamics models of $p\text{-}^{11}\text{B}$ burn propagation [7]. |
| **Marvel Fusion** [8] | Germany | Nanostructured Inertial Confinement | Currently constructing a $150M laser facility at Colorado State University to validate non-thermal, local target-ignition physics. |
| **XJTU / Chinese HEDP** [12,27] | China | Laser Beam-Target / Foam & Nano Targets | XG-III TNSA→boron-foam yields up to $10^{10}$ $\alpha$/sr/shot; nanowire and Nano-HEDM target programs [12]. |
| **Blue Laser Fusion** | US/Japan | High-Repetition Inertial Confinement | Founded by Shuji Nakamura; partnered with Caltech under a US DOE INFUSE award to develop advanced diagnostics for $p\text{-}^{11}\text{B}$ interactions. |
| **Anubal Fusion** | India | Inertial Confinement (Laser-driven) | Established in 2024; collaborating with TIFR Hyderabad and IIT Madras on advanced laser-target interactions. |
| **PROBONO COST Action (CA21128)** [9] | Europe | Multi-Platform (Consortium) | A European-funded network (2022–2026) coordinating $p\text{-}^{11}\text{B}$ research for energy and medical applications. Led by researchers from ELI Beamlines, ENEA, and INFN. |
| **The FUSION Project** [10] | Italy | Laser-Plasma Targets | Funded by INFN and ENEA; actively optimizing solid target geometries and alpha-yield diagnostic systems at the PALS facility in Prague. |
| **Pale Blue Fusion / Princeton–ARPA-E** [29–33] | USA | CHARM (Centrifugal Multi-Chamber Mirror) | ARPA-E OPEN 2021 “Economical Proton-Boron11 Fusion”; alpha channeling, helium-ash control, multi-chamber differential confinement; pivoting from academic program to Pale Blue Fusion startup [33]. |
| **Nanjing University** [11] | China | Muon-Catalyzed Theory | Published 2026 semi-classical and Monte Carlo evaluations of muon-enhanced $p\text{-}^{11}\text{B}$ fusion to lower the Coulomb barrier. |

---

## 8. Materials Science and Cooling Challenges
While $p\text{-}^{11}\text{B}$ avoids the severe neutron radiation damage associated with D-T fusion, it introduces a unique set of materials science challenges:

### 8.1 Cyclic Thermal Shock and Spallation
In pulsed inertial systems (such as those by HB11 and Marvel Fusion), the first wall is subjected to periodic, extremely intense bursts of X-rays and alpha particles. This rapid energy deposition causes instantaneous surface heating, leading to cyclic thermal expansion and shock waves. Over time, this leads to **spallation** (flaking and cracking of the surface), which can destroy the first-wall armor and contaminate the reaction chamber.

### 8.2 Impurity and Ash Poisoning
Because the Bremsstrahlung radiation loss scales with $Z_{eff}^2$, even trace amounts of high-$Z$ impurities (such as tungsten or copper sputtered from the reactor walls or electrodes) can catastrophically increase radiation losses, cooling the plasma and extinguishing the fusion reaction instantly. Consequently, the development of ultra-low-sputter coatings and highly efficient divertor systems is a critical prerequisite for any viable $p\text{-}^{11}\text{B}$ design. Fusion-born helium ash is a related but distinct poison: unlike wall impurities, it is produced *in situ* at three alphas per reaction, so magnetic and open-field concepts (notably CHARM; §3.6, §5.6) must remove $^4\mathrm{He}$ on timescales short compared with energy confinement or forfeit engineering breakeven [29].

---

## 9. Conclusion
Proton-boron fusion is transitioning from a theoretical ideal to an active engineering pursuit. By shifting away from thermal equilibrium models toward highly dynamic, non-thermal pulsed regimes—and, in China’s ST program and the Princeton/ARPA-E CHARM line, toward carefully managed non-Maxwellian and multi-chamber architectures—modern projects have identified multiple physical paths around or through the historic Rider Limit. Nuclear-data campaigns, spin polarization, foam and nanostructured targets, hybrid laser–magnetic proton sources, alpha channeling, and helium-ash control further enlarge the design space [12,29,33].

However, the field remains constrained by severe materials science and engineering barriers. Whether developers can construct high-voltage electrostatic grids that resist vacuum breakdown, electrodes that survive extreme alpha particle bombardment, switches capable of running at high repetition rates, ST divertors that tolerate Bremsstrahlung and heat fluxes without impurity poisoning, and (for CHARM) experimentally validated differential confinement and rotation remain open questions. The next decade of experimental validation at facilities like Marvel Fusion's CSU laser site, TAE's Norm-to-Da Vinci path, ENN’s EXL-50U/EHL-2 sequence, Chinese HEDP platforms, and whatever hardware follows Pale Blue Fusion’s in-silico campaign will determine if $p\text{-}^{11}\text{B}$ can become a viable source of commercial electricity.

---

## References

1. **Rider, T. H.** (1995). *Fundamental limitations on plasma fusion systems not in thermodynamic equilibrium*. Ph.D. thesis, Massachusetts Institute of Technology.
2. **Hora, H., et al.** (2017). Road map to clean energy using laser beam ignition of boron-proton fusion. *Laser and Particle Beams*, 35(4), 730-740.
3. **Ochs, I. E., Kolmes, E. J., & Fisch, N. J.** (2025). On the feasibility of radiation-trapping regimes in compressed proton-boron-11 plasmas. *Physics of Plasmas*, 32(2), 022504.
4. **Lerner, E. J., et al.** (2023). Bremsstrahlung suppression in high-density, highly magnetized plasmoids. *Journal of Fusion Energy*, 42(1), 12-21.
5. **Magee, R. M., et al.** (2023). First measurements of proton-boron fusion in a magnetically confined plasma. *Nature Communications*, 14, 955.
6. **Liang, Y., et al.** (2025). Overview of the physics design of the EHL-2 spherical torus. *Plasma Science and Technology*, 27, 024001.
7. **Sefkow, A. B., et al.** (2026). Kinetic and radiation hydrodynamics modeling of thermonuclear burn propagation in isochoric $p\text{-}^{11}\text{B}$. *Fusion Science and Technology*, 82(3), 214-228.
8. **Marvel Fusion GmbH.** (2025). Non-thermal inertial confinement fusion via nanostructured targets: A technical status report. *High Power Laser Science and Engineering*, 13, e14.
9. **Giuffrida, L., et al.** (2024). PROton BOron Nuclear fusion: from energy production to medical applications (PROBONO COST Action CA21128). *European Physical Journal Plus*, 139, 412.
10. **Cirrone, G. A. P., Consoli, F., et al.** (2025). Status and perspectives of the FUSION INFN project for the study and optimization of the $^{11}\text{B}(\text{p}, \alpha)2\alpha$ nuclear fusion reaction for Inertial Confinement applications. *Laser and Particle Beams*, 2025, 8820413.
11. **Wang, H.-Y., Li, Y.-Q., Wu, Q., & Cui, Z.-F.** (2026). A novel approach to proton-boron-11 fusion. *arXiv preprint arXiv:2604.18928v1* [nucl-th].
12. **Liu, B., Li, Z., Luo, D., Xiao, X., Huang, H. R., Zhao, G. C., Zhang, Y. S., Cheng, R., Ren, J. R., Zhao, Y. T., Shi, Y. J., Li, Y. C., Yang, W., Xie, H. S., Sun, T. T., Li, Y. Y., Wu, H. Y., Li, Z. H., Fan, T. S., Wu, D., Liu, S. J., Liu, Y. C., Hoffmann, D. H. H., Dong, J. Q., Peng, Y.-K. M., & Liu, M. S.** (2025). Progress of proton-boron research for fusion energy in China. *IAEA Fusion Energy Conference* pre-print OV-3111.
13. **Nevins, W. M., & Swain, R.** (2000). The thermonuclear fusion rate coefficient for $p\text{-}^{11}\text{B}$ reactions. *Nuclear Fusion*, 40, 865–872.
14. **Sikora, M. H., & Weller, H. R.** (2016). A new evaluation of the $^{11}\text{B}(p,\alpha)\alpha\alpha$ reaction rates. *Journal of Fusion Energy*, 35, 538–543.
15. **Ogawa, K., et al.** (2024). Demonstration of aneutronic $p\text{-}^{11}\text{B}$ reaction in a magnetic confinement device. *Nuclear Fusion*, 64, 096028.
16. **Liu, S., et al.** (2025). Feasibility of proton-boron fusion under non-thermonuclear steady-state conditions: Rider’s constraint revisited. *Physics of Plasmas*, 32, 012101.
17. **Xie, H.** (2023). A simple and fast approach for computing the fusion reactivities with arbitrary ion velocity distributions. *Computer Physics Communications*, 292, 108862.
18. **Xie, H., Tan, M., Luo, D., Li, Z., & Liu, B.** (2023). Fusion reactivities with drift bi-Maxwellian ion velocity distributions. *Plasma Physics and Controlled Fusion*, 65, 055019.
19. **Xie, H., & Wang, X.** (2024). On the upper bound of non-thermal fusion reactivity with fixed total energy. *Plasma Physics and Controlled Fusion*, 66, 065009.
20. **Peng, Y.-K., Shi, Y., Wang, M., Liu, B., & Yan, X.** (2020). Toroidal plasma conditions where the $p\text{-}^{11}\text{B}$ fusion Lawson criterion could be eased.
21. **Ning, X., et al.** (2022). Laser-driven proton-boron fusions: Influences of the boron state. *Laser and Particle Beams*, 2022, e8.
22. **Liu, M., et al.** (2024). ENN’s roadmap for proton-boron fusion based on spherical torus. *Physics of Plasmas*, 31, 062507.
23. **Shaing, K. C., Chu, M. S., & Peng, Y.-K. M.** (2021). Improved neoclassical plasma confinement and turbulence suppression in a magnetic well in tokamak reactors. *Nuclear Fusion*, 61, 096031.
24. **Shi, Y., et al.** (2025). Overview of EXL-50 research progress. *Nuclear Fusion*, 65, 092004.
25. **Li, Z., et al.** (2025). Evaluation of thermal and beam-thermal $p\text{-}^{11}\text{B}$ fusion reactions in the EHL-2 spherical torus. *Plasma Science and Technology*, 27, 024004.
26. **ENN Energy Research Team.** (2024). Physics design and parameters of the EHL-2 spherical torus. *Plasma Science and Technology*, 26(11), 115001–115013 (Special Issue).
27. **Zhao, Y., et al.** (2023). Proton-boron fusion: A dark horse in the fusion race shows yield much beyond expectation. Preprint at https://doi.org/10.21203/rs.3.rs-3224225/v1.
28. **Li, Z., et al.** (2024). Proton–boron fusion in a hydrogen-doped-boron target. *Laser and Particle Beams*, 42, e5.
29. **Ochs, I. E., Kolmes, E. J., & Fisch, N. J.** (2025). Preventing ash from poisoning proton–boron 11 fusion plasmas. *Physics of Plasmas*, 32, 052506.
30. **Ochs, I. E., Kolmes, E. J., Mlodik, M. E., Rubin, T., & Fisch, N. J.** (2022). Improving the feasibility of economical proton-boron-11 fusion via alpha channeling with a hybrid fast and thermal proton scheme. *Physical Review E*, 106, 055215.
31. **Ochs, I. E., & Fisch, N. J.** (2024). Lowering the reactor breakeven requirements for proton–boron 11 fusion. *Physics of Plasmas*, 31, 012503.
32. **Kolmes, E. J., Ochs, I. E., & Fisch, N. J.** (2022). Wave-supported hybrid beam-thermal $p\text{B}11$ fusion. *Physics of Plasmas*, 29, 110701.
33. **Fisch, N.** (2025). Economical proton-boron 11 fusion (ARPA-E OPEN 2021). Presentation at the *2025 ARPA-E Fusion Programs Annual Meeting*, 9 July 2025. https://arpa-e.energy.gov/sites/default/files/2025-08/Day2_08_Fisch.pdf
34. **Princeton University.** (2022). Fisch receives funding for ‘unlikely but fantastic’ clean energy technology. *Princeton News*, 10 March 2022. https://www.princeton.edu/news/2022/03/10/fisch-receives-funding-unlikely-fantastic-clean-energy-technology
35. **Clery, D.** (2023). Reactor experiment demonstrates alternative fusion scheme. *Science* (news), 28 February 2023. https://www.science.org/content/article/reactor-experiment-demonstrates-alternative-fusion-scheme
36. **Roche, T., et al.** (2025). Generation of field-reversed configurations via neutral beam injection. *Nature Communications*, 16, 3487. https://doi.org/10.1038/s41467-025-58849-5
37. **TAE Technologies.** (2025). TAE shortens device roadmap, prepares for commercial era. Company announcement, 17 November 2025. https://tae.com/tae-shortens-device-roadmap-prepares-for-commercial-era/
38. **Li, Z.** (2024). Comment on “ENN’s roadmap for proton-boron fusion based on spherical torus” [*Phys. Plasmas* **31**, 062507 (2024)]. *Physics of Plasmas*, 31, 084701. https://doi.org/10.1063/5.0223575
39. **Liu, M. S., et al.** (2024). Response to “Comment on ‘ENN’s roadmap for proton-boron fusion based on spherical torus’” [*Phys. Plasmas* **31**, 062507 (2024)]. *Physics of Plasmas*, 31, 084702. https://doi.org/10.1063/5.0225696
