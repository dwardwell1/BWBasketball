# Capstone1
'https://api.the-odds-api.com/v3/sports'

Betwell Basketball
https://bwellbball.herokuapp.com/
This site is a one stop shop to see all posted Head2Head odds for that day's slate of NBA games. 
With sports betting becoming more legal as times go on, its nice to see the spread of odds across most 
sports betting websites. THat way, if you wanted to bet, you would know where your money would go the furthest.

The features are relatively simple, the main page are all listed games with a highlight on the highest and lowest odds.
From there, if you sign up to become a member, you can select your favorite teams and see just those odds, as well
as captured data that ranks the best teams and best sportsbooks based on the captured performance

In terms of userflow its also simple. I didn't want to hide the main content behind signing up as I want easy 
access to what the site does. However I do prompt people to sign up to see some of I've deduced from the API as the days go on. 
Not much to it but the information is valuable I believe.

The API is listed above. One of the catches of the freemium model is that I can only make so many requests a month, so I decided to set a daily API call that I save to the database so there will be no drama with users calling the API past the limit set by the freemium.
If there wasn't a limit I might have designed the API interaction differently but I'm satisfied with the results.