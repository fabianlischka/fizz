fizz
====

A repository for random small independent stand-alone bits and pieces.

`sortedUniforms` yields N iid standard uniform random variables sorted in ascending order. Note that it's not actually faster than generating N uniforms and sorting them for most cases. It's just neat.

`pairwiseRound` is an itertool that yields (a,b), (b,c), (c,d), (d,a) for (a,b,c,d). Comes in handy occasionally.

Some jurisdictions XZY apparently require your bank to obtain your declaration that you are a "non-XYZ Person" according to XYZ law. `declare` is a small tool that generates pertinent declarations for a number of jurisdictions (pulled from the Wikipedia list of sovereign states, filtered by some states you specify), just in case those other jurisdictions also impose said obligation on your bank. You can run this, print it, sign it, and send it to your bank all in one fell swoop.

```
Printing 1414 declarations:


I am not a "Suriname (Republic of Suriname) resident alien".
I was not born in Algeria (People's Democratic Republic of Algeria) or a territory thereof.
I was not born in Kenya (Republic of Kenya) or a territory thereof.
I hereby undertake to notify the Bank, at my own initiative and within 30 days, if my status under Kosovo (Republic of Kosovo) tax principles changes to the status of a Kosovo (Republic of Kosovo) Person under Kosovo (Republic of Kosovo) tax principles, subject to the change being due to a change in my circumstances, not a change in the Kosovo (Republic of Kosovo) tax principles, and furthermore subject to the Bank explicitly having requested me to do so.
I am not a "Mauritius (Republic of Mauritius) person" under any sensible principles (and thus, presumably, under Mauritius (Republic of Mauritius) tax principles), as far as I can tell.
I was not born in Saudi Arabia (Kingdom of Saudi Arabia) or a territory thereof.
I declare that if there is a substantial presence test under Tunisia (Republic of Tunisia) tax principles and it allows for treatment as a nonresident alien under certain conditions (e.g. that I stay in Tunisia (Republic of Tunisia) less than 183 days a year and I maintain a tax home in a foreign country during the year to which I have a closer connection than to Tunisia (Republic of Tunisia)), then, as far as I can tell, I qualify for treatment as a nonresident alien under Tunisia (Republic of Tunisia) tax principles, because said conditions hold.
I am not a citizen of Malta (Republic of Malta).
I hereby declare that I am the beneficial owner of the assets and income to which this form relates, according to any sensible principles (and thus, presumably, according to Thailand (Kingdom of Thailand) tax principles), and that no other beneficial owner exists.
I am not a "Armenia (Republic of Armenia) person" under any sensible principles (and thus, presumably, under Armenia (Republic of Armenia) tax principles), as far as I can tell.
I hereby declare that I am the beneficial owner of the assets and income to which this form relates, according to any sensible principles (and thus, presumably, according to New Zealand tax principles), and that no other beneficial owner exists.
I am not a citizen of Kosovo (Republic of Kosovo).
```

etc.
