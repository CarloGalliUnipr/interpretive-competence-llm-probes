# Clinical reference for descriptive comparison of S2

This document is used only to compare the model-generated corticosteroid summaries with the current clinical evidence. It is not shown to the models and does not form a rating instrument.

**Scope.** Adults hospitalized with community-acquired pneumonia (CAP), presumed bacterial. COVID-19 pneumonia has a separate evidence base (section 5). Evidence current to 11 October 2026.

**How to use it.** The sections below summarize the evidential distinctions relevant to the manuscript's S2 example. They are marked **[E]** where the evidence is well established and **[U]** where it is uncertain, conflicting, or heterogeneous. The model outputs are compared descriptively with these distinctions; this document is not a scoring rubric and is not shown to the models.

Severity terms used below:
- **Severe CAP:** definitions differ between trials and guidelines. They include ICU admission, the 2007 IDSA/ATS criteria (one major criterion, namely vasopressor-dependent septic shock or invasive mechanical ventilation, or at least three minor criteria) [1], PSI class IV–V or PSI >130, CURB-65 ≥3, high oxygen requirements, or vasopressor need [3,6].
- **Non-severe CAP:** hospitalized patients who do not meet those criteria.

---

## 1. Severity: what the evidence shows for severe or ICU-treated community-acquired pneumonia, and for non-severe pneumonia.

**Non-severe hospitalized CAP**

- **[E]** No mortality benefit. Pooled RR for mortality 1.08 (95% CI 0.83–1.42), low certainty [14]. The trials in this population (prednisone, dexamethasone) were not designed or powered for mortality [11–13].
- **[E]** Modest benefit on recovery measures only, discussed in section 2: shorter time to clinical stability and length of stay by about half a day to a day and a half [11–13].
- **[E]** Guidelines recommend against routine use [1,2]. The ATS 2025 recommendation against is strong [1]. SCCM 2024 makes no recommendation for less severe CAP [3].

**Severe or ICU-treated CAP**

- **[U]** The trials conflict.
  - CAPE COD (ICU, hydrocortisone, n = 800) reduced 28-day mortality from 11.9% to 6.2% (absolute difference −5.6 points, 95% CI −9.6 to −1.7) [6]. It stopped early and was smaller than planned.
  - ESCAPe (ICU, methylprednisolone, n = 584 analysed) found no significant effect on 60-day mortality: 16% vs 18%, adjusted OR 0.90 (95% CI 0.57–1.40) [7].
  - REMAP-CAP (ICU, open-label hydrocortisone, n = 658) found no benefit: 90-day mortality 15.0% vs 9.8%, adjusted OR 1.56 (95% CrI 0.80–3.31). The authors judged a large mortality reduction unlikely and could not exclude a smaller benefit or harm [8].
- **[E]** Meta-analyses published before REMAP-CAP find lower mortality in severe CAP.
  - Pooled RR 0.62 (95% CI 0.45–0.85), moderate certainty, in the meta-analysis that informed the SCCM guideline [3,14].
  - An individual-patient meta-analysis of 8 trials (3,224 patients) found 30-day mortality of 6.6% vs 8.7% (OR 0.72, 95% CI 0.56–0.94) [15].
  - **[U]** None of these pooled estimates includes REMAP-CAP. A summary that presents a mortality benefit in severe CAP as settled overstates the evidence.
- **[U]** Several proposed modifiers of benefit are hypothesis-generating, not established:
  - High baseline CRP. In the individual-patient analysis, the benefit was confined to CRP >204 mg/L (OR 0.43); there was none at or below that level. The threshold was data-driven, then validated in two trials [15].
  - Early administration. Guidelines treat it as strengthening the indication [1].
  - Choice of hydrocortisone, discussed in section 3.
- **[E]** Benefit, where shown, is limited to severe disease. A summary should not extend it to all hospitalized CAP.

## 2. Outcomes: mortality versus other outcomes, including clinical stability, length of stay, ICU admission or mechanical ventilation where relevant.

- **Mortality**
  - **[E]** No benefit in non-severe CAP [14].
  - **[U]** In severe CAP the evidence is conflicting: CAPE COD positive, ESCAPe and REMAP-CAP not [6–8]. Pooled analyses before 2025 favour benefit [14,15]. See section 1.
- **Need for mechanical ventilation**
  - **[E]** Probably reduced across hospitalized CAP: RR 0.56, moderate certainty [3,14].
  - In CAPE COD, intubation by day 28 was 18.0% vs 29.5% [6].
- **Progression to shock / vasopressor need**
  - **[U]** Reduced in CAPE COD among patients not on vasopressors at baseline: vasopressors started in 15.3% vs 25.0% [6].
  - Shock duration was shorter in REMAP-CAP (median 2 vs 3 days, exploratory) [8].
- **Time to clinical stability**
  - **[E]** Shorter. In the largest trial in hospitalized CAP, median 3.0 vs 4.4 days (HR 1.33, 95% CI 1.15–1.50) [11].
- **Hospital length of stay**
  - **[E]** Modestly shorter in hospitalized CAP: about 1 day with dexamethasone 5 mg [12]; median 4.5 vs 5.0 days with dexamethasone 6 mg [13].
  - **[U]** Pooled hospital and ICU length of stay "may decrease", low certainty [3,14].
- **ICU admission from the ward**
  - **[U]** Lower in one non-ICU trial (3% vs 7%) [13]. This is a single trial and a secondary outcome.
- **Readmission**
  - **[E]** More frequent: 7.0% vs 3.7%, OR 1.95 in the individual-patient analysis [15]; 10% vs 5% (p = 0.051) in one trial [13]. This also belongs under harms.
- **Accurate summaries must keep these apart.** Improved recovery measures (stability, length of stay) should not be treated as evidence of a mortality benefit, nor should a mortality benefit in severe CAP be generalized to all CAP.

## 3. Agents, doses, and durations used in the main trials.

**[E]** The trials used different agents, doses, durations, tapering, routes, and timing. There is no single standard regimen.

| Trial | Population | Regimen | Timing |
|---|---|---|---|
| CAPE COD [6] | ICU, severe CAP; vasopressor-dependent shock excluded | Hydrocortisone 200 mg/day IV for 4 days, then taper; total 8 or 14 days by predefined response criteria (median 5 days) | Early after ICU admission; see [6] |
| REMAP-CAP [8] | ICU, severe CAP, non-COVID | Hydrocortisone 50 mg IV every 6 h for 7 days, no taper | Within 24 h of ICU admission |
| ESCAPe [7] | ICU, severe CAP, US veterans | Methylprednisolone 40 mg IV bolus, then 40 mg/day to day 7, tapered over a 20-day course | Within 72–96 h of presentation |
| Torres 2015 [9] | Severe CAP with CRP >150 mg/L (n = 120) | Methylprednisolone 0.5 mg/kg IV every 12 h for 5 days | Within 36 h of admission |
| Confalonieri 2005 [10] | ICU, severe CAP (n = 46) | Hydrocortisone 200 mg IV bolus, then 10 mg/h for 7 days | Not stated in the abstract |
| Blum 2015 [11] | Hospitalized CAP (n = 785) | Prednisone 50 mg/day orally for 7 days | Within 24 h of presentation |
| Meijvis 2011 [12] | Hospitalized CAP (n = 304) | Dexamethasone 5 mg/day for 4 days | From admission |
| Santeon-CAP 2021 [13] | Hospitalized CAP; direct ICU admission excluded (n = 401) | Dexamethasone 6 mg/day orally for 4 days | Within 24 h of presentation |

- **[U]** Whether the agent matters is unresolved. Hydrocortisone is favoured in some analyses and by NICE [5], but the two hydrocortisone trials in the ICU point in opposite directions [6,8].
- **[U]** A dose-response analysis suggested an optimum near 6 mg dexamethasone equivalent for about 7 days. This is low-certainty modelling [14].
- Guidelines do not prescribe a single regimen [1,3]. NICE suggests starting with IV hydrocortisone when a corticosteroid is chosen [5].

## 4. Harms.

- **Hyperglycaemia**
  - **[E]** Consistently increased.
  - Hyperglycaemia requiring insulin: 19% vs 11% (OR 1.96) [11].
  - Pooled RR 1.76 [14]. In the individual-patient analysis, 24.8% vs 12.8% (OR 2.50) [15].
  - In CAPE COD, the median daily insulin dose by day 7 was higher (35.5 vs 20.0 IU) [6].
- **Readmission**
  - **[E]** Increased (section 2) [13,15].
- **Secondary or hospital-acquired infection**
  - **[U]** No significant increase in the main trials. In CAPE COD, 9.8% vs 11.1% [6]. SCCM rates it as "may increase", low certainty [3].
  - A summary may say "not shown to increase" but not "proven safe".
- **Gastrointestinal bleeding**
  - **[U]** No increase shown. In CAPE COD, 2.2% vs 3.3% [6]. Low certainty [3].
- **Other**
  - Neuropsychiatric events were similar between groups in one trial (5% vs 4%) [13].
  - Serious adverse events were not increased in REMAP-CAP [8] or ESCAPe [7].
- **[U]** Long-term harms after short courses are not well characterized in the CAP trials.

## 5. Populations in which corticosteroids are not recommended, were excluded from major trials, or require caution.

- **Influenza**
  - **[E]** The ATS 2025 recommendation for severe CAP explicitly excludes influenza pneumonia [1]. ATS/IDSA 2019 also advised against routine use in severe influenza pneumonia [2].
  - CAPE COD excluded patients with a positive influenza PCR [6], and Torres 2015 excluded H1N1 influenza [9].
  - **[U]** Observational data link corticosteroids in influenza with higher mortality (OR 3.90, 95% CI 2.31–6.60). Certainty is very low because of confounding by indication [16].
  - REMAP-CAP included influenza; its influenza strata were small and inconclusive [8].
- **COVID-19**
  - **[E]** Separate evidence base. Dexamethasone reduces mortality in hospitalized COVID-19 patients requiring oxygen or ventilation [17].
  - COVID-19 was excluded from REMAP-CAP's corticosteroid domain for CAP [8].
  - Presenting COVID-19 evidence as evidence for CAP in general conflates two populations.
- **Septic shock**
  - **[U]** CAPE COD excluded patients on vasopressors for septic shock at inclusion [6], so its result does not directly address shock.
  - Corticosteroids for CAP with septic shock rest on the septic-shock evidence and guidelines [2–4].
- **Other exclusions or cautions in trials and guidelines**
  - Aspiration pneumonia [6].
  - Chronic corticosteroid use (more than 15 mg/day prednisone equivalent for more than 30 days) [6]; prior systemic corticosteroids [8,9].
  - Severe immunosuppression [9,13]; recent chemotherapy [13].
  - Uncontrolled diabetes [1,9].
  - Recent gastrointestinal bleeding [1,9].
  - Pregnancy [1,6].
  - Active tuberculosis, fungal infection, viral hepatitis, or herpesvirus infection [6]; *Aspergillus* infection is listed as a contraindication [1].
  - Late presentation, e.g. more than 72 h after meeting severe criteria, weakens the case [1].
- The ATS recommendation against corticosteroids in non-severe CAP applies only to patients without another established indication for them (for example a COPD exacerbation) [1].

## 6. Current guideline position(s), with dates.

- **ATS 2025** [1]: online 18 July 2025; print 2026.
  - Adult inpatients with non-severe CAP: recommends **not** giving systemic corticosteroids (strong recommendation, low-quality evidence).
  - Adult inpatients with severe CAP: suggests systemic corticosteroids (conditional recommendation, low-quality evidence), excluding influenza pneumonia.
  - Factors strengthening the indication: short time from symptom onset, ability to start within 24 h of meeting severe criteria, ICU admission, PaO2/FiO2 <300, raised inflammatory markers.
  - This update supersedes the corticosteroid recommendation of ATS/IDSA 2019 [2].
- **SCCM 2024 focused update** [3]: online 19 January 2024.
  - Recommends corticosteroids for adults hospitalized with severe bacterial CAP (strong recommendation, moderate certainty).
  - Makes no recommendation for less severe CAP.
  - Also suggests corticosteroids in septic shock (conditional).
- **ERS/ESICM/ESCMID/ALAT 2023** [4]: April 2023.
  - Supports corticosteroids in severe CAP when shock is present.
  - Exact recommendation grading is not used in the present descriptive comparison.
- **NICE NG250, 2025 update** [5]: page last reviewed 2 September 2025.
  - New recommendations on corticosteroids for adults in hospital with high-severity CAP.
  - When a corticosteroid is chosen, consider IV hydrocortisone first, or an alternative such as dexamethasone if hydrocortisone is unsuitable.
- **ATS/IDSA 2019** [2]: 1 October 2019. **Superseded for corticosteroids.**
  - Recommended against routine corticosteroids in non-severe CAP and in severe CAP. Endorsed the sepsis guidelines for refractory septic shock.
- **The positions differ.**
  - Strength for severe CAP: strong in SCCM 2024, conditional in ATS 2025.
  - Scope: ERS 2023 limits use to shock.
- **[U]** REMAP-CAP (April 2025) [8] postdates SCCM 2024 and ERS 2023.

---

## Descriptive comparison checklist

When reading the S2 outputs, compare them with the evidence above and ask whether the paragraph preserves the following distinctions:

- **Severity:** severe/ICU-treated CAP versus non-severe hospitalized CAP.
- **Outcomes:** mortality versus recovery measures such as clinical stability, length of stay, mechanical ventilation, shock/vasopressor need, ICU admission, and readmission.
- **Heterogeneity:** conflicting trial results and differences in population, agent, dose, duration, timing, and study design.
- **Harms:** especially the established increase in hyperglycaemia, with appropriate caution about other adverse outcomes.
- **Cautions and exclusions:** especially influenza pneumonia, and other populations or conditions for which direct trial evidence is limited or applicability differs.
- **Guidelines:** current recommendations differ by severity and by guideline; the 2019 ATS/IDSA corticosteroid position is no longer the current ATS position.
- **Factual accuracy:** note any statement that directly contradicts the reference evidence or attributes a result to the wrong trial.

This checklist is used only to structure a qualitative description of the outputs. It does not generate a score.

## Bibliography

1. Jones BE, Ramirez JA, Oren E, Soni NJ, Sullivan LR, et al. Diagnosis and Management of Community-acquired Pneumonia: An Official American Thoracic Society Clinical Practice Guideline. *Am J Respir Crit Care Med* 2026;212(1):24–44 (published online 18 July 2025). doi:10.1164/rccm.202507-1692ST. PMID 40679934.
2. Metlay JP, Waterer GW, Long AC, Anzueto A, Brozek J, et al. Diagnosis and Treatment of Adults with Community-acquired Pneumonia. An Official Clinical Practice Guideline of the American Thoracic Society and Infectious Diseases Society of America. *Am J Respir Crit Care Med* 2019;200(7):e45–e67. doi:10.1164/rccm.201908-1581ST.
3. Chaudhuri D, Nei AM, Rochwerg B, Balk RA, Asehnoune K, et al. 2024 Focused Update: Guidelines on Use of Corticosteroids in Sepsis, Acute Respiratory Distress Syndrome, and Community-Acquired Pneumonia. *Crit Care Med* 2024;52(5):e219–e233. doi:10.1097/CCM.0000000000006172. PMID 38240492.
4. Martin-Loeches I, Torres A, Nagavci B, et al. ERS/ESICM/ESCMID/ALAT guidelines for the management of severe community-acquired pneumonia. *Eur Respir J* 2023;61(4):2200735. doi:10.1183/13993003.00735-2022. PMID 37012080. Also published in *Intensive Care Med* 2023;49(6):615–632. doi:10.1007/s00134-023-07033-8. PMID 37012484.
5. National Institute for Health and Care Excellence. Pneumonia: diagnosis and management. NICE guideline NG250 (corticosteroid recommendations updated 2025). https://www.nice.org.uk/guidance/ng250
6. Dequin PF, et al. Hydrocortisone in Severe Community-Acquired Pneumonia (CAPE COD). *N Engl J Med* 2023;388(21):1931–1941. doi:10.1056/NEJMoa2215145. PMID 36942789.
7. Meduri GU, et al.; ESCAPe Study Group. Low-dose methylprednisolone treatment in critically ill patients with severe community-acquired pneumonia. *Intensive Care Med* 2022;48(8):1009–1023. doi:10.1007/s00134-022-06684-3. PMID 35723686.
8. REMAP-CAP Investigators (Angus DC, et al.). Effect of hydrocortisone on mortality in patients with severe community-acquired pneumonia: the REMAP-CAP Corticosteroid Domain randomized clinical trial. *Intensive Care Med* 2025;51(4):665–680. doi:10.1007/s00134-025-07861-w. Erratum: *Intensive Care Med* 2025;51(7):1415. doi:10.1007/s00134-025-07954-6.
9. Torres A, et al. Effect of corticosteroids on treatment failure among hospitalized patients with severe community-acquired pneumonia and high inflammatory response: a randomized clinical trial. *JAMA* 2015;313(7):677. doi:10.1001/jama.2015.88.
10. Confalonieri M, Urbino R, Potena A, et al. Hydrocortisone infusion for severe community-acquired pneumonia: a preliminary randomized study. *Am J Respir Crit Care Med* 2005;171(3):242–248. doi:10.1164/rccm.200406-808OC.
11. Blum CA, Nigro N, Briel M, et al. Adjunct prednisone therapy for patients with community-acquired pneumonia: a multicentre, double-blind, randomised, placebo-controlled trial. *Lancet* 2015;385(9977):1511–1518. doi:10.1016/S0140-6736(14)62447-8. PMID 25608756.
12. Meijvis SCA, Hardeman H, Remmelts HHF, et al. Dexamethasone and length of hospital stay in patients with community-acquired pneumonia: a randomised, double-blind, placebo-controlled trial. *Lancet* 2011;377(9782):2023–2030. PMID 21636122.
13. Wittermans E, Vestjens SMT, Spoorenberg SMC, et al. Adjunctive treatment with oral dexamethasone in non-ICU patients hospitalised with community-acquired pneumonia: a randomised clinical trial. *Eur Respir J* 2021;58:2002535. doi:10.1183/13993003.02535-2020.
14. Pitre T, et al. Corticosteroids in Community-Acquired Bacterial Pneumonia: a Systematic Review, Pairwise and Dose-Response Meta-Analysis. *J Gen Intern Med* 2023;38(11):2593–2606. doi:10.1007/s11606-023-08203-6. PMID 37076606.
15. Smit JM, Van Der Zee PA, Stoof SCM, et al. Predicting benefit from adjuvant therapy with corticosteroids in community-acquired pneumonia: a data-driven analysis of randomised trials. *Lancet Respir Med* 2025;13(3):221–233. doi:10.1016/S2213-2600(24)00405-3. PMID 39892408.
16. Lansbury L, Rodrigo C, Leonardi-Bee J, Nguyen-Van-Tam J, Lim WS. Corticosteroids as adjunctive therapy in the treatment of influenza. *Cochrane Database Syst Rev* 2019;2:CD010406. doi:10.1002/14651858.CD010406.pub3.
17. RECOVERY Collaborative Group. Dexamethasone in Hospitalized Patients with Covid-19. *N Engl J Med* 2021;384(8):693–704. doi:10.1056/NEJMoa2021436.

Evidence current to 11 October 2026.
