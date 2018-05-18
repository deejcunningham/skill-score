# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

from datetime import date
import mlbgame

# __author__ and LOGGER may not be required...?
__author__ = 'permanentlytemporary'
LOGGER = getLogger(__name__)

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

class ScoreSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(ScoreSkill, self).__init__(name="ScoreSkill")
        # Initialize working variables used within the skill.

    def get_date(self):
        today = str(date.today())
        year = int(today[0:4])
        month = int(today[5:7])
        day = int(today[8:0])
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
        result = str(self.game).split()
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
        if self.team_score == self.opp_score:
            self.result = "tied"
        if self.team_score < self.opp_score:
            self.result = "lost"
        else:   # Assume win
            self.result = "won"

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    # In this example that means it would match on utterances like:
    #   'Hello world'
    #   'Howdy you great big world'
    #   'Greetings planet earth'

    @ intent_handler(IntentBuilder("GetScoreIntent").require("Team").require("Score"))
    def handle_score_intent(self, message):
        self.team = message.data["Team"]
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