from app import app
from app import models

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='walrus',
            email="wal@rus.com",
            password='password',
            avatar="images/user_walrus.png",
            user_level="walrus"
        )
        models.User.create_user(
            username='matt',
            email="ma@tt.com",
            password='password',
        )
        models.Band.create_band(
            name="skeletonwitch",
            about="They are hella metal - Walrus",
            genre="Hella Metal",
            themes="data science is weird",
            img="images/band_skeletonwitch.jpg",
            bg_img="images/band_bg_thefantasticwalruses.jpg",
            skid="527207"
        )
        models.Venue.create_venue(
            name="the independent",
            about="Been there. It's alright.",
            img="images/venue_theindependent.jpg",
            skid="324"
        )

    except ValueError:
        pass
        
    app.run(debug=True, port=8000)