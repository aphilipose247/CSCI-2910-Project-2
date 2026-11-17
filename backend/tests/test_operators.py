# This file contains all of the tests for my CRRUD operations

# to run the tests, use the code : python -m pytest -v

# CREATE Operation Test
# I am going to use the same format that was done in Lab 06

def test_create_operator(client, sample_operator):
    # Act
    response = client.post("/operators/", json=sample_operator)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data["id"], int) # the response has an id which is an int
    for field, value in sample_operator.items():
        assert data[field] == value

# What the test above is going to do is that it is going first ACT by creating Coffey (using my sample operator from the fixture)
# If Coffey is created successfully, then a status code of 201 appears
# The assert isinstance(data["id"], int) line means that the database has assigned Coffey an id that wasn't assigned by me
# The for loop ensures that the same fields that I gave my other operators and Coffey aren't changed when they come back

#--------------------------------------------------------------------------------------------------

# READ ALL Operation Test

def test_read_all_operators(client, seeded_db):
    # Act
    response = client.get("/operators/")

    # Assert: All the seeded operators will come back in order
    assert response.status_code == 200
    names = [op["operator_name"] for op in response.json()]
    assert names == [op["operator_name"] for op in seeded_db]

# For this test above, for the ACT, you first GETs the full list of operators
# In Assert, you can see that it takes that list of operators and compares it to the operators in the seeded_db to ensure that all the operators are there and are in order by id

# -------------------------------------------------------------------------------------------------

# READ Operation Test

def test_read_operator(client, created_operator):
    # Act
    response = client.get(f"/operators/{created_operator['id']}")

    # Assert: This makes sure that we get what we put in
    assert response.status_code == 200
    assert response.json() == created_operator

# For this test above, the ACT is retrieving the sample operator we created (Coffey) and his id
# Then, what we get should be the same to what we created. This makes sure that it was saved in the database and can be retrieved by the id

# -------------------------------------------------------------------------------------------------

# UPDATE Operation Test

def test_update_operator(client, created_operator, updated_operator):
    # Arrange
    operator_id = created_operator["id"]
    expected = {"id" : operator_id, **updated_operator} # this helps create a new dict with Coffey's id and everything else in updated_operator (Ju Kwon)

    # Act
    response = client.put(f"/operators/{operator_id}", json=updated_operator)

    # Assert
    assert response.status_code == 200
    assert response.json() == expected
    saved = client.get(f"/operators/{operator_id}")
    assert saved.json() == expected

# In this test above, first we create the variable expected which holds Ju Kwon's data, but with Coffey's id
# A dict will get created with the new info
# in the Act section, we update Coffey to have Ju Kwon's data
# in Assert, the test checks that what we got equals the variable 'expected' to ensure that the API has been updated
# Another precaution is taken where the variable 'saved' gets the updated data and ensures that it is still the same as the 'expected' variable

# -------------------------------------------------------------------------------------------------

# DELETE Operation Test

def test_delete_operator(client, created_operator):
    # Arrange
    operator_id = created_operator["id"]

    # Act
    response = client.delete(f"/operators/{operator_id}")

    # Assert
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/operators/{operator_id}").status_code == 404 #ensures that the operator actually has been deleted

# In the test above, you first Arrange the data that you need (in this case, it is Coffey)
# Then, in the Act part, you then are deleting the operator using the delete request
# In the Assert, you are ensuring that the operator has been deleted by returning an empty body
# then you run a get request to ensure that the operator has actually been deleted and to make sure that the API didn't just say the operator was deleted