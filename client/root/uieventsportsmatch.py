import ui
import uiScriptLocale
import dbg
import app
from _weakref import proxy
import event
import localeInfo
import uicommon
import net
import uitooltip
import time

COUNTRIES_FLAGS = [
	"server_flag_qt.sub",
	"server_flag_ec.sub",
	"server_flag_sg.sub",
	"server_flag_nl.sub",
	"server_flag_en.sub",
	"server_flag_in.sub",
	"server_flag_us.sub",
	"server_flag_ws.sub",
	"server_flag_ar.sub",
	"server_flag_sa.sub",
	"server_flag_mx.sub",
	"server_flag_pl.sub",
	"server_flag_fr.sub",
	"server_flag_au.sub",
	"server_flag_dk.sub",
	"server_flag_tn.sub",
	"server_flag_es.sub",
	"server_flag_cr.sub",
	"server_flag_de.sub",
	"server_flag_jp.sub",
	"server_flag_be.sub",
	"server_flag_ca.sub",
	"server_flag_ma.sub",
	"server_flag_hr.sub",
	"server_flag_br.sub",
	"server_flag_xs.sub",
	"server_flag_ch.sub",
	"server_flag_cm.sub",
	"server_flag_pt.sub",
	"server_flag_gh.sub",
	"server_flag_uy.sub",
	"server_flag_kr.sub",
]

VNUM_REWARD_0 = 0
VNUM_REWARD_1 = 0
VNUM_REWARD_2 = 0

EVENT_END_TIME = 1671400800

class SportsMatchEventWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = False
		self.predictWindow = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		if self.isLoaded == True:
			return
		try:			
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/sportsmatchwindow.py")
		except:
			import exception
			exception.Abort("SportsMatchEventWindow.LoadDialog.LoadScript")

		try:
			self.match_predict_btn = self.GetChild("match_predict_btn")
			self.ticket_piece_count_text = self.GetChild("ticket_piece_count_text")
			self.ticket_count_text = self.GetChild("ticket_count_text")
			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))
			self.GetChild("exchange_reward_slot_0").SetItemSlot(0, VNUM_REWARD_0)
			self.GetChild("exchange_reward_slot_0").SetOverInItemEvent(lambda slotNumber, vnum=VNUM_REWARD_0: self.OnOverInItem(slotNumber, vnum))
			self.GetChild("exchange_reward_slot_0").SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
			self.GetChild("exchange_reward_slot_1").SetItemSlot(0, VNUM_REWARD_1)
			self.GetChild("exchange_reward_slot_1").SetOverInItemEvent(lambda slotNumber, vnum=VNUM_REWARD_1: self.OnOverInItem(slotNumber, vnum))
			self.GetChild("exchange_reward_slot_1").SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
			self.GetChild("exchange_reward_slot_2").SetItemSlot(0, VNUM_REWARD_2)
			self.GetChild("exchange_reward_slot_2").SetOverInItemEvent(lambda slotNumber, vnum=VNUM_REWARD_2: self.OnOverInItem(slotNumber, vnum))
			self.GetChild("exchange_reward_slot_2").SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))

			self.GetChild("ticket_piece_icon").OnMouseOverIn = lambda iType = 0: self.OnOverInImage(iType)
			self.GetChild("ticket_piece_icon").OnMouseOverOut = ui.__mem_func__(self.OnOverOutItem)
			self.GetChild("ticket_icon").OnMouseOverIn = lambda iType = 1: self.OnOverInImage(iType)
			self.GetChild("ticket_icon").OnMouseOverOut = ui.__mem_func__(self.OnOverOutItem)
			self.GetChild("ticket_use_btn").SetEvent(lambda command = "/eventsportsmatch exchange_tickets": net.SendChatPacket(command))
			self.GetChild("exchange_button_0").SetEvent(lambda iType = 0: self.ExchangeRewards(iType))
			self.GetChild("exchange_button_1").SetEvent(lambda iType = 1: self.ExchangeRewards(iType))
			self.GetChild("exchange_button_2").SetEvent(lambda iType = 2: self.ExchangeRewards(iType))
		except:
			import exception
			exception.Abort("SportsMatchEventWindow.LoadWindow.BindObject")

		try:
			self.match_predict_btn.SetEvent(ui.__mem_func__(self.OpenPredictWindow))
		except:
			import exception
			exception.Abort("SportsMatchEventWindow.LoadWindow.BindEvents")

		self.predictWindow = SportsMatchEventPredictWindow()
		self.toolTip = uitooltip.ItemToolTip()
		self.isLoaded = True

	def Destroy(self):
		if self.predictWindow:
			self.predictWindow.Destroy()
		self.ClearDictionary()
		self.predictWindow = None
		self.match_predict_btn = None
		self.ticket_piece_count_text = None
		self.ticket_count_text = None
		self.predictWindow = None
		self.toolTip = None

	def OpenPredictWindow(self):
		(x, y) = self.GetGlobalPosition()
		self.predictWindow.SetPosition(x + self.GetWidth(), y)
		self.predictWindow.Open()

	def SetTickets(self, pieces, tickets):
		self.ticket_piece_count_text.SetText(str(pieces))
		self.ticket_count_text.SetText(str(tickets))

	def SetTeams(self, teams):
		teamID = 0
		for teamStr in teams.split("/"):
			teamPoints = int(teamStr)
			if teamPoints > 0:
				self.predictWindow.SetTeamPoints(teamID, teamPoints)
			teamID += 1

	def SportsEventTeamPoints(self, teamID, points):
		self.predictWindow.SetTeamPoints(teamID, points)

	def OnOverInImage(self, iType):
		if self.toolTip:
			self.toolTip.ClearToolTip()
			title = localeInfo.SPORTS_MATCH_ITEM_FLAG_TICKET_PIECE_NAME
			desc = localeInfo.SPORTS_MATCH_EVENT_SOURCE_ITEM_FLAG_IMG_MESSAGE
			if iType == 1:
				title = localeInfo.SPORTS_MATCH_ITEM_FLAG_TICKET_NAME
				desc = localeInfo.SPORTS_MATCH_ITEM_FLAG_TICKET_DESC
			self.toolTip.SetTitle(title)
			for descLine in desc.split("\\n"):
				self.toolTip.AutoAppendTextLine(descLine)
			leftSec = max(0, EVENT_END_TIME - int(time.time()))
			timeLeft = localeInfo.SPORTS_MATCH_EXCHANGE_END_TIME % (localeInfo.SecondToDHM(leftSec))
			self.toolTip.AutoAppendTextLine(timeLeft)
			self.toolTip.AlignHorizonalCenter()
			self.toolTip.ShowToolTip()
	
	def OnOverInItem(self, slotIndex, vnum):
		if self.toolTip:
			self.toolTip.SetItemToolTip(vnum)

	def OnOverOutItem(self):
		if self.toolTip:
			self.toolTip.HideToolTip()

	def ExchangeRewards(self, iType):
		net.SendChatPacket("/eventsportsmatch exchange_reward %d" % (iType))

	def ClaimReward(self):
		net.SendChatPacket("/eventsportsmatch claim")

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Close(self):
		if self.predictWindow:
			self.predictWindow.Close()
		if self.toolTip:
			self.toolTip.HideToolTip()
		self.Hide()

	def Open(self, pieces, tickets, reward0, reward1, reward2):
		self.LoadWindow()
		self.SetTickets(pieces, tickets)
		if EVENT_END_TIME < time.time():
			self.match_predict_btn.SetText(localeInfo.SPORTS_MATCH_EVENT_REWARD)
			self.match_predict_btn.SetEvent(ui.__mem_func__(self.ClaimReward))
		if reward0 == 1:
			self.GetChild("exchange_button_0").SetUp()
			self.GetChild("exchange_button_0").Enable()
		else:
			self.GetChild("exchange_button_0").Down()
			self.GetChild("exchange_button_0").Disable()
		if reward1 == 1:
			self.GetChild("exchange_button_1").SetUp()
			self.GetChild("exchange_button_1").Enable()
		else:
			self.GetChild("exchange_button_1").Down()
			self.GetChild("exchange_button_1").Disable()
		if reward2 == 1:
			self.GetChild("exchange_button_2").SetUp()
			self.GetChild("exchange_button_2").Enable()
		else:
			self.GetChild("exchange_button_2").Down()
			self.GetChild("exchange_button_2").Disable()
		self.Show()

class CountryLabel:
	def __init__(self, teamID, parent, mainWindow):
		self.bg = None
		self.mainWindow = proxy(mainWindow)
		self.teamID = teamID
		self.points = 0
		self.CreateWindow(parent)

	def __del__(self):
		self.bg = None
		self.mainWindow = None
		self.teamID = None
		self.points = None
		self.flag = None
		self.name = None
		self.pointsText = None
		self.actionButton = None

	def CreateWindow(self, parent):
		self.bg = ui.ExpandedImageBox()
		self.bg.SetParentProxy(parent)
		self.bg.LoadImage( "d:/ymir work/ui/minigame/sports_match/team_bg.sub" )
		self.bg.Show()

		self.flag = ui.ImageBox()
		self.flag.SetParent(self.bg)
		self.flag.LoadImage("d:/ymir work/ui/intro/login/server_flag_sp7.sub")
		self.flag.SetPosition(9, 7)
		self.flag.Show()

		self.name = ui.TextLine()
		self.name.SetParent(self.bg)
		self.name.SetText("")
		self.name.SetPosition(40, 8)
		self.name.Show()

		self.pointsText = ui.TextLine()
		self.pointsText.SetParent(self.bg)
		self.pointsText.SetText("0")
		self.pointsText.SetPosition(161, 9)
		self.pointsText.SetHorizontalAlignCenter()
		self.pointsText.Show()

		self.actionButton = ui.Button()
		self.actionButton.SetParent(self.bg)
		self.actionButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.actionButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.actionButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.actionButton.SetPosition(183, 6)
		self.actionButton.SetEvent(ui.__mem_func__(self.ButtonPressed))
		self.actionButton.SetText(localeInfo.SPORTS_MATCH_EVENT_APPOINT)
		self.actionButton.Show()

	def SetPosition(self, x, y):
		self.bg.SetPosition(x, y)

	def SetCountryFlag(self, countryID):
		self.flag.LoadImage("d:/ymir work/ui/intro/login/%s" % (COUNTRIES_FLAGS[countryID]))

	def SetCountryName(self, name):
		self.name.SetText(name)

	def SetCountryPoints(self, points):
		if points > 0:
			self.SetIsSelected()
		self.points = points
		self.pointsText.SetText(str(points - 1))

	def SetIsSelected(self):
		self.bg.LoadImage("d:/ymir work/ui/minigame/sports_match/team_bg_highlight.sub")
		self.actionButton.SetText(localeInfo.SPORTS_MATCH_EVENT_CHEER)

	def ButtonPressed(self):
		if self.points > 0:
			net.SendChatPacket("/eventsportsmatch cheer %d" % (self.teamID))
			return
		self.mainWindow.ShowTicketQuestion(self.teamID)

	def Show(self):
		self.bg.Show()

	def Hide(self):
		self.bg.Hide()

class SportsMatchEventPredictWindow(ui.ScriptWindow):
	class DescriptionBox(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.descIndex = 0
			self.descY = 0
		def __del__(self):
			ui.Window.__del__(self)
		def SetIndex(self, index):
			self.descIndex = index
		def OnRender(self):
			event.RenderEventSet(self.descIndex)
		def OnUpdate(self):
			(xposEventSet, yposEventSet) = self.GetGlobalPosition()
			event.UpdateEventSet(self.descIndex, xposEventSet+7, -(yposEventSet+7+self.descY))
		def SetDescY(self, descY):
			self.descY = descY
	
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.countryLabels = []
		self.countryNames = []
		self.pageButtons = []
		self.descIndex = 0
		self.selectedPage = 0
		self.dlgQuestion = None
		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:			
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/sportsmatchpredictwindow.py")
		except:
			import exception
			exception.Abort("SportsMatchEventPredictWindow.LoadDialog.LoadScript")
		try:
			self.board = self.GetChild("board")
			self.board.SetCloseEvent(ui.__mem_func__(self.Close))
			self.GetChild("prev_button").SetEvent(ui.__mem_func__(self.PrevDescriptionPage))
			self.GetChild("next_button").SetEvent(ui.__mem_func__(self.NextDescriptionPage))
		except:
			import exception
			exception.Abort("SportsMatchEventPredictWindow.LoadWindow.BindObject")

		self.LoadCountries()

		for i in xrange(32):
			label = CountryLabel(i, self.GetChild("team_list_window"), self)
			label.SetPosition(3, 31 * i + ( 4 * (i + 1)))
			self.countryLabels.append(label)
			label.SetCountryFlag(i)
			label.SetCountryName(self.countryNames[i])

		for i in xrange(4):
			button = self.GetChild("page_button%d" % (i))
			button.SAFE_SetEvent(self.SetTeamsPage, i)
			self.pageButtons.append(button)
	
		self.descBox = self.DescriptionBox()
		self.descBox.SetParent(self.GetChild("description_window"))
		self.descBox.Show()
		event.ClearEventSet(self.descIndex)
		self.descIndex = event.RegisterEventSet("%s/sports_match_predict_desc.txt" % (app.GetLocalePath()))
		event.SetRestrictedCount(self.descIndex, 55)
		event.SetVisibleLineCount(self.descIndex, 4)
		self.descBox.SetIndex(self.descIndex)

		self.dlgQuestion = uicommon.QuestionDialog()
		self.dlgQuestion.SetText(localeInfo.SPORTS_MATCH_EVENT_APPOINT_POPUP_MESSAGE)
		self.dlgQuestion.Close()
		self.ArrangeTeams()

	def ArrangeTeams(self):
		self.countryLabels.sort(key=lambda x: x.points, reverse=True)
		map(lambda x: x.Hide(), self.countryLabels)
		for i in xrange(8):
			self.countryLabels[i + (8 * self.selectedPage)].SetPosition(3, 31 * i + ( 4 * (i + 1)))
			self.countryLabels[i + (8 * self.selectedPage)].Show()

	def LoadCountries(self):
		try:
			lines = pack_open("%s/sports_match_participate_list.txt" % (app.GetLocalePath()), "r").readlines()
		except IOError:
			dbg.TraceError("LoadCountriesError")
			return
		for line in lines:
			tokens = line[:-1].split("\t")
			if len(tokens) == 0 or not tokens[0]:
				continue
			self.countryNames.append(tokens[1])

	def SetTeamsPage(self, page):
		index = 0
		for button in self.pageButtons:
			if index == page:
				button.Down()
				button.Disable()
			else:
				button.SetUp()
				button.Enable()
			index += 1
		self.selectedPage = page
		self.ArrangeTeams()

	def SetTeamPoints(self, teamID, points):
		for team in self.countryLabels:
			if team.teamID == teamID:
				team.SetCountryPoints(points)

	def PrevDescriptionPage(self):
		line_height			= event.GetLineHeight(self.descIndex) + 4

		cur_start_line		= event.GetVisibleStartLine(self.descIndex)
		
		decrease_count = 4
		
		if cur_start_line - decrease_count < 0:
			return

		event.SetVisibleStartLine(self.descIndex, cur_start_line - decrease_count)
		self.descBox.SetDescY(cur_start_line - decrease_count)
		
	def NextDescriptionPage(self):
		line_height			= event.GetLineHeight(self.descIndex) + 4

		total_line_count	= event.GetLineCount(self.descIndex)
		cur_start_line		= event.GetVisibleStartLine(self.descIndex)
		
		increase_count = 4
		
		if cur_start_line + increase_count >= total_line_count:
			increase_count = total_line_count - cur_start_line

		if increase_count < 0 or cur_start_line + increase_count >= total_line_count:
			return
		
		event.SetVisibleStartLine(self.descIndex, cur_start_line + increase_count)
		self.descBox.SetDescY((line_height * increase_count) * -1)

	def ShowTicketQuestion(self, teamID):
		self.dlgQuestion.SetText(localeInfo.SPORTS_MATCH_EVENT_APPOINT_POPUP_MESSAGE % (self.countryNames[teamID]))
		self.dlgQuestion.SetAcceptEvent(lambda arg=teamID: self.AnswerTicketQuestion(arg))
		self.dlgQuestion.SetCancelEvent(ui.__mem_func__(self.CloseTicketQuestion))
		self.dlgQuestion.Open()

	def AnswerTicketQuestion(self, teamID):
		net.SendChatPacket("/eventsportsmatch choose %d" % (teamID))
		self.dlgQuestion.Hide()

	def CloseTicketQuestion(self):
		self.dlgQuestion.Hide()

	def Open(self):
		self.SetTeamsPage(0)
		self.SetTop()
		self.Show()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.ClearDictionary()
		self.countryLabels = []
		self.countryNames = []
		self.pageButtons = []
		self.descIndex = 0
		self.selectedPage = 0
		self.dlgQuestion = None
		self.descBox = None
		self.board = None
