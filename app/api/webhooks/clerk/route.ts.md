# Internal Code Documentation: Clerk Webhook Handler

## Table of Contents

* [1. Overview](#1-overview)
* [2. Function: POST](#2-function-post)
    * [2.1. Webhook Verification](#21-webhook-verification)
    * [2.2. Event Handling](#22-event-handling)
        * [2.2.1. `user.created` Event](#221-usercreated-event)
        * [2.2.2. `user.updated` Event](#222-userupdated-event)
        * [2.2.3. `user.deleted` Event](#223-userdeleted-event)
* [3. Error Handling](#3-error-handling)


## 1. Overview

This document details the implementation of a serverless function (`POST`) designed to handle webhooks from Clerk.  The function receives webhook events, verifies their authenticity, and performs corresponding actions based on the event type. These actions involve creating, updating, and deleting users in an internal system. The function integrates with the Clerk API and a third-party library (`svix`) for webhook management.


## 2. Function: POST

This function acts as the endpoint for incoming Clerk webhooks.  It performs the following steps:

1. **Retrieves necessary environment variables and headers:**  It accesses the `WEBHOOK_SECRET` from environment variables and extracts `svix-id`, `svix-timestamp`, and `svix-signature` headers from the incoming request.  These headers are crucial for webhook verification.

2. **Input Validation:** Checks for the presence of all required headers. If any are missing it returns a 400 error.

3. **Webhook Verification:** Uses the `svix` library to verify the authenticity of the webhook payload using the provided headers and secret. This step is crucial for security, ensuring that only legitimate webhooks from Clerk are processed.  The verification process uses a cryptographic signature to confirm the integrity and origin of the request.

4. **Event Handling:** Based on the `eventType` in the verified webhook payload, the function performs the following actions:

### 2.1. Webhook Verification

The webhook verification process is implemented using the `svix` library. The `wh.verify()` method takes the request body (`body`), and the headers as input. It compares the computed signature with the `svix-signature` header to verify the authenticity of the webhook. If verification fails, an error is caught, and a 400 error response is returned.

Algorithm: The `svix` library handles the cryptographic signature verification internally. This likely involves a HMAC (Hash-based Message Authentication Code) algorithm using a shared secret key (`WEBHOOK_SECRET`). The library computes the expected signature based on the body and secret, and compares it to the received signature.


### 2.2. Event Handling

The function processes different Clerk webhook events:

#### 2.2.1. `user.created` Event

1. Extracts relevant user data from the webhook payload.
2. Constructs a `user` object with cleaned and standardized data, handling potential missing fields (e.g., `first_name`, `last_name`).
3. Calls `createUser` function from `@/lib/actions/user.actions` to create the user in the internal system.
4. Sets public metadata in Clerk using the `clerkClient.users.updateUserMetadata` function. This metadata links the Clerk user ID to the internal system's user ID.
5. Returns a JSON response indicating success and including the newly created user data.


#### 2.2.2. `user.updated` Event

1. Extracts relevant user data from the webhook payload.
2. Constructs a `user` object containing updated user information.
3. Calls `updateUser` function from `@/lib/actions/user.actions` to update the user in the internal system.
4. Returns a JSON response indicating success and including the updated user data.


#### 2.2.3. `user.deleted` Event

1. Extracts the user ID from the webhook payload.
2. Calls `deleteUser` function from `@/lib/actions/user.actions` to delete the user from the internal system.
3. Returns a JSON response indicating success and including the deleted user data.


## 3. Error Handling

The function includes error handling for several scenarios:

* **Missing `WEBHOOK_SECRET`:** Throws an error if the `WEBHOOK_SECRET` environment variable is not set.
* **Missing Svix Headers:** Returns a 400 error if any of the required Svix headers are missing.
* **Webhook Verification Failure:** Catches errors during webhook verification and returns a 400 error.  Detailed error messages are logged to the console for debugging purposes.  Generic error message returned to client.

All other unhandled errors will be caught by Next.js' error handling.
