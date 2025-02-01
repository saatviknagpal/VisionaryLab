# Profile Page Code Documentation

[Linked Table of Contents](#linked-table-of-contents)

## Linked Table of Contents

* [1. Overview](#1-overview)
* [2. `Profile` Component](#2-profile-component)
    * [2.1. Authentication and Redirection](#21-authentication-and-redirection)
    * [2.2. Data Fetching](#22-data-fetching)
    * [2.3. UI Rendering](#23-ui-rendering)
* [3. External Dependencies](#3-external-dependencies)


## 1. Overview

This document details the implementation of the `/profile` page, which displays a user's profile information including their credit balance and the number of processed images.  The page uses data fetched from backend services to populate the UI.

## 2. `Profile` Component

The `Profile` component is a functional React component responsible for rendering the user's profile page.


### 2.1. Authentication and Redirection

The component first checks for user authentication using `const { userId } = auth();` from the Clerk.js library. If the `userId` is not found (meaning the user is not logged in), the user is redirected to the `/sign-in` page using `redirect("/sign-in");`.

### 2.2. Data Fetching

The core logic involves fetching user data.  This happens in two steps:

1. **Fetch User Data:** The `getUserById(userId)` function retrieves the user's information from the backend, including their credit balance (`user.creditBalance`). This function is assumed to handle database interaction and error handling.

2. **Fetch User Images:** The `getUserImages({ page, userId: user._id })` function retrieves a paginated list of images associated with the user.  The `page` parameter controls which page of results to fetch.  The function likely interacts with the database to retrieve image data, performing pagination to manage large datasets.  The returned object contains `data` (an array of image objects) and `totalPages` (the total number of pages).


### 2.3. UI Rendering

The component renders the following elements:

* **Header:** A `<Header>` component displays "Profile" as the page title.
* **Credit Balance:** Displays the user's credit balance fetched from the database, using  `user.creditBalance`.  The UI includes an icon (`/assets/icons/coins.svg`).
* **Processed Images:** Displays the number of processed images (`images?.data.length`).  The UI includes an icon (`/assets/icons/photo.svg`).
* **Image Collection:** A `<Collection>` component is used to display the fetched images. This component handles pagination, passing the `images?.data`, `totalPages`, and `page` properties.



## 3. External Dependencies

The component utilizes several external libraries:

| Library             | Purpose                                      |
|----------------------|----------------------------------------------|
| `@clerk/nextjs/server` | Authentication and authorization.            |
| `next/image`          | Image component for optimized image loading. |
| `next/navigation`    | Client-side navigation.                     |
| `@/components/shared/Collection` | Reusable component for displaying image collections. |
| `@/components/shared/Header`  | Reusable header component.                 |
| `@/lib/actions/image.actions` | Functions for fetching image data.       |
| `@/lib/actions/user.actions` | Functions for fetching user data.         |

This documentation assumes familiarity with Next.js and React concepts.  Further details on the implementation of the helper functions (`getUserById`, `getUserImages`)  can be found in their respective documentation.
