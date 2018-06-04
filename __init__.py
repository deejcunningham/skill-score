# The MIT License (MIT)	

# Copyright (c) 2018 David Cunningham

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# TODO: Add intent to ask when the game starts (today)
# TODO: Figure out stop method
# TODO: Handle offseason?
# TODO: Find NFL and MLS APIs

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from mycroft import intent_handler

from datetime import date, timedelta
import mlbgame

__author__ = 'deejcunningham'
# LOGGER = getLogger(__name__)

class ScoreSkill(MycroftSkill):
    def __init__(self):
        super(ScoreSkill, self).__init__(name="ScoreSkill")

    def get_date(self, adjust=0):
        """Gets a date, default to today, can be adjusted by day with positive or negative adjust"""
        adjust = timedelta(days=adjust)
        self.date = str(date.today()+adjust)
        self.year = int(self.date[0:4])
        self.month = int(self.date[5:7])
        self.day = int(self.date[8:])

    def get_game(self):
        """Gets the last valid (not pre_game) game, so IN_PROGRESS or FINAL"""
        # CHECK to see what happens to game[0].game_status on rain outs/cancelled games... they are 'FINAL'
        self.get_date()     # Gets todays date
        self.game = mlbgame.day(self.year, self.month, self.day, home=self.team, away=self.team)
        adjust = -1
        while self.game == [] or self.game[-1].game_status == 'PRE_GAME':  # If the game today hasn't started yet or there is no game at all today, look back each day to find one
            self.get_date(adjust)
            self.game = mlbgame.day(self.year, self.month, self.day, home=self.team, away=self.team)
            adjust -= 1
        self.game = self.game[-1]   # Sets the game attribute to the actual game instead of a list containing a single game (this may mess up on days with doube-headers...)

    def get_relative_day(self):
        self.game_date = date(year=self.game.date.year, month=self.game.date.month, day=self.game.date.day)
        difference = date.today() - self.game_date
        if difference < timedelta(days=1):
            self.relative_day = 'earlier today'
        elif difference == timedelta(days=1):
            self.relative_day = 'yesterday'
        elif difference == timedelta(days=2):
            self.relative_day = 'two days ago'
        else:
            self.relative_day = 'on {}'.format(self.game_date)

    def get_inning(self):
        self.overview = mlbgame.overview(self.game.game_id)
        self.inning_state = self.overview.inning_state.lower()
        self.inning = self.overview.inning
        # Format the inning number...
        if self.inning == 1:
            self.inning = str(self.inning) + 'st'
        elif self.inning == 2:
            self.inning = str(self.inning) + 'nd'
        elif self.inning == 3:
            self.inning = str(self.inning) + 'rd'
        else:
            self.inning = str(self.inning) + 'th'

    def get_result(self):
        """Takes tangled mlbgame.ScoreBoard object and pulls out teams + their scores then calculates result"""
        self.get_game()
        if self.game.game_status == 'IN_PROGRESS':
            self.get_inning()
        if self.game.home_team == self.team:
            self.team_score = self.game.home_team_runs
            self.opponent = self.game.away_team
            self.opponent_score = self.game.away_team_runs
        else:
            self.team_score = self.game.away_team_runs
            self.opponent = self.game.home_team
            self.opponent_score = self.game.home_team_runs
        
        if self.team_score > self.opponent_score:
            self.result = 'winning'
        elif self.team_score < self.opponent_score:
            self.result = 'losing'
        else:
            self.result = 'tied'
        
        if self.game.game_status == 'FINAL':
            self.get_relative_day()
            if self.result == 'winning':
                self.result = 'won'
            elif self.result == 'losing':
                self.result = 'lost'

    @ intent_handler(IntentBuilder("GetLiveScoreIntent").require("Team").require("Score").build())
    def handle_live_score_intent(self, message):
        self.team = message.data.get("Team")
        self.get_result()
        if self.game.game_status == 'IN_PROGRESS':
            # "The {{team}} are {{result}} {{team_score}} to {{opponent_score}} against the {{opponent}} in the {{inning_state}} of the {{inning}}
            self.speak_dialog("livescore", data={"team": self.team, "result": self.result, "team_score": self.team_score, "opponent_score": self.opponent_score, "opponent": self.opponent, "inning_state": self.inning_state, "inning": self.inning,})
        else:
            # "The {{team}} {{result}} {{team_score}} to {{opponent_score}} against the {{opponent}} {{relative_day}}"
            self.speak_dialog("pastscore", data={"team": self.team, "result": self.result, "team_score": self.team_score, "opponent_score": self.opponent_score, "opponent": self.opponent,"relative_day": self.relative_day})

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
