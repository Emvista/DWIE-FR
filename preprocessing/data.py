
"""File containing constants."""

# Path
PATH_DWIE = "data/DWIE/"
PATH_DWIE_BENCHMARK = PATH_DWIE + "benchmark"
PATH_DWIE_COREF_WL = PATH_DWIE + "COREF/WL/dwie_data.json"
PATH_DWIE_COREF_WL_PREDICTIONS = PATH_DWIE + "COREF/WL"
PATH_DWIE_DATA = PATH_DWIE + "annotated_texts"
PATH_DWIE_GROUNDTRUTH_KBS = PATH_DWIE + "groundtruth"
PATH_DWIE_INIT_KB = PATH_DWIE + "init_kb.pickle"

PATH_DWIE_LINK_MERIT = "data/models/LINK/MERIT/"
PATH_DWIE_LINK_MERIT_CLASSIFIER = "data/models/LINK/MERIT/weights/classifier_dwie.pt"
PATH_DWIE_LINK_MERIT_PREDS = "data/DWIE/LINK/MERIT/predictions"
PATH_DWIE_LINK_WARM_CONTENT = PATH_DWIE_LINK_MERIT + "warm_content.pickle"

PATH_DWIE_NER_FLAIR = PATH_DWIE + "/home/sylvain/POPCORN/DWIE/data/CoNLL_format"
PATH_DWIE_NER_FLAIR_MODEL = (
    PATH_DWIE_NER_FLAIR + "taggers/sota-ner-flair/final-model.pt"
)
PATH_DWIE_NER_FLAIR_TEST = PATH_DWIE_NER_FLAIR + "predictions"
PATH_DWIE_RE_ATLOP = PATH_DWIE + "RE/ATLOP"
PATH_DWIE_RE_ATLOP_PREDS = PATH_DWIE_RE_ATLOP + "/predictions"
PATH_DWIE_TEST_FILES = PATH_DWIE + "test_files.pickle"

PATH_FLAIR_DATA = "data/models/NER/Flair/"
PATH_FLAIR_CHECKPOINT = PATH_FLAIR_DATA + "checkpoint.pt"
PATH_FLAIR_BASE_MODEL = PATH_FLAIR_DATA + "taggers/sota-ner-flair"


SENTENCE_END_CHAR = [".", '"', "?", "!"]

PRONOUNS = [
    "they",
    "he",
    "her",
    "his",
    "him",
    "their",
    "them",
    "we",
    "it",
    "i",
    "our",
    "its",
    "this",
    "you",
    "the",
]

UNWANTED_ENT_TYPES = [
    "footer",
    "none",
    "skip",
    "time",
    "money",
    "value",
    "role",
    "religion",
    "religion-x",
]

UNWANTED_TAG_TYPES = [
    "topic",
    "iptc",
    "gender",
    "sport",
    "slot",
    "meta",
    "sector",
    "sport_event",
    "policy",
]
DWIE_NER_TYPES = {
    "entity": 0,
    "language": 1,
    "location": 1,
    "waterbody": 2,
    "regio": 2,
    "facility": 2,
    "gpe": 2,
    "gpe0": 3,
    "gpe2": 3,
    "gpe1": 3,
    "organization": 1,
    "education_org": 2,
    "ngo": 2,
    "media": 2,
    "igo": 2,
    "so": 3,
    "party": 2,
    "company": 2,
    "sport_team": 2,
    "governmental_organisation": 2,
    "agency": 3,
    "armed_movement": 2,
    "person": 1,
    "deity": 2,
    "activist": 2,
    "journalist": 2,
    "gov_per": 2,
    "employee": 2,
    "politician": 2,
    "head_of_state": 3,
    "head_of_gov": 3,
    "minister": 3,
    "police_per": 2,
    "military_personnel": 2,
    "sport_coach": 2,
    "sport_player": 2,
    "artist": 2,
    "politics_per": 2,
    "manager": 2,
    "offender": 2,
    "misc": 1,
    "product": 2,
    "award": 2,
    "treaty": 2,
    "object": 2,
    "work_of_art": 2,
    "event": 1,
    "war": 2,
    "competition": 2,
    "sport_competition": 3,
    "ethnicity": 1,
    "other": 0,
    "loc-x": 1,
    "gpe0-x": 1,
    "gpe1-x": 1,
}

DWIE_UNLINKABLE_TYPES = ["gpe1-x", "gpe0-x", "loc-x"]
DWIE_NER_ONTOLOGY = {
    "entity": ["entity"],
    "language": ["language", "entity"],
    "location": ["location", "entity"],
    "loc": ["loc", "location", "entity"],
    "waterbody": ["waterbody", "location", "entity"],
    "facility": ["facility", "location", "entity"],
    "gpe": ["gpe", "location", "entity"],
    "gpe0": ["gpe0", "gpe", "location", "entity"],
    "gpe1": ["gpe1", "gpe", "location", "entity"],
    "gpe2": ["gpe2", "gpe", "location", "entity"],
    "regio": ["regio", "location", "entity"],
    "organization": ["organization", "entity"],
    "ngo": ["ngo", "organization", "entity"],
    "education_org": ["education_org", "organization", "entity"],
    "media": ["media", "organization", "entity"],
    "sport_team": ["sport_team", "organization", "entity"],
    "armed_mov": ["armed_movement", "organization", "entity"],
    "governmental_organisation": [
        "governmental_organisation",
        "organization",
        "entity",
    ],
    "agency": [
        "agency",
        "governmental_organisation",
        "organization",
        "entity",
    ],
    "armed_movement": ["armed_movement", "organization", "entity"],
    "company": ["company", "organization", "entity"],
    "igo": ["igo", "organization", "entity"],
    "so": ["so", "organization", "entity", "igo"],
    "party": ["party", "organization", "entity"],
    "person": ["person", "entity"],
    "deity": ["deity", "person", "entity"],
    "sport_player": ["sport_player", "person", "entity"],
    "artist": ["artist", "person", "entity"],
    "politics_per": ["politics_per", "person", "entity"],
    "sport_coach": ["sport_coach", "person", "entity"],
    "police_per": ["police_per", "person", "entity"],
    "military_personnel": ["military_personnel", "person", "entity"],
    "manager": ["manager", "person", "entity"],
    "offender": ["offender", "person", "entity"],
    "employee": ["employee", "person", "entity"],
    "gov_per": ["gov_per", "person", "entity"],
    "journalist": ["journalist", "person", "entity"],
    "activist": ["activist", "person", "entity"],
    "politician": ["politician", "person", "entity"],
    "head_of_state": ["head_of_state", "person", "entity", "politician"],
    "head_of_gov": ["head_of_gov", "person", "entity", "politician"],
    "minister": ["minister", "person", "entity", "politician"],
    "ethnicity": ["ethnicity", "entity"],
    "event": ["event", "entity"],
    "war": ["event", "war"],
    "competition": ["competition", "event", "entity"],
    "sport_competition": ["sport_competition", "competition", "event", "entity"],
    "misc": ["misc", "entity"],
    "product": ["product", "misc", "entity"],
    "award": ["award", "misc", "entity"],
    "work_of_art": ["work_of_art", "misc", "entity"],
    "object": ["object", "misc", "entity"],
    "treaty": ["treaty", "misc", "entity"],
    "other": ["other"],
    "gpe0-x": ["gpe0-x", "other"],
    "gpe1-x": ["gpe1-x", "other"],
    "loc-x": ["loc-x", "other"],
}

"""
DWIE_NER_TYPES = {
    "entity",
    "person",
    "work_of_art",
    "music_title",
    "misc",
    "organization",
    "armed_movement",
    "music_band",
    "other",
    "sport_org",
    "sport_player",
    "event",
    "war",
    "artist",
    "writer",
    "musician",
    "politician",
    "gpe",
    "gpe0",
    "gpe1",
    "gpe2",
    "gpe0-x",
    "party",
    "igo",
    "manager",
    "regio",
    "location",
    "company",
    "media",
    "technology",
    "business_per",
    "ideology",
    "facility",
    "offender",
    "advisor",
    "loc-x",
    "tv_award",
    "culture_misc",
    "treaty",
    "celestial_loc",
    "journalist",
    "ethnicity",
    "religion",
    "religion-x",
    "film_title",
    "criminal_org",
    "police_per",
    "head_of_state",
    "health_facility",
    "policy_institute",
    "politics_per",
    "district",
    "loc",
    "so",
    "science_per",
    "teacher",
    "education_org",
    "sport_team",
    "gpe1-x",
    "governmental_organisation",
    "minister",
    "island",
    "competition",
    "military_alliance",
    "head_of_gov",
    "sport_competition",
    "victim",
    "agency",
    "project",
    "award",
    "army",
    "music_band",
    "book_title",
    "language",
    "gov_per",
    "justice_per",
    "judge",
    "festive_event",
    "sport_head",
    "ngo",
    "ministry",
    "activist",
    "deity",
    "court",
    "politician_regional",
    "filmmaker",
    "health_disease",
    "sport_facility",
    "sport_coach",
    "military_facility",
    "politics_facility",
    "military_personnel",
    "royalty",
    "religion_misc",
    "history",
    "business_org",
    "business_misc",
    "clergy",
    "actor",
    "object",
    "character",
    "protest",
    "union",
    "researcher",
    "holiday",
    "waterbody",
    "research_center",
    "movement",
    "report",
    "politician_local",
    "police",
    "gpe2-x",
    "military_rebel",
    "religious_event",
    "education_student",
    "health_per",
    "product",
    "prison",
    "employee",
    "religion_org",
    "sport_award",
    "tv_title",
    "business_facility",
    "justice_misc",
    "street",
    "culture_per",
    "union_rep",
    "military_equipment",
    "film_award",
    "politician_national",
    "summit_meeting",
    "culture_facility",
    "justice_facility",
    "religion_facility",
    "advocacy",
    "politics_org",
    "education_per",
    "culture_title",
    "festival",
    "theatre_title",
    "military_mission",
    "market_index",
    "concept",
    "education_study",
    "scandal",
    "research_journal",
    "filmfestival",
    "union_member",
    "politics_misc",
    "incident",
    "trade_fair",
    "health_org",
    "mountain",
    "species",
    "exhibition_title",
    "book_award",
    "market_exchange",
    "politic_event",
    "storm",
    "relative",
    "case",
    "brand",
    "culture_org",
    "musical_title",
    "health_drug",
    "union_head",
    "politics_event",
    "police_org",
    "justice_org",
    "education_facility",
    "sport_referee",
}
"""


DWIE_NER_TYPES = {
  "Sport_referee":{
    "Niv":2
  },
  "Culture_per":{
    "Niv":2
  },
  "Case":{
    "Niv":2
  },
  "Religion":{
    "Niv":2
  },
  "Religion-x":{
    "Niv":2
  },
  "Competition":{
    "Niv":2
  },
  "Sport_competition":{
    "Niv":3
  },
  "Igo":{
    "Niv":2
  },
  "Misc":{
    "Niv":1
  },
  "Festive_event":{
    "Niv":2
  },
  "Gpe0":{
    "Niv":3
  },
  "Agency":{
    "Niv":3
  },
  "Mountain":{
    "Niv":2
  },
  "Manager":{
    "Niv":2
  },
  "Gpe1-x":{
    "Niv":3
  },
  "Education_per":{
    "Niv":2
  },
  "Health_per":{
    "Niv":2
  },
  "Culture_facility":{
    "Niv":3
  },
  "Offender":{
    "Niv":2
  },
  "Sport_award":{
    "Niv":3
  },
  "So":{
    "Niv":3
  },
  "Filmmaker":{
    "Niv":3
  },
  "Brand":{
    "Niv":2
  },
  "Book_title":{
    "Niv":3
  },
  "Business_org":{
    "Niv":2
  },
  "Head_of_gov":{
    "Niv":3
  },
  "Police_org":{
    "Niv":2
  },
  "Object":{
    "Niv":2
  },
  "Species":{
    "Niv":2
  },
  "Politician_national":{
    "Niv":3
  },
  "Storm":{
    "Niv":2
  },
  "Culture_misc":{
    "Niv":2
  },
  "Book_award":{
    "Niv":3
  },
  "Education_facility":{
    "Niv":3
  },
  "Military_facility":{
    "Niv":3
  },
  "Gpe2-x":{
    "Niv":3
  },
  "Report":{
    "Niv":2
  },
  "Police":{
    "Niv":1
  },
  "Army":{
    "Niv":3
  },
  "Scandal":{
    "Niv":2
  },
  "Relative":{
    "Niv":2
  },
  "Military_mission":{
    "Niv":2
  },
  "Journalist":{
    "Niv":2
  },
  "Advocacy":{
    "Niv":2
  },
  "Military_equipment":{
    "Niv":2
  },
  "Party":{
    "Niv":2
  },
  "Sport_head":{
    "Niv":2
  },
  "Politician_local":{
    "Niv":3
  },
  "Event":{
    "Niv":1
  },
  "Gpe1":{
    "Niv":3
  },
  "Justice_per":{
    "Niv":2
  },
  "Health_facility":{
    "Niv":3
  },
  "Person":{
    "Niv":1
  },
  "Religion_facility":{
    "Niv":3
  },
  "Religious_event":{
    "Niv":2
  },
  "Culture_title":{
    "Niv":2
  },
  "Award":{
    "Niv":2
  },
  "Union":{
    "Niv":2
  },
  "Education_org":{
    "Niv":2
  },
  "Protest":{
    "Niv":2
  },
  "Sport_team":{
    "Niv":2
  },
  "Music_band":{
    "Niv":2
  },
  "Royalty":{
    "Niv":2
  },
  "Gpe2":{
    "Niv":3
  },
  "Sport_player":{
    "Niv":2
  },
  "Business_misc":{
    "Niv":2
  },
  "Ministry":{
    "Niv":3
  },
  "Facility":{
    "Niv":2
  },
  "Market_exchange":{
    "Niv":2
  },
  "Education_study":{
    "Niv":2
  },
  "Company":{
    "Niv":2
  },
  "Education_student":{
    "Niv":2
  },
  "Artist":{
    "Niv":2
  },
  "Politics_event":{
    "Niv":2
  },
  "Musical_title":{
    "Niv":3
  },
  "Gpe0-x":{
    "Niv":3
  },
  "Politics_org":{
    "Niv":2
  },
  "Island":{
    "Niv":2
  },
  "Film_award":{
    "Niv":3
  },
  "Regio":{
    "Niv":2
  },
  "Minister":{
    "Niv":3
  },
  "Celestial_loc":{
    "Niv":2
  },
  "Research_center":{
    "Niv":2
  },
  "War":{
    "Niv":2
  },
  "History":{
    "Niv":2
  },
  "Researcher":{
    "Niv":2
  },
  "Summit_meeting":{
    "Niv":2
  },
  "Sport_org":{
    "Niv":2
  },
  "Union_head":{
    "Niv":2
  },
  "Technology":{
    "Niv":2
  },
  "Armed_movement":{
    "Niv":2
  },
  "Sport_facility":{
    "Niv":3
  },
  "Union_rep":{
    "Niv":2
  },
  "Police_per":{
    "Niv":2
  },
  "Loc":{
    "Niv":2
  },
  "Exhibition_title":{
    "Niv":2
  },
  "Religion_misc":{
    "Niv":2
  },
  "Employee":{
    "Niv":2
  },
  "Prison":{
    "Niv":3
  },
  "Criminal_org":{
    "Niv":2
  },
  "District":{
    "Niv":2
  },
  "Military_alliance":{
    "Niv":3
  },
  "Ngo":{
    "Niv":2
  },
  "Filmfestival":{
    "Niv":2
  },
  "Head_of_state":{
    "Niv":2
  },
  "Character":{
    "Niv":2
  },
  "Governmental_organisation":{
    "Niv":2
  },
  "Health_drug":{
    "Niv":2
  },
  "Business_facility":{
    "Niv":3
  },
  "Union_member":{
    "Niv":2
  },
  "Deity":{
    "Niv":2
  },
  "Advisor":{
    "Niv":2
  },
  "Film_title":{
    "Niv":3
  },
  "Politician_regional":{
    "Niv":3
  },
  "Ethnicity":{
    "Niv":1
  },
  "Military_personnel":{
    "Niv":2
  },
  "Market_index":{
    "Niv":2
  },
  "Street":{
    "Niv":2
  },
  "Project":{
    "Niv":2
  },
  "Trade_fair":{
    "Niv":2
  },
  "Court":{
    "Niv":2
  },
  "Gov_per":{
    "Niv":2
  },
  "Victim":{
    "Niv":2
  },
  "Culture_org":{
    "Niv":2
  },
  "Judge":{
    "Niv":2
  },
  "Politician":{
    "Niv":2
  },
  "Military_rebel":{
    "Niv":2
  },
  "Incident":{
    "Niv":2
  },
  "Tv_award":{
    "Niv":3
  },
  "Organization":{
    "Niv":1
  },
  "Research_journal":{
    "Niv":2
  },
  "Politics_misc":{
    "Niv":2
  },
  "Theatre_title":{
    "Niv":3
  },
  "Actor":{
    "Niv":3
  },
  "Justice_org":{
    "Niv":2
  },
  "Holiday":{
    "Niv":2
  },
  "Health_org":{
    "Niv":2
  },
  "Sport_coach":{
    "Niv":2
  },
  "Movement":{
    "Niv":2
  },
  "Teacher":{
    "Niv":2
  },
  "Festival":{
    "Niv":2
  },
  "Language":{
    "Niv":1
  },
  "Tv_title":{
    "Niv":3
  },
  "Health_disease":{
    "Niv":2
  },
  "Loc-x":{
    "Niv":2
  },
  "Musician":{
    "Niv":3
  },
  "Concept":{
    "Niv":2
  },
  "Science_per":{
    "Niv":2
  },
  "Activist":{
    "Niv":2
  },
  "Entity":{
    "Niv":0
  },
  "Value":{
    "Niv":0
  },
  "Money":{
    "Niv":1
  },
  "Role":{
    "Niv":1
  },
  "Time":{
    "Niv":1
  },
  "Other":{
    "Niv":0
  },
  "Footer":{
    "Niv":1
  },
  "Skip":{
    "Niv":1
  },
  "Waterbody":{
    "Niv":2
  },
  "Politics_facility":{
    "Niv":3
  },
  "Gpe":{
    "Niv":2
  },
  "Treaty":{
    "Niv":2
  },
  "Work_of_art":{
    "Niv":2
  },
  "Business_per":{
    "Niv":2
  },
  "Product":{
    "Niv":2
  },
  "Music_title":{
    "Niv":3
  },
  "Location":{
    "Niv":1
  },
  "Justice_misc":{
    "Niv":2
  },
  "Policy_institute":{
    "Niv":2
  },
  "Ideology":{
    "Niv":1
  },
  "Writer":{
    "Niv":3
  },
  "Politics_per":{
    "Niv":2
  },
  "Religion_org":{
    "Niv":2
  },
  "Media":{
    "Niv":2
  },
  "Clergy":{
    "Niv":2
  }
}
