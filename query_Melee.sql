.print "How many players?"
Select Count(*)
From Players;

.print "How many players from the USA?"
Select Count(*)
From Players
Where Nationality = "USA";

.print "How many tournaments?"
Select Count(*)
From Tournaments;

.print "How many tournaments outside the USA?"
Select Count(*)
From Tournaments
Where Country <> "USA";

.print "How many large tournaments (at least 500 entrants)?"
Select Count(*)
From Tournaments
Where Entrants > 499;

.print "What is the average prize pool that each country offers at its tournaments?"
Select Country, AVG(Prize_Pool)
From Tournaments
Group By Country
Order By AVG(Prize_Pool) ASC;

.print "Which players have won more than 3 tournaments?"
Select Winner, Count(Winner)
From Tournaments
Group By Winner
Having Count(Winner) > 3
Order By Count(Winner) DESC;

.print "Which player has won the most tournaments? Where are they from and what characters do they play?"
Select t.Winner, p.Nationality, p.Character_1, p.Character_2, p.Character_3
From Tournaments t, Players p
Where t.Winner = p.Tag
Group By t.Winner
Having Count(t.Winner) = (
						Select Max(c)
						From(
								Select Count(*) as c
								From Tournaments
								Group By Winner
								)
						);

.print "Which characters have the most tournament wins, where a win for a character is a win by a player who plays them as their first choice? Compare this to character tier rating."
Select wins.Character_1, Count(*), c.Tier
From Characters c, (
					Select t.Winner, p.Character_1
					From Tournaments t, Players p
					Where t.Winner = p.Tag
					) wins
Where c.Name = wins.Character_1
Group By wins.Character_1
Order By Count(*) DESC;
