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
