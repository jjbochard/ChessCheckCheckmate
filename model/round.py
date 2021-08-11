import json
from datetime import datetime


class Round:
    def __init__(
        self,
        name,
        start_date,
        current_round,
        status_round,
        end_date=None,
        list_of_match=[],
    ):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.list_of_match = list_of_match
        self.current_round = current_round
        self.status_round = status_round

    @classmethod
    def create_round(cls):
        current_round = 1
        name = "Round " + str(current_round)
        start_date = json.dumps(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        status_round = "pending"
        return Round(name, start_date, current_round, status_round)

    def end_round(round_table):
        round_table.update(
            {"status_round": "finished"},
            doc_ids=[round_table.all()[-1].doc_id],
        )
        round_table.update(
            {
                "end_date": json.dumps(
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"), default=str
                )
            },
            doc_ids=[round_table.all()[-1].doc_id],
        )
