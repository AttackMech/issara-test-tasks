# Issara Institute Test Task

This is the coding challenge for the position of either front end or full stack developer at Issara Institute in Bangkok, Thailand. There are two separate sections: Back End & Full Stack.

## Table of Contents

- [Back End](#back-end)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Notes](#notes)
- [Full Stack](#full-stack)


## Back End

- [Installation](#installation)
- [Usage](#usage)
- [Notes](#notes)

### Installation

1. Clone this github repository onto your machine
2. Install Docker onto your machine (get Docker [here](https://docs.docker.com/get-docker/))
3. Build the Docker image
    ```
    docker build -t your-image-name .
    ```
4. Run the Docker container
    ```
    docker run -p 5000:5000 your-image-name
    ``` 
    - change port mapping if desired
5. Access in web browser, Postman, or other application

### Usage

Build and run the docker container using the installation instructions.

**Endpoints:**
1. GET /values - Get all the values of the store and reset all TTL.
    - Response: `{key1: value1, key2: value2, key3: value3...}`

2. GET /values?keys=key1,key2 - Get one or more specific values from the store and also reset the TTL of those keys.
    - Response: `{key1: value1, key2: value2}`

3. POST /values - Save a value in the store.
    - Request: `{key1: value1, key2: value2..}`
    - Response: `{"message": "Items successfully added"}`

4. PATCH /values - Update a value in the store and also reset the TTL.
    - Request: `{key1: value1, key2: value2..}`
    - Response: `204 No Content`

Each key has a _Time to Live_ (TTL) of 300s (5 minutes). Creating, updating and retrieving will update the TTL of any key accessed.

Here is an example POST request using Postman:
![Screenshot of Postman application](Images/Screenshot - Back End POST.png)

### Notes

I followed the constraints as well as possible:
1. Use appropriate status codes with all the responses.
    - 200 for successful retrieval
    - 201 for creation
    - 204 for update
    - 400 for no keys (GET only) or invalid JSON
    - 404 when provided keys do not exist
    - 409 when attempting to create existing keys
    - I did not check for empty objects or nested values in the POST/PATCH endpoints. I did not feel it was necessary for this exercise, but it can be easily added.
2. Remove all values stored over more than 5 minutes. Set a TTL
    - TTL set 300 s. Can be changed in **key_val_store.py**
    - I do not actually remove keys when the TTL is complete. To keep things fast and simple, I simply remove expired keys when a request is made, before fulfilling the request. To do it in real time, I would create a separate worker thread that would check and remove the values each second. However, I felt that was overkill for this exercise.
3. Reset TTL on every GET Request.
    - The `get_keys()` function of the `KeyValStore` class will handles update and removal of keys based on TTL.
4. Has to be FAST
    - Flask is a lightweight application
    - This is fast at a smaller scale
    - At large scale, obviously there are a lot of loops to go through. This can be reduced by utilizing a separate thread for TTL removal (outlined above), or by redesigning the application (eg. using an actual DB). I didn't think it was necessary to have this application scale to extremely huge values.
5. Values can be of arbitrary length
    - The underlying structure is a dict, so no issues there.
6. Must be fault-tolerant, persistent
    - Errors handled as outlined above
    - `KeyValStore` class used for persistent data
7. Must deploy using Docker.
    - Completed. Instructions outlined above.



## Full Stack


