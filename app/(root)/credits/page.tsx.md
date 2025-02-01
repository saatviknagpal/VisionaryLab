# Credits Page Code Documentation

## Table of Contents

* [1. Overview](#1-overview)
* [2. `Credits` Component](#2-credits-component)
    * [2.1 Authentication and Redirection](#21-authentication-and-redirection)
    * [2.2 User Data Retrieval](#22-user-data-retrieval)
    * [2.3 Plan Rendering](#23-plan-rendering)
    * [2.4 Inclusion Display](#24-inclusion-display)
    * [2.5 Checkout Integration](#25-checkout-integration)


## 1. Overview

This document details the implementation of the `Credits` page component, responsible for displaying various credit plans to users and facilitating the purchase process.  The page uses Clerk.js for authentication and a custom checkout component.


## 2. `Credits` Component

The `Credits` component renders a list of credit plans fetched from the `plans` constant. Each plan includes details like name, price, credits offered, and a list of inclusions.

### 2.1 Authentication and Redirection

```javascript
const { userId } = auth();
if (!userId) redirect("/sign-in");
```

The component first uses the `auth()` hook from `@clerk/nextjs/server` to obtain the currently authenticated user's ID. If no user ID is found (meaning the user is not signed in), the user is redirected to the `/sign-in` page using the `redirect()` hook from `next/navigation`.


### 2.2 User Data Retrieval

```javascript
const user = await getUserById(userId);
```

Once the user is authenticated, the component retrieves the user's data using the `getUserById` function from `@/lib/actions/user.actions`. This function (not shown in provided code) presumably fetches user details from a database based on the provided `userId`.  The returned user object is then used in the Checkout component to associate the purchase with the correct user.


### 2.3 Plan Rendering

```javascript
{plans.map((plan) => (
  // ... JSX to render each plan ...
))}
```

The `plans` constant (not shown in provided code) is an array of objects, each representing a credit plan. The component iterates over this array using `.map()` to render a list item (`<li>`) for each plan. Each list item displays the plan's icon, name, price, and the number of credits included.


### 2.4 Inclusion Display

```javascript
{plan.inclusions.map((inclusion) => (
  // ... JSX to render each inclusion ...
))}
```

Within each plan's rendering, the component iterates through the `inclusions` array (part of each plan object) to display a list of features included in that plan.  An icon (`check.svg` or `cross.svg`) indicates whether each inclusion is present. This uses conditional rendering based on the `inclusion.isIncluded` boolean property.


### 2.5 Checkout Integration

```javascript
{plan.name === "Free" ? (
  // ... JSX for free plan button ...
) : (
  <SignedIn>
    <Checkout
      plan={plan.name}
      amount={plan.price}
      credits={plan.credits}
      buyerId={user._id}
    />
  </SignedIn>
)}
```

Conditional rendering is used to display either a simple "Free Consumable" button for the free plan or a `Checkout` component for paid plans. The `Checkout` component (not shown in the provided code) handles the actual payment processing.  The `SignedIn` component from `@clerk/nextjs` ensures that the checkout is only rendered for authenticated users.  The `Checkout` component receives the plan name, amount, credits, and the user's ID (`user._id`) as props.


The structure of the `plans` constant and the `Checkout` component are not provided, but their expected formats are implied by the code's usage.  Further documentation of those components would enhance the completeness of this documentation.
