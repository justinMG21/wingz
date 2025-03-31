@my_profile
Feature: My Profile Wingz


    Scenario: Verify that the user can navigate to the profile page
        Given the user login to wingz using "justinmgguma@gmail.com"
        When the user navigates to the account page
            And the user navigates to the my profile page
        Then the user should be redirected to the my_profile page

    Scenario: Verify that the user can successfully update their profile with gender, first name, last name, home city, bio, and save the changes
        Given the user login to wingz using "justinmgguma@gmail.com"
        When the user navigates to the account page
            And the user navigates to the my profile page
        When the user provide "Justin" "Cruise" "Manila" "Hi, I'm Justin"
            And the user clicks save button
        Then the user should be able to see the changes saved


