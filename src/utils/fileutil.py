import json

# Loads normal & DAO proposals (ticker -> id) dict
# This needs work for ensuring we dont miss any. Save last X in a list?
def load_proposals_from_file(filename: str) -> dict:    
    with open(filename, 'r') as f:
        proposals = json.load(f)       
    return proposals

def save_proposals(filename: str, proposals: dict) -> None:
    if len(proposals) > 0:
        with open(filename, 'w') as f:
            json.dump(proposals, f)

def update_proposal_value(ticker: str, newPropNumber: int, proposals: dict):    
    proposals[ticker] = newPropNumber
    save_proposals()
    return proposals