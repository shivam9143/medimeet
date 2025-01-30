# MediMeet API Documentation

This document provides API endpoints for MediMeet, including user authentication, doctor listings, and appointment booking.

## Authentication

### 1. Send OTP

**Endpoint:** `POST /send-otp/`  
**Description:** Sends an OTP to the provided mobile number.

#### Request
```sh
curl --location 'https://api.rabattindia.com/send-otp/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'mobile_number=9044224967'

{
    "code": 201,
    "message": "OTP sent to your mobile number.",
    "data": {
        "verification_id": "1525010",
        "mobile_number": "9044224967",
        "timeout": "60.0"
    },
    "error": null
}

{
    "code": 400,
    "message": "Something went wrong!",
    "data": null,
    "error": "User not registered"
}
```

### 2. Endpoint: POST /verify-otp/
**Description:** Verifies the OTP sent to the user.

```sh
curl --location 'https://api.rabattindia.com/verify-otp/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'mobile_number=9044224967' \
--data-urlencode 'otp=123456' \
--data-urlencode 'verification_id=1525010'

{
    "code": 200,
    "message": "Success",
    "data": {
        "user": {
            "id": "5468066d-cc9b-4f75-b38b-690a8aa39046",
            "name": "Shivam Kanodia",
            "age": 28,
            "gender": "Male",
            "mobile_number": "9044224967",
            "photo_url": null,
            "is_verified": true,
            "created_at": "2025-01-29T03:12:46.156620Z"
        },
        "token": "YOUR_JWT_TOKEN"
    },
    "error": null
}
```

User Registration

### 3. Endpoint: POST /register-user/
**Description:** Registers a new user.

```sh
curl --location 'https://api.rabattindia.com/register-user/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'mobile_number=9044224967' \
--data-urlencode 'name=Shivam jio' \
--data-urlencode 'age=28' \
--data-urlencode 'gender=male'

{
    "code": 400,
    "message": "Something went wrong!",
    "data": null,
    "error": "{'mobile_number': ['user with this mobile number already exists.']}"
}
```
Doctor Listings

Endpoint: GET /doctors/
Description: Fetches the list of available doctors.

Request

```sh
curl --location 'https://api.rabattindia.com/doctors'

{
    "code": 200,
    "message": "Doctors retrieved successfully",
    "data": [
        {
            "id": "e6904247-e829-4dea-a327-db8d6aa89922",
            "name": "Ashutosh Trivedi",
            "specialization": "General Physician",
            "age": 53,
            "gender": "Male",
            "mobile_number": "9876543210",
            "photo_url": "",
            "is_verified": true,
            "created_at": "2025-01-29T03:17:36.627180Z"
        }
    ],
    "error": null
}

```

Doctor Appointment Slots

Endpoint: GET /clinic-management/doctors/{doctor_id}/slots/
Description: Fetches available slots for a doctor.

Request

```sh
curl --location 'https://api.rabattindia.com/clinic-management/doctors/e6904247-e829-4dea-a327-db8d6aa89922/slots/'

[
    {
        "id": "c65e4501-3c03-42c5-b328-0c7f62243708",
        "start_time": "2025-01-29T20:30:00Z",
        "end_time": "2025-01-29T21:00:00Z",
        "is_available": true
    }
]

```

Book an Appointment

Endpoint: POST /clinic-management/appointments/book/{slot_id}/
Description: Books an available appointment slot.

Request

```sh
curl --location --request POST 'https://api.rabattindia.com/clinic-management/appointments/book/12ac119d-efab-4814-94b6-bafa4c5c6df6/' \
--header 'Authorization: Bearer YOUR_JWT_TOKEN'

```

Cancel an Appointment

Endpoint: POST /clinic-management/appointments/cancel/
Description: Cancels a booked appointment.

```sh

curl --location 'https://api.rabattindia.com/clinic-management/appointments/cancel/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'slot_id=12ac119d-efab-4814-94b6-bafa4c5c6df6'

```

Get User Appointments

Endpoint: GET /clinic-management/appointments/
Description: Fetches a user’s booked appointments.

Request

```sh

curl --location 'https://api.rabattindia.com/clinic-management/appointments/'

{
    "code": 400,
    "message": "Something went wrong!",
    "data": null,
    "error": "['“AnonymousUser” is not a valid UUID.']"
}

```

Authentication & Authorization
	•	All protected routes require a valid JWT token in the Authorization header.
	•	The JWT token is returned in the /verify-otp/ response and should be used for all authenticated requests.

Notes
	•	Replace YOUR_JWT_TOKEN with the actual token obtained from /verify-otp/.
	•	Replace {doctor_id} and {slot_id} with the actual values retrieved from previous API calls.
	•	All timestamps are in UTC format (YYYY-MM-DDTHH:MM:SSZ).

 This README file provides clear documentation for all API endpoints, requests, responses, and error handling. Let me know if you need any modifications! 🚀
