allroles = {
    "Jailor": ["Jailor"],
    "TI": ["Investigator", "Policeman", "Witness", "Psychologist"],
    "TP": ["Doctor", "Spellcaster"],
    "TK": ["Vigilante", "Veteran"],
    "TS": ["Mayor", "Medium", "Tranquilizer"],
    "RT": ["Investigator", "Policeman", "Witness", "Psychologist", "Doctor", "Spellcaster", "Vigilante", "Veteran", "Mayor", "Tranquilizer"],
    "MK": ["Mafioso"],
    "MS": ["Framer", "Consort", "Consigliere", "Janitor"],
    "NE": ["Jester", "Executioner"]
}

role_to_alignment = {
    "Jailor": "TK",
    "Investigator": "TI",
    "Policeman": "TI",
    "Witness": "TI",
    "Psychologist": "TI",
    "Doctor": "TP",
    "Spellcaster": "TP",
    "Vigilante": "TK",
    "Veteran": "TK",
    "Mayor": "TS",
    "Medium": "TS",
    "Tranquilizer": "TS",
    "Mafioso": "MK",
    "Framer": "MS",
    "Consort": "MS",
    "Consigliere": "MS",
    "Janitor": "MS",
    "Jester": "NE",
    "Executioner": "NE"
}

rolelist = ["Jailor", "TI", "TP", "TK", "TS", "RT", "RT", "MK", "MS", "NE"]

required_player_count = 2