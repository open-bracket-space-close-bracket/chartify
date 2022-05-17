# Software Requirements

## Vision

### What is the vision of this product?

An easy to use web page where users can view data visualization of stocks and crypto currencies.

### What pain point does this project solve?

Ease of access, and light weight viewing of seeing all stocks and cryptos on one page. A very streamlined approach to help you focus on what you want to focus on.

### Why should we care about your product?

It's free with no ads and easy to use, consumer friendly.

## Scope (In/Out)

Take in realtime data on stocks and crypto currencies and display the charts based on user preference

**Out of scope**, this is not providing financial advice. NOthing being sold ont this platform. Not providing up to the minute data.

## Minimum Viable Product

### What will your MVP functionality be?

Call an external API, get data to display on a dashboard of selected currencies/stocks the user wants to follow.
Pass the  data to frontend with flask using JSON.
Requests: flask server - external API endpoints
Make charts on frontend of flask with passed data

## Stretch

### What are your stretch goals?

- Persistence of requests
- OAUTH - Dance
- Forum page
- Containerize! DOCKER  

## Functional Requirements

List the functionality of your product. This will consist of tasks such as the following:

1. A user can search stock/crypto currency
2. A user can view data on searched values over various time frames
3. A user can remove a stock from their list of saved stocks
4. A user can change the time frame to see different visualizations

## Data Flow

- Get list of saved favorites of stock/crypto from database.
- Get data from external API.
- Next step, clean the data.
- Third step, pass the data to the flask template page where it is needed

## Non-Functional Requirements

### Security

- API Key will be hidden, and Auth0 will be used as well.

### Testability

- Use vercel to test during development.
- Use pytest to test specific functions.