from pupa.scrape import Jurisdiction, Organization
from .people import SeattlePersonScraper
# TODO: Implement these scrapers
# from .events import SeattleEventScraper
# from .bills import SeattleBillScraper
# from .vote_events import SeattleVoteEventScraper

class Seattle(Jurisdiction):
    division_id = "ocd-division/country:us/state:wa/place:seattle"
    classification = "legislature"
    name = "Seattle City Council"
    url = "https://www.seattle.gov/council"

    scrapers = {
        "people": SeattlePersonScraper,
        # TODO: Add these back when implemented
        # "events": SeattleEventScraper,
        # "bills": SeattleBillScraper,
        # "vote_events": SeattleVoteEventScraper,
    }
    
    def get_organizations(self):
        org = Organization(
            name="Seattle City Council",
            classification="legislature"
        )

        # Add district seats (7 districts)
        for i in range(1, 8):
            org.add_post(
                label=f"District {i}",
                role="Councilmember"
            )

        # Add at-large positions (2 positions)
        for i in range(8, 10):
            org.add_post(
                label=f"Position {i}",
                role="Councilmember"
            )

        yield org