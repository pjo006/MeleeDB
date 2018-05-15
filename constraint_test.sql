Pragma foreign_keys = on;

.print "Inserting non-unique player name:"
Insert Into players Values('Mango', 'USA', 'Fox', NULL, NULL, 1, 2, 3, 4, 5);

.print "\nInserting non-valid foreign reference:"
Insert Into tournaments values ('The Mango', 100, 'USA', 'Los Angeles', 'CA', '2018-03-15', 100, 'Mango', 'Armada', 'Hungrybox', 'Mew2King', 'PPMD', 'Axe', 'PJ', 'Leffen');

.print "\nInserting non-valid date:"
Insert Into tournaments values ('The Mango', 100, 'USA', 'Los Angeles', 'CA', '2000-03-15', 100, 'Mango', 'Armada', 'Hungrybox', 'Mew2King', 'PPMD', 'Axe', 'SFAT', 'Leffen');

.print "\nInserting negative entrants:"
Insert Into tournaments values ('The Mango', -100, 'USA', 'Los Angeles', 'CA', '2010-03-15', 100, 'Mango', 'Armada', 'Hungrybox', 'Mew2King', 'PPMD', 'Axe', 'SFAT', 'Leffen');

.print "\nInserting character with invalid tier:"
Insert Into characters values ("Corrin", "Fire Emblem", "Z");
