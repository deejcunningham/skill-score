# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.
# TODO: Handle games on the day but which haven't started yet (currently reports as 0-0 tie but should say "the game is scheduled to start at self.game_start_time")
# TODO: Handle beginning of month problem (see def latest_game(self):)
# TODO: Handle games on past days by adding "yesterday or Monday or whatever makes sense" -- make sure to see how intents are prioritized and code accordingly
# TODO: Figure out stop method
# TODO: Handle offseason?
# TODO: Add more specific information (inning?)
# TODO: Add other sports

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from mycroft import intent_handler

from datetime import date
import mlbgame

# __author__ and LOGGER may not be required...?
__author__ = 'permanentlytemporary'
# LOGGER = getLogger(__name__)

class ScoreSkill(MycroftSkill):

    def __init__(self):
        super(ScoreSkill, self).__init__(name="ScoreSkill")

    def get_date(self):
        self.date = str(date.today())
        self.year = int(self.date[0:4])
        self.month = int(self.date[5:7])
        self.day = int(self.date[8:])

    def get_game(self):
        # ISSUE: subtracting of days makes beginning of months bad - handle by checking for valid game on that date and stating "no game on that date" if none
        # ISSUE: long load times/loops during offseason while looping back/checking for latest game? - possible solution: get important dates from mlbgame and report end of season standing or record during offseason instead?
        self.game = []
        counter = 0
        try:    # checks to see if the date was set by the intent handler method
            self.date
        except AttributeError:   # if not, gets todays date
            self.get_date()
        else:   # if yes, should do nothing
            pass
        while self.game == []:
            self.game = mlbgame.day(self.year, self.month, self.day-counter, home=self.team, away=self.team)
            counter += 1

    def get_result(self):
        self.get_game()
        # Separates out team names and scores
        result = str(self.game[0]).split()
        team_1 = result[0]
        team_1_score = int(''.join(i for i in result[1] if i.isdigit()))
        team_2 = result[3]
        team_2_score = int(''.join(i for i in result[4] if i.isdigit()))

        # Assigns team_1 or team_2 to team and opponent
        if team_1 == self.team:
            self.team = team_1
            self.team_score = team_1_score
            self.opponent = team_2
            self.opponent_score = team_2_score
        else:
            self.team = team_2
            self.team_score = team_2_score
            self.opponent = team_1
            self.opponent_score = team_1_score

        # Compare scores for actual result
        if self.team_score > self.opponent_score:
            self.result = "winning"
        if self.team_score < self.opponent_score:
            self.result = "losing"
        else:   # Assume tied
            self.result = "tied"

    # TODO: Add Date.voc with regex for handling dates in past
    # @ intent_handler(IntentBuilder("GetPastScoreIntent").require("Team").require("Score").require("Date").build())
    # def handle_past_score_intent(self, message):
    #     self.team = message.data.get("Team")
    #     # Add parser for date speech? (or is that sort of done by Date.voc + STT?) and set self.year, self.month, self.day accordingly
    #     # Should the parsing be handled by self.get_date()?
    #     self.date = message.data.get("Date")
    #     # Add a past_score.dialog - check if I can use single dialog with optional data?
    #     # "The {{team}} {{result}} {{team_score}} to {{opponent_score}} against the {{opponent}} on {{date}}"
    #     self.speak_dialog("past_score", data={"team": self.team, "result": self.result, "team_score": self.team_score, "opponent_score": self.opponent_score, "opponent": self.opponent, "date": self.date})

    @ intent_handler(IntentBuilder("GetLiveScoreIntent").require("Team").require("Score").build())
    def handle_live_score_intent(self, message):
        self.team = message.data.get("Team")
        # TODO: check to see if a game is in progress
        self.get_result()
        # "The {{team}} are {{result}} {{team_score}} to {{opponent_score}} against the {{opponent}}"
        self.speak_dialog("score", data={"team": self.team, "result": self.result, "team_score": self.team_score, "opponent_score": self.opponent_score, "opponent": self.opponent})

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    pass
    #    return False

def create_skill():
    return ScoreSkill()