### Session 08/03:
Start implementing planning maker with randim date assignment inside constraint + taking into account existing events.

 TODO next time:
- create Tasks class + integrate with Planner

### Session 09/03 
First jab at task & tested scheduling multiple task
First jab at preference_analyzer. More work required on using the analysis part.
First jab at bucket list of tasks
TODO today:
- Implement timeslot for preferences

### Session 12/03
First appeareance of task priority. Idea: task with "lower" priority ( 1:max prio, 10: min prio) are scheduled before other tasks.
Default value is 5. 

TODO today:
- ~~implement timeslot updating for user~~.
- implement priority scheduling. > ironically, not a priority
- ~~implement task completion checking~~

### Session 13/03
Task creation to design. Maybe 3 lists ? 
Potential lists: 
- Backlog (tasks created but not currently scheduled)
- Scheduled (tasks that have a scheduled date in the future)
- Past (tasks whose scheduled date is in the past)
Workflow is as follows:
1. User use the client app to create tasks that goes into the backlog
2. Every Sunday afternoon the server app:
   1. Check Gevents from the last week and match them to the Scheduled Tasks (using their IDs added to the description)
   2. Depending on the Gevent status ("completed" or "canceled"), the preferences of the user are updated (already implemented)'
   3. The tasks from the Scheduled list that are found are moved to the Past list (Error if a task is not found ?).
   4. At most user_max_tasks are selected from the Backlog, and for each of these tasks
      1. A date and time are scheduled (based on planning + preferences)
      2. A Gevent is created in the user's calendare (potentially create new calendars ?)
      3. the task is moved to the "Scheduled" list

TODO today:
 - Think about clent app design
 - Start implementing "real" workflow

## Session 14/05
renamed main.py to app.py 

TODO today:
- ~~front: modify time selection widget to increment every "full turn"~~
- back: retrieve event send from front and add it to weely list 
- back: find out how to trigger scheduling function every day

## Session 28/05
Goal: finish the flow v1
Required TODO:
- Trigger the scheduling

Optional TODO: 
- Flesh up testing