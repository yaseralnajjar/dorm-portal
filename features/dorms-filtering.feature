Feature: filtering dorms

    Scenario: As a student
              I want to filter dorms based on the choosen filters
              So that I get exactly what Im looking for

        Given we have 2 dormitory with 4 rooms with couple of choices

        When not doing any filtering for the dorms
        Then get the 2 dorms with the 4 rooms
        And get the rooms left equals the sum quota

        When one of the alfam rooms has no quota
        Then get all the room except the one with no quota
        And return the quota back for the alfam room

        When filter free wifi
        Then get only dovec which has free wifi with two rooms

        When filter price between 1100 and 1800
        Then get 2 dorms with 1 room for each (1200, 1700)

        When filter PUBLIC dorm price between 1100 and 1800
        Then get alfam dorm with just 1 room (1200)

        When filter meals (breakfast & both) + luxury shower
        Then get only dovec with two rooms

        When filter meals (without any option sent)
        Then ignore the meals filter

        When (breakfast&both) + luxuryshower + airconidtioner + price(1500,2000) + bathrooms(1,2)
        Then get only dovec with one room only

        When deserialize the same filter above
        Then validate the deserialized filters successfully

        When serialize the returned dorms data from the last filters
        Then get deserialize data for (only dovec with one room only)

        When hitting POST /dorms endpoint with filter above
        Then get 200 OK with data for (only dovec with one room only)