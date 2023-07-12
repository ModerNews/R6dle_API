# R6dle REST API

## Introduction
This is basic REST API used to gather simple statistical data for the R6dle.
There is no authentication or authorization implemented, 
and the Bearer token is **purely for user identification, it does not provide any safety!!!**

## Routes
### GET `/token`
Generates url safe token for user identification.

### GET `/stats/global`
Returns global statistics for the daily operator in R6dle.  
**Query Parameters:**
- `date` - date in format `YYYY-MM-DD` (default: today)

### GET `/stats/user`
Returns user statistics for the in R6dle - `max_streak, current_streak, total_solves`.

### PATCH `/stats`
**Requires token**  
Updates statistics with new guess, as provided (both user and global).  
**Query Parameters:**
- `solves` - number of guesses that it took user to solve the daily operator

### GET `/operator`
**Requires token**  
Returns the daily operator (*as sha256 hash*, to make it harder to scrape it for the user) for the R6dle.

## CORS
Currently, CORS is enabled strictly for the `https://rwlodarczyk.github.io` - domain of R6dle, so it's harder to abuse the tokens. 

## Important Files and Directories to keep track of
- `postgres-data` directory will store state of the postgres database from the Docker container.
-  `static` directory will store static files handled by the server 