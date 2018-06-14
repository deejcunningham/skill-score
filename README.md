skill-score
======
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

**User**: "What is the Royals score?"
<br />**Mycroft**: "The Royals are winning 2 to 1 against the Yankees in the bottom of the sixth inning."

**User**: "What is the Angels score?"
<br />**Mycroft**: "The Angels lost 2 to 5 against the Mariners yesterday."

**User**: "What is the Yankees score?"
<br />**Mycroft**: "The Yankees won 5 to 4 against the Royals two days ago."

## Getting Started

### Prerequisites
Download the following prerequisites:
1. Mycroft - see [installation details](https://mycroft.ai/get-mycroft/)
2. Mycroft Skills Manager (msm) - see [installation details](https://github.com/MycroftAI/mycroft-skills-manager)
    - msm will install skill-score in the correct directory with the necessary requirements

### Installation
In the console, install skill-score using:
~~~
msm install https://github.com/deejcunningham/skill-score
~~~


## Credits 
David Cunningham
Thanks panzarino for the well-documented API
