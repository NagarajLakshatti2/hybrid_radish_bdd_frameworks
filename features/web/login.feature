Feature: Web Login

@smoke
@regression
Scenario: Successful login with valid credentials
  Given I open the login page
  When I login with valid credentials
  Then I should be logged in

@smoke
@regression
Scenario: Failed login with invalid credentials
  Given I open the login page
  When I login with invalid credentials
  Then login should fail

