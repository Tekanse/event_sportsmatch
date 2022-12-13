#Under:
import localeInfo
#Add:
import uieventsportsmatch


#Under:
		self.privateShopBuilder.Hide()
#Add:
		self.dlgEventSportsMatch = uieventsportsmatch.SportsMatchEventWindow()
		self.dlgEventSportsMatch.Hide()


#Under:
		if self.privateShopBuilder:
			self.privateShopBuilder.Destroy()
#Add:
		if self.dlgEventSportsMatch:
			self.dlgEventSportsMatch.Destroy()


#Under:
		del self.privateShopBuilder
#Add:
		del self.dlgEventSportsMatch


#Under:
	def EmptyFunction(self):
		pass
#Add:
	def SportsEventOpen(self, pieces, tickets, reward0, reward1, reward2):
		self.dlgEventSportsMatch.Open(pieces, tickets, reward0, reward1, reward2)

	def SportsEventSetTickets(self, pieces, tickets):
		self.dlgEventSportsMatch.SetTickets(pieces, tickets)

	def SportsEventSetTeams(self, teams):
		self.dlgEventSportsMatch.SetTeams(teams)

	def SportsEventTeamPoints(self, teamID, points):
		self.dlgEventSportsMatch.SportsEventTeamPoints(teamID, points)