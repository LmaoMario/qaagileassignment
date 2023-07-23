Feature: Support Ticket Management

  Scenario: User login
    Given the user is on the login page
    When the user enters valid credentials
    Then the user should be logged in successfully

  Scenario: Admin login
    Given the admin is on the login page
    When the admin enters valid credentials
    Then the admin should be logged in successfully

  Scenario: User creates a support ticket
    Given the user is logged in
    When the user navigates to the support ticket creation page
    And the user enters the ticket details
    And submits the ticket
    Then the ticket should be created successfully

  Scenario: Admin views support tickets
    Given the admin is logged in
    When the admin navigates to the support ticket management page
    Then the admin should see a list of support tickets

  Scenario: Admin replies to a support ticket
    Given the admin is logged in
    When the admin selects a support ticket to view
    And enters a reply message
    And submits the reply
    Then the reply should be added to the ticket successfully

  Scenario: Admin deletes a support ticket
    Given the admin is logged in
    When the admin selects a support ticket to delete
    And confirms the deletion
    Then the ticket should be deleted successfully