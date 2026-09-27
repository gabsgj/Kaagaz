"""
Kaagaz — pre-researched seed set.

These entries are REAL researched answers, not placeholders and not invented
figures. They were compiled by researching each case against primary sources —
bank product pages, RBI directions, and state registration department sites —
during the build, and they carry the URLs that were actually read.

Why they exist: a live research call takes 15-40 seconds and depends on a
search provider being up. A recorded demo cannot afford either. These rows are
the pre-warmed cache so the demo hits the fast path.

They are flagged `is_seed = 1` in the database and labelled as pre-researched
in the UI, so the app never implies they were fetched on demand.

Accuracy rules applied throughout this file (see .aimem/decisions.md):
  - Stamp duty and registration fees are NEVER attributed to the RBI.
  - Interest rates are always bands, never single numbers.
  - Anything not published is written as an explicit "not disclosed" rather
    than estimated.
  - The exact research query is recorded on every row.
"""

# Reusable primary sources across entries.
SBI_HL_DOCS = "https://homeloans.sbi.bank.in/products/view/regular-home-loan"
SBI_NRI_HL = "https://homeloans.sbi.bank.in/products/view/nri-home-loan"
SBI_HL_FAQ = "https://homeloans.sbi.bank.in/faq"
SBI_RATES = ("https://sbi.bank.in/web/interest-rates/interest-rates/"
             "loan-schemes-interest-rates/home-loans-interest-rates-current")
HDFC_HL_DOCS = "https://homeloans.hdfc.bank.in/checklist/documents-charges"
HDFC_HL_MAIN = "https://homeloans.hdfc.bank.in/housing-loans/home-loans"
HDFC_HL_RATES = "https://homeloans.hdfc.bank.in/checklist/home-loan-interest-rates"
SBI_EDU = "https://sbi.bank.in/web/personal-banking/loans/education-loans/student-loan-scheme"
SBI_EDV = ("https://sbi.bank.in/web/personal-banking/loans/education-loans/"
           "global-ed-vantage-scheme")
SBI_EDU_MITC = ("https://sbi.bank.in/documents/16012/49127069/"
                "MITC-Student+Loan+-+Nov%272024.pdf/e9519b55-b254-5560-50c3-152353c5d8f1")
SBI_LAFD = "https://sbi.bank.in/web/yono/loan-against-fixed-deposit"
SBI_LAFD_TD = ("https://sbi.bank.in/web/personal-banking/loans/loans-against-securities/"
               "loan-against-time-deposit")
SBI_LAS_RATES = ("https://sbi.bank.in/web/interest-rates/interest-rates/"
                 "loan-schemes-interest-rates/"
                 "loan-against-securities-and-consumer-durable-loans")
AXIS_LAFD = "https://www.axis.bank.in/loans/loan-against-fixed-deposit"
AXIS_LAFD_OD = "https://www.axis.bank.in/loans/24x7-instant-loan/24x7-overdraft-against-fixed-deposit"
SBI_NRE_NRO = "https://sbi.bank.in/web/nri/quick-links/nre-nro-account-opening-procedure"
KOTAK_NRI = ("https://www.kotak.bank.in/en/personal-banking/nri/accounts-deposits/"
             "current-account/nro-rupee-current-account/rupee-current-account/documentation.html")
HDFC_FEMA = ("https://www.hdfcbank.com/content/bbp/repositories/723fb80a-2dde-42a3-9793-7ae1be57c87f/"
             "?path=%2FFooter%2FResource%2FForms+Centre%2FContent%2FDetail+Page%2FForms+Center+-+NRI%2F"
             "SERVICE+RELATED+FORMS+Links%2FFEMA_Declaration.pdf")
KL_STAMP = "https://registration.kerala.gov.in/wp-content/uploads/2022/07/Stamp-Duty-Fees-Ready-reckoner-2023.xlsx-Table-1.pdf"
KL_SOP = "https://pearl.registration.kerala.gov.in/downloads/SOP_Regn_2024.pdf"
KL_FLOW = "https://registration.kerala.gov.in/wp-content/uploads/2021/03/Process_Flow_Registration.pdf"
ICICI_CA = "https://www.icici.bank.in/business-banking/accounts/current-account/documentation"
KOTAK_CA = "https://www.kotak.bank.in/en/business/accounts/current-accounts/required-documents.html"
SBI_GOLD_FORM = ("https://sbi.bank.in/documents/53471/263971/"
                 "Gold+Loan+Application-English.pdf/03234859-7238-8808-eacd-dbd90625e753")
RBI_GOLD = "https://ibjarates.com/pdf/RBI-Notification/New-Gold-Loan-Regulations.pdf"
MUDRA = "https://projectreportbank.com/mudra-loan-documents-required/"


def _src(*pairs):
    return [{"url": u, "title": t} for t, u in pairs]


SEED_ENTRIES = [
    # ══════════════════════════════════════════════════════════════════
    # 1. Home loan — HDFC Bank, resident applicant
    # ══════════════════════════════════════════════════════════════════
    {
        "transaction_type": "home loan",
        "bank": "HDFC Bank",
        "residency": "resident",
        "state": "",
        "summary": (
            "An HDFC Bank home loan needs three separate bundles: KYC (identity and "
            "address), income proof, and property title documents. Property documents "
            "are the ones that cause delays — the bank wants an unbroken chain of "
            "title, not just the latest deed. HDFC benchmarks its rate to the Policy "
            "Repo Rate, so your actual rate sits somewhere inside a wide published "
            "band and depends on your credit score, not on what is advertised."
        ),
        "interest_rate_range": "7.75% - 13.20% p.a. (Policy Repo Rate + 2.50% to 7.95%)",
        "processing_fee_note": (
            "Up to 0.50% of the loan amount or ₹4,000, whichever is higher, plus "
            "applicable taxes, for salaried and self-employed professionals. Up to "
            "1.50% or ₹5,000 for self-employed non-professionals. Non-refundable."
        ),
        "regulatory_note": (
            "The RBI governs the KYC, income-assessment norms and the benchmark "
            "linking your rate to the Repo Rate. HDFC's own credit policy sets the "
            "documentation depth, the LTV and the fee schedule. Stamp duty and "
            "registration charges on the property are set by the state and are "
            "charged at actual — they are not an HDFC or RBI charge."
        ),
        "disclosures": [
            "Stamp duty and registration charges are levied by the state government "
            "and vary by state and property value; HDFC charges these at actual cost.",
            "HDFC publishes a minimum rate rather than a customer-specific rate. "
            "The rate you are offered depends on your credit score and profile.",
        ],
        "items": [
            {
                "document_name": "Completed home loan application form",
                "plain_explanation": "HDFC's own application form, signed by every applicant and co-applicant, with passport-size photographs affixed and signed across.",
                "where_to_obtain": "homeloans.hdfc.bank.in — apply online, or any HDFC Bank branch",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "HDFC Bank home loan documents checklist",
            },
            {
                "document_name": "PAN card, or Form 60 if you have no PAN",
                "plain_explanation": "PAN is mandatory for every applicant. If you genuinely do not have one, Form 60 is the substitute declaration.",
                "where_to_obtain": "Income Tax Department, or Form 60 from the HDFC branch",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "Completed home loan application form",
                "source_note": "HDFC KYC table, row A",
            },
            {
                "document_name": "Officially Valid Document for identity and address",
                "plain_explanation": "One OVD serves as both identity and address proof: unexpired passport, driving licence, voter ID, NREGA job card, NPR letter, or voluntary Aadhaar.",
                "where_to_obtain": "As applicable — passport from your embassy/consulate, licence/Voter ID from the state",
                "approx_cost_min": 0, "approx_cost_max": 500, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "PAN card, or Form 60 if you have no PAN",
                "source_note": "HDFC KYC table, officially valid documents",
            },
            {
                "document_name": "Last 3 months' salary slips",
                "plain_explanation": "Proves your current take-home. HDFC wants three consecutive months, not one.",
                "where_to_obtain": "Your employer's HR department",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "HDFC income proof table, salaried",
            },
            {
                "document_name": "Last 6 months' bank statements showing salary credits",
                "plain_explanation": "HDFC traces your salary credits to match them against the slips. This is where loan officers catch inconsistencies.",
                "where_to_obtain": "Your bank — net banking or a branch statement request",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "bank_internal", "depends_on": "Last 3 months' salary slips",
                "source_note": "HDFC income proof table, salaried",
            },
            {
                "document_name": "Latest Form 16 and acknowledged ITR",
                "plain_explanation": "Your tax return for the last assessment year, cross-checked against your declared income.",
                "where_to_obtain": "incometax.gov.in — download or verify your return",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "HDFC income proof table, salaried",
            },
            {
                "document_name": "Allotment letter or buyer agreement",
                "plain_explanation": "Your contract with the builder or seller. For resale, HDFC instead wants the title deeds covering the previous chain of ownership.",
                "where_to_obtain": "From the builder or the seller",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "HDFC property documents",
            },
            {
                "document_name": "Title deeds with unbroken previous chain",
                "plain_explanation": "For resale or construction, the full chain of title back to the original grant. A gap here is the single most common reason a home loan stalls.",
                "where_to_obtain": "Sub-registrar office where each deed was registered",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 7,
                "regulatory_source": "registrar", "depends_on": "Allotment letter or buyer agreement",
                "source_note": "HDFC property documents, resale homes",
            },
            {
                "document_name": "Encumbrance certificate for the property",
                "plain_explanation": "Proves nobody else has already mortgaged or claimed a charge over the property. Without it HDFC cannot legally lend against it.",
                "where_to_obtain": "State registration department — apply online via the state portal",
                "approx_cost_min": 500, "approx_cost_max": 2500, "approx_time_days": 7,
                "regulatory_source": "registrar", "depends_on": "Title deeds with unbroken previous chain",
                "source_note": "HDFC property documents, construction",
            },
            {
                "document_name": "Receipts for payments made to seller or builder",
                "plain_explanation": "Bank statements or receipts proving your down payment. The loan is only the balance, so this proves you have already funded your share.",
                "where_to_obtain": "Your own bank statements and the builder/seller's receipts",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "HDFC property documents",
            },
            {
                "document_name": "Proof of your own contribution",
                "plain_explanation": "Evidence of the margin you are bringing in — usually 10-20% of the property value depending on your LTV band.",
                "where_to_obtain": "Your bank statements",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "HDFC other documents list",
            },
            {
                "document_name": "Passport-size photographs, all applicants",
                "plain_explanation": "Affixed to the application form and signed across by each applicant and co-applicant.",
                "where_to_obtain": "Any photo studio",
                "approx_cost_min": 100, "approx_cost_max": 300, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "Completed home loan application form",
                "source_note": "HDFC other documents list",
            },
            {
                "document_name": "Cheque for the processing fee",
                "plain_explanation": "Payable to HDFC Bank. The fee is non-refundable, so the loan must be sanctioned before you pay it.",
                "where_to_obtain": "Your bank, after the bank quotes you the sanction terms",
                "approx_cost_min": 4000, "approx_cost_max": 4000, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "Completed home loan application form",
                "source_note": "HDFC home loan charges table",
            },
            {
                "document_name": "Cheque dishonour charge schedule (for your reference)",
                "plain_explanation": "HDFC publishes its full incidental charge schedule. A dishonoured cheque is ₹300; duplicate document lists and photocopies are up to ₹500 each. Read this before you commit.",
                "where_to_obtain": "homeloans.hdfc.bank.in/checklist/documents-charges",
                "approx_cost_min": 300, "approx_cost_max": 2000, "approx_time_days": 0,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "HDFC other charges table",
            },
        ],
        "sources": _src(
            ("HDFC Bank — Home Loan Required Documents, Charges, Processing Fee 2026", HDFC_HL_DOCS),
            ("HDFC Bank — Home Loan product page and rate table", HDFC_HL_MAIN),
            ("HDFC Bank — Home Loan Interest Rate", HDFC_HL_RATES),
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # 2. Home loan — SBI, NRI applicant
    # ══════════════════════════════════════════════════════════════════
    {
        "transaction_type": "home loan",
        "bank": "State Bank of India",
        "residency": "nri",
        "state": "",
        "summary": (
            "SBI's NRI home loan differs from the resident version in three specific "
            "places: a valid work permit, an employment contract that is attested if "
            "it is not in English, and six months of overseas bank statements instead "
            "of Indian ones. The Indian income-tax return requirement is waived if you "
            "are resident in a Middle East country or work in the Merchant Navy. The "
            "property papers themselves are the same as for a resident borrower."
        ),
        "interest_rate_range": "8.70% - 11.60% p.a. (repo-linked, EBLR framework)",
        "processing_fee_note": (
            "Not published as a fixed rupee figure on the product page — SBI states "
            "a low processing fee with no hidden charges. Ask your branch for the "
            "current amount before sanction, as it is not disclosed online."
        ),
        "regulatory_note": (
            "The RBI governs FEMA compliance for NRI lending, the KYC norms and the "
            "external-benchmark rate linking. The work permit and the attestation "
            "requirements are SBI's own policy. Stamp duty and registration on the "
            "property remain a state subject, charged at actual."
        ),
        "disclosures": [
            "SBI does not publish a specific processing fee amount for NRI home "
            "loans — contact the branch directly for the current figure.",
            "Attestation requirements for a non-English employment contract vary by "
            "SBI's foreign office; confirm which attestation the branch will accept.",
        ],
        "items": [
            {
                "document_name": "Valid work permit",
                "plain_explanation": "Proves you are legally employed and resident in your country of residence. This is the document an NRI applicant most often does not have ready.",
                "where_to_obtain": "From your employer or the immigration authority of your country of residence",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "SBI NRI home loan, income proof for salaried",
            },
            {
                "document_name": "Employment contract, attested if not in English",
                "plain_explanation": "Must be an English translation, attested by your employer, the consulate, an SBI foreign office, or the embassy. An unattested foreign-language contract is routinely rejected.",
                "where_to_obtain": "Your employer; attestation from the Indian consulate or embassy in your country",
                "approx_cost_min": 0, "approx_cost_max": 5000, "approx_time_days": 7,
                "regulatory_source": "bank_internal", "depends_on": "Valid work permit",
                "source_note": "SBI NRI home loan, income proof for salaried",
            },
            {
                "document_name": "Last 3 months' salary certificate or slips",
                "plain_explanation": "Current income evidence, required in original plus a copy of your employer-issued identity card.",
                "where_to_obtain": "Your employer's HR department",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "Valid work permit",
                "source_note": "SBI NRI home loan, income proof for salaried",
            },
            {
                "document_name": "Last 6 months' overseas bank statement",
                "plain_explanation": "Must show salary credit and savings. This replaces the Indian bank statement an SBI resident applicant would submit.",
                "where_to_obtain": "Your overseas bank — a branch in your country of residence",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "Last 3 months' salary certificate or slips",
                "source_note": "SBI NRI home loan, account statement",
            },
            {
                "document_name": "Individual tax return acknowledgement — with a stated exemption",
                "plain_explanation": "Normally the last year's Indian return is required. SBI explicitly exempts NRIs and PIOs located in Middle East countries and Merchant Navy employees from this.",
                "where_to_obtain": "incometax.gov.in, if you are not in the exempt category",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "SBI NRI home loan, income proof for salaried",
            },
            {
                "document_name": "Passport and valid visa",
                "plain_explanation": "Your passport is the primary identity document for an NRI applicant; the visa or residence permit proves current residency.",
                "where_to_obtain": "As held; renew through your embassy if expiring",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "SBI NRI home loan, KYC",
            },
            {
                "document_name": "Property title documents",
                "plain_explanation": "The same title chain, allotment letter, occupancy certificate and payment receipts an Indian resident applicant submits. Residency does not change what the property must prove.",
                "where_to_obtain": "Builder/seller, plus the sub-registrar for prior title deeds",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 7,
                "regulatory_source": "registrar", "depends_on": "Passport and valid visa",
                "source_note": "SBI home loan, property papers",
            },
            {
                "document_name": "NRI-specific address and communication proof",
                "plain_explanation": "If your address has changed, SBI asks for a fresh address proof. Overseas address proof may need attestation depending on the branch.",
                "where_to_obtain": "Utility bill or lease from your country of residence",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "Passport and valid visa",
                "source_note": "SBI home loan FAQ, KYC-compliant accounts",
            },
            {
                "document_name": "Passport-size photographs, all applicants",
                "plain_explanation": "Affixed to the application and signed across by each applicant.",
                "where_to_obtain": "Any photo studio in your country of residence",
                "approx_cost_min": 100, "approx_cost_max": 300, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "SBI home loan, application form",
            },
            {
                "document_name": "Processing fee payment — amount not published",
                "plain_explanation": "SBI advertises a low processing fee but does not publish the amount for NRI home loans. Get it in writing from the branch before you commit to the property.",
                "where_to_obtain": "SBI branch, or SBI's overseas foreign office",
                "approx_cost_min": None, "approx_cost_max": None, "approx_time_days": None,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "SBI NRI home loan, features — fee amount not disclosed",
            },
        ],
        "sources": _src(
            ("SBI — NRI Home Loan, documents required", SBI_NRI_HL),
            ("SBI Home Loan FAQ", SBI_HL_FAQ),
            ("SBI — Home Loans Interest Rates (current)", SBI_RATES),
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # 3. Education loan — SBI, all-NRI household, study abroad
    # ══════════════════════════════════════════════════════════════════
    {
        "transaction_type": "education loan (study abroad)",
        "bank": "State Bank of India",
        "residency": "all_nri",
        "state": "",
        "summary": (
            "For a study-abroad loan, the passport is the document that changes "
            "everything: SBI mandates it explicitly for studies abroad. The loan "
            "structure depends on amount — up to ₹7.50 lakh needs only a parent or "
            "guardian as co-obligant with no security, while above ₹7.50 lakh "
            "collateral is required and the ceiling under Global Ed-Vantage rises to "
            "₹3 crore. Sanction can happen before you receive your student visa, which "
            "is the reason banks advertise this product to overseas students."
        ),
        "interest_rate_range": "Not publicly disclosed as a band on the product page — SBI prices education loans off MCLR. Contact the branch for the current band.",
        "processing_fee_note": (
            "Not published on the product page. Ask your branch; no amount is "
            "disclosed online for education loans."
        ),
        "regulatory_note": (
            "The RBI governs the KYC, the education-loan sanction norms and the "
            "repayment restructuring rules. The security threshold at ₹7.50 lakh and "
            "the requirement for insurance above that amount are SBI's own policy. "
            "There is no state stamp-act component in an education loan at all."
        ),
        "disclosures": [
            "SBI does not publish a specific interest-rate band or processing fee for "
            "education loans on the product page — both are branch-specific.",
            "The ₹7.50 lakh security threshold and the ₹3 crore Global Ed-Vantage "
            "ceiling are SBI scheme limits and are subject to change.",
        ],
        "items": [
            {
                "document_name": "Passport — mandatory for studies abroad",
                "plain_explanation": "SBI requires the passport specifically for study-abroad cases, separate from ordinary KYC. This is non-negotiable and cannot be substituted with a visa alone.",
                "where_to_obtain": "Passport Seva Kendra, or your embassy/consulate if issued abroad",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "SBI education loan checklist, KYC row",
            },
            {
                "document_name": "Proof of admission or offer letter",
                "plain_explanation": "An offer letter or admission letter from the institution. A conditional admission letter is acceptable for study-abroad cases.",
                "where_to_obtain": "From your university",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "bank_internal", "depends_on": "Passport — mandatory for studies abroad",
                "source_note": "SBI education loan checklist, student academic details",
            },
            {
                "document_name": "10th, 12th and graduation mark sheets",
                "plain_explanation": "Semester-wise marksheets for graduation where applicable. Academic history is how SBI checks course eligibility.",
                "where_to_obtain": "Your previous institutions",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "SBI student loan scheme, academic records",
            },
            {
                "document_name": "Entrance exam result (GRE, IELTS, TOEFL, CAT, etc.)",
                "plain_explanation": "The score through which admission was obtained. For overseas study this is often the primary academic credential SBI reviews.",
                "where_to_obtain": "From the examining body",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "bank_internal", "depends_on": "10th, 12th and graduation mark sheets",
                "source_note": "SBI student loan scheme, entrance exam result",
            },
            {
                "document_name": "Course cost schedule / statement of expenses",
                "plain_explanation": "A breakdown of tuition, living and travel costs. The loan amount sanctioned is tied to this schedule, so gaps in it reduce your sanctioned amount.",
                "where_to_obtain": "From the university, or prepared by you with their fee structure",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "bank_internal", "depends_on": "Proof of admission or offer letter",
                "source_note": "SBI education loan checklist, schedule of expenses",
            },
            {
                "document_name": "Gap certificate, if applicable",
                "plain_explanation": "Explains any break in your academic record. Required where there is a gap between finishing one course and starting the next.",
                "where_to_obtain": "From your previous institution or a medical authority, as applicable",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "SBI education loan checklist, gap certificate",
            },
            {
                "document_name": "Scholarship or freeship letters, if any",
                "plain_explanation": "Reduces the amount you need to borrow. SBI deducts confirmed scholarship from the sanctioned amount.",
                "where_to_obtain": "From the institution awarding it",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "bank_internal", "depends_on": "Course cost schedule / statement of expenses",
                "source_note": "SBI education loan checklist, scholarship letters",
            },
            {
                "document_name": "Co-applicant or guarantor KYC and income proof",
                "plain_explanation": "Mandatory co-obligation of a parent or guardian, whether or not the loan exceeds ₹7.50 lakh. Salary slip or Form 16 for a salaried guarantor.",
                "where_to_obtain": "Guarantor's employer and income tax portal",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "Proof of admission or offer letter",
                "source_note": "SBI MITC Student Loan, security and co-obligator clauses",
            },
            {
                "document_name": "Last 6 months' bank statements — all applicants",
                "plain_explanation": "For every bank account held by the applicant, the student and the co-applicant.",
                "where_to_obtain": "Your bank",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "SBI education loan checklist, account statement",
            },
            {
                "document_name": "Asset-liability statement — if loan exceeds ₹7.50 lakh",
                "plain_explanation": "Required above ₹7.50 lakh for the applicant, co-applicant or guarantor. This is the threshold at which security becomes mandatory.",
                "where_to_obtain": "Prepared by you on SBI's format",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "Co-applicant or guarantor KYC and income proof",
                "source_note": "SBI education loan checklist, forms",
            },
            {
                "document_name": "Security documents if loan exceeds ₹7.50 lakh",
                "plain_explanation": "Immovable security (title deeds, sale deed) or movable security such as a bank deposit, LIC policy, PSU bonds or mutual funds. Third-party collateral is accepted.",
                "where_to_obtain": "Sub-registrar for property; the issuing institution for deposits or policies",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 7,
                "regulatory_source": "bank_internal", "depends_on": "Asset-liability statement — if loan exceeds ₹7.50 lakh",
                "source_note": "SBI MITC Student Loan, security clause",
            },
            {
                "document_name": "Insurance policy for loans above ₹7.50 lakh",
                "plain_explanation": "SBI requires the borrower to obtain insurance for any loan above ₹7.50 lakh. This is an SBI requirement on top of the security.",
                "where_to_obtain": "Any insurer; SBI Life products are accepted",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "Security documents if loan exceeds ₹7.50 lakh",
                "source_note": "SBI student loan scheme, terms",
            },
            {
                "document_name": "Previous loan account statement, if any",
                "plain_explanation": "One year of statements for any earlier loan from another bank or lender, so SBI can assess your existing obligations.",
                "where_to_obtain": "The lending bank",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "SBI student loan scheme, previous loan",
            },
        ],
        "sources": _src(
            ("SBI — Student Loan Scheme, document checklist", SBI_EDU),
            ("SBI — Global Ed-Vantage Scheme (studies abroad)", SBI_EDV),
            ("SBI — MITC Student Loan Terms and Conditions (Nov 2024)", SBI_EDU_MITC),
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # 4. Loan against FD — SBI (the contrast case for #5)
    # ══════════════════════════════════════════════════════════════════
    {
        "transaction_type": "loan against fixed deposit",
        "bank": "State Bank of India",
        "residency": "resident",
        "state": "",
        "summary": (
            "A loan against your own fixed deposit is the lightest borrowing in Indian "
            "banking: the deposit itself is the security, so the bank takes a lien and "
            "you keep earning interest on it. You can borrow up to 90% of the deposit "
            "value, and SBI charges exactly 1% above the rate your deposit earns — so "
            "the rate is quoted as a spread, not a fixed percentage. Applied for online "
            "through YONO it is an overdraft only, with zero processing charge. The "
            "critical distinction: your FD stays pledged and is yours again once you "
            "repay."
        ),
        "interest_rate_range": "Deposit rate + 1.00% to 2.90% (1.00% over the deposit rate for TDR/STDR; 2.90% over 1-year MCLR for FCNR(B))",
        "processing_fee_note": (
            "Zero processing charge and no prepayment penalty when the loan against "
            "FD is taken through YONO as an overdraft. Branch-channel pricing is not "
            "published — confirm with the branch."
        ),
        "regulatory_note": (
            "The RBI governs the LTV and margin norms for loans against securities and "
            "the KYC framework. The 1% spread and the 90% ceiling are SBI's own "
            "product terms. There is no state stamp-act component — your deposit is "
            "never registered, only pledged."
        ),
        "disclosures": [
            "The rate is quoted as a spread over your deposit rate, so the final "
            "number depends on which deposit slab your FD sits in.",
            "YONO offers overdraft only; a term loan against FD must be requested at a branch.",
        ],
        "items": [
            {
                "document_name": "Your fixed deposit or TDR receipt",
                "plain_explanation": "The deposit itself is the security. You do not surrender it — the bank records a lien over it while the loan runs.",
                "where_to_obtain": "Your own SBI deposit account",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 0,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "SBI YONO loan against fixed deposit",
            },
            {
                "document_name": "Identity and address proof (KYC)",
                "plain_explanation": "Standard OVD. If you already hold a KYC-compliant SBI account, no fresh KYC document is required.",
                "where_to_obtain": "Passport, licence, Voter ID or Aadhaar",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "SBI home loan FAQ, KYC treatment",
            },
            {
                "document_name": "PAN card",
                "plain_explanation": "Required if not already recorded in SBI's system. A Form 60 is the substitute if you have no PAN.",
                "where_to_obtain": "Income Tax Department",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "SBI KYC treatment for compliant accounts",
            },
            {
                "document_name": "Passport-size photograph",
                "plain_explanation": "Required for the loan record where your KYC on file is not current or a photo is not held.",
                "where_to_obtain": "Any photo studio",
                "approx_cost_min": 100, "approx_cost_max": 200, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "Identity and address proof (KYC)",
                "source_note": "SBI YONO loan against fixed deposit",
            },
            {
                "document_name": "Loan agreement — lien acknowledgement over the deposit",
                "plain_explanation": "The agreement that creates the bank's lien on your deposit and sets the margin and the repayment terms. You keep receiving interest on the deposit throughout.",
                "where_to_obtain": "SBI branch, or accepted digitally through YONO",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "Your fixed deposit or TDR receipt",
                "source_note": "SBI loan against time deposit, security",
            },
            {
                "document_name": "Processing fee cheque — nil for the YONO overdraft route",
                "plain_explanation": "The YONO overdraft against a fixed deposit carries zero processing charge and no prepayment penalty, so no cheque is needed on that route.",
                "where_to_obtain": "Not applicable on the YONO overdraft route",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 0,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "SBI YONO loan against fixed deposit, features",
            },
        ],
        "sources": _src(
            ("SBI — Loan Against Fixed Deposit (YONO)", SBI_LAFD),
            ("SBI — Loan Against Time Deposit", SBI_LAFD_TD),
            ("SBI — Loans Against Securities: rate of interest", SBI_LAS_RATES),
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # 5. FD as guarantee — the contrast case (Section 2 / README)
    # ══════════════════════════════════════════════════════════════════
    {
        "transaction_type": "FD as guarantee (term deposit as third-party security)",
        "bank": "State Bank of India",
        "residency": "resident",
        "state": "",
        "summary": (
            "This is NOT the same product as a loan against FD, and the confusion "
            "costs people money. With a loan against your FD, the FD is the only "
            "security and you receive cash. With an FD used as a guarantee, somebody "
            "else's loan is being secured by your deposit, and you get nothing — you "
            "are standing as a third-party guarantor. The danger is asymmetric: if the "
            "borrower defaults, the bank liquidates your deposit, and until it does, "
            "you carry the risk with no benefit. The FD-as-guarantee route also "
            "requires third-party security consent, which is why SBI's education loan "
            "terms specify that third-party collateral is only accepted in defined "
            "circumstances."
        ),
        "interest_rate_range": (
            "Not applicable — you are not borrowing. The relevant rate is the rate on "
            "the loan you are guaranteeing, which the borrower pays, not you."
        ),
        "processing_fee_note": (
            "No fee to you as guarantor. Be aware that if the guarantee is invoked, "
            "the bank may deduct its recovery and legal costs from the deposit."
        ),
        "regulatory_note": (
            "The RBI governs KYC and the general norms on third-party guarantees. "
            "The requirement for a guarantor to give independent consent, and the "
            "circumstances in which a bank may accept third-party security, are "
            "set by the bank's own credit policy. No state stamp duty arises, because "
            "a deposit pledge is not a registered instrument."
        ),
        "disclosures": [
            "If you are being asked to use your FD as a guarantee for someone else's "
            "loan, obtain written legal advice before signing. The risk is entirely "
            "one-sided.",
            "Banks are not obliged to accept third-party security; SBI's education "
            "loan terms accept it only in specified cases.",
        ],
        "items": [
            {
                "document_name": "Your fixed deposit passbook or deposit receipt",
                "plain_explanation": "The deposit being pledged. The bank records a lien or assignment over it as security for someone else's loan.",
                "where_to_obtain": "Your own deposit account",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 0,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "SBI education loan, movable security — bank deposit",
            },
            {
                "document_name": "Independent written consent to pledge",
                "plain_explanation": "The single most important document. Your consent must be independent and informed. Do not sign a pre-executed blank pledge — read every page.",
                "where_to_obtain": "Prepared by the lending bank; you sign it personally",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "Your fixed deposit passbook or deposit receipt",
                "source_note": "SBI MITC Student Loan, third-party security clause",
            },
            {
                "document_name": "Your KYC — identity and address proof",
                "plain_explanation": "As a third party to the loan you are subject to the same KYC standards as the primary borrower.",
                "where_to_obtain": "Passport, licence, Voter ID or Aadhaar",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "RBI KYC Directions, applied to third parties",
            },
            {
                "document_name": "Declaration that the deposit is not already pledged",
                "plain_explanation": "Confirms the deposit is unencumbered. A deposit already pledged elsewhere cannot be pledged again.",
                "where_to_obtain": "You declare it on the bank's format",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "Your fixed deposit passbook or deposit receipt",
                "source_note": "SBI education loan, movable security",
            },
            {
                "document_name": "Bank's written terms of the guarantee",
                "plain_explanation": "Sets out what happens on default: the order in which the deposit is liquidated, your notice rights, and the shortfall you would owe if the deposit does not cover the loan.",
                "where_to_obtain": "From the lending bank, in writing, before you sign",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "bank_internal", "depends_on": "Independent written consent to pledge",
                "source_note": "Bank credit policy on third-party security",
            },
        ],
        "sources": _src(
            ("SBI — Student Loan Scheme, movable security including bank deposits", SBI_EDU),
            ("SBI — MITC Student Loan, third-party collateral terms", SBI_EDU_MITC),
            ("SBI — Loan Against Fixed Deposit, for contrast", SBI_LAFD),
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # 6. NRI account opening — SBI
    # ══════════════════════════════════════════════════════════════════
    {
        "transaction_type": "nri account",
        "bank": "State Bank of India",
        "residency": "nri",
        "state": "",
        "summary": (
            "Opening an NRE or NRO account has one non-obvious trap: if you already "
            "hold a Resident Indian domestic account with the same bank, it must be "
            "converted to NRO or closed first, because an NRI cannot maintain a "
            "domestic account. Second, applications that arrive by email cannot be "
            "acted upon — documents must be posted or couriered, or submitted in "
            "person. Third, if you are opening while still abroad, self-attested "
            "copies need attestation by an overseas bank official, a notary, a court "
            "magistrate, or the Indian embassy."
        ),
        "interest_rate_range": (
            "Savings account rates are published on SBI's NRE/NRO rate pages and "
            "change periodically — check the current published rate at the time of "
            "application."
        ),
        "processing_fee_note": (
            "Not published on the account-opening procedure page. Account opening "
            "fees vary by channel — confirm with the branch or SBI's Global NRI "
            "Centre."
        ),
        "regulatory_note": (
            "This is one of the few transactions where the RBI is genuinely the whole "
            "story: FEMA and the RBI's Master Direction on NRI accounts govern what "
            "NRE and NRO balances may be used for and how much may be repatriated. "
            "There is no state component whatsoever."
        ),
        "disclosures": [
            "SBI states that account-opening applications received by email cannot be "
            "acted upon for security reasons.",
            "An existing domestic account must be converted to NRO or closed before a "
            "new NRE/NRO account is opened.",
        ],
        "items": [
            {
                "document_name": "NRI account opening application form",
                "plain_explanation": "SBI's own NRI account opening form, filled in BLOCK letters. It is the same form whether you submit it in India or from abroad.",
                "where_to_obtain": "sbi.bank.in NRI quick links, or any SBI branch",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "SBI NRE/NRO account opening procedure",
            },
            {
                "document_name": "Passport — copies of the relevant pages",
                "plain_explanation": "The pages showing your name, photograph, date and place of birth, specimen signature, date of issue and expiry, and address.",
                "where_to_obtain": "Held by you; certified copies from your embassy if issued abroad",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "rbi", "depends_on": "NRI account opening application form",
                "source_note": "SBI NRE/NRO account opening procedure; Kotak NRI documentation",
            },
            {
                "document_name": "Valid visa, work permit or residence permit",
                "plain_explanation": "Proves your current lawful stay outside India. Required in addition to the passport, not instead of it.",
                "where_to_obtain": "From the immigration authority of your country of residence",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "rbi", "depends_on": "Passport — copies of the relevant pages",
                "source_note": "Kotak Bank NRI account documentation",
            },
            {
                "document_name": "Proof of overseas mailing address",
                "plain_explanation": "Must match the communication address you select on the application. Banks generally allow this to follow later if you have only just relocated.",
                "where_to_obtain": "Utility bill, lease or employer letter from your country of residence",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "Valid visa, work permit or residence permit",
                "source_note": "Kotak Bank NRI account documentation",
            },
            {
                "document_name": "PAN card, or Form 60 if opening while in India",
                "plain_explanation": "PAN is needed to open while residing overseas. If you are physically in India you can substitute Form 60.",
                "where_to_obtain": "Income Tax Department",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "Kotak NRI account opening guide",
            },
            {
                "document_name": "Attestation of documents submitted from abroad",
                "plain_explanation": "Required if you are not appearing in person. Acceptable attesting authorities: an overseas branch official of an Indian scheduled commercial bank, a notary public or court magistrate, or the Indian embassy/consulate in your country.",
                "where_to_obtain": "Indian bank branch abroad, notary, or the Indian embassy",
                "approx_cost_min": 0, "approx_cost_max": 3000, "approx_time_days": 5,
                "regulatory_source": "rbi", "depends_on": "Passport — copies of the relevant pages",
                "source_note": "Kotak Bank NRI account documentation, attestation list",
            },
            {
                "document_name": "Latest passport-size photograph",
                "plain_explanation": "One recent colour photograph, passport size.",
                "where_to_obtain": "Any photo studio in your country of residence",
                "approx_cost_min": 100, "approx_cost_max": 300, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "Kotak Bank NRI account documentation",
            },
            {
                "document_name": "Conversion or closure request for an existing domestic account",
                "plain_explanation": "If you hold a Resident Indian savings account with SBI, this letter converts it to NRO. An NRI cannot hold both, so this is not optional.",
                "where_to_obtain": "SBI 'Download Forms' — the standard conversion request letter",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "NRI account opening application form",
                "source_note": "SBI NRE/NRO account opening procedure",
            },
            {
                "document_name": "FEMA declaration — for NRO to NRE transfers",
                "plain_explanation": "Only needed later, when you repatriate from NRO to NRE under the USD 1 million annual limit. It must be accompanied by Form 15CB from a chartered accountant and Form 15CA from the income tax portal.",
                "where_to_obtain": "HDFC Bank publishes a specimen FEMA declaration; forms 15CB/15CA from your CA and incometax.gov.in",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "rbi", "depends_on": "Conversion or closure request for an existing domestic account",
                "source_note": "HDFC Bank FEMA declaration for USD 1 million transfers",
            },
        ],
        "sources": _src(
            ("SBI — NRE / NRO account opening procedure", SBI_NRE_NRO),
            ("Kotak Mahindra Bank — NRI current account documentation and attestation", KOTAK_NRI),
            ("HDFC Bank — FEMA declaration for NRO to NRE transfers", HDFC_FEMA),
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # 7. Property registration — Kerala (state stamp act showcase)
    # ══════════════════════════════════════════════════════════════════
    {
        "transaction_type": "property registration",
        "bank": "",
        "residency": "not_applicable",
        "state": "Kerala",
        "summary": (
            "Kerala charges stamp duty and registration fee as two separate "
            "percentages of the higher of the consideration or the property's fair "
            "value — 8% and 2% respectively, totalling 10%. Fair value can be higher "
            "than your deal price, so a below-market sale does not reduce your stamp "
            "duty. The threshold that changes your process is ₹1 lakh: below it you can "
            "buy physical stamp paper from a licensed vendor, at or above it e-stamping "
            "is mandatory. Registration fee is always paid online."
        ),
        "interest_rate_range": "Not applicable — this is a state registration charge, not a loan product.",
        "processing_fee_note": (
            "Stamp duty and registration fee are state levies, not bank charges. "
            "Budget roughly 10% of the higher of consideration or fair value. A "
            "licensed document writer or advocate's fee is separate and varies."
        ),
        "regulatory_note": (
            "This is a purely state transaction and the RBI has no role in it. Stamp "
            "duty arises under the Kerala Stamp Act; registration is performed by the "
            "Sub-Registrar under the Registration Department. Filing fees such as "
            "copying and search fees are separate minor charges. Any bank appearing in "
            "a property purchase is only financing the buyer's margin — the bank does "
            "not set either charge."
        ),
        "disclosures": [
            "Stamp duty and registration fee are each charged on the HIGHER of the "
            "consideration or the property's fair value, so a discounted sale price "
            "does not reduce the duty.",
            "Filing, copying, translation and search fees are separate minor charges "
            "listed in the Kerala ready reckoner.",
        ],
        "items": [
            {
                "document_name": "Sale deed / conveyance deed on stamp paper",
                "plain_explanation": "The actual transfer instrument. Stamp duty on a conveyance in Kerala is 8 rupees for every ₹100 of the higher of fair value or consideration — effectively 8%.",
                "where_to_obtain": "Drafted by a licensed document writer or advocate, or from the department's model deed",
                "approx_cost_min": None, "approx_cost_max": None, "approx_time_days": 3,
                "regulatory_source": "state_stamp_act", "depends_on": "",
                "source_note": "Kerala stamp duty ready reckoner, Article 21/22",
            },
            {
                "document_name": "E-stamp of ₹1 lakh or more",
                "plain_explanation": "If the stamp duty is ₹1 lakh or above, e-stamping is mandatory in Kerala. Below that, physical stamp paper from a licensed vendor is acceptable.",
                "where_to_obtain": "Generated on the Kerala Registration portal (pearl.registration.kerala.gov.in)",
                "approx_cost_min": None, "approx_cost_max": None, "approx_time_days": 1,
                "regulatory_source": "state_stamp_act", "depends_on": "Sale deed / conveyance deed on stamp paper",
                "source_note": "Kerala Registration SOP 2024, fees procedure",
            },
            {
                "document_name": "Stamp duty payment — 8% of higher of consideration or fair value",
                "plain_explanation": "Charged as 8 rupees per ₹100 of the higher of the consideration set forth in the deed or the property's fair value. Fair value is verifiable on the state land-value portal.",
                "where_to_obtain": "Licensed stamp vendors, or e-payment on the registration portal",
                "approx_cost_min": None, "approx_cost_max": None, "approx_time_days": 1,
                "regulatory_source": "state_stamp_act", "depends_on": "E-stamp of ₹1 lakh or more",
                "source_note": "Kerala stamp duty ready reckoner; registration process flow",
            },
            {
                "document_name": "Registration fee — 2% of higher of consideration or fair value",
                "plain_explanation": "A separate 2% charged to the Sub-Registrar for registering the document. It is not part of stamp duty, and the two together come to 10%.",
                "where_to_obtain": "Paid online via the Kerala registration portal, or e-POS at the sub-registry",
                "approx_cost_min": None, "approx_cost_max": None, "approx_time_days": 1,
                "regulatory_source": "registrar", "depends_on": "Stamp duty payment — 8% of higher of consideration or fair value",
                "source_note": "Kerala registration process flow, 2% registration fee",
            },
            {
                "document_name": "Building valuation certificate",
                "plain_explanation": "Required where a building is also being transferred, issued by an approved agency under sections 28B or 28C of the Stamp Act. It forms part of the document itself.",
                "where_to_obtain": "Approved valuer appointed by the department",
                "approx_cost_min": None, "approx_cost_max": None, "approx_time_days": 7,
                "regulatory_source": "state_stamp_act", "depends_on": "",
                "source_note": "Kerala Registration SOP 2024, mandatory documents",
            },
            {
                "document_name": "Form 1B — where a building is also transferred",
                "plain_explanation": "A form that must form part of the document where the building, as distinct from the land, is being conveyed.",
                "where_to_obtain": "Downloaded from the Kerala registration portal",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "state_stamp_act", "depends_on": "Sale deed / conveyance deed on stamp paper",
                "source_note": "Kerala Registration SOP 2024, mandatory documents",
            },
            {
                "document_name": "Form 1 — Prevention of Undervaluation Rules",
                "plain_explanation": "Required under Rule 3 of the Prevention of Undervaluation Rules. Kerala can impound a deed and refer it to the District Registrar if stamp duty appears short.",
                "where_to_obtain": "Downloaded from the Kerala registration portal",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "state_stamp_act", "depends_on": "",
                "source_note": "Kerala Registration SOP 2024, impounding procedure",
            },
            {
                "document_name": "Form 58 — declaration regarding excess land",
                "plain_explanation": "To be signed by both parties where the property includes excess land. A common rejection reason when omitted.",
                "where_to_obtain": "Downloaded from the Kerala registration portal",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "state_stamp_act", "depends_on": "",
                "source_note": "Kerala Registration SOP 2024, mandatory documents",
            },
            {
                "document_name": "Form 60 under the Income Tax Act",
                "plain_explanation": "Required only if a party is not an income-tax assessee, has no PAN card, and the transaction exceeds ₹10 lakh. Frequently overlooked because it is conditional.",
                "where_to_obtain": "Downloaded from the Kerala registration portal",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "Kerala Registration SOP 2024, Form 60 condition",
            },
            {
                "document_name": "Previous title deeds and property tax receipts",
                "plain_explanation": "The chain of title, in original, going back far enough to establish the seller's title. This is what the Sub-Registrar actually verifies.",
                "where_to_obtain": "From the seller's records; previous Sub-Registrar offices",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "registrar", "depends_on": "",
                "source_note": "Kerala Registration SOP 2024, mandatory documents",
            },
            {
                "document_name": "No-objection certificate from the District Collector",
                "plain_explanation": "Required only where the property is restricted from transacting — for example government property, or land with a freeze.",
                "where_to_obtain": "District Collector's office, where the restriction applies",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 15,
                "regulatory_source": "registrar", "depends_on": "",
                "source_note": "Kerala Registration SOP 2024, mandatory documents",
            },
            {
                "document_name": "Identity proof of both parties, in original and copy",
                "plain_explanation": "Presented at the appearance before the Registering Officer, who records your admission of execution and affixes your thumb impression in the register.",
                "where_to_obtain": "Aadhaar, passport, driving licence or Voter ID",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 0,
                "regulatory_source": "registrar", "depends_on": "",
                "source_note": "Kerala registration process flow, appearance before Sub-Registrar",
            },
            {
                "document_name": "Filing, copying, search and translation fees",
                "plain_explanation": "Minor statutory fees: ₹210 for the first 10 pages and ₹5 per additional page for copying, ₹105 for a search over the first 5 years, ₹105 for filing a translation where the document language is unfamiliar to the Sub-Registrar.",
                "where_to_obtain": "Paid at the sub-registry alongside the registration fee",
                "approx_cost_min": 105, "approx_cost_max": 1050, "approx_time_days": 0,
                "regulatory_source": "registrar", "depends_on": "Registration fee — 2% of higher of consideration or fair value",
                "source_note": "Kerala stamp duty ready reckoner, fee schedule",
            },
        ],
        "sources": _src(
            ("Kerala Registration Department — Stamp Duty and Fees ready reckoner", KL_STAMP),
            ("Kerala Registration Department — Standard Operating Procedure for Registration (2024)", KL_SOP),
            ("Kerala Registration Department — Process flow for registration of documents", KL_FLOW),
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # 8. Business current account — ICICI Bank
    # ══════════════════════════════════════════════════════════════════
    {
        "transaction_type": "business current account",
        "bank": "ICICI Bank",
        "residency": "not_applicable",
        "state": "",
        "summary": (
            "The document list for a current account depends on how your business is "
            "constituted, not on what it does. A sole proprietorship needs two "
            "documents proving the business exists in the proprietor's own name. A "
            "partnership needs the partnership deed. A private limited company needs "
            "incorporation papers, the memorandum and articles, and a board resolution. "
            "Across every structure there are two items people forget: beneficial-owner "
            "declarations for anyone holding more than 10%, and an account-opening "
            "cheque from an existing current account."
        ),
        "interest_rate_range": "Not applicable — a current account does not carry an interest rate.",
        "processing_fee_note": (
            "Account-opening and annual maintenance fees depend on the chosen account "
            "variant and are published in ICICI Bank's current account schedule. Not "
            "quoted on the documentation page."
        ),
        "regulatory_note": (
            "Account opening is governed entirely by RBI KYC norms and the Customer "
            "Due Diligence framework, which is why beneficial-owner identification "
            "applies to every structure. The constitution documents themselves come "
            "from the Registrar of Companies or the Partnership Registration "
            "Authority. There is no stamp-duty component unless you are also "
            "registering a partnership deed."
        ),
        "disclosures": [
            "ICICI Bank does not publish account-opening or maintenance fees on its "
            "documentation page — check the current account fee schedule.",
            "A company cannot open a current account without a PAN in the company's "
            "own name.",
        ],
        "items": [
            {
                "document_name": "PAN card in the name of the entity",
                "plain_explanation": "Mandatory for every structure. A company or firm cannot open a current account without a PAN in the entity's own name — Form 60 is not a substitute here.",
                "where_to_obtain": "Income Tax Department",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "ICICI Bank current account documentation",
            },
            {
                "document_name": "Proof of business existence — two documents for a sole proprietorship",
                "plain_explanation": "Any two of: Shop and Establishment licence, GST certificate, IEC from DGFT, a professional body's registration certificate, a complete ITR showing the firm's income, a TAN allotment letter, or utility bills in the firm's name.",
                "where_to_obtain": "Municipal corporation, GSTN portal, DGFT, or your CA",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 7,
                "regulatory_source": "rbi", "depends_on": "PAN card in the name of the entity",
                "source_note": "Kotak Mahindra Bank required documents, sole proprietorship",
            },
            {
                "document_name": "Certificate of incorporation",
                "plain_explanation": "For a private limited or LLP. Issued by the Registrar of Companies and is the foundational document for a corporate account.",
                "where_to_obtain": "MCA portal — Ministry of Corporate Affairs",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "registrar", "depends_on": "",
                "source_note": "ICICI Bank current account documentation, private/public limited",
            },
            {
                "document_name": "Memorandum and Articles of Association",
                "plain_explanation": "The company's constitutional documents, required in updated form. A partnership firm instead submits its partnership deed.",
                "where_to_obtain": "MCA portal",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "registrar", "depends_on": "Certificate of incorporation",
                "source_note": "ICICI Bank current account documentation",
            },
            {
                "document_name": "Board resolution for opening a current account",
                "plain_explanation": "The company's own formal decision to open the account and appoint signatories. ICICI Bank publishes its own resolution template for this.",
                "where_to_obtain": "Company board meeting; ICICI Bank supplies a template",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 7,
                "regulatory_source": "bank_internal", "depends_on": "Memorandum and Articles of Association",
                "source_note": "ICICI Bank current account documentation",
            },
            {
                "document_name": "Partnership deed, if a partnership firm",
                "plain_explanation": "The deed that creates the firm and sets out the partners' rights. Required in place of the memorandum and articles.",
                "where_to_obtain": "Held by the firm; registered with the Registrar of Firms where applicable",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "registrar", "depends_on": "",
                "source_note": "ICICI Bank current account documentation, partnership firm",
            },
            {
                "document_name": "Updated list of directors and shareholding pattern",
                "plain_explanation": "The current statutory registers, on letterhead. Banks check these against MCA records and reject stale versions.",
                "where_to_obtain": "Company secretary; MCA portal",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "registrar", "depends_on": "Certificate of incorporation",
                "source_note": "ICICI Bank current account documentation",
            },
            {
                "document_name": "Beneficial owner declaration",
                "plain_explanation": "A list of every natural person holding more than 10% directly or indirectly, with their KYC. This is the most frequently omitted document on corporate current account applications.",
                "where_to_obtain": "Company secretary prepares; each beneficial owner supplies KYC",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 5,
                "regulatory_source": "rbi", "depends_on": "PAN card in the name of the entity",
                "source_note": "ICICI Bank current account documentation, beneficial owners",
            },
            {
                "document_name": "KYC of all authorised signatories",
                "plain_explanation": "One valid photo identification and address proof plus a recent passport-size photograph for each person who will operate the account.",
                "where_to_obtain": "Each signatory individually",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "ICICI Bank current account documentation",
            },
            {
                "document_name": "Identity and address proof of the proprietor or all partners",
                "plain_explanation": "For proprietorship and partnership structures, KYC for the individual proprietors or every partner.",
                "where_to_obtain": "Each individual",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "Kotak Mahindra Bank required documents",
            },
            {
                "document_name": "Proof of business or communication address",
                "plain_explanation": "Required where the address differs from the one on the certificate of registration — utility bill, lease or rent agreement.",
                "where_to_obtain": "Utility provider or your landlord",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "ICICI Bank current account documentation",
            },
            {
                "document_name": "Account-opening cheque from an existing current account",
                "plain_explanation": "A cheque drawn on an existing current account in the entity's name, used to initialise the new account. A recurring reason accounts are held up.",
                "where_to_obtain": "Your existing bank",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "PAN card in the name of the entity",
                "source_note": "ICICI Bank current account documentation",
            },
        ],
        "sources": _src(
            ("ICICI Bank — Current Account eligibility and documents required", ICICI_CA),
            ("Kotak Mahindra Bank — Documents required for current account opening", KOTAK_CA),
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # 9. Gold loan — SBI
    # ══════════════════════════════════════════════════════════════════
    {
        "transaction_type": "gold loan",
        "bank": "State Bank of India",
        "residency": "resident",
        "state": "",
        "summary": (
            "A gold loan is the shortest banking process in this app — you walk out "
            "with cash the same day, and no income proof is required because the gold "
            "is the security. What changed recently is paperwork, not eligibility. The "
            "RBI's November 2025 directions, with a compliance deadline of 1 April "
            "2026, require a detailed assay certificate for every loan, the borrower's "
            "physical presence during valuation, a photographed record of the "
            "collateral, and the Key Fact Statement to be acknowledged before "
            "disbursal."
        ),
        "interest_rate_range": "9.15% - 10.55% p.a. (varies by term; SBI publishes a starting rate of 9.15%)",
        "processing_fee_note": (
            "Gold appraiser fee, safe-keeping charges and other charges are levied in "
            "addition to interest, and under the 2025 RBI directions all of them must "
            "be listed in the Key Fact Statement. The amounts are branch-specific and "
            "are not published — ask for the KFS before sanction."
        ),
        "regulatory_note": (
            "The RBI's Responsible Business Conduct Directions for Commercial Banks "
            "govern gold lending almost end to end: valuation method, LTV, the assay "
            "certificate, borrower presence at valuation, and auction procedure. The "
            "appraiser and safe-keeping fees are the bank's own charges. No state "
            "stamp duty arises, because pledging ornaments is not a registered "
            "instrument."
        ),
        "disclosures": [
            "Appraiser and safe-keeping charges are not published by SBI and are "
            "branch-specific; the 2025 RBI directions require them in the Key Fact "
            "Statement.",
            "The LTV ratio is capped by RBI rules at 75% for standard gold loans.",
        ],
        "items": [
            {
                "document_name": "Proof of identity",
                "plain_explanation": "Any one OVD: passport, PAN card, Aadhaar card, Voter's ID or driving licence. Income proof is not required for a gold loan because the collateral secures it.",
                "where_to_obtain": "Held by you",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "SBI Gold Loan Application, documents checklist",
            },
            {
                "document_name": "Proof of residence",
                "plain_explanation": "Any one of: electricity bill, Aadhaar card, telephone bill, passport or Voter's ID.",
                "where_to_obtain": "Utility provider",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "Proof of identity",
                "source_note": "SBI Gold Loan Application, documents checklist",
            },
            {
                "document_name": "Two latest passport-size photographs",
                "plain_explanation": "Required on Form A of the application.",
                "where_to_obtain": "Any photo studio",
                "approx_cost_min": 100, "approx_cost_max": 200, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "Proof of identity",
                "source_note": "SBI Gold Loan Application, documents checklist",
            },
            {
                "document_name": "Form A and Form B, signed separately by each applicant",
                "plain_explanation": "Form A is your personal details, Form B the loan details including the ornaments being pledged. They must be filled completely and signed by the applicant and co-applicant separately.",
                "where_to_obtain": "SBI branch — or download the form in advance",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "Two latest passport-size photographs",
                "source_note": "SBI Gold Loan Application, instructions",
            },
            {
                "document_name": "Your physical presence during valuation and assaying",
                "plain_explanation": "Mandatory under the RBI's 2025 directions. The borrower must be present while the gold is assayed, and the deductions for stones and fastenings must be explained to you and recorded.",
                "where_to_obtain": "At the branch, at the time of valuation",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 0,
                "regulatory_source": "rbi", "depends_on": "Form A and Form B, signed separately by each applicant",
                "source_note": "RBI gold loan directions, assaying conduct clauses",
            },
            {
                "document_name": "Assay and valuation certificate — collect your copy",
                "plain_explanation": "Must state purity in carats, gross weight, net gold weight, any deductions for stones or fastenings, damage noted, an image of the collateral, and the value arrived at. One copy is kept by the bank, one is given to you.",
                "where_to_obtain": "Issued by the bank at the time of valuation",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 0,
                "regulatory_source": "rbi", "depends_on": "Your physical presence during valuation and assaying",
                "source_note": "RBI gold loan directions, certificate on letterhead clause",
            },
            {
                "document_name": "Key Fact Statement — acknowledge before disbursal",
                "plain_explanation": "Mandatory acknowledgement before funds are released. It must itemise every charge including appraising and auction charges. Under the 2025 directions the KFS should be available in your language.",
                "where_to_obtain": "From the bank before sanction",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "Assay and valuation certificate — collect your copy",
                "source_note": "RBI gold loan directions, KFS and charges clause",
            },
            {
                "document_name": "Ownership declaration for the ornaments",
                "plain_explanation": "You declare the ornaments are your bonafide property and not pledged elsewhere. The RBI directions require this declaration in all cases where ownership could be doubtful, and for inherited or gifted jewellery a self-declaration on ownership is usually required.",
                "where_to_obtain": "Declared on Form B of the application",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 0,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "RBI gold loan directions, ownership declaration clause",
            },
        ],
        "sources": _src(
            ("SBI — Gold Loan Application form with document checklist", SBI_GOLD_FORM),
            ("RBI — Directions on loans against eligible collateral (gold and silver)", RBI_GOLD),
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # 10. Mudra loan — general (government scheme, no single bank)
    # ══════════════════════════════════════════════════════════════════
    {
        "transaction_type": "mudra loan",
        "bank": "",
        "residency": "resident",
        "state": "",
        "summary": (
            "MUDRA is a refinancing scheme, not a loan product — the government "
            "refinances the lender, which then sets its own rate, so there is no single "
            "MUDRA interest rate. The category you fall into determines the paperwork: "
            "Shishu (up to ₹50,000) is deliberately light, while Kishore and Tarun "
            "expect 6-12 months of bank statements, prior ITRs, and increasingly a "
            "project report with CMA data. GST and Udyam registration are not "
            "mandatory, but their absence is the most common reason a Tarun application "
            "is declined."
        ),
        "interest_rate_range": "8.85% - 16.00% p.a. (set by each lending institution, not by MUDRA; public sector banks typically price at the lower end)",
        "processing_fee_note": (
            "Typically nil to 1% of the loan amount, set by the individual lender. "
            "MUDRA itself charges no processing fee to the borrower."
        ),
        "regulatory_note": (
            "MUDRA Ltd and the Department of Financial Services set the scheme's "
            "category limits and refinancing terms. The RBI governs KYC and the "
            "lending norms the bank must follow. Because these are unsecured "
            "collateral-free loans, there is no property, no registration and no "
            "stamp duty anywhere in the process."
        ),
        "disclosures": [
            "There is no single MUDRA interest rate — each lending institution prices "
            "its own loans within MCLR-linked limits.",
            "GST and Udyam registration are not mandatory, but strongly affect "
            "sanction for Kishore and Tarun categories.",
        ],
        "items": [
            {
                "document_name": "MUDRA loan application form",
                "plain_explanation": "The lender's own form. Every MUF (micro unit) uses the same government-scheme category, so the form content is broadly similar across banks.",
                "where_to_obtain": "Any MUDRA-lending bank, NBFC or microfinance institution",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "MUDRA loan document checklist",
            },
            {
                "document_name": "Identity proof",
                "plain_explanation": "Aadhaar, PAN, Voter ID or passport. PAN is effectively required in every case.",
                "where_to_obtain": "Held by you; Aadhaar and PAN from the relevant authorities",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "MUDRA loan application form",
                "source_note": "MUDRA loan document checklist",
            },
            {
                "document_name": "Address proof",
                "plain_explanation": "Aadhaar, an electricity or telephone bill, a rent agreement, or a bank passbook.",
                "where_to_obtain": "Utility provider or your bank",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "rbi", "depends_on": "Identity proof",
                "source_note": "MUDRA loan document checklist",
            },
            {
                "document_name": "Passport-size photographs",
                "plain_explanation": "Two to six depending on the category of the loan and the lender.",
                "where_to_obtain": "Any photo studio",
                "approx_cost_min": 100, "approx_cost_max": 400, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "Identity proof",
                "source_note": "MUDRA loan document checklist",
            },
            {
                "document_name": "Proof of business existence",
                "plain_explanation": "Business registration, Udyam certificate, trade licence or Shop and Establishment certificate. Not required for every Shishu case but expected from Kishore upward.",
                "where_to_obtain": "Udyam portal, GSTN, or your municipal corporation",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 7,
                "regulatory_source": "bank_internal", "depends_on": "MUDRA loan application form",
                "source_note": "MUDRA loan document checklist, by category",
            },
            {
                "document_name": "Project report or DPR",
                "plain_explanation": "Basic for Shishu, required for Kishore and Tarun. Should include business description, cost of project, means of finance, sales and profit projections, and a repayment schedule. Incomplete project reports are a leading cause of decline.",
                "where_to_obtain": "Prepared by you, or by a consultant or your CA",
                "approx_cost_min": 0, "approx_cost_max": 5000, "approx_time_days": 7,
                "regulatory_source": "bank_internal", "depends_on": "Proof of business existence",
                "source_note": "MUDRA project report requirement",
            },
            {
                "document_name": "CMA data (Credit Monitoring Arrangement)",
                "plain_explanation": "A CA-prepared set of financial statements with projected balance sheets, cash flow and DSCR. Increasingly requested even for smaller MUDRA instalment loans.",
                "where_to_obtain": "From a chartered accountant",
                "approx_cost_min": 1000, "approx_cost_max": 5000, "approx_time_days": 7,
                "regulatory_source": "bank_internal", "depends_on": "Project report or DPR",
                "source_note": "MUDRA CMA data requirement",
            },
            {
                "document_name": "Bank statements — 6 months for Kishore, 12 for Tarun",
                "plain_explanation": "Statements of all operative accounts used for the business, not only the account held with the lending bank. Banks look for clean credits and no cheque returns.",
                "where_to_obtain": "Your bank",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "bank_internal", "depends_on": "Identity proof",
                "source_note": "MUDRA loan document checklist, by category",
            },
            {
                "document_name": "Income tax returns for the previous year",
                "plain_explanation": "Or sales tax returns where applicable. Not required for Shishu where the business is new; expected from Kishore upward and essential for Tarun.",
                "where_to_obtain": "incometax.gov.in or the sales tax portal",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "rbi", "depends_on": "Bank statements — 6 months for Kishore, 12 for Tarun",
                "source_note": "MUDRA loan document checklist",
            },
            {
                "document_name": "Quotation for machinery or equipment",
                "plain_explanation": "Required where the loan funds assets, so the lender can assess the project cost. Quoted prices must be realistic — an inflated quote undermines the sanction.",
                "where_to_obtain": "From suppliers or dealers",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "bank_internal", "depends_on": "Project report or DPR",
                "source_note": "MUDRA loan document checklist",
            },
            {
                "document_name": "Constitution documents, if the borrower is not an individual",
                "plain_explanation": "Partnership deed for a firm; certificate of incorporation, MOA, AOA, board resolution and director list for a company; LLP agreement for an LLP.",
                "where_to_obtain": "Registrar of Firms, or the MCA portal",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 7,
                "regulatory_source": "registrar", "depends_on": "MUDRA loan application form",
                "source_note": "MUDRA documents by borrower constitution",
            },
        ],
        "sources": _src(
            ("MUDRA loan documents required 2026 — full checklist by category", MUDRA),
            ("Bajaj Finserv — Pradhan Mantri MUDRA interest rate and categories", "https://www.bajajfinserv.in/pradhan-mantri-mudra-loan-interest-rate"),
        ),
    },
]


# ── Source URLs for the extended seed set ───────────────────────────────
KOTAK_PL = "https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/required-documents.html"
ICICI_PL = "https://www.icici.bank.in/personal-banking/loans/personal-loan/documentation"
SBI_KCC = "https://sbi.bank.in/web/agri-rural/agriculture-banking/crop-loan/kisan-credit-card"
RBI_KCC = "https://www.rbi.org.in/scripts/NotificationUser.aspx?Id=13524&Mode=0"
HDFC_CAR = "https://www.hdfc.bank.in/car-loan/documentation"
HDFC_TW = "https://www.hdfc.bank.in/two-wheeler-loan/documentation"
HDFC_LAP = "https://www.hdfc.bank.in/loan-against-property/documentation"
HDFC_LAP_RATES = "https://www.hdfc.bank.in/loan-against-property/interest-rates-and-charges"


SEED_ENTRIES += [
    # ══════════════════════════════════════════════════════════════════
    # 11. Personal loan — the most-asked, most-borrowed retail product
    # ══════════════════════════════════════════════════════════════════
    {
        "transaction_type": "personal loan",
        "bank": "",
        "residency": "resident",
        "state": "",
        "summary": (
            "A personal loan is unsecured, so the document list is short and "
            "almost entirely about proving you can repay. Two banks make the "
            "point sharply in opposite directions: Kotak asks for three months "
            "of slips AND statements, while ICICI will pull your income proof "
            "itself through net banking or an account aggregator and asks for "
            "nothing physical. The practical difference between them is not the "
            "policy on paper, it is whether you already bank with them."
        ),
        "interest_rate_range": "10.99% - 24.00% p.a. (unsecured, so pricing spans the full credit range)",
        "processing_fee_note": (
            "Typically 1% - 3% of the loan amount plus taxes. Because the rate "
            "looks competitive, always compare the APR rather than the headline "
            "rate: a 10.50% loan with a 1.5% processing fee is an 11.16% APR."
        ),
        "regulatory_note": (
            "The RBI governs KYC, responsible lending conduct and the disclosure "
            "of the total cost of borrowing in the Key Fact Statement. The "
            "document list and the fee are the lender's own policy. No state "
            "stamp duty arises, because an unsecured loan is not registered."
        ),
        "disclosures": [
            "Rate ranges for unsecured lending are wide because the price is set "
            "by credit score, and the same borrower can be offered very different "
            "rates by different lenders.",
            "The effective cost is the APR, not the headline rate — include "
            "processing fees, documentation fees and insurance when comparing.",
        ],
        "items": [
            {
                "document_name": "PAN card",
                "plain_explanation": "Mandatory for the applicant and every co-applicant. Both ICICI and Kotak treat PAN as non-negotiable for a personal loan.",
                "where_to_obtain": "Income Tax Department",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "Kotak and ICICI personal loan documentation",
            },
            {
                "document_name": "Identity and address proof (officially valid document)",
                "plain_explanation": "One OVD serves as both: passport, driving licence, Voter ID, NREGA job card, an NPR letter, or voluntary Aadhaar.",
                "where_to_obtain": "As applicable — licence and Voter ID from the state, passport from your embassy",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "PAN card",
                "source_note": "Kotak personal loan required documents",
            },
            {
                "document_name": "Last 3 months' salary slips",
                "plain_explanation": "If you have no salary slips, Kotak accepts three months of bank statements showing regular salary credits, supported by your ITR.",
                "where_to_obtain": "Your employer",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "Identity and address proof (officially valid document)",
                "source_note": "Kotak personal loan, alternative to salary slips",
            },
            {
                "document_name": "Last 3 months' bank statement showing salary credit",
                "plain_explanation": "The period varies by lender: Kotak asks for three months, ICICI three months for salaried applicants. Some lenders ask six.",
                "where_to_obtain": "Your bank — net banking or a branch request",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "Kotak and ICICI personal loan documentation",
            },
            {
                "document_name": "Two to three passport-size photographs",
                "plain_explanation": "Both lenders require them on the application.",
                "where_to_obtain": "Any photo studio",
                "approx_cost_min": 100, "approx_cost_max": 300, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "Kotak personal loan required documents",
            },
            {
                "document_name": "ITR or Form 16 — if you are self-employed",
                "plain_explanation": "Salaried applicants at ICICI usually skip this entirely because income is verified from banking records. Self-employed applicants submit two years of returns.",
                "where_to_obtain": "incometax.gov.in",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "PAN card",
                "source_note": "ICICI personal loan documentation, self-employed",
            },
            {
                "document_name": "Employment proof — employee ID or appointment letter",
                "plain_explanation": "Not always asked for, but useful when you are changing jobs and have a thin statement history at the new employer.",
                "where_to_obtain": "Your employer",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "Industry-standard personal loan checklist",
            },
            {
                "document_name": "Key Fact Statement acknowledgement",
                "plain_explanation": "Mandatory under RBI rules before disbursal. It must itemise the total cost of borrowing, which is where the processing fee stops being invisible.",
                "where_to_obtain": "From the lender, digitally, before sanction",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "Last 3 months' bank statement showing salary credit",
                "source_note": "RBI Key Fact Statement requirements",
            },
        ],
        "sources": _src(
            ("Kotak Mahindra Bank — Personal Loan required documents", KOTAK_PL),
            ("ICICI Bank — Personal Loan documentation", ICICI_PL),
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # 12. Kisan Credit Card — agricultural, and a different regulator mix
    # ══════════════════════════════════════════════════════════════════
    {
        "transaction_type": "kisan credit card",
        "bank": "State Bank of India",
        "residency": "resident",
        "state": "",
        "summary": (
            "A Kisan Credit Card is a cash-credit facility, not a term loan, and "
            "two things follow from that. First, collateral is waived up to "
            "Rs 2 lakh (Rs 3 lakh where the bank has a tie-up), so the security "
            "documents that dominate every other secured product largely "
            "disappear. Second, interest is 7% up to Rs 3 lakh only if the "
            "3% prompt-repayment subvention is available, and that requires your "
            "Aadhaar to be linked to the account. Self-reported timely repayment, "
            "not credit history, is what earns the subvention."
        ),
        "interest_rate_range": "7.00% p.a. up to Rs 3.00 lakh with the 3% interest subvention; above Rs 3.00 lakh and below Rs 50.00 lakh, 3.25% above 1-year MCLR",
        "processing_fee_note": (
            "Not published on the product page. Service charges and the card "
            "annual fee vary by issuing bank and are set out in the Key Fact "
            "Statement — ask for it before you accept the card."
        ),
        "regulatory_note": (
            "Unusually for this product, the RBI sets a great deal of the rule "
            "itself: the Kisan Credit Card Scheme Directions specify eligibility, "
            "the six-year composite facility, the interest ceiling, the minimum "
            "balance basis on which interest is charged, and the one-time land "
            "record documentation. Land records and cropping pattern come from "
            "state revenue authorities, so a state agricultural department is "
            "involved but no stamp duty arises."
        ),
        "disclosures": [
            "The 7% rate up to Rs 3 lakh depends on the prompt-repayment "
            "incentive, which requires linked Aadhaar. Without it you are on the "
            "standard MCLR-linked rate.",
            "For sharecroppers and oral lessees who cannot certify identity or "
            "occupation, banks accept an affidavit describing the land tilled and "
            "crops grown — but only for loans up to Rs 50,000.",
        ],
        "items": [
            {
                "document_name": "Kisan Credit Card application form",
                "plain_explanation": "The bank's KCC application, covering the limit sought and the cropping plan.",
                "where_to_obtain": "Any agri branch, or the bank's agri portal",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "SBI Kisan Credit Card, documents required",
            },
            {
                "document_name": "Two passport-size photographs",
                "plain_explanation": "Standard KYC photograph requirement.",
                "where_to_obtain": "Any photo studio",
                "approx_cost_min": 100, "approx_cost_max": 200, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "SBI Kisan Credit Card, documents required",
            },
            {
                "document_name": "Proof of landholding certified by revenue authorities",
                "plain_explanation": "The land record, or a tenancy certificate, or an equivalent under the bank's credit policy. This is the one-time documentation the RBI directions require at application.",
                "where_to_obtain": "State revenue department / taluk office",
                "approx_cost_min": 100, "approx_cost_max": 1000, "approx_time_days": 7,
                "regulatory_source": "rbi", "depends_on": "Kisan Credit Card application form",
                "source_note": "RBI KCC Scheme Directions, one-time documentation",
            },
            {
                "document_name": "Cropping pattern with acreage",
                "plain_explanation": "What you intend to grow and over how much land. The sanctioned limit is set against this, so an understated pattern limits your card.",
                "where_to_obtain": "Your own records, submitted with the application",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "bank_internal", "depends_on": "Proof of landholding certified by revenue authorities",
                "source_note": "SBI Kisan Credit Card, documents required",
            },
            {
                "document_name": "Security documents — only if the limit exceeds Rs 2.00 lakh",
                "plain_explanation": "An equitable or registered mortgage of land valued at 100% of the loan. This is waived up to Rs 2.00 lakh, and up to Rs 3.00 lakh where the bank has a tie-up arrangement.",
                "where_to_obtain": "Sub-registrar, for a registered mortgage",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 15,
                "regulatory_source": "registrar", "depends_on": "Cropping pattern with acreage",
                "source_note": "SBI Kisan Credit Card, collateral terms",
            },
            {
                "document_name": "Aadhaar linked to the account",
                "plain_explanation": "Not a document you file, but the thing that decides your rate. The 3% prompt-repayment incentive requires Aadhaar details to reach the bank, and it is what takes the rate to 7% up to Rs 3 lakh.",
                "where_to_obtain": "UIDAI, or through your bank's net banking",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "SBI Kisan Credit Card, interest subvention terms",
            },
            {
                "document_name": "Occupational affidavit — for sharecroppers and oral lessees only",
                "plain_explanation": "Where certification of identity or occupational status is difficult, an affidavit describing the land tilled and the crops grown is accepted. RBI limits this route to loans up to Rs 50,000.",
                "where_to_obtain": "You write it; notarise if the bank requires",
                "approx_cost_min": 100, "approx_cost_max": 1000, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "Proof of landholding certified by revenue authorities",
                "source_note": "RBI KCC Scheme Directions, sharecroppers and oral lessees",
            },
        ],
        "sources": _src(
            ("SBI — Kisan Credit Card, documents required and interest", SBI_KCC),
            ("RBI — Regional Rural Banks Kisan Credit Card Scheme Directions", RBI_KCC),
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # 13. Vehicle loan — HDFC, car and two-wheeler
    # ══════════════════════════════════════════════════════════════════
    {
        "transaction_type": "vehicle loan",
        "bank": "HDFC Bank",
        "residency": "resident",
        "state": "",
        "summary": (
            "A vehicle loan is the easiest secured product to document, because "
            "the collateral is new and the bank already holds the invoice. Two "
            "HDFC specifics trip people up: a redacted Aadhaar copy is accepted "
            "only if submitted voluntarily with a consent letter, and a physical "
            "copy must be under 30 days old. For a two-wheeler the income proof "
            "requirement is explicitly 'if applicable' — many borrowers are not "
            "asked for anything beyond identity, address and the dealer's invoice."
        ),
        "interest_rate_range": "8.70% - 14.00% p.a. (new car loans, varies by tenure and model)",
        "processing_fee_note": (
            "Not published on the documentation page. HDFC's car-loan route "
            "typically charges a processing fee plus RTO and hypothecation "
            "charges, which are statutory and set by the RTO — ask for the itemised "
            "Key Fact Statement."
        ),
        "regulatory_note": (
            "The RBI governs KYC and the fair practice of not bundling insurance. "
            "RTO and hypothecation fees are statutory charges collected on your "
            "behalf and paid to the Regional Transport Office, not bank income — "
            "they are not set by HDFC and not by the RBI. The loan agreement and "
            "insurance requirement are the bank's own policy."
        ),
        "disclosures": [
            "Hypothecation and RTO charges are statutory and collected for the "
            "vehicle registry; they vary by state and are not a bank margin.",
            "For a two-wheeler, income proof is listed by HDFC as required only "
            "if applicable, so check before you assemble anything.",
        ],
        "items": [
            {
                "document_name": "Identity and address proof",
                "plain_explanation": "Passport, permanent driving licence, Voter ID, NREGA job card, NPR letter — or a voluntarily submitted Aadhaar with a consent letter and the first 8 digits redacted.",
                "where_to_obtain": "As applicable — licence and Voter ID from the state",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "HDFC car loan documentation",
            },
            {
                "document_name": "Valid driving licence",
                "plain_explanation": "Must be permanent and unexpired. A learner's permit or a temporary licence will not do, and this is checked separately from identity proof.",
                "where_to_obtain": "Any RTO in India",
                "approx_cost_min": 500, "approx_cost_max": 1500, "approx_time_days": 15,
                "regulatory_source": "registrar", "depends_on": "",
                "source_note": "HDFC two-wheeler documentation",
            },
            {
                "document_name": "Address proof, if different from your identity proof",
                "plain_explanation": "Utility bill under two months old, property or municipal tax receipt, pension payment order containing the address, or an employer accommodation letter.",
                "where_to_obtain": "Utility provider, or your employer",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "Identity and address proof",
                "source_note": "HDFC two-wheeler documentation, address proof list",
            },
            {
                "document_name": "Latest salary slip and Form 16",
                "plain_explanation": "Income proof for a salaried car-loan applicant. HDFC accepts the latest slip and Form 16; the two-wheeler product instead accepts any one of three months' slips, three months' statements showing salary credit, or Form 16.",
                "where_to_obtain": "Your employer, and incometax.gov.in",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "HDFC car and two-wheeler documentation",
            },
            {
                "document_name": "Previous 6 months' bank statements",
                "plain_explanation": "For a car loan. The two-wheeler product asks for three months instead, or the latest ITR if you are self-employed.",
                "where_to_obtain": "Your bank",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "HDFC car loan documentation",
            },
            {
                "document_name": "Latest ITR — if self-employed",
                "plain_explanation": "Self-employed sole proprietors submit their latest return. Partnership and company applicants submit two years of audited balance sheet, profit and loss account, and company ITR.",
                "where_to_obtain": "incometax.gov.in, or your CA",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 2,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "HDFC car loan documentation, self-employed",
            },
            {
                "document_name": "Invoice or quotation from the dealer",
                "plain_explanation": "Proof of purchase. For a two-wheeler this is listed explicitly; for a car it underpins the valuation the bank lends against.",
                "where_to_obtain": "The dealership",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "HDFC two-wheeler documentation, proof of purchase",
            },
        ],
        "sources": _src(
            ("HDFC Bank — Car Loan documentation", HDFC_CAR),
            ("HDFC Bank — Two Wheeler Loan documentation", HDFC_TW),
        ),
    },

    # ══════════════════════════════════════════════════════════════════
    # 14. Loan against property — the LTV/tax-benefit contrast with a home loan
    # ══════════════════════════════════════════════════════════════════
    {
        "transaction_type": "loan against property",
        "bank": "HDFC Bank",
        "residency": "resident",
        "state": "",
        "summary": (
            "A loan against property borrows against a property you already own, "
            "which changes three things relative to a home loan. The money is "
            "disposable, so the money is yours rather than the bank's. The "
            "loan-to-value is lower — up to 65% of market value against 90% for a "
            "home loan. And the Section 24(b) interest deduction available on a "
            "self-occupied home loan does not apply to the same extent, so the "
            "after-tax cost is genuinely higher even when the headline rate looks "
            "similar. Decisioning can take up to 25 days where a field "
            "investigation or valuation is needed."
        ),
        "interest_rate_range": "8.30% - 12.75% p.a. (Policy Repo Rate + 3.05% to 7.50%)",
        "processing_fee_note": (
            "Applicable taxes and charges are payable at actual, including stamp "
            "duty on the mortgage deed. Document retrieval after disbursement is "
            "charged at Rs 75 per document set, and an amortisation schedule is "
            "Rs 50 per request."
        ),
        "regulatory_note": (
            "RBI governs KYC and responsible lending, including a 2% p.a. charge "
            "on the principal outstanding where the borrower fails to comply with "
            "sanction terms, capped at Rs 50,000 for critical documents. But the "
            "stamp duty on the mortgage deed itself is a state charge levied on "
            "registering the mortgage, and that is the single largest "
            "state-versus-central distinction in this product."
        ),
        "disclosures": [
            "Stamp duty and registration on the mortgage deed are state charges "
            "and vary by state and by the value of the property. They are not an "
            "HDFC charge and not an RBI charge.",
            "Decisioning is within 7 days with complete documents, but up to 25 "
            "days where a field investigation or property valuation is required.",
        ],
        "items": [
            {
                "document_name": "Identity proof",
                "plain_explanation": "Voter's ID, employer's card, or any other officially valid document. If your ID carries your address, a separate address proof is not needed.",
                "where_to_obtain": "As applicable",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "HDFC loan against property documentation",
            },
            {
                "document_name": "Proof of residence",
                "plain_explanation": "Ration card, telephone bill, electricity bill, or Voter's ID — any one of them.",
                "where_to_obtain": "Utility provider, or the local ration shop",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "rbi", "depends_on": "",
                "source_note": "HDFC loan against property documentation",
            },
            {
                "document_name": "Last 6 months' salary slips and Form 16 for 2 years",
                "plain_explanation": "HDFC asks for six months of slips for a salaried applicant here, which is longer than the three months a personal loan needs.",
                "where_to_obtain": "Your employer, and incometax.gov.in",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "bank_internal", "depends_on": "Identity proof",
                "source_note": "HDFC loan against property documentation, salaried",
            },
            {
                "document_name": "Certified financial statements for 3 years",
                "plain_explanation": "Required if you are self-employed, to demonstrate financial stability and business income over time.",
                "where_to_obtain": "Your chartered accountant",
                "approx_cost_min": 3000, "approx_cost_max": 15000, "approx_time_days": 7,
                "regulatory_source": "bank_internal", "depends_on": "",
                "source_note": "HDFC loan against property documentation, self-employed",
            },
            {
                "document_name": "Sale deed or title deed of the property",
                "plain_explanation": "The most recent instrument conferring title on you. This is the anchor document; everything else exists to prove the chain back from it.",
                "where_to_obtain": "Sub-registrar office where the deed was registered",
                "approx_cost_min": 100, "approx_cost_max": 500, "approx_time_days": 3,
                "regulatory_source": "registrar", "depends_on": "",
                "source_note": "HDFC loan against property documentation",
            },
            {
                "document_name": "Chain of title — previous deeds",
                "plain_explanation": "Every earlier deed back to the original grant. An incomplete chain, not your income, is the usual reason a loan against property stalls.",
                "where_to_obtain": "Sub-registrar offices where each deed was registered",
                "approx_cost_min": 300, "approx_cost_max": 3000, "approx_time_days": 7,
                "regulatory_source": "registrar", "depends_on": "Sale deed or title deed of the property",
                "source_note": "HDFC loan against property documentation",
            },
            {
                "document_name": "Encumbrance certificate",
                "plain_explanation": "Proves the property is free of existing charges. Without it the bank cannot take a clean mortgage, so this is not optional paperwork.",
                "where_to_obtain": "State registration department, via the state portal",
                "approx_cost_min": 500, "approx_cost_max": 2500, "approx_time_days": 7,
                "regulatory_source": "registrar", "depends_on": "Chain of title — previous deeds",
                "source_note": "HDFC loan against property documentation",
            },
            {
                "document_name": "Occupancy or completion certificate",
                "plain_explanation": "Proves the building is lawfully completed and fit to occupy, which the bank needs before accepting it as security.",
                "where_to_obtain": "Municipal corporation or the local development authority",
                "approx_cost_min": 200, "approx_cost_max": 1000, "approx_time_days": 10,
                "regulatory_source": "registrar", "depends_on": "Sale deed or title deed of the property",
                "source_note": "HDFC loan against property documentation",
            },
            {
                "document_name": "Property tax receipts and maintenance bills",
                "plain_explanation": "Evidence that taxes and society or maintenance charges are current, which is a standard condition of the mortgage.",
                "where_to_obtain": "Your municipal corporation, and the society or association",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 3,
                "regulatory_source": "registrar", "depends_on": "Sale deed or title deed of the property",
                "source_note": "HDFC loan against property documentation",
            },
            {
                "document_name": "Approved building plan",
                "plain_explanation": "The sanctioned plan for the property, which lets the bank verify the built structure matches what was approved.",
                "where_to_obtain": "Municipal corporation or the local development authority",
                "approx_cost_min": 0, "approx_cost_max": 500, "approx_time_days": 7,
                "regulatory_source": "registrar", "depends_on": "Occupancy or completion certificate",
                "source_note": "HDFC loan against property documentation",
            },
            {
                "document_name": "Property valuation report",
                "plain_explanation": "The bank lends against market value, and the valuation is what sets the loan-to-value of up to 65%. It is arranged by the bank, and where it needs a field investigation it is the reason decisioning stretches to 25 days.",
                "where_to_obtain": "Arranged by HDFC Bank",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 10,
                "regulatory_source": "bank_internal", "depends_on": "Encumbrance certificate",
                "source_note": "HDFC loan against property, decisioning timelines",
            },
            {
                "document_name": "Stamp duty and registration on the mortgage deed",
                "plain_explanation": "A state charge levied on registering the mortgage, payable at actual. It is the item most often mistaken for an HDFC fee, and it is neither an HDFC charge nor an RBI one.",
                "where_to_obtain": "State sub-registrar, or via the state stamp portal",
                "approx_cost_min": None, "approx_cost_max": None, "approx_time_days": 7,
                "regulatory_source": "state_stamp_act", "depends_on": "Sale deed or title deed of the property",
                "source_note": "HDFC loan against property charges, applicable at actual",
            },
            {
                "document_name": "Loan Against Property agreement and Key Facts Statement",
                "plain_explanation": "Signed at sanction. A Dropline Overdraft agreement is also signed if you take the overdraft variant, and a Loan Against Rent Receivables agreement if the property is tenanted.",
                "where_to_obtain": "Provided by the bank at sanction",
                "approx_cost_min": 0, "approx_cost_max": 0, "approx_time_days": 1,
                "regulatory_source": "bank_internal", "depends_on": "Property valuation report",
                "source_note": "HDFC loan against property formalities",
            },
        ],
        "sources": _src(
            ("HDFC Bank — Loan Against Property, documents required", HDFC_LAP),
            ("HDFC Bank — Loan Against Property interest rates and charges", HDFC_LAP_RATES),
        ),
    },
]
