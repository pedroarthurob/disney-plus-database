import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, redirect, render_template, Flask, request, url_for
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = {}
    stats = db.execute('''
    SELECT * FROM
      (SELECT COUNT(*) AS media FROM MEDIA)
    JOIN
      (SELECT COUNT(*) AS cast FROM CAST)
    JOIN
      (SELECT COUNT(*) AS director FROM DIRECTOR)
    JOIN 
      (SELECT COUNT(*) AS genres FROM GENRE)
    JOIN 
      (SELECT COUNT(*) AS country FROM COUNTRY)
    JOIN 
      (SELECT COUNT(*) AS type FROM TYPE)
    ''').fetchone()
    logging.info(stats)
    return render_template('index.html',stats=stats)

# Medias
@APP.route('/medias/')
def list_medias():
    medias = db.execute(
    '''
    SELECT m.ID, t.Name as TypeName, m.Title, m.Date_Added, m.Release_year, m.Rating, m.Duration, m.Description 
    FROM MEDIA m JOIN TYPE t ON m.TypeID = t.ID
    ORDER BY m.ID
    ''').fetchall()
    return render_template('media-list.html', medias=medias)

@APP.route('/medias/<int:id>/')
def get_media(id):
  media = db.execute(
    '''
    SELECT m.ID, t.Name, m.Title, m.Date_Added, m.Release_year, m.Rating, m.Duration, m.Description 
    FROM MEDIA m JOIN TYPE t ON m.TypeID = t.ID
    WHERE m.ID = ?
    ''', [id]).fetchone()

  if media is None:
     abort(404, 'Media ID {} não existe.'.format(id))

  types = db.execute(
    '''
    SELECT m.TypeID, t.Name 
    FROM TYPE t JOIN MEDIA m ON m.TypeID = t.ID
    WHERE m.ID = ? 
    ''', [id]).fetchall()

  genres = db.execute(
    '''
    SELECT g.ID, g.Name
    FROM GENRE g JOIN MEDIAGENRE mg ON mg.GenreID = g.ID JOIN MEDIA m ON m.ID = mg.MediaID
    WHERE m.ID = ? 
    ORDER BY g.Name
    ''', [id]).fetchall()
  
  countries = db.execute(
    '''
    SELECT c.ID, c.Name
    FROM COUNTRY c JOIN MEDIACOUNTRY mc ON mc.CountryID = c.ID JOIN MEDIA m ON m.ID = mc.MediaID
    WHERE m.ID = ? 
    ORDER BY c.Name
    ''', [id]).fetchall()

  casts = db.execute(
    '''
    SELECT p.ID, p.Name
    FROM PERSON p JOIN CAST c ON p.ID = c.PersonID JOIN MEDIA m ON c.MediaID = m.ID
    WHERE m.ID = ?
    ORDER BY p.Name
    ''', [id]).fetchall()

  directors = db.execute(
    ''' 
    SELECT p.ID, p.Name
    FROM PERSON p JOIN DIRECTOR d ON p.ID = d.PersonID JOIN MEDIA m ON d.MediaID = m.ID
    WHERE m.ID = ?
    ORDER BY p.Name
    ''', [id]).fetchall()
  
  return render_template('media.html', 
           media=media, types=types, genres=genres, countries=countries, casts=casts, directors=directors)

@APP.route('/medias/search/<expr>/')
def search_media(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  medias = db.execute(
    ''' 
    SELECT ID, Title
    FROM MEDIA
    WHERE Title LIKE ?
    ''', [expr]).fetchall()
  return render_template('media-search.html',
           search=search,medias=medias)

# Elenco
@APP.route('/cast/')
def list_cast():
    casts = db.execute(
    '''
    SELECT m.Title, p.ID, p.Name, m.ID AS mediaID
    FROM PERSON p JOIN CAST c ON p.ID = c.PersonID JOIN MEDIA m ON c.MediaID = m.ID
    ORDER BY p.Name
    ''').fetchall()
    return render_template('cast-list.html', casts=casts)


@APP.route('/cast/<int:id>/')
def view_movies_by_cast(id):
  cast = db.execute(
    '''
    SELECT p.ID, p.Name 
    FROM PERSON p JOIN CAST c ON p.ID = c.PersonID JOIN MEDIA m ON c.MediaID = m.ID
    WHERE p.ID = ?
    ''', [id]).fetchone()

  if cast is None:
     abort(404, 'ID {} do ator não existe.'.format(id))

  medias = db.execute(
    '''
    SELECT m.ID, m.Title
    FROM PERSON p JOIN CAST c ON p.ID = c.PersonID JOIN MEDIA m ON c.MediaID = m.ID
    WHERE p.ID = ?
    ORDER BY m.Title
    ''', [id]).fetchall()

  return render_template('cast.html', 
           cast=cast, medias=medias)
 
@APP.route('/cast/search/<expr>/')
def search_cast(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  casts = db.execute(
    ''' 
    SELECT p.ID, p.Name, m.ID, m.Title 
    FROM PERSON p JOIN CAST c ON p.ID = c.PersonID JOIN MEDIA m ON c.MediaID = m.ID
    WHERE p.Name LIKE ?
    ''', [expr]).fetchall()

  return render_template('cast-search.html', 
           search=search,casts=casts)

# Diretores
@APP.route('/director/')
def list_directors():
    directors = db.execute(
    '''
    SELECT p.ID, p.Name 
    FROM PERSON p JOIN DIRECTOR d ON p.ID = d.PersonID JOIN MEDIA m ON d.MediaID = m.ID
    ORDER BY p.Name
    ''').fetchall()
    return render_template('director-list.html', directors=directors)


@APP.route('/director/<int:id>/')
def view_medias_by_director(id):
  directors = db.execute(
    '''
    SELECT p.ID, p.Name 
    FROM PERSON p JOIN DIRECTOR d ON p.ID = d.PersonID JOIN MEDIA m ON d.MediaID = m.ID
    WHERE p.ID = ?
    ''', [id]).fetchone()

  if directors is None:
     abort(404, 'ID {} do diretor não existe.'.format(id))

  medias = db.execute(
    '''
    SELECT m.ID, m.Title
    FROM PERSON p JOIN DIRECTOR d ON p.ID = d.PersonID JOIN MEDIA m ON d.MediaID = m.ID
    WHERE p.ID = ?
    ORDER BY m.Title
    ''', [id]).fetchall()

  return render_template('director.html', 
           directors=directors, medias=medias)
 
@APP.route('/director/search/<expr>/')
def search_director(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  directors = db.execute(
    ''' 
    SELECT p.ID, p.Name, m.ID, m.Title 
    FROM PERSON p JOIN DIRECTOR d ON p.ID = d.PersonID JOIN MEDIA m ON d.MediaID = m.ID
    WHERE p.Name LIKE ?
    ''', [expr]).fetchall()

  return render_template('director-search.html', 
           search=search,directors=directors)

# Genero
@APP.route('/genres/')
def list_genres():
    genre = db.execute('''
      SELECT g.ID, g.Name
      FROM GENRE g
      ORDER BY g.ID
    ''').fetchall()
    return render_template('genre-list.html', genre=genre)

@APP.route('/genres/<int:id>/')
def view_medias_by_genre(id):
  genre = db.execute(
    '''
    SELECT g.ID, g.Name
    FROM GENRE g JOIN MEDIAGENRE mg ON g.ID = mg.GenreID JOIN MEDIA m ON mg.MediaID = m.ID
    WHERE g.ID = ?
    ''', [id]).fetchone()

  if genre is None:
     abort(404, 'ID {} do gênero não existe.'.format(id))

  medias = db.execute(
    '''
    SELECT m.ID, m.Title
    FROM GENRE g JOIN MEDIAGENRE mg ON g.ID = mg.GenreID JOIN MEDIA m ON mg.MediaID = m.ID
    WHERE g.ID = ?
    ORDER BY m.Title
    ''', [id]).fetchall()

  return render_template('genre.html', 
           genre=genre, medias=medias)

@APP.route('/genres/search/')
def search_genre():
    # Pega o valor do parâmetro 'expr' da query string
    expr = request.args.get('expr', '')  # Valor padrão é uma string vazia
    search = {'expr': expr}
    expr = f"%{expr}%"

    # Executa a consulta no banco de dados
    genres = db.execute(
        '''
        SELECT ID, Name
        FROM GENRE
        WHERE Name LIKE ?
        ''', [expr]
    ).fetchall()

    # Renderiza o template com os resultados
    return render_template('genre-search.html', search=search, genres=genres)

# Pais de origem
@APP.route('/countries/')
def list_country():
    country = db.execute('''
    SELECT ID, Name
    FROM COUNTRY
    ORDER BY ID
    ''').fetchall()
    return render_template('country-list.html', country=country)

@APP.route('/countries/<int:id>/')
def view_medias_by_country(id):
  country = db.execute(
    '''
    SELECT ID, Name
    FROM COUNTRY
    WHERE ID = ?
    ''', [id]).fetchone()

  if country is None:
     abort(404, 'ID {} do país de origem não existe.'.format(id))
  
  medias = db.execute(
    '''
    SELECT m.ID, m.Title
    FROM COUNTRY c JOIN MEDIACOUNTRY mc ON c.ID = mc.CountryID JOIN MEDIA m ON mc.MediaID = m.ID
    WHERE c.ID = ?
    ORDER BY m.Title
    ''', [id]).fetchall()

  return render_template('country.html', 
           medias=medias, country=country)



# @APP.route('/countries/search/<expr>/')
# def search_country(expr):
#   search = { 'expr': expr }
#   expr = '%' + expr + '%'
#   countries = db.execute(
#     ''' 
#     SELECT ID, Name
#     FROM COUNTRY
#     WHERE Name LIKE ?
#     ''', [expr]).fetchall()
#   return render_template('country-search.html',
#            search=search,countries=countries)

@APP.route('/countries/search/', methods=['GET'])
def search_country():
    expr = request.args.get('expr')  # Pega o valor do parâmetro 'expr' da query string
    
    # Adiciona os '%' apenas na busca SQL
    search_expr = '%' + expr + '%'
    countries = db.execute(
        ''' 
        SELECT ID, Name
        FROM COUNTRY
        WHERE Name LIKE ?
        ''', [search_expr]).fetchall()

    # Passa o valor de 'expr' sem os '%'
    return render_template('country-search.html',
        search={'expr': expr},
        countries=countries)

# Tipo
@APP.route('/types/')
def list_types():
    type = db.execute('''
      SELECT t.ID, t.Name
      FROM TYPE t
      ORDER BY t.ID
    ''').fetchall()
    return render_template('type-list.html', type=type)

@APP.route('/types/<int:id>/')
def view_medias_by_types(id):
  type = db.execute(
    '''
    SELECT t.ID, t.Name
    FROM TYPE t JOIN MEDIA m ON m.TypeID = t.ID
    WHERE t.ID = ?
    ''', [id]).fetchone()

  if type is None:
     abort(404, 'ID {} do tipo de media não existe.'.format(id))

  medias = db.execute(
    '''
    SELECT m.ID, m.Title
    FROM TYPE t JOIN MEDIA m ON m.TypeID = t.ID
    WHERE t.ID = ?
    ORDER BY m.Title
    ''', [id]).fetchall()

  return render_template('type.html', 
           type=type, medias=medias)

@APP.route('/types/search/<expr>/')
def search_type(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  type = db.execute(
    ''' 
    SELECT m.ID, m.Title, t.Name 
    FROM TYPE t JOIN MEDIA m ON m.TypeID = t.ID
    WHERE t.Name LIKE ?
    ''', [expr]).fetchall()

  return render_template('type-search.html', 
           search=search,type=type)