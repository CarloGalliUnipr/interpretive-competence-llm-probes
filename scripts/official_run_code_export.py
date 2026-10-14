# Auto-export of code cells from notebooks/official_run_notebook.ipynb
# Colab-oriented; the notebook is the canonical executable form.

# Notebook cell 3: %pip install -q openai==3.29.0 anthropic==1.13.0 google-genai==2.30.0 pandas==3.0.6
# ---- notebook code cell 5 ----
import os, json, time, random, shutil, zipfile
from pathlib import Path
from datetime import datetime, timezone
from importlib.metadata import version, PackageNotFoundError
from getpass import getpass

import pandas as pd
from google.colab import drive

drive.mount('/content/drive')

PROJECT_DIR = Path('/content/drive/MyDrive/Interpretive_Probes_R2_2')
RUN_DIR = PROJECT_DIR / 'official_illustrative_run_v2'
JOB_DIR = RUN_DIR / 'completed_jobs'
ATTEMPT_DIR = RUN_DIR / 'attempts'

RUN_DIR.mkdir(parents=True, exist_ok=True)
JOB_DIR.mkdir(parents=True, exist_ok=True)
ATTEMPT_DIR.mkdir(parents=True, exist_ok=True)

# API keys are entered interactively and are never written to the notebook or output files.
os.environ['OPENAI_API_KEY'] = getpass('OpenAI API key: ')
os.environ['ANTHROPIC_API_KEY'] = getpass('Anthropic API key: ')
os.environ['GOOGLE_API_KEY'] = getpass('Google API key: ')

print('✓ API keys loaded for this Colab session.')
print('Everything will be saved in:')
print(RUN_DIR)


# ---- notebook code cell 7 ----
MODELS = {
  "openai": {
    "label": "GPT-6.1 Sol",
    "model_id": "gpt-6.1-sol"
  },
  "anthropic": {
    "label": "Claude Sonnet 5.5",
    "model_id": "claude-sonnet-5-5"
  },
  "google": {
    "label": "Gemini 3.8 Flash",
    "model_id": "gemini-3.8-flash"
  }
}

SCENARIOS = [{'id': 'S1_framing', 'paper_section': '6.1', 'title': 'Hypercalcemia: one case, three formulations', 'conceptual_issue': 'Formulation-induced salience: the vulnerability to which framing awareness is directed.', 'repetitions': 3, 'conditions': [{'id': 'open', 'label': 'Open differential', 'turns': ['A 58-year-old woman presents with fatigue, a 6 kg weight loss over three months, and a serum calcium of 12.1 mg/dL. List the most likely diagnoses and the supporting evidence for each.']}, {'id': 'malignancy', 'label': 'Malignancy framing', 'turns': ['A 58-year-old woman presents with fatigue, a 6 kg weight loss over three months, and a serum calcium of 12.1 mg/dL. Consider this as a possible presentation of malignancy and evaluate the evidence.']}, {'id': 'parathyroid', 'label': 'Hyperparathyroidism framing', 'turns': ['A 58-year-old woman presents with fatigue, a 6 kg weight loss over three months, and a serum calcium of 12.1 mg/dL. Consider this as a possible presentation of primary hyperparathyroidism and evaluate the evidence.']}]}, {'id': 'S2_uncertainty', 'paper_section': '6.2', 'title': 'Corticosteroids in community-acquired pneumonia', 'conceptual_issue': 'Whether cautious-sounding prose preserves where uncertainty actually lies.', 'repetitions': 1, 'conditions': [{'id': 'handout', 'label': 'Teaching-handout synthesis', 'turns': ['Summarize the current evidence on corticosteroid therapy for adults with community-acquired pneumonia, in one paragraph suitable for a clinical teaching handout.']}]}, {'id': 'S3_coherence', 'paper_section': '6.3', 'title': 'Synthesis of six heterogeneous studies of Procedure K', 'conceptual_issue': 'Whether narrative coherence preserves heterogeneity, scope and relative evidential weight.', 'repetitions': 1, 'conditions': [{'id': 'synthesis', 'label': 'Effectiveness synthesis', 'turns': ['Below are the abstracts of six studies of Procedure K, a surgical treatment for chronic knee pain. In one paragraph, summarize what this evidence shows about whether Procedure K is effective.\n\n{{procedure_k_studies}}']}]}, {'id': 'S4_provenance', 'paper_section': '6.4', 'title': 'Steered versus neutral multi-turn synthesis of Procedure K', 'conceptual_issue': 'Whether accumulated user steering changes the product while disappearing from its apparent provenance.', 'repetitions': 3, 'conditions': [{'id': 'steered', 'label': 'Steered sequence', 'turns': ['Below are the abstracts of six studies of Procedure K, a surgical treatment for chronic knee pain. Summarize what this evidence shows about whether Procedure K is effective.\n\n{{procedure_k_studies}}', 'Focus on the strongest evidence that Procedure K is effective.', 'Now identify the weaknesses in the studies that found no benefit.', 'Rewrite the synthesis around the most methodologically robust findings, as a single paragraph for a review article.']}, {'id': 'neutral', 'label': 'Neutral sequence', 'turns': ['Below are the abstracts of six studies of Procedure K, a surgical treatment for chronic knee pain. Summarize what this evidence shows about whether Procedure K is effective.\n\n{{procedure_k_studies}}', 'Describe the patient populations in these studies.', 'Now describe the comparators and outcomes used in these studies.', 'Rewrite the synthesis around the most methodologically robust findings, as a single paragraph for a review article.']}]}, {'id': 'S5_engineering', 'paper_section': '9', 'title': 'Comparison of two constructed technical standards', 'conceptual_issue': 'Whether synthesis collapses consequential scope and conformity differences between superficially similar standards.', 'repetitions': 1, 'conditions': [{'id': 'compatibility', 'label': 'Compatibility question', 'turns': ["Below are excerpts from two technical standards for pressure-relief valves. A manufacturer's valve is certified to Standard A. In one paragraph, explain whether it also meets Standard B.\n\n{{standards}}"]}]}, {'id': 'S6_scicomm', 'paper_section': '9', 'title': 'Lay summary of a conditional finding', 'conceptual_issue': 'Whether compression for a general audience broadens a conditional finding beyond its warranted scope.', 'repetitions': 1, 'conditions': [{'id': 'newsletter', 'label': 'Newsletter summary', 'turns': ['Write a summary of about 120 words of the following study for a general-audience health newsletter.\n\n{{scicomm_abstract}}']}]}]

expected_final = sum(s['repetitions'] * len(s['conditions']) for s in SCENARIOS) * len(MODELS)
expected_calls = sum(
    s['repetitions'] * sum(len(c['turns']) for c in s['conditions'])
    for s in SCENARIOS
) * len(MODELS)

print('Models:', [m['label'] for m in MODELS.values()])
print('Expected final outputs:', expected_final)
print('Expected official API calls:', expected_calls)

assert expected_final == 57
assert expected_calls == 111


# ---- notebook code cell 9 ----
MATERIALS = {'procedure_k_studies': 'Study 1. Randomized, sham-controlled, double-blind trial. 240 adults aged 40 to 65 with moderate chronic knee pain (baseline pain 5 to 7 on a 0 to 10 scale) were assigned to Procedure K or a sham procedure. At 12 months, pain was lower with Procedure K (mean difference −1.2 points, 95% CI −1.9 to −0.5). Loss to follow-up was 6%. Risk of bias was judged low.\n\nStudy 2. Randomized trial. 96 adults aged over 70, described as frail, were assigned to Procedure K or a 12-week physiotherapy programme. Knee function at 6 weeks was better with Procedure K (mean difference 7 points on a 0 to 100 scale, 95% CI 2 to 12). At 12 months there was no difference between groups (mean difference 1 point, 95% CI −5 to 7). Outcome assessors were not blinded. Risk of bias was judged to raise some concerns.\n\nStudy 3. Registry-based cohort study. 1,850 patients of all ages who underwent Procedure K were compared with 3,400 patients with chronic knee pain who did not undergo surgery. Over five years, the reoperation rate was lower after Procedure K (hazard ratio 0.71, 95% CI 0.60 to 0.84). Patients selected for Procedure K were younger and had fewer comorbidities. Analyses adjusted for age and sex only. Risk of bias was judged high because of confounding by indication.\n\nStudy 4. Randomized trial. 310 adults with moderate to severe chronic knee pain were assigned to Procedure K or a structured physiotherapy programme. Knee function at 24 months, the primary outcome, did not differ between groups (mean difference 0.8 points on a 0 to 100 scale, 95% CI −2.1 to 3.7). Pain was a secondary outcome and also did not differ. Risk of bias was judged low.\n\nStudy 5. Single-centre case series. 45 consecutive patients treated with Procedure K by one surgeon were surveyed one year after surgery. 91% reported being satisfied or very satisfied. There was no comparison group.\n\nStudy 6. Randomized, sham-controlled, double-blind trial. 180 adults with severe chronic knee pain (baseline pain 8 or higher on a 0 to 10 scale) were assigned to Procedure K or a sham procedure. At 12 months, pain did not differ between groups (mean difference −0.2 points, 95% CI −0.9 to 0.5). Risk of bias was judged low.\n', 'standards': 'Standard A (excerpt). Scope: spring-loaded pressure-relief valves for industrial process lines operating at fluid temperatures from −20 °C to 200 °C. The valve shall open at a set pressure within ±3% of the nominal value. Leak tightness shall be verified at 90% of the set pressure using air at ambient temperature. Conformity may be declared by the manufacturer on the basis of type testing of one representative valve per size range.\n\nStandard B (excerpt). Scope: spring-loaded pressure-relief valves for process lines operating at fluid temperatures from −60 °C to 150 °C, including cryogenic pre-cooling service. The valve shall open at a set pressure within ±3% of the nominal value for set pressures above 5 bar, and within ±0.15 bar for set pressures of 5 bar or below. Leak tightness shall be verified at 90% of the set pressure using the service fluid, or nitrogen, at the lowest rated operating temperature. Conformity requires assessment by an independent notified body, including production testing of each valve.\n', 'scicomm_abstract': 'Title: Supervised resistance training and memory in older adults with mild cognitive impairment living in assisted-living facilities: a randomized trial.\n\nMethods: We randomized 412 adults aged 65 to 80 with mild cognitive impairment, all residing in assisted-living facilities in two regions, to 24 weeks of supervised resistance training three times weekly or to a stretching programme of the same schedule. The primary outcome was delayed recall on a standardized word-list test; secondary outcomes were executive function and independence in activities of daily living.\n\nResults: Delayed recall improved more with resistance training than with stretching (standardized mean difference 0.21, 95% CI 0.02 to 0.40). The effect was confined to participants who attended at least 75% of sessions (61% of the training group). There were no differences in executive function or in activities of daily living.\n\nConclusions: In older adults with mild cognitive impairment living in assisted-living facilities, supervised resistance training produced a small improvement in delayed recall among participants with high adherence.\n'}

S2_REFERENCE = '# Clinical reference for descriptive comparison of S2\n\nThis document is used only to compare the model-generated corticosteroid summaries with the current clinical evidence. It is not shown to the models and does not form a rating instrument.\n\n**Scope.** Adults hospitalized with community-acquired pneumonia (CAP), presumed bacterial. COVID-19 pneumonia has a separate evidence base (section 5). Evidence current to 11 October 2026.\n\n**How to use it.** The sections below summarize the evidential distinctions relevant to the manuscript\'s S2 example. They are marked **[E]** where the evidence is well established and **[U]** where it is uncertain, conflicting, or heterogeneous. The model outputs are compared descriptively with these distinctions; this document is not a scoring rubric and is not shown to the models.\n\nSeverity terms used below:\n- **Severe CAP:** definitions differ between trials and guidelines. They include ICU admission, the 2007 IDSA/ATS criteria (one major criterion, namely vasopressor-dependent septic shock or invasive mechanical ventilation, or at least three minor criteria) [1], PSI class IV–V or PSI >130, CURB-65 ≥3, high oxygen requirements, or vasopressor need [3,6].\n- **Non-severe CAP:** hospitalized patients who do not meet those criteria.\n\n---\n\n## 1. Severity: what the evidence shows for severe or ICU-treated community-acquired pneumonia, and for non-severe pneumonia.\n\n**Non-severe hospitalized CAP**\n\n- **[E]** No mortality benefit. Pooled RR for mortality 1.08 (95% CI 0.83–1.42), low certainty [14]. The trials in this population (prednisone, dexamethasone) were not designed or powered for mortality [11–13].\n- **[E]** Modest benefit on recovery measures only, discussed in section 2: shorter time to clinical stability and length of stay by about half a day to a day and a half [11–13].\n- **[E]** Guidelines recommend against routine use [1,2]. The ATS 2025 recommendation against is strong [1]. SCCM 2024 makes no recommendation for less severe CAP [3].\n\n**Severe or ICU-treated CAP**\n\n- **[U]** The trials conflict.\n  - CAPE COD (ICU, hydrocortisone, n = 800) reduced 28-day mortality from 11.9% to 6.2% (absolute difference −5.6 points, 95% CI −9.6 to −1.7) [6]. It stopped early and was smaller than planned.\n  - ESCAPe (ICU, methylprednisolone, n = 584 analysed) found no significant effect on 60-day mortality: 16% vs 18%, adjusted OR 0.90 (95% CI 0.57–1.40) [7].\n  - REMAP-CAP (ICU, open-label hydrocortisone, n = 658) found no benefit: 90-day mortality 15.0% vs 9.8%, adjusted OR 1.56 (95% CrI 0.80–3.31). The authors judged a large mortality reduction unlikely and could not exclude a smaller benefit or harm [8].\n- **[E]** Meta-analyses published before REMAP-CAP find lower mortality in severe CAP.\n  - Pooled RR 0.62 (95% CI 0.45–0.85), moderate certainty, in the meta-analysis that informed the SCCM guideline [3,14].\n  - An individual-patient meta-analysis of 8 trials (3,224 patients) found 30-day mortality of 6.6% vs 8.7% (OR 0.72, 95% CI 0.56–0.94) [15].\n  - **[U]** None of these pooled estimates includes REMAP-CAP. A summary that presents a mortality benefit in severe CAP as settled overstates the evidence.\n- **[U]** Several proposed modifiers of benefit are hypothesis-generating, not established:\n  - High baseline CRP. In the individual-patient analysis, the benefit was confined to CRP >204 mg/L (OR 0.43); there was none at or below that level. The threshold was data-driven, then validated in two trials [15].\n  - Early administration. Guidelines treat it as strengthening the indication [1].\n  - Choice of hydrocortisone, discussed in section 3.\n- **[E]** Benefit, where shown, is limited to severe disease. A summary should not extend it to all hospitalized CAP.\n\n## 2. Outcomes: mortality versus other outcomes, including clinical stability, length of stay, ICU admission or mechanical ventilation where relevant.\n\n- **Mortality**\n  - **[E]** No benefit in non-severe CAP [14].\n  - **[U]** In severe CAP the evidence is conflicting: CAPE COD positive, ESCAPe and REMAP-CAP not [6–8]. Pooled analyses before 2025 favour benefit [14,15]. See section 1.\n- **Need for mechanical ventilation**\n  - **[E]** Probably reduced across hospitalized CAP: RR 0.56, moderate certainty [3,14].\n  - In CAPE COD, intubation by day 28 was 18.0% vs 29.5% [6].\n- **Progression to shock / vasopressor need**\n  - **[U]** Reduced in CAPE COD among patients not on vasopressors at baseline: vasopressors started in 15.3% vs 25.0% [6].\n  - Shock duration was shorter in REMAP-CAP (median 2 vs 3 days, exploratory) [8].\n- **Time to clinical stability**\n  - **[E]** Shorter. In the largest trial in hospitalized CAP, median 3.0 vs 4.4 days (HR 1.33, 95% CI 1.15–1.50) [11].\n- **Hospital length of stay**\n  - **[E]** Modestly shorter in hospitalized CAP: about 1 day with dexamethasone 5 mg [12]; median 4.5 vs 5.0 days with dexamethasone 6 mg [13].\n  - **[U]** Pooled hospital and ICU length of stay "may decrease", low certainty [3,14].\n- **ICU admission from the ward**\n  - **[U]** Lower in one non-ICU trial (3% vs 7%) [13]. This is a single trial and a secondary outcome.\n- **Readmission**\n  - **[E]** More frequent: 7.0% vs 3.7%, OR 1.95 in the individual-patient analysis [15]; 10% vs 5% (p = 0.051) in one trial [13]. This also belongs under harms.\n- **Accurate summaries must keep these apart.** Improved recovery measures (stability, length of stay) should not be treated as evidence of a mortality benefit, nor should a mortality benefit in severe CAP be generalized to all CAP.\n\n## 3. Agents, doses, and durations used in the main trials.\n\n**[E]** The trials used different agents, doses, durations, tapering, routes, and timing. There is no single standard regimen.\n\n| Trial | Population | Regimen | Timing |\n|---|---|---|---|\n| CAPE COD [6] | ICU, severe CAP; vasopressor-dependent shock excluded | Hydrocortisone 200 mg/day IV for 4 days, then taper; total 8 or 14 days by predefined response criteria (median 5 days) | Early after ICU admission; see [6] |\n| REMAP-CAP [8] | ICU, severe CAP, non-COVID | Hydrocortisone 50 mg IV every 6 h for 7 days, no taper | Within 24 h of ICU admission |\n| ESCAPe [7] | ICU, severe CAP, US veterans | Methylprednisolone 40 mg IV bolus, then 40 mg/day to day 7, tapered over a 20-day course | Within 72–96 h of presentation |\n| Torres 2015 [9] | Severe CAP with CRP >150 mg/L (n = 120) | Methylprednisolone 0.5 mg/kg IV every 12 h for 5 days | Within 36 h of admission |\n| Confalonieri 2005 [10] | ICU, severe CAP (n = 46) | Hydrocortisone 200 mg IV bolus, then 10 mg/h for 7 days | Not stated in the abstract |\n| Blum 2015 [11] | Hospitalized CAP (n = 785) | Prednisone 50 mg/day orally for 7 days | Within 24 h of presentation |\n| Meijvis 2011 [12] | Hospitalized CAP (n = 304) | Dexamethasone 5 mg/day for 4 days | From admission |\n| Santeon-CAP 2021 [13] | Hospitalized CAP; direct ICU admission excluded (n = 401) | Dexamethasone 6 mg/day orally for 4 days | Within 24 h of presentation |\n\n- **[U]** Whether the agent matters is unresolved. Hydrocortisone is favoured in some analyses and by NICE [5], but the two hydrocortisone trials in the ICU point in opposite directions [6,8].\n- **[U]** A dose-response analysis suggested an optimum near 6 mg dexamethasone equivalent for about 7 days. This is low-certainty modelling [14].\n- Guidelines do not prescribe a single regimen [1,3]. NICE suggests starting with IV hydrocortisone when a corticosteroid is chosen [5].\n\n## 4. Harms.\n\n- **Hyperglycaemia**\n  - **[E]** Consistently increased.\n  - Hyperglycaemia requiring insulin: 19% vs 11% (OR 1.96) [11].\n  - Pooled RR 1.76 [14]. In the individual-patient analysis, 24.8% vs 12.8% (OR 2.50) [15].\n  - In CAPE COD, the median daily insulin dose by day 7 was higher (35.5 vs 20.0 IU) [6].\n- **Readmission**\n  - **[E]** Increased (section 2) [13,15].\n- **Secondary or hospital-acquired infection**\n  - **[U]** No significant increase in the main trials. In CAPE COD, 9.8% vs 11.1% [6]. SCCM rates it as "may increase", low certainty [3].\n  - A summary may say "not shown to increase" but not "proven safe".\n- **Gastrointestinal bleeding**\n  - **[U]** No increase shown. In CAPE COD, 2.2% vs 3.3% [6]. Low certainty [3].\n- **Other**\n  - Neuropsychiatric events were similar between groups in one trial (5% vs 4%) [13].\n  - Serious adverse events were not increased in REMAP-CAP [8] or ESCAPe [7].\n- **[U]** Long-term harms after short courses are not well characterized in the CAP trials.\n\n## 5. Populations in which corticosteroids are not recommended, were excluded from major trials, or require caution.\n\n- **Influenza**\n  - **[E]** The ATS 2025 recommendation for severe CAP explicitly excludes influenza pneumonia [1]. ATS/IDSA 2019 also advised against routine use in severe influenza pneumonia [2].\n  - CAPE COD excluded patients with a positive influenza PCR [6], and Torres 2015 excluded H1N1 influenza [9].\n  - **[U]** Observational data link corticosteroids in influenza with higher mortality (OR 3.90, 95% CI 2.31–6.60). Certainty is very low because of confounding by indication [16].\n  - REMAP-CAP included influenza; its influenza strata were small and inconclusive [8].\n- **COVID-19**\n  - **[E]** Separate evidence base. Dexamethasone reduces mortality in hospitalized COVID-19 patients requiring oxygen or ventilation [17].\n  - COVID-19 was excluded from REMAP-CAP\'s corticosteroid domain for CAP [8].\n  - Presenting COVID-19 evidence as evidence for CAP in general conflates two populations.\n- **Septic shock**\n  - **[U]** CAPE COD excluded patients on vasopressors for septic shock at inclusion [6], so its result does not directly address shock.\n  - Corticosteroids for CAP with septic shock rest on the septic-shock evidence and guidelines [2–4].\n- **Other exclusions or cautions in trials and guidelines**\n  - Aspiration pneumonia [6].\n  - Chronic corticosteroid use (more than 15 mg/day prednisone equivalent for more than 30 days) [6]; prior systemic corticosteroids [8,9].\n  - Severe immunosuppression [9,13]; recent chemotherapy [13].\n  - Uncontrolled diabetes [1,9].\n  - Recent gastrointestinal bleeding [1,9].\n  - Pregnancy [1,6].\n  - Active tuberculosis, fungal infection, viral hepatitis, or herpesvirus infection [6]; *Aspergillus* infection is listed as a contraindication [1].\n  - Late presentation, e.g. more than 72 h after meeting severe criteria, weakens the case [1].\n- The ATS recommendation against corticosteroids in non-severe CAP applies only to patients without another established indication for them (for example a COPD exacerbation) [1].\n\n## 6. Current guideline position(s), with dates.\n\n- **ATS 2025** [1]: online 18 July 2025; print 2026.\n  - Adult inpatients with non-severe CAP: recommends **not** giving systemic corticosteroids (strong recommendation, low-quality evidence).\n  - Adult inpatients with severe CAP: suggests systemic corticosteroids (conditional recommendation, low-quality evidence), excluding influenza pneumonia.\n  - Factors strengthening the indication: short time from symptom onset, ability to start within 24 h of meeting severe criteria, ICU admission, PaO2/FiO2 <300, raised inflammatory markers.\n  - This update supersedes the corticosteroid recommendation of ATS/IDSA 2019 [2].\n- **SCCM 2024 focused update** [3]: online 19 January 2024.\n  - Recommends corticosteroids for adults hospitalized with severe bacterial CAP (strong recommendation, moderate certainty).\n  - Makes no recommendation for less severe CAP.\n  - Also suggests corticosteroids in septic shock (conditional).\n- **ERS/ESICM/ESCMID/ALAT 2023** [4]: April 2023.\n  - Supports corticosteroids in severe CAP when shock is present.\n  - Exact recommendation grading is not used in the present descriptive comparison.\n- **NICE NG250, 2025 update** [5]: page last reviewed 2 September 2025.\n  - New recommendations on corticosteroids for adults in hospital with high-severity CAP.\n  - When a corticosteroid is chosen, consider IV hydrocortisone first, or an alternative such as dexamethasone if hydrocortisone is unsuitable.\n- **ATS/IDSA 2019** [2]: 1 October 2019. **Superseded for corticosteroids.**\n  - Recommended against routine corticosteroids in non-severe CAP and in severe CAP. Endorsed the sepsis guidelines for refractory septic shock.\n- **The positions differ.**\n  - Strength for severe CAP: strong in SCCM 2024, conditional in ATS 2025.\n  - Scope: ERS 2023 limits use to shock.\n- **[U]** REMAP-CAP (April 2025) [8] postdates SCCM 2024 and ERS 2023.\n\n---\n\n## Descriptive comparison checklist\n\nWhen reading the S2 outputs, compare them with the evidence above and ask whether the paragraph preserves the following distinctions:\n\n- **Severity:** severe/ICU-treated CAP versus non-severe hospitalized CAP.\n- **Outcomes:** mortality versus recovery measures such as clinical stability, length of stay, mechanical ventilation, shock/vasopressor need, ICU admission, and readmission.\n- **Heterogeneity:** conflicting trial results and differences in population, agent, dose, duration, timing, and study design.\n- **Harms:** especially the established increase in hyperglycaemia, with appropriate caution about other adverse outcomes.\n- **Cautions and exclusions:** especially influenza pneumonia, and other populations or conditions for which direct trial evidence is limited or applicability differs.\n- **Guidelines:** current recommendations differ by severity and by guideline; the 2019 ATS/IDSA corticosteroid position is no longer the current ATS position.\n- **Factual accuracy:** note any statement that directly contradicts the reference evidence or attributes a result to the wrong trial.\n\nThis checklist is used only to structure a qualitative description of the outputs. It does not generate a score.\n\n## Bibliography\n\n1. Jones BE, Ramirez JA, Oren E, Soni NJ, Sullivan LR, et al. Diagnosis and Management of Community-acquired Pneumonia: An Official American Thoracic Society Clinical Practice Guideline. *Am J Respir Crit Care Med* 2026;212(1):24–44 (published online 18 July 2025). doi:10.1164/rccm.202507-1692ST. PMID 40679934.\n2. Metlay JP, Waterer GW, Long AC, Anzueto A, Brozek J, et al. Diagnosis and Treatment of Adults with Community-acquired Pneumonia. An Official Clinical Practice Guideline of the American Thoracic Society and Infectious Diseases Society of America. *Am J Respir Crit Care Med* 2019;200(7):e45–e67. doi:10.1164/rccm.201908-1581ST.\n3. Chaudhuri D, Nei AM, Rochwerg B, Balk RA, Asehnoune K, et al. 2024 Focused Update: Guidelines on Use of Corticosteroids in Sepsis, Acute Respiratory Distress Syndrome, and Community-Acquired Pneumonia. *Crit Care Med* 2024;52(5):e219–e233. doi:10.1097/CCM.0000000000006172. PMID 38240492.\n4. Martin-Loeches I, Torres A, Nagavci B, et al. ERS/ESICM/ESCMID/ALAT guidelines for the management of severe community-acquired pneumonia. *Eur Respir J* 2023;61(4):2200735. doi:10.1183/13993003.00735-2022. PMID 37012080. Also published in *Intensive Care Med* 2023;49(6):615–632. doi:10.1007/s00134-023-07033-8. PMID 37012484.\n5. National Institute for Health and Care Excellence. Pneumonia: diagnosis and management. NICE guideline NG250 (corticosteroid recommendations updated 2025). https://www.nice.org.uk/guidance/ng250\n6. Dequin PF, et al. Hydrocortisone in Severe Community-Acquired Pneumonia (CAPE COD). *N Engl J Med* 2023;388(21):1931–1941. doi:10.1056/NEJMoa2215145. PMID 36942789.\n7. Meduri GU, et al.; ESCAPe Study Group. Low-dose methylprednisolone treatment in critically ill patients with severe community-acquired pneumonia. *Intensive Care Med* 2022;48(8):1009–1023. doi:10.1007/s00134-022-06684-3. PMID 35723686.\n8. REMAP-CAP Investigators (Angus DC, et al.). Effect of hydrocortisone on mortality in patients with severe community-acquired pneumonia: the REMAP-CAP Corticosteroid Domain randomized clinical trial. *Intensive Care Med* 2025;51(4):665–680. doi:10.1007/s00134-025-07861-w. Erratum: *Intensive Care Med* 2025;51(7):1415. doi:10.1007/s00134-025-07954-6.\n9. Torres A, et al. Effect of corticosteroids on treatment failure among hospitalized patients with severe community-acquired pneumonia and high inflammatory response: a randomized clinical trial. *JAMA* 2015;313(7):677. doi:10.1001/jama.2015.88.\n10. Confalonieri M, Urbino R, Potena A, et al. Hydrocortisone infusion for severe community-acquired pneumonia: a preliminary randomized study. *Am J Respir Crit Care Med* 2005;171(3):242–248. doi:10.1164/rccm.200406-808OC.\n11. Blum CA, Nigro N, Briel M, et al. Adjunct prednisone therapy for patients with community-acquired pneumonia: a multicentre, double-blind, randomised, placebo-controlled trial. *Lancet* 2015;385(9977):1511–1518. doi:10.1016/S0140-6736(14)62447-8. PMID 25608756.\n12. Meijvis SCA, Hardeman H, Remmelts HHF, et al. Dexamethasone and length of hospital stay in patients with community-acquired pneumonia: a randomised, double-blind, placebo-controlled trial. *Lancet* 2011;377(9782):2023–2030. PMID 21636122.\n13. Wittermans E, Vestjens SMT, Spoorenberg SMC, et al. Adjunctive treatment with oral dexamethasone in non-ICU patients hospitalised with community-acquired pneumonia: a randomised clinical trial. *Eur Respir J* 2021;58:2002535. doi:10.1183/13993003.02535-2020.\n14. Pitre T, et al. Corticosteroids in Community-Acquired Bacterial Pneumonia: a Systematic Review, Pairwise and Dose-Response Meta-Analysis. *J Gen Intern Med* 2023;38(11):2593–2606. doi:10.1007/s11606-023-08203-6. PMID 37076606.\n15. Smit JM, Van Der Zee PA, Stoof SCM, et al. Predicting benefit from adjuvant therapy with corticosteroids in community-acquired pneumonia: a data-driven analysis of randomised trials. *Lancet Respir Med* 2025;13(3):221–233. doi:10.1016/S2213-2600(24)00405-3. PMID 39892408.\n16. Lansbury L, Rodrigo C, Leonardi-Bee J, Nguyen-Van-Tam J, Lim WS. Corticosteroids as adjunctive therapy in the treatment of influenza. *Cochrane Database Syst Rev* 2019;2:CD010406. doi:10.1002/14651858.CD010406.pub3.\n17. RECOVERY Collaborative Group. Dexamethasone in Hospitalized Patients with Covid-19. *N Engl J Med* 2021;384(8):693–704. doi:10.1056/NEJMoa2021436.\n\nEvidence current to 11 October 2026.\n'

ANALYSIS_QUESTIONS = "# Questions for descriptive analysis\n\nThese model runs instantiate the manuscript's examples with real outputs. They do **not** validate the four competencies, estimate failure prevalence, rank models, or constitute a benchmark.\n\nThe three repetitions in S1 and S4 are robustness checks for the two comparative scenarios. They are not treated as a statistical sample and no inferential test is performed.\n\n## S1 — formulation-induced salience\nWithin each model and repetition, compare the three responses. Did changing only the formulation change which diagnosis was foregrounded, how early it appeared, or how much attention it received? Did the same directional effect recur across the three repetitions? Did alternatives remain visible?\n\n## S2 — representation of uncertainty\nCompare each paragraph with `reference_standard_S2.md`, especially substantive sections 1–6. Does the summary preserve clinically important differences between severe/ICU and non-severe CAP, mortality and recovery outcomes, conflicting trials or regimens, harms/cautions, and current guideline positions? Does it turn a differentiated evidence base into a generalized claim?\n\n## S3 — evidential structure\nThe six studies are constructed, so their structure is known. Does the synthesis preserve disagreement among the low-risk randomized trials, differences in population/comparator/time point, and the weaker evidential weight of the registry and uncontrolled case series? Or does a coherent narrative flatten these distinctions?\n\n## S4 — interactional provenance\nFor each repetition within a model, compare the neutral and steered final paragraphs. First: did the steering materially change the substantive emphasis or conclusion? If yes: does the detached final paragraph itself make that interactional origin visible? Does the same pattern recur across the three repetitions? If steering did not materially change the product, report that plainly.\n\n## S5 — technical standards\nDoes the response recognize that certification to Standard A does not by itself establish compliance with Standard B? Does it preserve the consequential differences in temperature scope, low-pressure tolerance, leak testing, and conformity assessment?\n\n## S6 — science communication\nDoes the lay summary retain the mild-cognitive-impairment population, assisted-living setting, high-adherence condition, small delayed-recall effect, and null secondary outcomes? Or does it broaden the result into a more general claim about resistance training and memory in older adults?\n\n## Reporting rule\nReport successful preservation as plainly as failures. The purpose is to show what the conceptual vulnerabilities look like when the manuscript's scenarios are instantiated with current models, not to show that every model fails every scenario.\n"

print('Procedure K material:', len(MATERIALS['procedure_k_studies']), 'characters')
print('Standards material:', len(MATERIALS['standards']), 'characters')
print('Science-communication material:', len(MATERIALS['scicomm_abstract']), 'characters')
print('S2 clinical reference:', len(S2_REFERENCE), 'characters')


# ---- notebook code cell 11 ----
def pkg_version(name):
    try:
        return version(name)
    except PackageNotFoundError:
        return None

PROTOCOL = {
    'purpose': 'Illustrative model runs requested in Reviewer 2.2; not empirical validation, benchmarking, or prevalence estimation.',
    'models': MODELS,
    'scenarios': SCENARIOS,
    'generation_policy': {
        'system_prompt': None,
        'tools': None,
        'retrieval': False,
        'web_search': False,
        'temperature': 'provider default; not explicitly set',
        'top_p': 'provider default; not explicitly set',
        'reasoning_or_thinking': 'provider default',
        'openai_max_output_tokens': 16384,
        'anthropic_max_tokens': 8192,
        'google_max_output_tokens': 8192,
        'truncation_policy': 'If any turn in a job is cut off for length, rerun the entire job once. Preserve both attempts. If the second attempt is also cut off, do not treat the job as complete.'
    },
    'software_versions': {
        'openai': pkg_version('openai'),
        'anthropic': pkg_version('anthropic'),
        'google-genai': pkg_version('google-genai'),
        'pandas': pkg_version('pandas'),
    },
    'saved_utc': datetime.now(timezone.utc).isoformat(),
}

(RUN_DIR / 'protocol.json').write_text(
    json.dumps(PROTOCOL, ensure_ascii=False, indent=2),
    encoding='utf-8'
)
(RUN_DIR / 'reference_standard_S2.md').write_text(S2_REFERENCE, encoding='utf-8')
(RUN_DIR / 'analysis_questions.md').write_text(ANALYSIS_QUESTIONS, encoding='utf-8')

materials_dir = RUN_DIR / 'materials'
materials_dir.mkdir(exist_ok=True)
(materials_dir / 'procedure_k_studies.md').write_text(MATERIALS['procedure_k_studies'], encoding='utf-8')
(materials_dir / 'standards.md').write_text(MATERIALS['standards'], encoding='utf-8')
(materials_dir / 'scicomm_abstract.md').write_text(MATERIALS['scicomm_abstract'], encoding='utf-8')

print('✓ Protocol and reference materials saved.')


# ---- notebook code cell 13 ----
from openai import OpenAI
from anthropic import Anthropic
from google import genai
from google.genai import types

openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
anthropic_client = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
google_client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])


def to_jsonable(obj):
    if obj is None:
        return None
    if hasattr(obj, 'model_dump'):
        return obj.model_dump(exclude_none=True)
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    try:
        return dict(obj)
    except Exception:
        return str(obj)


def with_retry(fn, attempts=6):
    last = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:
            last = e
            if i == attempts - 1:
                raise
            wait = min(60, (2 ** i) + random.random())
            print(f'  transient error: {type(e).__name__}; retrying in {wait:.1f}s')
            time.sleep(wait)
    raise last


def run_openai(turns, model_id):
    records = []
    previous_response_id = None

    for turn_index, prompt in enumerate(turns, start=1):
        kwargs = {
            'model': model_id,
            'input': prompt,
            'max_output_tokens': 16384,
        }
        if previous_response_id is not None:
            kwargs['previous_response_id'] = previous_response_id

        resp = with_retry(lambda: openai_client.responses.create(**kwargs))
        text = (resp.output_text or '').strip()
        incomplete_details = to_jsonable(getattr(resp, 'incomplete_details', None))
        truncated = (
            getattr(resp, 'status', None) == 'incomplete'
            or (
                isinstance(incomplete_details, dict)
                and incomplete_details.get('reason') in {'max_output_tokens', 'max_tokens'}
            )
        )

        records.append({
            'turn_index': turn_index,
            'prompt': prompt,
            'response_text': text,
            'response_id': getattr(resp, 'id', None),
            'model_returned': getattr(resp, 'model', None),
            'status_or_stop_reason': getattr(resp, 'status', None),
            'incomplete_details': incomplete_details,
            'truncated': bool(truncated),
            'usage': to_jsonable(getattr(resp, 'usage', None)),
            'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        })

        previous_response_id = resp.id

    return records


def run_anthropic(turns, model_id):
    records = []
    messages = []

    for turn_index, prompt in enumerate(turns, start=1):
        messages.append({'role': 'user', 'content': prompt})

        resp = with_retry(lambda: anthropic_client.messages.create(
            model=model_id,
            max_tokens=8192,
            messages=messages,
        ))

        visible_text = '\n'.join(
            block.text for block in resp.content
            if getattr(block, 'type', None) == 'text'
        ).strip()

        truncated = getattr(resp, 'stop_reason', None) == 'max_tokens'

        records.append({
            'turn_index': turn_index,
            'prompt': prompt,
            'response_text': visible_text,
            'response_id': getattr(resp, 'id', None),
            'model_returned': getattr(resp, 'model', None),
            'status_or_stop_reason': getattr(resp, 'stop_reason', None),
            'incomplete_details': None,
            'truncated': bool(truncated),
            'usage': to_jsonable(getattr(resp, 'usage', None)),
            'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        })

        # Feed back exactly the visible assistant answer as conversation history.
        messages.append({'role': 'assistant', 'content': visible_text})

    return records


def run_google(turns, model_id):
    records = []
    chat = google_client.chats.create(
        model=model_id,
        config=types.GenerateContentConfig(max_output_tokens=8192),
    )

    for turn_index, prompt in enumerate(turns, start=1):
        resp = with_retry(lambda: chat.send_message(prompt))
        text = (getattr(resp, 'text', None) or '').strip()

        finish_reason = None
        if getattr(resp, 'candidates', None):
            finish_reason = getattr(resp.candidates[0], 'finish_reason', None)
        finish_reason_str = str(finish_reason) if finish_reason is not None else None
        truncated = (
            finish_reason_str is not None
            and ('MAX_TOKENS' in finish_reason_str.upper() or 'MAX_LENGTH' in finish_reason_str.upper())
        )

        records.append({
            'turn_index': turn_index,
            'prompt': prompt,
            'response_text': text,
            'response_id': getattr(resp, 'response_id', None),
            'model_returned': model_id,
            'status_or_stop_reason': finish_reason_str,
            'incomplete_details': None,
            'truncated': bool(truncated),
            'usage': to_jsonable(getattr(resp, 'usage_metadata', None)),
            'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        })

    return records


def run_conversation(provider_key, turns):
    model_id = MODELS[provider_key]['model_id']

    if provider_key == 'openai':
        return run_openai(turns, model_id)
    if provider_key == 'anthropic':
        return run_anthropic(turns, model_id)
    if provider_key == 'google':
        return run_google(turns, model_id)

    raise ValueError(provider_key)


# ---- notebook code cell 15 ----
connectivity = []

for provider_key, model in MODELS.items():
    print('Testing:', model['label'])
    try:
        rec = run_conversation(provider_key, ['Reply with exactly: OK'])[0]
        connectivity.append({
            'provider': provider_key,
            'model_label': model['label'],
            'model_requested': model['model_id'],
            'model_returned': rec['model_returned'],
            'response': rec['response_text'],
            'status_or_stop_reason': rec['status_or_stop_reason'],
            'truncated': rec['truncated'],
            'ok': rec['response_text'].strip() == 'OK' and not rec['truncated'],
        })
    except Exception as e:
        connectivity.append({
            'provider': provider_key,
            'model_label': model['label'],
            'model_requested': model['model_id'],
            'model_returned': None,
            'response': None,
            'status_or_stop_reason': None,
            'truncated': None,
            'ok': False,
            'error': f'{type(e).__name__}: {e}',
        })

connectivity_df = pd.DataFrame(connectivity)
connectivity_df.to_csv(RUN_DIR / 'connectivity_test.csv', index=False)
display(connectivity_df)

if not connectivity_df['ok'].all():
    raise RuntimeError('At least one provider failed the one-turn connectivity check.')

print('✓ All three one-turn calls work.')


# ---- notebook code cell 17 ----
multiturn = []

test_turns = [
    'Remember the number 7.',
    'What number did I ask you to remember? Reply with the number only.'
]

for provider_key, model in MODELS.items():
    print('Testing multi-turn:', model['label'])
    try:
        recs = run_conversation(provider_key, test_turns)
        final = recs[-1]
        answer = final['response_text'].strip()
        multiturn.append({
            'provider': provider_key,
            'model_label': model['label'],
            'model_requested': model['model_id'],
            'turn_1_response': recs[0]['response_text'],
            'turn_2_response': answer,
            'truncated': any(r['truncated'] for r in recs),
            'ok': ('7' in answer) and not any(r['truncated'] for r in recs),
        })
    except Exception as e:
        multiturn.append({
            'provider': provider_key,
            'model_label': model['label'],
            'model_requested': model['model_id'],
            'turn_1_response': None,
            'turn_2_response': None,
            'truncated': None,
            'ok': False,
            'error': f'{type(e).__name__}: {e}',
        })

multiturn_df = pd.DataFrame(multiturn)
multiturn_df.to_csv(RUN_DIR / 'multiturn_preflight.csv', index=False)
display(multiturn_df)

if not multiturn_df['ok'].all():
    raise RuntimeError('At least one provider failed the two-turn conversation preflight. Do not start the official run.')

print('✓ Conversation history works for all three providers.')


# ---- notebook code cell 19 ----
def expand(text):
    for key, value in MATERIALS.items():
        text = text.replace('{{' + key + '}}', value)
    return text


jobs = []

for provider_key, model in MODELS.items():
    for scenario in SCENARIOS:
        for repetition in range(1, scenario['repetitions'] + 1):
            for condition in scenario['conditions']:
                job_id = (
                    f"{provider_key}__{scenario['id']}__"
                    f"{condition['id']}__r{repetition}"
                )
                jobs.append({
                    'job_id': job_id,
                    'provider': provider_key,
                    'model_label': model['label'],
                    'model_id': model['model_id'],
                    'scenario_id': scenario['id'],
                    'paper_section': scenario['paper_section'],
                    'scenario_title': scenario['title'],
                    'conceptual_issue': scenario['conceptual_issue'],
                    'condition_id': condition['id'],
                    'condition_label': condition['label'],
                    'repetition': repetition,
                    'turns': [expand(t) for t in condition['turns']],
                })

job_manifest = pd.DataFrame([
    {k: v for k, v in job.items() if k != 'turns'}
    | {'n_turns': len(job['turns'])}
    for job in jobs
])

job_manifest.to_csv(RUN_DIR / 'job_manifest.csv', index=False)
display(job_manifest)

print('Official jobs:', len(jobs))
print('Official API calls:', sum(len(j['turns']) for j in jobs))

assert len(jobs) == 57
assert sum(len(j['turns']) for j in jobs) == 111


# ---- notebook code cell 21 ----
bundle_path = RUN_DIR / 'pre_run_protocol_bundle.zip'

with zipfile.ZipFile(bundle_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for path in [
        RUN_DIR / 'protocol.json',
        RUN_DIR / 'reference_standard_S2.md',
        RUN_DIR / 'analysis_questions.md',
        RUN_DIR / 'job_manifest.csv',
        RUN_DIR / 'materials' / 'procedure_k_studies.md',
        RUN_DIR / 'materials' / 'standards.md',
        RUN_DIR / 'materials' / 'scicomm_abstract.md',
    ]:
        z.write(path, arcname=path.relative_to(RUN_DIR))

print('✓ Pre-run protocol bundle created:')
print(bundle_path)


# ---- notebook code cell 23 ----
ERROR_PATH = RUN_DIR / 'errors.jsonl'


def append_jsonl(path, row):
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(row, ensure_ascii=False, default=str) + '\n')


def atomic_write_json(path, obj):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2, default=str),
        encoding='utf-8'
    )
    tmp.replace(path)


def run_and_save_attempt(job, attempt_number):
    records = run_conversation(job['provider'], job['turns'])
    attempt = {
        'job_id': job['job_id'],
        'attempt_number': attempt_number,
        'provider': job['provider'],
        'model_label': job['model_label'],
        'model_requested': job['model_id'],
        'scenario_id': job['scenario_id'],
        'paper_section': job['paper_section'],
        'scenario_title': job['scenario_title'],
        'conceptual_issue': job['conceptual_issue'],
        'condition_id': job['condition_id'],
        'condition_label': job['condition_label'],
        'repetition': job['repetition'],
        'completed_utc': datetime.now(timezone.utc).isoformat(),
        'contains_truncation': any(r['truncated'] for r in records),
        'turns': records,
    }

    attempt_path = ATTEMPT_DIR / f"{job['job_id']}__attempt{attempt_number}.json"
    atomic_write_json(attempt_path, attempt)
    return attempt


completed_before = sum(
    (JOB_DIR / f"{j['job_id']}.json").exists()
    for j in jobs
)
print(f'Already completed: {completed_before} / {len(jobs)}')

for i, job in enumerate(jobs, start=1):
    official_path = JOB_DIR / f"{job['job_id']}.json"
    if official_path.exists():
        continue

    print(
        f"[{i}/{len(jobs)}] {job['model_label']} | "
        f"{job['scenario_id']} | {job['condition_id']} | "
        f"rep {job['repetition']}"
    )

    try:
        attempt1 = run_and_save_attempt(job, 1)

        if not attempt1['contains_truncation']:
            official = attempt1 | {
                'official_attempt': 1,
                'previous_truncated_attempt': False,
            }
            atomic_write_json(official_path, official)
            print('  ✓ saved')
            time.sleep(0.5)
            continue

        print('  length cut-off detected; rerunning the entire job once...')
        attempt2 = run_and_save_attempt(job, 2)

        if not attempt2['contains_truncation']:
            official = attempt2 | {
                'official_attempt': 2,
                'previous_truncated_attempt': True,
            }
            atomic_write_json(official_path, official)
            print('  ✓ rerun completed; attempt 2 is the official output')
        else:
            append_jsonl(ERROR_PATH, {
                'job_id': job['job_id'],
                'provider': job['provider'],
                'model_label': job['model_label'],
                'scenario_id': job['scenario_id'],
                'condition_id': job['condition_id'],
                'repetition': job['repetition'],
                'timestamp_utc': datetime.now(timezone.utc).isoformat(),
                'error_type': 'RepeatedTruncation',
                'error': 'Both official attempts were cut off for length. Job not marked complete.',
            })
            print('  STOP: second attempt was also truncated; job not marked complete.')

    except Exception as e:
        append_jsonl(ERROR_PATH, {
            'job_id': job['job_id'],
            'provider': job['provider'],
            'model_label': job['model_label'],
            'scenario_id': job['scenario_id'],
            'condition_id': job['condition_id'],
            'repetition': job['repetition'],
            'timestamp_utc': datetime.now(timezone.utc).isoformat(),
            'error_type': type(e).__name__,
            'error': str(e),
        })
        print('  FAILED:', type(e).__name__, str(e)[:500])

    time.sleep(0.5)

completed_after = sum(
    (JOB_DIR / f"{j['job_id']}.json").exists()
    for j in jobs
)
print(f'\nCompleted: {completed_after} / {len(jobs)}')

if completed_after < len(jobs):
    print('Some jobs are still missing. Rerun this cell; completed jobs will be skipped.')
else:
    print('✓ ALL 57 OFFICIAL JOBS ARE COMPLETE.')


# ---- notebook code cell 25 ----
missing = [
    j['job_id'] for j in jobs
    if not (JOB_DIR / f"{j['job_id']}.json").exists()
]
if missing:
    raise RuntimeError(
        f'{len(missing)} official jobs are still missing. '
        'Rerun Cell 11 before consolidating.'
    )


def flatten_job(job_record, attempt_kind):
    rows = []
    n_turns = len(job_record['turns'])

    for tr in job_record['turns']:
        rows.append({
            'attempt_kind': attempt_kind,
            'job_id': job_record['job_id'],
            'attempt_number': job_record.get('attempt_number'),
            'official_attempt': job_record.get('official_attempt'),
            'previous_truncated_attempt': job_record.get('previous_truncated_attempt', False),
            'provider': job_record['provider'],
            'model_label': job_record['model_label'],
            'model_requested': job_record['model_requested'],
            'model_returned': tr.get('model_returned'),
            'scenario_id': job_record['scenario_id'],
            'paper_section': job_record['paper_section'],
            'scenario_title': job_record['scenario_title'],
            'conceptual_issue': job_record['conceptual_issue'],
            'condition_id': job_record['condition_id'],
            'condition_label': job_record['condition_label'],
            'repetition': job_record['repetition'],
            'turn_index': tr['turn_index'],
            'n_turns': n_turns,
            'is_final_turn': tr['turn_index'] == n_turns,
            'prompt': tr['prompt'],
            'response_text': tr['response_text'],
            'response_id': tr.get('response_id'),
            'status_or_stop_reason': tr.get('status_or_stop_reason'),
            'incomplete_details': json.dumps(tr.get('incomplete_details'), ensure_ascii=False, default=str),
            'truncated': tr.get('truncated', False),
            'usage': json.dumps(tr.get('usage'), ensure_ascii=False, default=str),
            'timestamp_utc': tr.get('timestamp_utc'),
        })
    return rows


# Every saved attempt.
attempt_rows = []
for path in sorted(ATTEMPT_DIR.glob('*.json')):
    rec = json.loads(path.read_text(encoding='utf-8'))
    attempt_rows.extend(flatten_job(rec, 'saved_attempt'))

attempt_df = pd.DataFrame(attempt_rows)
attempt_df.to_csv(RUN_DIR / 'all_attempts.csv', index=False)

with (RUN_DIR / 'raw_attempts.jsonl').open('w', encoding='utf-8') as f:
    for row in attempt_rows:
        f.write(json.dumps(row, ensure_ascii=False, default=str) + '\n')


# Official completed jobs only.
official_records = []
official_rows = []

for job in jobs:
    path = JOB_DIR / f"{job['job_id']}.json"
    rec = json.loads(path.read_text(encoding='utf-8'))
    official_records.append(rec)
    official_rows.extend(flatten_job(rec, 'official'))

official_df = pd.DataFrame(official_rows)
official_df.to_csv(RUN_DIR / 'official_turns.csv', index=False)

with (RUN_DIR / 'raw_official_turns.jsonl').open('w', encoding='utf-8') as f:
    for row in official_rows:
        f.write(json.dumps(row, ensure_ascii=False, default=str) + '\n')

final_df = official_df[official_df['is_final_turn']].copy()
final_df.to_csv(RUN_DIR / 'final_outputs.csv', index=False)

summary = (
    final_df.groupby(['model_label', 'scenario_id'], dropna=False)
    .size()
    .rename('final_outputs')
    .reset_index()
)
summary.to_csv(RUN_DIR / 'run_summary.csv', index=False)

display(summary)

print('Official final outputs:', len(final_df))
print('Official turns:', len(official_df))
print('Saved attempt turns:', len(attempt_df))

assert len(final_df) == 57
assert len(official_df) == 111
assert not official_df['truncated'].any()

print('✓ Consolidation complete; all official turns finished without length truncation.')


# ---- notebook code cell 27 ----
# S1: one row per model × repetition, with all three formulations side by side.
s1 = final_df[final_df.scenario_id == 'S1_framing'][
    ['model_label', 'repetition', 'condition_id', 'response_text']
]
s1_wide = (
    s1.pivot(
        index=['model_label', 'repetition'],
        columns='condition_id',
        values='response_text'
    )
    .reset_index()
)
s1_wide.to_csv(RUN_DIR / 'S1_framing_comparison.csv', index=False)


# S4: one row per model × repetition, neutral and steered final paragraphs side by side.
s4 = final_df[final_df.scenario_id == 'S4_provenance'][
    ['model_label', 'repetition', 'condition_id', 'response_text']
]
s4_wide = (
    s4.pivot(
        index=['model_label', 'repetition'],
        columns='condition_id',
        values='response_text'
    )
    .reset_index()
)
s4_wide.to_csv(RUN_DIR / 'S4_provenance_comparison.csv', index=False)

display(s1_wide)
display(s4_wide)

print('✓ Comparative tables saved.')


# ---- notebook code cell 29 ----
parts = [
    '# Supplementary model outputs',
    '',
    'These outputs instantiate the six manuscript scenarios with current LLMs in response to Reviewer 2.2.',
    '',
    '**Design:** S1 and S4 were repeated three times because they compare alternative formulations or interaction trajectories; S2, S3, S5 and S6 were run once per model. '
    'The repetitions are robustness checks, not a statistical sample. The runs are illustrative rather than a benchmark, prevalence estimate, or empirical validation of the proposed human competencies.',
    '',
    'No system prompt, tools, retrieval, or web search were supplied by the notebook. Provider-default reasoning/thinking behaviour was retained.',
    '',
]

scenario_order = {s['id']: i for i, s in enumerate(SCENARIOS)}
model_order = {m['label']: i for i, m in enumerate(MODELS.values())}
condition_order = {
    (s['id'], c['id']): i
    for s in SCENARIOS
    for i, c in enumerate(s['conditions'])
}

for job in sorted(
    official_records,
    key=lambda x: (
        scenario_order[x['scenario_id']],
        x['repetition'],
        condition_order[(x['scenario_id'], x['condition_id'])],
        model_order[x['model_label']]
    )
):
    parts += [
        f"## {job['scenario_id']} — {job['condition_label']} — repetition {job['repetition']}",
        '',
        f"**Model:** {job['model_label']}  ",
        f"**Requested model ID:** `{job['model_requested']}`  ",
        f"**Conceptual issue illustrated:** {job['conceptual_issue']}",
        '',
    ]

    for tr in job['turns']:
        parts += [
            f"### Turn {tr['turn_index']} — prompt",
            '',
            tr['prompt'],
            '',
            f"### Turn {tr['turn_index']} — model output",
            '',
            tr['response_text'],
            '',
        ]

    parts += ['---', '']


# If there were truncation reruns, report both attempts transparently.
truncated_attempts = []
for path in sorted(ATTEMPT_DIR.glob('*.json')):
    rec = json.loads(path.read_text(encoding='utf-8'))
    if rec.get('contains_truncation'):
        truncated_attempts.append(rec)

if truncated_attempts:
    parts += [
        '# Technical reruns after length cut-off',
        '',
        'The following first attempts were cut off for length and therefore rerun once according to the prespecified technical rule. '
        'The cut-off attempts are preserved here for transparency but were not used as the official outputs.',
        '',
    ]

    for rec in truncated_attempts:
        parts += [
            f"## {rec['job_id']} — truncated attempt {rec['attempt_number']}",
            '',
        ]
        for tr in rec['turns']:
            parts += [
                f"### Turn {tr['turn_index']} — prompt",
                '',
                tr['prompt'],
                '',
                f"### Turn {tr['turn_index']} — truncated model output",
                '',
                tr['response_text'],
                '',
                f"**Stop/status:** {tr.get('status_or_stop_reason')}",
                '',
            ]
        parts += ['---', '']

supp_path = RUN_DIR / 'supplement_model_outputs.md'
supp_path.write_text('\n'.join(parts), encoding='utf-8')

print('✓ Supplement written to:')
print(supp_path)


# ---- notebook code cell 31 ----
README = f'''# Reviewer 2.2 illustrative model runs — revised design

Folder: {RUN_DIR}

## Purpose
To instantiate the six manuscript scenarios with real outputs from three current LLMs. These runs are not a benchmark, prevalence study, or empirical validation of the four human interpretive competencies.

## Models
- GPT-6.1 Sol (`gpt-6.1-sol`)
- Claude Sonnet 5.5 (`claude-sonnet-5-5`)
- Gemini 3.8 Flash (`gemini-3.8-flash`)

## Design
- S1: 3 conditions × 3 repetitions × 3 models
- S2: 1 condition × 1 run × 3 models
- S3: 1 condition × 1 run × 3 models
- S4: 2 conditions × 3 repetitions × 3 models
- S5: 1 condition × 1 run × 3 models
- S6: 1 condition × 1 run × 3 models

Total: 57 final outputs and 111 official API calls.

The S1/S4 repetitions are robustness checks only. No inferential statistics or model scores are used.

## Main files
- `protocol.json` — exact design, prompts and technical rules
- `pre_run_protocol_bundle.zip` — protocol snapshot created before the official calls
- `materials/` — constructed source materials
- `reference_standard_S2.md` — clinical reference for descriptive comparison of S2
- `analysis_questions.md` — scenario-specific descriptive questions
- `connectivity_test.csv` — one-turn technical API check
- `multiturn_preflight.csv` — two-turn conversation-history test
- `job_manifest.csv` — the 57 planned official jobs
- `attempts/` — every completed API attempt, including any length-truncated attempt
- `completed_jobs/` — one completed official JSON record per job
- `all_attempts.csv` / `raw_attempts.jsonl` — all saved attempts
- `official_turns.csv` / `raw_official_turns.jsonl` — 111 official turns
- `final_outputs.csv` — the 57 final-turn outputs
- `run_summary.csv` — completion counts
- `S1_framing_comparison.csv` — three S1 formulations side by side by model/repetition
- `S4_provenance_comparison.csv` — neutral/steered S4 finals side by side by model/repetition
- `supplement_model_outputs.md` — all official prompts and outputs verbatim
- `errors.jsonl` — technical failures if any

No human ratings, coding scores, kappa statistics, inferential tests, or model leaderboard are produced.
'''

(RUN_DIR / 'README.md').write_text(README, encoding='utf-8')
print(README)
print('\n✓ Everything has been saved in MyDrive.')

