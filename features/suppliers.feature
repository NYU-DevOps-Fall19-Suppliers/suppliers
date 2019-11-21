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
        | Target       | Boston  | 5             | 2             |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Supplier Demo REST API Service" in the title
    And I should not see "404 Not Found"

Scenario: List all suppliers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "Walmart" in the results
    And I should see "Costco" in the results
    And I should not see "notASupplier" in the results

Scenario: The server is running
    When I create a supplier with name "Apple", address "NYC", and product "2,3"
    Then I should get "201 Created"
    And I should not see "500 Internal Server Error"

Scenario: Read a Supplier
    When I visit the "Home Page"
    And I change "averageRating" to "4"
    And I press the "Search" button
    Then I should see "LA" in the "address" field
    When I copy from the "supplier_id" field
    And I press the "Clear" button
    And I paste to the "supplier_id" field
    And I press the "Retrieve" button
    Then I should see "Costco" in the "supplierName" field
    And I should see "LA" in the "address" field
    And I should see "1,2,3,4,5" in the "productIdList" field
    And I should see "4" in the "averageRating" field

Scenario: Query suppliers by averageRating
    When I visit the "Home Page"
    And I change "averageRating" to "4"
    And I press the "Search" button
    Then I should see "Costco" in the results
    And I should not see "Walmart" in the results
    And I should not see "Ikea" in the results

Scenario: Recommend suppliers that provide give products
    When I visit the "Home Page"
    And I change "ProductId" to "5"
    And I press the "Recommend" button
    Then I should see "Costco" in the results
    And I should see "Ikea" in the results
    And I should not see "Target" in the results

Scenario: Update a Supplier
    When I visit the "Home Page"
    And I change "supplierName" to "Walmart"
    And I press the "Search" button
    Then I should see "Walmart" in the "supplierName" field
    When I change "supplierName" to "Target"
    And I press the "Update" button
    Then I should see the message "success"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "Target" in the results

Scenario: Delete a supplier
    When I visit the "Home Page"
    And I press the "Search" button
    When I copy from the "supplier_id" field
    And I press the "Clear" button
    And I paste to the "supplier_id" field
    And I press the "Delete" button
    Then I should see the message "Supplier has been Deleted!"
    And I should not see "500 Internal Server Error"
