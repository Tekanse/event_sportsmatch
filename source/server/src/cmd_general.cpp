//Under:
ACMD(do_click_mall)
{
	ch->ChatPacket(CHAT_TYPE_COMMAND, "ShowMeMallPassword");
}


//Add:
ACMD(do_eventsportsmatch)
{
	DWORD EVENT_END_TIME = 1671400800;

	DWORD CHEST_VNUM = 0;
	DWORD COUNTRY_TICKET_VNUM = 0;
	DWORD CHEERING_TICKET_VNUM = 0;
	DWORD EVENT_REWARD = 0;

	//{RewardVnum, requiredTicketCount}
	DWORD REWARDS[3][2] = {
		{0, 5},
		{0, 7},
		{0, 10},
	};

	const char *line;

	char arg1[256], arg2[256], arg3[256];

	line = two_arguments(argument, arg1, sizeof(arg1), arg2, sizeof(arg2));
	one_argument(line, arg3, sizeof(arg3));

	if (!*arg1)
	{
		return;
	}

	const std::string& strArg1 = std::string(arg1);
	if (strArg1 == "open")
	{
		time_t theTime = time(NULL);
		struct tm *aTime = localtime(&theTime);
		int day = aTime->tm_mday;

		std::string commandString = "SportsEventTeams ";
		char teamPoints[32];
		char flagName[32];
		for (int i = 0; i < 32; ++i)
		{
			sprintf(flagName, "eventsports.t%d", i);
	
			sprintf(teamPoints, "%d", ch->GetQuestFlag(flagName));

			commandString += std::string(teamPoints) + "/";
		}
		commandString.erase(commandString.size() - 1);
		ch->ChatPacket(CHAT_TYPE_COMMAND, "SportsEventOpen %d %d %d %d %d", ch->GetQuestFlag("eventsports.pieces"), ch->GetQuestFlag("eventsports.tickets"),
																			ch->GetQuestFlag("eventsports.reward0") == day ? 0 : 1,
																			ch->GetQuestFlag("eventsports.reward1") == day ? 0 : 1,
																			ch->GetQuestFlag("eventsports.reward2") == day ? 0 : 1);
		ch->ChatPacket(CHAT_TYPE_COMMAND, "%s", commandString.c_str());
	}
	else if (strArg1 == "exchange_tickets")
	{
		if (EVENT_END_TIME < time(0))
			return;
		if (ch->GetQuestFlag("eventsports.tickets") <= 0)
			return;
		ch->SetQuestFlag("eventsports.tickets", ch->GetQuestFlag("eventsports.tickets") - 1);
		ch->AutoGiveItem(CHEST_VNUM);
		ch->ChatPacket(CHAT_TYPE_COMMAND, "SportsEventTickets %d %d", ch->GetQuestFlag("eventsports.pieces"), ch->GetQuestFlag("eventsports.tickets"));
	}
	else if (strArg1 == "exchange_reward")
	{
		if (EVENT_END_TIME < time(0))
			return;
		if (!*arg2)
		{
			return;
		}
		BYTE rewardType = 0;
		str_to_number(rewardType, arg2);
		if (rewardType > 2)
			return;

		time_t theTime = time(NULL);
		struct tm *aTime = localtime(&theTime);
		int day = aTime->tm_mday;

		if (ch->GetQuestFlag("eventsports.tickets") < REWARDS[rewardType][1])
		{
			ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You dont have enough tickets."));
			return;
		}

		char flagName[32];
		sprintf(flagName, "eventsports.reward%d", rewardType);
		if (ch->GetQuestFlag(flagName) == day)
		{
			return;
		}
		ch->SetQuestFlag(flagName, day);

		ch->SetQuestFlag("eventsports.tickets", ch->GetQuestFlag("eventsports.tickets") - REWARDS[rewardType][1]);
		ch->AutoGiveItem(REWARDS[rewardType][0]);
		if (rewardType == 0)
			ch->AutoGiveItem(COUNTRY_TICKET_VNUM);

		ch->ChatPacket(CHAT_TYPE_COMMAND, "SportsEventOpen %d %d %d %d %d", ch->GetQuestFlag("eventsports.pieces"), ch->GetQuestFlag("eventsports.tickets"),
																			ch->GetQuestFlag("eventsports.reward0") == day ? 0 : 1,
																			ch->GetQuestFlag("eventsports.reward1") == day ? 0 : 1,
																			ch->GetQuestFlag("eventsports.reward2") == day ? 0 : 1);
	}
	else if (strArg1 == "choose")
	{
		if (EVENT_END_TIME < time(0))
			return;
		if (!*arg2)
		{
			return;
		}
		BYTE teamID = 0;
		str_to_number(teamID, arg2);
		if (teamID >= 32)
			return;

		if (ch->CountSpecifyItem(COUNTRY_TICKET_VNUM) <= 0)
		{
			ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You need %s"), ITEM_MANAGER::instance().GetTable(COUNTRY_TICKET_VNUM)->szLocaleName);
			return;
		}
		ch->RemoveSpecifyItem(COUNTRY_TICKET_VNUM, 1);

		char flagName[32];
		sprintf(flagName, "eventsports.t%d", teamID);
		ch->SetQuestFlag(flagName, 1);
		ch->ChatPacket(CHAT_TYPE_COMMAND, "SportsEventTeamPoints %d %d", teamID, ch->GetQuestFlag(flagName));
	}
	else if (strArg1 == "cheer")
	{
		if (EVENT_END_TIME < time(0))
			return;
		if (!*arg2)
		{
			return;
		}
		BYTE teamID = 0;
		str_to_number(teamID, arg2);
		if (teamID >= 32)
			return;

		if (ch->CountSpecifyItem(CHEERING_TICKET_VNUM) <= 0)
		{
			ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You need %s"), ITEM_MANAGER::instance().GetTable(CHEERING_TICKET_VNUM)->szLocaleName);
			return;
		}
		ch->RemoveSpecifyItem(CHEERING_TICKET_VNUM, 1);

		char flagName[32];
		sprintf(flagName, "eventsports.t%d", teamID);
		ch->SetQuestFlag(flagName, ch->GetQuestFlag(flagName) + 1);
		ch->ChatPacket(CHAT_TYPE_COMMAND, "SportsEventTeamPoints %d %d", teamID, ch->GetQuestFlag(flagName));
	}
	else if (strArg1 == "claim")
	{
		if (ch->GetQuestFlag("eventsports.claimed") > 0)
		{
			ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("Reward already claimed."));
			return;
		}
		DWORD dwEndTime = time(0);
		if (EVENT_END_TIME > dwEndTime || quest::CQuestManager::instance().GetEventFlag("eventsportsmatch_winner") == 0)
		{
			ch->ChatPacket(CHAT_TYPE_INFO, LC_TEXT("You cant do it yet."));
			return;
		}
		char flagName[32];
		sprintf(flagName, "eventsports.t%d", quest::CQuestManager::instance().GetEventFlag("eventsportsmatch_winner") - 1);
		if (ch->GetQuestFlag(flagName) > 0)
		{
			ch->AutoGiveItem(EVENT_REWARD, ch->GetQuestFlag(flagName));
		}
		for (int i = 0; i < 32; ++i)
		{
			sprintf(flagName, "eventsports.t%d", i);
			ch->SetQuestFlag(flagName, 0);
		}
		ch->SetQuestFlag("eventsports.claimed", 1);
	}
}