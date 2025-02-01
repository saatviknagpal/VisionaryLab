# AddTransformationTypePage Component Documentation

[Linked Table of Contents](#linked-table-of-contents)

## Linked Table of Contents

* [1. Overview](#1-overview)
* [2. Component Hierarchy](#2-component-hierarchy)
* [3. Props](#3-props)
* [4. Functions and Algorithms](#4-functions-and-algorithms)
* [5. Usage](#5-usage)


## 1. Overview

The `AddTransformationTypePage` component is a Next.js page responsible for rendering a form allowing users to add a new transformation of a specific type.  It fetches user data and transformation type details to populate the form.  Authentication is handled via Clerk.js.

## 2. Component Hierarchy

The component utilizes the following sub-components:

*   `Header`: A shared header component displaying the title and subtitle of the transformation type.
*   `TransformationForm`: A shared form component for adding transformations.  This component handles user input and submission.


## 3. Props

The `AddTransformationTypePage` component receives the following prop:

| Prop Name      | Type             | Description                                                                   |
|-----------------|------------------|-------------------------------------------------------------------------------|
| `params.type`   | String           |  The type of transformation to be added (e.g., 'image', 'video'). This is passed as a route parameter.   |


## 4. Functions and Algorithms

The `AddTransformationTypePage` component employs the following key functions and algorithms:

1. **Authentication:** The component uses `auth()` from `@clerk/nextjs/server` to retrieve the currently authenticated user's ID (`userId`). If no user is authenticated (`!userId`), it redirects the user to the `/sign-in` page using `redirect` from `next/navigation`.

2. **Data Fetching:**  It retrieves user details using `getUserById(userId)` from `@/lib/actions/user.actions`. This function (not shown in the provided code snippet) presumably fetches user information from a database or API based on the provided `userId`.  The fetched user data includes  `_id` and `creditBalance`.

3. **Transformation Type Lookup:** The component accesses transformation type details from `transformationTypes[type]`. This implies `transformationTypes` is a constant object (defined elsewhere) that maps type strings (e.g., 'image', 'video') to objects containing `title`, `subTitle`, and `type` properties. The `type` property is explicitly cast as `TransformationTypeKey` (type definition not provided) in the `TransformationForm` prop.

4. **Conditional Rendering:** Based on the fetched data, the component renders the `Header` and `TransformationForm` components, passing relevant properties.


## 5. Usage

The `AddTransformationTypePage` component is accessed via a URL route containing the transformation type as a parameter, for example `/add-transformation/image`.  The route parameter (`type`) is used to determine which transformation type's form to display.  The component handles user authentication and data fetching to provide a seamless user experience for adding transformations.
