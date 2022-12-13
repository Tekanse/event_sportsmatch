#Under:
			"mall"			: self.__InGameShop_Show,
#Add:
			"SportsEventOpen"		: self.SportsEventOpen,
			"SportsEventTickets"	: self.SportsEventTickets,
			"SportsEventTeams"		: self.SportsEventTeams,
			"SportsEventTeamPoints"	: self.SportsEventTeamPoints,

#Under:
	def __InGameShop_Show(self, url):
		if constInfo.IN_GAME_SHOP_ENABLE:
			self.interface.OpenWebWindow(url)
#Add:
	def SportsEventOpen(self, pieces, tickets, reward0, reward1, reward2):
		self.interface.SportsEventOpen(int(pieces), int(tickets), int(reward0), int(reward1), int(reward2))

	def SportsEventTickets(self, pieces, tickets):
		self.interface.SportsEventSetTickets(pieces, tickets)

	def SportsEventTeams(self, teams):
		self.interface.SportsEventSetTeams(teams)

	def SportsEventTeamPoints(self, teamID, points):
		self.interface.SportsEventTeamPoints(int(teamID), int(points))