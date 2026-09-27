"""
Kaagaz — reference data & normalisation.

The product must answer for *any* Indian banking / loan / document transaction.
That means banks, states and transaction types are free text, normalised against
compile-time reference lists purely for (a) spelling correction in the UI and
(b) cache-key canonicalisation. A value that matches nothing in the lists is
still perfectly valid — it simply passes through unchanged.

Reference lists are for normalisation, never for validation or rejection.
"""

# ────────────────────────────────────────────────────────────────────────────
# States & Union Territories (36 + 8)
# ────────────────────────────────────────────────────────────────────────────
STATES = {
    "andaman and nicobar islands": "Andaman & Nicobar Islands",
    "andhra pradesh": "Andhra Pradesh",
    "arunachal pradesh": "Arunachal Pradesh",
    "assam": "Assam",
    "bihar": "Bihar",
    "chandigarh": "Chandigarh",
    "chhattisgarh": "Chhattisgarh",
    "dadra and nagar haveli and daman and diu": "Dadra & Nagar Haveli and Daman & Diu",
    "daman and diu": "Dadra & Nagar Haveli and Daman & Diu",
    "delhi": "Delhi (NCT of Delhi)",
    "goa": "Goa",
    "gujarat": "Gujarat",
    "haryana": "Haryana",
    "himachal pradesh": "Himachal Pradesh",
    "jammu and kashmir": "Jammu & Kashmir",
    "jharkhand": "Jharkhand",
    "karnataka": "Karnataka",
    "kerala": "Kerala",
    "ladakh": "Ladakh",
    "lakshadweep": "Lakshadweep",
    "madhya pradesh": "Madhya Pradesh",
    "maharashtra": "Maharashtra",
    "manipur": "Manipur",
    "meghalaya": "Meghalaya",
    "mizoram": "Mizoram",
    "nagaland": "Nagaland",
    "odisha": "Odisha",
    "orissa": "Odisha",
    "puducherry": "Puducherry",
    "pondicherry": "Puducherry",
    "punjab": "Punjab",
    "rajasthan": "Rajasthan",
    "sikkim": "Sikkim",
    "tamil nadu": "Tamil Nadu",
    "telangana": "Telangana",
    "tripura": "Tripura",
    "uttar pradesh": "Uttar Pradesh",
    "uttarakhand": "Uttarakhand",
    "west bengal": "West Bengal",
}

# Two-letter and common shorthand. People type these constantly ("KA", "MH")
# and a silent pass-through would make the same question miss the cache twice
# under two different keys.
_STATE_CODES = {
    "an": "Andaman & Nicobar Islands", "ap": "Andhra Pradesh",
    "ar": "Arunachal Pradesh", "as": "Assam", "br": "Bihar",
    "ch": "Chandigarh", "cg": "Chhattisgarh", "dd": "Dadra & Nagar Haveli and Daman & Diu",
    "dl": "Delhi (NCT of Delhi)", "ga": "Goa", "gj": "Gujarat",
    "hr": "Haryana", "hp": "Himachal Pradesh", "jk": "Jammu & Kashmir",
    "jh": "Jharkhand", "ka": "Karnataka", "kl": "Kerala",
    "la": "Ladakh", "ld": "Lakshadweep", "mp": "Madhya Pradesh",
    "mh": "Maharashtra", "mn": "Manipur", "ml": "Meghalaya",
    "mz": "Mizoram", "nl": "Nagaland", "od": "Odisha", "or": "Odisha",
    "py": "Puducherry", "pb": "Punjab", "rj": "Rajasthan",
    "sk": "Sikkim", "tn": "Tamil Nadu", "tg": "Telangana", "ts": "Telangana",
    "tr": "Tripura", "up": "Uttar Pradesh", "uk": "Uttarakhand",
    "wb": "West Bengal", "dl-1": "Delhi (NCT of Delhi)",
    # Concatenated forms people actually type
    "andhra": "Andhra Pradesh", "tamilnadu": "Tamil Nadu",
    "westbengal": "West Bengal", "uttarakhand": "Uttarakhand",
    "himachal": "Himachal Pradesh", "karnataka": "Karnataka",
    "maharashtra": "Maharashtra", "punjab": "Punjab",
    "rajasthan": "Rajasthan", "gujarat": "Gujarat", "punjab state": "Punjab",
    "new delhi": "Delhi (NCT of Delhi)", "nct of delhi": "Delhi (NCT of Delhi)",
    "pondicherry": "Puducherry", "orissa": "Odisha",
    "j&k": "Jammu & Kashmir", "uttaranchal": "Uttarakhand",
    "pondy": "Puducherry", "bengaluru": "Karnataka", "bangalore": "Karnataka",
}
STATES.update(_STATE_CODES)

# ────────────────────────────────────────────────────────────────────────────
# Banks
# ────────────────────────────────────────────────────────────────────────────
# key = lowercase canonical token, value = display name.
# Groups are recorded separately so the UI can offer a sensibly ordered
# dropdown (PSB first — they are what most users actually apply to).

PUBLIC_SECTOR_BANKS = {
    "state bank of india": "State Bank of India",
    "sbi": "State Bank of India",
    "punjab national bank": "Punjab National Bank",
    "pnb": "Punjab National Bank",
    "bank of baroda": "Bank of Baroda",
    "bob": "Bank of Baroda",
    "canara bank": "Canara Bank",
    "union bank of india": "Union Bank of India",
    "union bank": "Union Bank of India",
    "indian bank": "Indian Bank",
    "indian overseas bank": "Indian Overseas Bank",
    "iob": "Indian Overseas Bank",
    "bank of india": "Bank of India",
    "central bank of india": "Central Bank of India",
    "uco bank": "UCO Bank",
    "uco": "UCO Bank",
    "punjab and sind bank": "Punjab & Sind Bank",
    "psb": "Punjab & Sind Bank",
    "punjab & sind bank": "Punjab & Sind Bank",
    "bank of maharashtra": "Bank of Maharashtra",
    "corporation bank": "Corporation Bank",
    "oriental bank of commerce": "Oriental Bank of Commerce",
    "obc": "Oriental Bank of Commerce",
    "syndicate bank": "Syndicate Bank",
    "allahabad bank": "Allahabad Bank (merged into Indian Bank)",
    "andhra bank": "Andhra Bank (merged into SBI)",
    "allahabad bank and indian bank": "Allahabad Bank + Indian Bank (merged)",
    "new india assurance": "New India Assurance",
}

PRIVATE_SECTOR_BANKS = {
    "hdfc bank": "HDFC Bank",
    "hdfc": "HDFC Bank",
    "icici bank": "ICICI Bank",
    "icici": "ICICI Bank",
    "axis bank": "Axis Bank",
    "kotak mahindra bank": "Kotak Mahindra Bank",
    "kotak": "Kotak Mahindra Bank",
    "yes bank": "Yes Bank",
    "indusind bank": "IndusInd Bank",
    "idbi bank": "IDBI Bank",
    "idbi": "IDBI Bank",
    "federal bank": "Federal Bank",
    "rbl bank": "RBL Bank",
    "ratnakar bank": "RBL Bank",
    "au small finance bank": "AU Small Finance Bank",
    "au bank": "AU Small Finance Bank",
    "bandhan bank": "Bandhan Bank",
    "csb bank": "CSB Bank",
    "karur vysya bank": "Karur Vysya Bank",
    "kv bank": "Karur Vysya Bank",
    "karnataka bank": "Karnataka Bank",
    "tamilnad mercantile bank": "Tamilnad Mercantile Bank",
    "tmb": "Tamilnad Mercantile Bank",
    "south indian bank": "South Indian Bank",
    "dbs bank": "DBS Bank",
    "dbs": "DBS Bank",
    "citibank": "Citibank India",
    "citi": "Citibank India",
    "standard chartered": "Standard Chartered India",
    "hsbc": "HSBC India",
    "barclays bank": "Barclays Bank India",
    "deutsche bank": "Deutsche Bank India",
    "kotak mahindra": "Kotak Mahindra Bank",
    "uco bank limited": "UCO Bank",
    "uco bank ltd": "UCO Bank",
}

SMALL_FINANCE_BANKS = {
    "equitas small finance bank": "Equitas Small Finance Bank",
    "equitas": "Equitas Small Finance Bank",
    "ujjivan small finance bank": "Ujjivan Small Finance Bank",
    "ujjivan": "Ujjivan Small Finance Bank",
    "jana small finance bank": "Jana Small Finance Bank",
    "jana": "Jana Small Finance Bank",
    "suryoday small finance bank": "Suryoday Small Finance Bank",
    "suryoday": "Suryoday Small Finance Bank",
    "shivalik small finance bank": "Shivalik Small Finance Bank",
    "north east small finance bank": "North East Small Finance Bank",
    "unity small finance bank": "Unity Small Finance Bank",
    "fincare small finance bank": "FinCare Small Finance Bank",
    "fincare": "FinCare Small Finance Bank",
    "gramin bank": "Gramin Bank",
    "pragati bank": "Pragati Bank",
    "dakshin bank": "Dakshin Bank",
    "tripura gramin bank": "Tripura Gramin Bank",
    "assam gramin bank": "Assam Gramin Bank",
    "baroda up bank": "Baroda UP Bank",
    "entity bank": "Entity Bank",
    "unity bank": "Unity Small Finance Bank",
}

COOPERATIVE_BANKS = {
    "udhampur co-operative bank": "Udhampur Co-operative Bank",
    "odisha state cooperative bank": "Odisha State Cooperative Bank",
    "tamilnad state apex bank": "Tamil Nadu State Apex Cooperative Bank",
}

NBFCS_AND_OTHER = {
    "bajaj finserv": "Bajaj Finserv",
    "bajaj": "Bajaj Finserv",
    "muthoot finance": "Muthoot Finance",
    "muthoot": "Muthoot Finance",
    "shriram finance": "Shriram Finance",
    "manappuram finance": "Manappuram Finance",
    "lic housing finance": "LIC Housing Finance",
    "lichousing": "LIC Housing Finance",
    "sbi life": "SBI Life",
    "icici prudential": "ICICI Prudential",
    "paytm payments bank": "Paytm Payments Bank",
    "airtel payments bank": "Airtel Payments Bank",
    "post office": "Post Office / India Post",
    "indiapost": "India Post",
    "nSDL": "NSDL",
    "indian banks' association": "Indian Banks' Association (IBA)",
    "iba": "Indian Banks' Association (IBA)",
}

BANKS = {}
BANKS.update(PUBLIC_SECTOR_BANKS)
BANKS.update(PRIVATE_SECTOR_BANKS)
BANKS.update(SMALL_FINANCE_BANKS)
BANKS.update(COOPERATIVE_BANKS)
BANKS.update(NBFCS_AND_OTHER)

BANK_GROUPS = (
    ("Public Sector Banks", PUBLIC_SECTOR_BANKS),
    ("Private Sector Banks", PRIVATE_SECTOR_BANKS),
    ("Small Finance Banks", SMALL_FINANCE_BANKS),
    ("Co-operative & Payments Banks", COOPERATIVE_BANKS),
    ("NBFCs, Insurers & Other Financial Institutions", NBFCS_AND_OTHER),
)


def bank_options():
    """[(display_name, group_label), ...] — de-duplicated, ordered for the UI."""
    seen = {}
    for group_label, table in BANK_GROUPS:
        for display in table.values():
            if display not in seen:
                seen[display] = group_label
    return [(name, group) for name, group in seen.items()]


# ────────────────────────────────────────────────────────────────────────────
# Applicant residency status  (Section 4 enum)
# ────────────────────────────────────────────────────────────────────────────
RESIDENCY = {
    "resident": {
        "label": "Resident Indian",
        "blurb": "Ordinary resident — taxed in India on global income. No FEMA declaration needed.",
    },
    "nri": {
        "label": "Non-Resident Indian (NRI)",
        "blurb": "Indian citizen resident outside India. FEMA (20) forms and bank-specific NRI declarations apply.",
    },
    "mixed_resident_nri": {
        "label": "Mixed — Resident income, NRI funds",
        "blurb": "Resident by status, but earning or holding money abroad. Both RBI income-tax rules and FEMA remittance rules can apply.",
    },
    "all_nri": {
        "label": "All-NRI household / joint loan",
        "blurb": "Every applicant is an NRI, or the borrower and guarantor are both overseas. Heaviest attestation burden.",
    },
    "not_applicable": {
        "label": "Not applicable",
        "blurb": "Residency does not change the answer for this transaction (e.g. business account for a domestic firm).",
    },
}

RESIDENCY_ORDER = ("resident", "nri", "mixed_resident_nri", "all_nri", "not_applicable")

RESIDENCY_PHRASES = {
    "resident": "a resident Indian applicant (ordinary resident, taxed in India)",
    "nri": "a Non-Resident Indian (NRI) applicant who is resident outside India",
    "mixed_resident_nri": "a mixed household — an ordinary Resident Indian applicant who also earns or holds funds from abroad",
    "all_nri": "an all-NRI household where every applicant is resident outside India",
    "not_applicable": "an applicant whose residency status does not affect the requirement",
}

# ────────────────────────────────────────────────────────────────────────────
# Transaction / product categories
# ────────────────────────────────────────────────────────────────────────────
# Free text is always allowed. This list exists so the picker can suggest
# common starting points and so seed queries can be canonicalised.
CATEGORIES = {
    "home loan": "Home loan",
    "home-loan": "Home loan",
    "education loan": "Education loan",
    "study abroad loan": "Education loan (study abroad)",
    "study-abroad": "Education loan (study abroad)",
    "overseas education loan": "Education loan (study abroad)",
    "personal loan": "Personal loan",
    "vehicle loan": "Vehicle loan",
    "car loan": "Vehicle loan",
    "auto loan": "Vehicle loan",
    "two wheeler loan": "Vehicle loan (two-wheeler)",
    "gold loan": "Gold loan",
    "loan against property": "Loan against property",
    "lap": "Loan against property",
    "loan against fd": "Loan against fixed deposit",
    "fd loan": "Loan against fixed deposit",
    "loan against fixed deposit": "Loan against fixed deposit",
    "fd as guarantee": "FD as guarantee (term deposit as third-party security)",
    "fd as collateral": "FD as guarantee (term deposit as third-party security)",
    "loan against securities": "Loan against securities",
    "las": "Loan against securities",
    "margin loan": "Loan against securities",
    "msme loan": "MSME / business loan",
    "business loan": "MSME / business loan",
    "working capital": "Working capital / overdraft",
    "overdraft": "Overdraft",
    "od against salary": "Overdraft against salary",
    "kcc": "Kisan Credit Card (agricultural)",
    "agricultural loan": "Agricultural / KCC loan",
    "kisan credit card": "Kisan Credit Card (agricultural)",
    "mudra loan": "Mudra loan (Shishu / Kishor / Tarun)",
    "shishu loan": "Mudra loan (Shishu / Kishor / Tarun)",
    "tarun loan": "Mudra loan (Shishu / Kishor / Tarun)",
    "cgtmsme loan": "CGTMSE loan (collateral-free MSME guarantee)",
    "pmegp": "PMEGP loan (government scheme)",
    "nri account": "NRI account opening (NRE / NRO)",
    "nre account": "NRI account opening (NRE / NRO)",
    "nro account": "NRI account opening (NRE / NRO)",
    "property registration": "Property sale deed registration",
    "property sale deed": "Property sale deed registration",
    "sale deed registration": "Property sale deed registration",
    "property mutation": "Property mutation / khata transfer",
    "encumbrance certificate": "Encumbrance certificate",
    "business account": "Business current account opening",
    "business current account": "Business current account opening",
    "current account": "Current account opening",
    "savings account": "Savings account opening",
    "demat account": "Demat account opening",
    "credit card": "Credit card application",
    "credit card against fd": "Credit card against FD",
    "credit card against property": "Credit card against property",
    "joint account": "Joint account opening",
    "minor account": "Minor account opening",
    "ncc": "NCC / fixed deposit opening",
    "fixed deposit": "Fixed deposit opening",
    "recurring deposit": "Recurring deposit opening",
    "ppf account": "PPF / small-savings account opening",
    "post office savings": "Post office savings account",
    "provident fund": "Provident fund / PF claim",
    "epfo claim": "EPFO provident fund claim",
    "esic": "ESIC contribution / claim",
    "insurance claim": "Insurance claim settlement",
    "lic claim": "LIC claim settlement",
    "vehicle transfer": "Vehicle RC transfer / NOC",
    "vehicle registration": "Vehicle registration (RC transfer)",
    "passport": "Passport application / documents",
    "vfs global": "Passport / visa application documents",
    "visa": "Visa application documents",
    "apostille": "Apostille / attestation",
    "attestation": "Apostille / attestation",
    "name change": "Name change / bank records correction",
    "address proof update": "Address proof / KYC update",
    "kyc update": "KYC update at bank",
    "pension": "Pension / EPFO pension claim",
    "will writing": "Will writing / testament",
    "power of attorney": "Power of attorney",
    "partnership deed": "Partnership deed registration",
    "gst registration": "GST registration",
    "company incorporation": "Company incorporation (MCA)",
    "sole proprietorship": "Sole proprietorship registration (Udyam)",
    "fssai license": "FSSAI licence",
    "trade license": "Trade licence",
    "tender document": "Tender / government bid documents",
    "msme udyam": "Udyam / MSME registration",
    "food licence": "FSSAI / food licence",
}

# Transactions where residency cannot change the answer. Keys are compared
# lowercased against the normalised category, so they must be the *display*
# form from CATEGORIES, in lower case.
RESIDENCY_IRRELEVANT = {
    "business current account opening",
    "current account opening",
    "savings account opening",
    "property sale deed registration",
    "property mutation / khata transfer",
    "post office savings account",
    "ppf / small-savings account opening",
    "tender / government bid documents",
    "gst registration",
    "company incorporation (mca)",
    "trade licence",
    "fssai licence",
    "fssai / food licence",
    "encumbrance certificate",
    "minor account opening",
}

# Shown on the picker as quick-start chips. The full category space is open —
# these are starting points, not a menu.
POPULAR_CATEGORIES = [
    "home loan",
    "education loan",
    "study abroad loan",
    "personal loan",
    "loan against property",
    "loan against fd",
    "fd as guarantee",
    "gold loan",
    "vehicle loan",
    "msme loan",
    "nri account",
    "property registration",
    "business account",
    "business loan",
    "loan against securities",
    "overdraft",
    "kcc",
    "mudra loan",
    "savings account",
    "credit card",
]


# ────────────────────────────────────────────────────────────────────────────
# Normalisation
# ────────────────────────────────────────────────────────────────────────────
_NOISE = (" pvt ltd", " private limited", " limited", " ltd", " bank ltd",
          " co", " the ", " branch")


def _clean(text):
    return " ".join((text or "").strip().lower().split())


def normalize_bank(raw):
    """Return a display name for a bank, or '' if blank.

    Unknown banks are passed through with just whitespace collapsed — the
    research agent handles banks we have never heard of.
    """
    key = _clean(raw)
    if not key:
        return ""
    for noise in _NOISE:
        if key.endswith(noise):
            key = key[: -len(noise)].strip()
    if key in BANKS:
        return BANKS[key]
    # Try progressively: drop trailing words ("hdfc bank retail" -> "hdfc bank")
    words = key.split()
    while len(words) > 1:
        words = words[:-1]
        if " ".join(words) in BANKS:
            return BANKS[" ".join(words)]
    return " ".join((raw or "").strip().split())


def bank_group(display_name):
    for group_label, table in BANK_GROUPS:
        if display_name in table.values():
            return group_label
    return "Other"


def normalize_state(raw):
    key = _clean(raw)
    if not key:
        return ""
    if key in STATES:
        return STATES[key]
    words = key.split()
    while len(words) > 1:
        words = words[:-1]
        if " ".join(words) in STATES:
            return STATES[" ".join(words)]
    return " ".join((raw or "").strip().split())


def normalize_category(raw):
    """Canonicalise a transaction type by EXACT alias match only.

    Deliberately no prefix trimming. An earlier version walked backwards
    through the words looking for a known category, which meant
    "gold loan for senior citizens" collapsed to "Gold loan" — silently
    returning a cached answer to a different, more specific question, and
    guaranteeing a cache hit on a question that had never been researched.
    Qualifiers carry the meaning, so anything that is not an exact alias
    passes through untouched and goes to live research.
    """
    key = _clean(raw)
    if not key:
        return ""
    if key in CATEGORIES:
        return CATEGORIES[key]
    return " ".join((raw or "").strip().split())


def normalize_residency(raw):
    key = _clean(raw).replace("-", "_").replace(" ", "_")
    if key in RESIDENCY:
        return key
    aliases = {
        "resident_indian": "resident", "resident_india": "resident",
        "residing_in_india": "resident", "domiciled_in_india": "resident",
        "non_resident_indian": "nri", "nonresident_indian": "nri",
        "nri_indian": "nri", "nra": "nri", "non_resident": "nri",
        "nri_oio": "nri", "person_of_indian_origin": "nri",
        "mixed": "mixed_resident_nri", "resident_nri_mixed": "mixed_resident_nri",
        "both": "mixed_resident_nri", "nri_and_resident": "mixed_resident_nri",
        "all_nris": "all_nri", "nri_joint": "all_nri", "nri_family": "all_nri",
        "n/a": "not_applicable", "na": "not_applicable", "none": "not_applicable",
        "not_relevant": "not_applicable", "irrelevant": "not_applicable",
    }
    return aliases.get(key, "resident")


def residency_label(key):
    return RESIDENCY.get(key, {}).get("label", key)


def residency_phrase(key):
    return RESIDENCY_PHRASES.get(key, RESIDENCY_PHRASES["resident"])


def suggest(raw, table, limit=6):
    """Substring suggestions for the free-text inputs, best-match first."""
    key = _clean(raw)
    if not key:
        return []
    scored = []
    for candidate in sorted(set(table.values())):
        c = candidate.lower()
        if c.startswith(key):
            scored.append((0, len(c), candidate))
        elif key in c:
            scored.append((1, len(c), candidate))
    scored.sort()
    return [s[2] for s in scored[:limit]]
