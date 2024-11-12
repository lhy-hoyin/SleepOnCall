# Tests (WIP)

Members: `@Admin` `@User`

## `/dc` Command

### user disconnect when not in voice channel
- Given:
  - Member(s) connected: None
- When:
  - Command: `/dc`
- Then:
  - Output (User only):
    > User is not in any voice channel.

### user disconnect with timer
- Given:
    - Member(s) connected: `@User`
- When: 
    - Command: `/dc timer:300`
- Then:
    - Output:
      > `@User` will be disconnected `in 5 minutes`.  
      > To cancel, use `/abort`.

### user disconnect immediately
- Given:
  - Member(s) connected: `@User`
- When:
  - Command: `/dc`
- Then:
  - Member(s) connected: None

### user disconnect admin
- Given:
  - Member(s) connected: `@Admin` `@User`
- When:
  - Command: `/dc member:@admin` 
- Then:
  - Output (User only):
    > You do not have permission to disconnect Admin.
  - Member(s) connected: `@Admin` `@User`

### admin disconnect user
- Given:
  - Member(s) connected: `@Admin` `@User`
- When:
  - Command: `/dc member:@user`
- Then:
  - Output:
    > Disconnecting `@User` ...
  - Member(s) connected: `@Admin`


## `/abort` Command 

### user abort disconnect
- Given:
    - Member(s) connected: `@User`
    - `@User` has a disconnect request
- When:
  - Command: `/abort`
- Then:
  - Output:
    > `@User` will no longer be disconnected.

### user abort disconnect without any active request
- Given:
  - Member(s) connected: `@User`
- When:
  - Command: `/abort`
- Then:
  - Output (user only):
    > `@User` do not have any disconnect request.

## Template

### test name
- Given:
- When:
  - Command: 
- Then:
  - Output:
    > 