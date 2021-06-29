from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Count

from . import team_maker

def index(request):
	# SPORTS ORM I
	# 1. todas las ligas de béisbol
	baseball_leagues = League.objects.filter(sport='Baseball')
	# 2. todas las ligas de mujeres
	women_leagues = League.objects.filter(name__contains='Womens')
	# 3. todas las ligas donde el deporte es cualquier tipo de hockey
	hockey_leagues = League.objects.filter(sport__contains='Hockey')
	# 4. todas las ligas donde el deporte no sea football
	no_football_leagues = League.objects.exclude(sport='Football')
	# 5. todas las ligas que se llaman "conferencias"
	conference_leagues = League.objects.filter(name__contains='Conference')
	# 6. todas las ligas de la región atlántica
	atlantic_leagues = League.objects.filter(name__contains="Atlantic")
	# 7. todos los equipos con sede en Dallas
	dallas_teams = Team.objects.filter(location='Dallas')
	# 8. todos los equipos nombraron los Raptors
	raptors_teams = Team.objects.filter(team_name='Raptors')
	# 9. todos los equipos cuya ubicación incluye "Ciudad" 
	city_teams = Team.objects.filter(location__contains='City')
	# 10. todos los equipos cuyos nombres comienzan con "T"
	t_teams = Team.objects.filter(team_name__startswith='T')
	# 11. todos los equipos, ordenados alfabéticamente por ubicación
	location_order_teams = Team.objects.all().order_by('location')
	# 12. todos los equipos, ordenados por nombre de equipo en orden alfabético inverso
	name_order_teams = Team.objects.all().order_by('-team_name')
	# 13. cada jugador con apellido "Cooper"
	cooper_players = Player.objects.filter(last_name='Cooper')
	# 14. cada jugador con nombre "Joshua"
	joshua_players = Player.objects.filter(first_name='Joshua')
	# 15. todos los jugadores con el apellido "Cooper" EXCEPTO aquellos con "Joshua" como primer nombre
	cooper_joshua_players = Player.objects.filter(last_name='Cooper').exclude(first_name='Joshua')
	# 16. todos los jugadores con nombre "Alexander" O nombre "Wyatt"
	alexander_wyatt_players = Player.objects.filter(first_name='Alexander') | Player.objects.filter(first_name='Wyatt')
	
	#SPORTS ORM II
	# 1. todos los equipos en la Atlantic Women's Soccer Federeation
	awsf_teams = Team.objects.filter(league__name="Atlantic Womens' Soccer Federation")
	# 2. todos los jugadores (actuales) en los Raleigh Penguins
	rp_players = Player.objects.filter(curr_team__team_name="Penguins", curr_team__location="Raleigh")
	# 3. todos los jugadores (actuales) en la International Collegiate Football Association
	icfa_players = Player.objects.filter(curr_team__league__name="International Collegiate Football Association")
	# 4. todos los jugadores (actuales) en la Conferencia Americana de Fútbol Amateur con el apellido "Wilson"
	wilson_acaf = Player.objects.filter(curr_team__league__name="American Conference of Amateur Football", last_name="Wilson")
	# 5. todos los jugadores de fútbol
	football_players = Player.objects.filter(curr_team__league__sport="Football")
	# 6. todos los equipos con un jugador (actual) llamado "Sophia"
	sophia_teams = Team.objects.filter(curr_players__first_name="Sophia")
	# 7. todas las ligas con un jugador (actual) llamado "Sophia"
	sophia_leagues = League.objects.filter(teams__curr_players__first_name="Sophia")
	# 8. todos los jugadores con el apellido "Flores" que NO (actualmente) juegan para los DC Nuggets
	flores_nodcn = Player.objects.filter(last_name="Flores").exclude(curr_team__team_name="Nuggets")
	# 9. todos los equipos, pasados y presentes, con los que Charlotte Evans ha jugado
	ce_teams = Team.objects.filter(all_players__last_name="Evans", all_players__first_name="Charlotte")
	# 10. todos los jugadores, pasados y presentes, de Calgary Generals
	cg_players = Player.objects.filter(all_teams__team_name="Generals", all_teams__location="Calgary")
	# 11. todos los jugadores que anteriormente estaban (pero que no lo están) con los Wisconsin White Sox
	old_wws_players = Player.objects.filter(all_teams__team_name="White Sox", all_teams__location="Wisconsin").exclude(curr_team__team_name="White Sox")
	# 12. cada equipo para el que Christian Roberts jugó antes de unirse a los Chicago Cubs
	cr_oldteams = Team.objects.filter(all_players__last_name="Roberts", all_players__first_name="Christian").exclude(team_name="Cubs", location="Chicago")
	# 13. todos llamados "Joshua" que alguna vez han jugado en la Pacific Basketball Athletics Conference
	pbac_joshua_players = Player.objects.filter(all_teams__league__name="Pacific Basketball Athletics Conference", first_name="Joshua")
	# 14. todos los equipos que han tenido 12 o más jugadores, pasados y presentes
	twelveplus_teams = Team.objects.annotate(Count('all_players'))
	# 15. todos los jugadores y el número de equipos para los que jugó, ordenados por la cantidad de equipos para los que han jugado
	players_teams = Player.objects.annotate(num_teams=Count('all_teams')).order_by('-num_teams')
	
	
	context = {
		#SPORTS ORM II
		'players_teams': players_teams,
		'twelveplus_teams': twelveplus_teams,
		'pbac_joshua_players': pbac_joshua_players,
		'cr_oldteams': cr_oldteams,
		'old_wws_players': old_wws_players,
		'cg_players': cg_players,
		'ce_teams': ce_teams,
		'flores_nodcn': flores_nodcn,
		'sophia_leagues': sophia_leagues,
		'sophia_teams': sophia_teams,
		'football_players': football_players,
		'wilson_acaf': wilson_acaf,
		'icfa_players': icfa_players,
		'rp_players': rp_players,
		'awsf_teams': awsf_teams,

		#SPORTS ORM I
		'alexander_wyatt_players': alexander_wyatt_players,
		'cooper_joshua_players': cooper_joshua_players,
		'joshua_players': joshua_players,
		'cooper_players': cooper_players,
		'name_order_teams': name_order_teams,
		'location_order_teams': location_order_teams,
		't_teams': t_teams,
		'city_teams': city_teams,
		'raptors_teams': raptors_teams,
		'dallas_teams': dallas_teams,
		'atlantic_leagues': atlantic_leagues,
		'conference_leagues': conference_leagues,
		'no_football_leagues': no_football_leagues,
		'hockey_leagues': hockey_leagues,
		'women_leagues': women_leagues,
		'baseball_leagues': baseball_leagues,

		#DEFAULT
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")