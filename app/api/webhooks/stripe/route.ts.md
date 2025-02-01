# Internal Code Documentation: Stripe Webhook Handler

[Linked Table of Contents](#table-of-contents)

## Table of Contents <a name="table-of-contents"></a>

* [1. Overview](#overview)
* [2. Function: POST](#function-post)
    * [2.1. Input](#input)
    * [2.2. Processing](#processing)
    * [2.3. `checkout.session.completed` Event Handling](#checkoutsessioncompleted-event-handling)
    * [2.4. Error Handling](#error-handling)
    * [2.5. Output](#output)


## 1. Overview <a name="overview"></a>

This document details the functionality of the Stripe webhook handler. This serverless function is responsible for receiving and processing webhook events from Stripe.  The primary function is to handle `checkout.session.completed` events, creating a transaction record in the system upon successful checkout.


## 2. Function: POST <a name="function-post"></a>

This function acts as the entry point for incoming webhook requests from Stripe.

### 2.1. Input <a name="input"></a>

The function accepts a POST request from Stripe.  The request includes:

*   **Request Body (body):** A JSON payload containing the webhook event data.
*   **Stripe Signature Header (`stripe-signature`):** A header used for verifying the authenticity of the request.


### 2.2. Processing <a name="processing"></a>

1.  **Retrieve Request Data:** The function first retrieves the request body as text and the `stripe-signature` header.

2.  **Webhook Verification:** The core security step involves verifying the signature using the `stripe.webhooks.constructEvent` function. This function takes the request body, signature, and the `STRIPE_WEBHOOK_SECRET` environment variable (containing the secret key from Stripe) as input.  This step ensures that the request originates from Stripe and hasn't been tampered with.  Failure to verify the signature results in an error.

3.  **Event Type Extraction:**  The event type (`eventType`) is extracted from the verified event object.

4.  **Event Handling:**  Currently, only the `checkout.session.completed` event is handled.  Other event types result in a silent 200 OK response.


### 2.3. `checkout.session.completed` Event Handling <a name="checkoutsessioncompleted-event-handling"></a>

If the event type is `checkout.session.completed`, the following steps are performed:

1.  **Data Extraction:** Relevant data (ID, total amount, metadata) is extracted from the event data.

2.  **Transaction Data Preparation:** A `transaction` object is created.  The `amount_total` from Stripe is converted from cents to dollars. Metadata fields (plan, credits, buyerId) are extracted; default values are used if these fields are missing.

3.  **Transaction Creation:** The `createTransaction` function (located in `@/lib/actions/transaction.action`) is called asynchronously to persist the transaction data in the database.

4.  **Response:** A JSON response is sent, indicating success and including the newly created transaction data.


### 2.4. Error Handling <a name="error-handling"></a>

If the webhook signature verification fails, a JSON response containing an error message and the error object is returned.

### 2.5. Output <a name="output"></a>

The function returns different responses based on the outcome:

| Status Code | Condition                                         | Response Body                                      |
| :---------- | :------------------------------------------------- | :-------------------------------------------------- |
| 200         | Webhook signature verification failure             | `{ message: "Webhook error", error: err }`        |
| 200         | `checkout.session.completed` event processed successfully | `{ message: "OK", transaction: newTransaction }` |
| 200         | Other event types                                  | `""` (empty string)                                |


