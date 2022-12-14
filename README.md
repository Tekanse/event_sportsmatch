All you need to do is add required items and set vnums, icons are included.

To open event window you need to call command `/eventsportsmatch open`

Vnums to change:

`uieventsportsmatch.py`
```
VNUM_REWARD_0 = 0
VNUM_REWARD_1 = 0
VNUM_REWARD_2 = 0
```

`cmd_general.cpp`
```
	DWORD CHEST_VNUM = 0;
	DWORD COUNTRY_TICKET_VNUM = 0;
	DWORD CHEERING_TICKET_VNUM = 0;
	DWORD EVENT_REWARD = 0;
  	DWORD REWARDS[3][2] = {
		{0, 5},
		{0, 7},
		{0, 10},
	};
  ```
  
  Event will end on 18.12.2022 22:00 UTC, after that time players will be able to claim reward ("CHEER" button will change to "Claim reward" button) and wont be able to exchange tickets.
  
  You just need to set eventflag `eventsportsmatch_winner` to ID of the team that won world cup. You can find teams ID's in `sports_match_participate_list.txt`.
  
  ![](eventsportsmatch.gif)
