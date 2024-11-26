# Technical Test for Bookline.ai

## Variables
 
Used variables explanation.

### `Car List`

Hardcoded list of the differents types of cars that are available for rent. A basic list is enough to have the information on the available cars.

Since this is a small list for the example, there is not need to save it to a file.

### `Rented Car List`

Dependent variable of executed bookings that contains both the reserved car and the booking date as a dictionary in a list. The dictionary allows us to have all the reservation information in a single position on the list.

It is saved in the database (JSON file) every time a successfull booking is created.

## Endpoints
 
Used endpoints explanation.

### `List of Available Cars`

GET endpoint that lists all available cars for a specific date.

### `Create a Booking`

POST endpoint that create a booking for a car on a given date after performing some checks.

 - Check that the car exists on the availables cars.
 - Check that the car is not already rented for the given date.

## Database Storage

JSON file used for simplicity.

Accessing file using Python 'os' library.
