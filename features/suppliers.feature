Feature: The supplier  service back-end
    As a Supplier Manager
    I need a RESTful catalog service
    So that I can keep track of all my suppliers

Background:
    Given the following suppliers
        | supplierName | address | productIdList | averageRating |
        | Walmart      | NYC     | 1,2,3         | 3             |
        | Costco       | LA      | 1,2,3,4,5     | 4             |
        | Ikea         | SF      | 2,3,5         | 3             |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Supplier Demo REST API Service" in the title
    And I should not see "404 Not Found"

Scenario: List all pets
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "Walmart" in the results
    And I should see "Costco" in the results
    And I should not see "notASupplier" in the results

Scenario: The server is running
    When I create a supplier with name "Apple", address "NYC", and product "2,3"
    Then I should get "201 Created"
    And I should not see "500 Internal Server Error"
