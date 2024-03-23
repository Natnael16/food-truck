# FoodTruck 🍔🚚

Welcome to FoodTruck, a Django-based backend application that helps users search for food trucks from anywhere in San Francisco. Users can specify their food preferences and search radius to find food trucks in their vicinity. The application also provides sophisticated search functionality for users to find specific food trucks and food items.

## Installation and Configuration

To get started with FoodTruck, follow these steps:

1. Clone this repository to your local machine.
2. Install pipenv if you haven't already: `pip install pipenv`.
3. Activate the virtual environment: `pipenv shell`.
4. Install dependencies: `pipenv install`
5. Ensure MongoDB is installed and running on your environment.
6. Seed the data in the csv file to MongoDB: `python manage.py seed_data`.
7. Run the Django server: `python manage.py runserver`.

## Usage

### Endpoints/API Documentation

#### Nearby Food Trucks:
- **Description:** Retrieve nearby food trucks based on provided location coordinates.
- **URL:** `/api/foodtruck/nearby/`
- **Method:** `GET`
- **Query Parameters:**
- `latitude` (optional): Latitude coordinate of the center point for the search (default: 0).
- `longitude` (optional): Longitude coordinate of the center point for the search (default: 0).
- `radius` (optional): Search radius in meters (default: 1000).
- **Returns:** JSON response containing count and data of nearby food trucks. Example response format provided in the comment.

#### All Food Trucks:
- **Description:** Retrieve all food trucks from the database.
- **URL:** `/api/foodtruck/all/`
- **Method:** `GET`
- **Returns:** JSON response containing count and data of all food trucks. Same as the previous endpoint.

#### Food Truck Search:
- **Description:** Search for food trucks based on various filters.
- **URL:** `/api/foodtruck/search/`
- **Method:** `GET`
- **Query Parameters:**
- `q` (optional): Search query string.
- `status` (optional): Filter by status. Avialable status are APPROVED, SUSPENDED, REQUESTED, EXPIRED.
- `facility_type` (optional): Filter by facility type. It can be either Truck or Push Cart.
- `latitude` (optional): Latitude coordinate for geospatial search.
- `longitude` (optional): Longitude coordinate for geospatial search.
- `radius` (optional): Search radius in meters for geospatial search.
- **Returns:** JSON response containing count and data of searched food trucks. Same as the previous endpoints.

#### Food Search:
- **Description:** Search for foods.
- **URL:** `/api/foods/search/`
- **Method:** `GET`
- **Query Parameters:**
- `name` (optional): The name of the food to search for.
- **Returns:** JSON response containing the count of foods and the serialized data.

## Database

FoodTruck uses MongoDB as the database due to its flexibility and schema-less nature. With no direct relationships between models, MongoDB provides an ideal solution for this scenario.

### Collections:
- **food_truck:** Collection storing information about food trucks.
- **foods:** Collection storing information about food items.

## Testing

To run tests for FoodTruck, execute the following command: `python manage.py test`

**Third-Party Libraries**

- `pymongo`: Facilitates communication with the MongoDB database.
- `mongoengine`: Streamlines interaction with MongoDB models within a Django context.
- `django-rest-framework`: Empowers the creation of robust RESTful APIs for food truck and food data retrieval.

**Future Enhancements**

- **Chatbot Integration:** Introduce a chatbot to provide interactive guidance and personalized recommendations.
- **Authentication:** Implement user authentication for features like ratings, favorites, and friend sharing.
- **Ratings and Favorites:** Allow users to rate food trucks and mark favorites for a more curated experience.
- **Social Sharing:** Facilitate effortless sharing of food truck discoveries with friends and family.


