import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime

today = datetime.now()
def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         if today is not None:
             comp = [competition for competition in listOfCompetitions if
                     datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") >= today]
             return comp
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def showSummary():
    email = request.form.get('email')
    if not email:
        flash('Veuillez entrer votre adresse mail!', 'error')
        return redirect(url_for('index'))
    matching_clubs = [club for club in clubs if club['email'] == email]
    if not matching_clubs:
        flash('Aucun club trouvé avec cette adresse e-mail.', 'error')
        return redirect(url_for('index'))
    club = matching_clubs[0]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']
    club_name = request.form['club']
    placesRequired = int(request.form['places'])
    competition = [c for c in competitions if c['name'] == competition_name][0]
    club = [c for c in clubs if c['name'] == club_name][0]
    if int(club['points']) < placesRequired:
        flash('Point insuffisant!')
        return render_template('welcome.html', club=club, competitions=competitions)
    if int(competition['numberOfPlaces']) < placesRequired:
        flash('Nombre de places insuffisant pour la compétition {}!'.format(competition_name))
        return render_template('welcome.html', club=club, competitions=competitions)
    if 'places_reserved_' + competition_name not in club:
        club['places_reserved_' + competition_name] = 0
    if club['places_reserved_' + competition_name] + placesRequired > 12:
        flash('Nombre maximal de places réservées atteint pour la compétition {}!'.format(competition_name))
        return render_template('welcome.html', club=club, competitions=competitions)
    club['points'] = int(club['points']) - placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['places_reserved_' + competition_name] += placesRequired
    flash('Réservation réussie pour la compétition {}!'.format(competition_name))
    return render_template('welcome.html', club=club, competitions=competitions)

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))