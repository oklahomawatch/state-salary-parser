GARBAGE_STRINGS = (
    ("  ", " "),
    ("WORKER'S COMP", "WORKERS COMP"),
    ("OKLA.", "OKLAHOMA"),
    ("OF OK\r\n", "OF OKLAHOMA"),
    ("BD. OF", "BOARD OF"),
    ("HCM\r\n", "HUMAN CAPITAL MANAGEMENT"),
    (" BD\r\n", " BOARD"),
    ("OK COMMISSION", "OKLAHOMA COMMISSION"),
    ("STATEBOARD", "STATE BOARD"),
    ("ENDMT", "ENDOWMENT"),
    ("SERV\r\n", "SERVICES"),
    ("LIC.", "LICENSED"),
    ("OK.", "OKLAHOMA"),
    ("SUPV.", "SUPERVISION"),
    ("UNIV.", "UNIVERSITY"),
    ("ST.", "STATE"),
    ("SERV.", "SERVICE"),
    ("SYS.", "SYSTEM"),
    ("ST.BOARD", "STATE BOARD"),
    ("OSU-", "OSU "),
    ("DEV.", "DEVELOPMENT"),
    ("AUTH.", "AUTHORITY"),
    ("EDUCATION AUTH-", "EDUCATION AUTHORITY "),
    ("ST. BOARD", "STATE BOARD"),
    ("VETERINARY MED. EXAM.", "VETERINARY MEDICAL EXAMINERS"),
    ("MATH.", "MATHEMATICS"),
    ("CNTR.", "CENTER"),
    ("ADVANC.", "ADVANCEMENT"),
    ("EDUC.", "EDUCATION"),
    ("S. E. ", "SOUTHEAST "),
    ("TRNG.", "TRAINING"),
    ("ENFC.", "ENFORCEMENT"),
    ("COMM.", "COMMISSION"),
    (" ED. ", " EDUCATION "),
    ("ENFORCE.", "ENFORCEMENT"),
    ("DEPT.", "DEPARTMENT"),
    ("ST BD ", "STATE BOARD "),
    ("PENS.", "PENSION"),
    ("RET.", "RETIREMENT"),
    ("ORG.", "ORGANIZATION"),
    ("BEV.", "BEVERAGE"),
    ("Okla.", "OKLAHOMA"),
    ("OSTEOPATHIC MED.", "OSTEOPATHIC MEDICINE"),
    ("OSTEOPATHIC EXAM.\r\n", "OSTEOPATHIC EXAMINERS"),
    ("MED. EXAM.", "MEDICAL EXAMINER"),
    ("EXAM.", "EXAMINER"),
    ("NATIVE AMER.CULTURAL", "NATIVE AMERICAN CULTURAL"),
    ("BD OF LIC ", "BOARD OF LICENSURE FOR "),
    ("DRUG COUNS", "DRUG COUNSELING"),
    ("DCAM-OMES", "DIVISION OF CAPITAL ASSETS MANAGEMENT, OFFICE OF "
        "MANAGEMENT AND ENTERPRISE SERVICES"),
    ("BOARD OF MED. LICENSURE", "BOARD OF MEDICAL LICENSURE"),
    ("PROF. ENGI. ", "PROFESSIONAL ENGINEERING "),
    ("LP GAS RES, MRKT. & SAFETY COMMISSION", "LP GAS RESEARCH, MARKETING "
        "AND SAFETY COMMISSION"),
    ("DEPT ", "DEPARTMENT "),
    ("WORKER'S COMP.", "WORKER'S COMP "),
    ("SOER - ", ""),
    ("UNIVERSITYOF", "UNIVERSITY OF"),
    ("A & M", "A&M"),
    ("BOARD OF EXAM.", "BOARD OF EXAMINERS"),
    ("LT CARE ADMIN.", "LONG-TERM CARE ADMINISTRATION"),
    ("CHIROPRACTIC EXAM.", "CHIROPRACTIC EXAMINERS"),
    ("PROF. PRAC. PLAN.", "PROFESSIONAL PRACTICE PLANNING"),
    ("UNIVERSITY OF OK ", "UNIVERSITY OF OKLAHOMA "),
    ("BOARD OF EXAMINER ", "BOARD OF EXAMINERS "),
    ("J. M. ", "J.M. "),
    ("BOARD OF CHEM. TEST ALCOHOL/DRUG", "BOARD OF TESTS FOR ALCOHOL AND "
        "DRUG INFLUENCE"),
    ("S. W. ", "SOUTHWEST "),
    ("PRIV.", "PRIVATE"),
    ("N. E. ", "NORTHEAST "),
    ("OKLAHOMA BUREAU OF NARCOTICS AND DANGEROUS\r\n", "OKLAHOMA BUREAU OF"
        " NARCOTICS AND DANGEROUS DRUGS"),
    ("STATE & EDUCATION EMP. GRP. INS. BD.", "STATE AND EDUCATION EMPLOYEES "
        "GROUP INSURANCE BOARD"),
    ("\r\n", ""),
    ("PYMTS", "PAYMENTS"),
    ("ASSTCE.", "ASSISTANCE"),
    ("ASSTCE", "ASSISTANCE"),
    ("PAYMENTS(PR ONLY\r\n", "PAYMENTS (PR ONLY)"),
    ("H.E.", "HIGHER EDUCATION"),
    ("SANTA CLAUSE COMMISSION", "SANTA CLAUS COMMISSION"),
    ("AGCY.", "AGENCY"),
    ("AGCY", "AGENCY"),
    ("PROG.", "PROGRAMS"),
    ("BLDGS.", "BUILDINGS"),
    ("STRUCT.", "STRUCTURES"),
    ("CONSTR. & RENOV.", "CONSTRUCTION & RENOVATION"),
    ("WIC - ", ""),
    ("SVCS.", "SERVICES"),
    (" PYMT ", " PAYMENT "),
    (", ...", ""),
    (" ...", ""),
    ("\r\n", "")
)

EDU_TITLES = [
    "HIGHER ED POSITION",
    "HE POSITION"
]

EDU_AGENCIES = [
    "623",
    "010",
    "011",
    "012",
    "013",
    "014",
    "015",
    "016",
    "490",
    "758",
    "660",
    "530",
    "770",
    "831",
    "773",
    "420",
    "610",
    "531",
    "825",
    "108",
    "241",
    "100",
    "041",
    "760",
    "240",
    "761",
    "633",
    "461",
    "165",
    "505",
    "765",
    "605",
    "150",
    "606",
    "600",
    "750",
    "230",
    "470",
    "325",
    "775",
    "771",
    "665",
    "485",
    "480",
    "120",
    "LU0",
    "CSC",
    "NEO",
    "CU0",
    "OSU",
    "OU0",
    "PSU",
    "607"
]

EXTRA_EDU_AGENCIES = {
    "LU0": "LANGSTON UNIVERSITY (RETIREE)",
    "CSC": "CONNORS STATE COLLEGE (RETIREE)",
    "NEO": "NORTHEASTERN OKLAHOMA (RETIREE)",
    "CU0": "CAMERON UNIVERSITY (RETIREE)",
    "OSU": "OSU (RETIREE)",
    "OU0": "OU (RETIREE)",
    "PSU": "PANHANDLE STATE UNIVERSITY (RETIREE)",
    "607": "ARDMORE HIGHER EDUCATION CENTER (RETIREE)"
}

EXTRA_PAYROLL_CODES = {
    "1130": "EDUCATION LOAN INCENTIVES"
}
