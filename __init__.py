# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.
# TODO: Handle game in progress with separate "live" dialog - "The {{team}} are {{winning|losing|tied}} at {{team_score}} to {{opponent_score}} {{against|with}} the {{opponent}}"
# TODO: Handle games on past days by adding "yesterday or Monday or whatever makes sense"
# TODO: Handle beginning of month problem (see def latest_game(self):)
# TODO: Handle games on the day but which haven't started yet (currently reports as 0-0 tie but should say "the game hasn't started yet" or just report latest final score)
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
        today = str(date.today())
        year = int(today[0:4])
        month = int(today[5:7])
        day = int(today[8:])
        return year, month, day

    def latest_game(self):
        # ISSUE: subtracting of days should happen while getting current date otherwise beginning of months are bad
        # ISSUE: long load times/loops during offseason while looping back/checking for latest game? - possible solution: get important dates from mlbgame and report end of season standing or record during offseason instead?
        self.game = []
        counter = 0
        while self.game == []:
            year = self.get_date()[0]
            month = self.get_date()[1]
            day = self.get_date()[2]
            self.game = mlbgame.day(year, month, day-counter, home=self.team, away=self.team)
            counter += 1

    def get_result(self):
        self.latest_game()
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
            self.result = "won"
        if self.team_score < self.opponent_score:
            self.result = "lost"
        else:   # Assume tied
            self.result = "tied"

    @ intent_handler(IntentBuilder("GetScoreIntent").require("Team").require("Score").build())
    def handle_score_intent(self, message):
        self.team = message.data.get("Team")
        self.get_result()
        # "The {{team}} {{result}} {{team_score}} to {{opponent_score}} against the {{opponent}}"
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

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return ScoreSkill()