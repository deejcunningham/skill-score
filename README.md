## score
Reports latest MLB scores

## Description 
Skill-score is an application that enables Mycroft to answer user questions about Major League Baseball (MLB) scores. [Mycroft](https://mycroft.ai) is an open-source AI voice assistant. Skill-score uses [panzarino's mlbgame API](https://github.com/panzarino/mlbgame) to report an MLB team's latest final scores, including live scores. 

User input has the format:
<br />"What is the {team}'s score?"

If a game is in progress, Mycroft will respond:
<br />"The {team} are winning/losing {score} to {score} against the {opponent} in the top/middle/bottom/end of the {inning}."

If a game is not in progress, Mycroft will respond:
<br />"The {team} won/lost {score} to {score} against the {opponent} {number-of-days} ago."

The next goals for skill-score are the ability to: 
* give the time of the next MLB game; and
* support more leagues (e.g., National Football League, National Basketball League), depending on available APIs.

## Examples 
* "what is the Royals score"
* "what is the Angels score"
* "what is the Yankees score"

## Credits 
deejcunningham