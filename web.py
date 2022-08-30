
from flask import Flask, url_for,render_template, request, jsonify
import time
from flask_sqlalchemy import SQLAlchemy 
from flask_accept import accept

app = Flask("lyrics")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lyrics'
db = SQLAlchemy(app)

class Artists(db.Model):
    __tablename__="artists"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    songs = db.relationship("Songs", back_populates="artist")

    def __repr__(self):
        return f"Songs('{self.name}')"

class Songs(db.Model):
    __tablename__="songs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    lyrics = db.Column(db.String)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    artist = db.relationship("Artists", back_populates="songs")

    def __repr__(self):
        return f"Artists('{self.name}')"


@app.route("/")
def index():
    artists = Artists.query.all()
    # formatted = []
    # for i in artists:
    #     target = url_for("artists", artist_id = i.id)
    #     link = f'<a href="{target}">{i.name}</a>'
    #     formatted.append(f"<li>{link}</li>")
    return render_template("artist.html", artists = artists)
    #return "<ul>" + "".join(formatted) + "</ul>"

@app.route("/artist/<int:artist_id>")
def artists(artist_id):
    songs = Songs.query.filter_by(artist_id = artist_id).all()
    artist = Artists.query.get(artist_id)
    # formatted = []
    # for i in songs:
    #     target = url_for("songs",song_id=i.id)
    #     link = f'<a href="{target}">{i.name}</a>'
    #     formatted.append(f"<li>{link}</li>")
    return render_template("songs.html", songs = songs, artist_name=artist.name)
    #return "<ul>" + "".join(formatted) + "</ul>"
    

@app.route("/song/<int:song_id>")
@accept("text/html")
def songs(song_id):
    song = Songs.query.filter_by(id = song_id).first()
    lyrics = song.lyrics.replace("\n","<br>")
    songs = song.artist.songs
    song_name = song.name
    artist_name = song.artist.name

    #return f"""<h2>{song.name}</h2>
#{lyrics}"""
    return render_template("lyrics.html", lyrics = lyrics, songs=songs,song_name=song_name ,artist_name=artist_name)

# @app.route("/lyrics/<int:song_id>")
# @accept("text/html")
# def lyrics(song_id):
#     song = Songs.query.filter_by(id = song_id).first()
#     songs = song.artist.songs
#     lyrics = song.lyrics
#     song_id = song.id
#     return render_template("lyrics.html", song=song, songs=songs, lyrics=lyrics)


@songs.support("application/json")
def song_json(song_id):
    print("I'm returning json!")
    song = Songs.query.filter_by(id=song_id).first()
    songs = song.artist.songs
    ret = dict(song = dict(name = song.name,
                                  lyrics = song.lyrics,
                                  id = song.id,
                                  artist = dict(name = song.artist.name,
                                  id = song.artist.id)))
    return jsonify(ret)


